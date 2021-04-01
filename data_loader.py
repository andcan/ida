import itertools
from data import merge_if_not_present, Mapping, PropertyMapping, PropertySchema, Schema, NodeSchema
from typing import Any, Dict, List, Optional, Sequence, Tuple
import pandas as pd
import re
import Levenshtein as levenshtein
import pandas as pd
import re
import dateparser
import datetime
import xmltodict
import json
import jsonpath_ng
import datetime

preferred_case_match_source = 'preferred_case_match_source'
preferred_case_snake_case = 'preferred_case_snake_case'
preferred_case_camel_case = 'preferred_case_camel_case'

phone_regex = re.compile(r'((\d{2}|\+)?\d{2})?(\d[ -]*){3,10}')


ddp = dateparser.DateDataParser(languages=['it'], settings={
    'DATE_ORDER': 'DMY'
})


def parse_date(s: str):
    data = ddp.get_date_data(s)
    if data:
        return data['date_obj']
    return None

# def parse_date(s: str) -> Optional[datetime.datetime]:
#     # try:
#     #     datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%s')
#     # except ValueError:
#     #     raise ValueError("Incorrect data format, should be YYYY-MM-DD")
#     return dateparser.parse(s, languages=['it'], settings={
#         'DATE_ORDER': 'YMD'
#     })


class DataLoader(object):

    def dataframe_from_csv(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(filename, delimiter=';', dtype=str)

    def dataframe_from_xml(self, filename: str, path: str) -> pd.DataFrame:
        with open(filename, 'r') as f:
            d = xmltodict.parse(f.read())
            pathexpr = jsonpath_ng.parse(path)
            matches = pathexpr.find(d)
            if len(matches) == 0:
                raise Exception('no matches fot path <{}>'.format(path))
            return pd.json_normalize(matches[0].value)

    def dataframe_from_json(self, filename: str, path: Optional[str] = None) -> pd.DataFrame:
        with open(filename, 'r') as f:
            d = json.loads(f.read())
            if path is not None and path != '':
                pathexpr = jsonpath_ng.parse(path)
                matches = pathexpr.find(d)
                if len(matches) == 0:
                    raise Exception('no matches fot path <{}>'.format(path))
                d = matches[0].value
            return pd.json_normalize(d)

    def load(self, filename, query: Optional[str] = None, path: Optional[str] = None) -> pd.DataFrame:
        if filename.endswith('.csv'):
            df = self.dataframe_from_csv(filename)
        elif filename.endswith('.xml'):
            if path is None or path == '':
                raise Exception('path is required')
            df = self.dataframe_from_xml(filename, path=path)
        elif filename.endswith('.json'):
            df = self.dataframe_from_json(filename, path=path)
        else:
            raise Exception('unsupported file type')
        if query != None:
            df = df.query(query)
        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        return df

    def generate_mapping(
        self,
        node: NodeSchema,
        df: pd.DataFrame,
        tolerance: float = 0.5,
        preferred_merge_behavior: str = merge_if_not_present,
        map_all: bool = True,
    ) -> Optional[Mapping]:
        def _normalize(s: str) -> str:
            s = s.lower()
            return re.sub(r'[^A-Za-z0-9]', '', s)

        def _gen_name(s: str) -> str:
            s = re.sub(r'[^A-Za-z0-9 ]', '', s)
            s = '_'.join(s.split(' '))
            while True:
                matches = re.findall('_{2,}', s)
                if len(matches) == 0:
                    break
                s = s.replace(max(matches), '_')
            return s

        def _distances(properties: Sequence[PropertySchema], keys: Sequence[str]) -> List[Tuple[PropertySchema, str, int]]:
            if len(keys) == 0:
                return []
            if len(properties) == 0:
                if not map_all:
                    return []
                return list(
                    map(
                        lambda e: (
                            PropertySchema(
                                name=_gen_name(e),
                                kind='str'  # TODO: infer kind
                            ),
                            e,
                            -1,
                        ),
                        keys,
                    )
                )

            x: Tuple[PropertySchema, str, int] = min(
                map(
                    lambda e: (
                        e[0],
                        e[1],
                        levenshtein.distance(
                            _normalize(e[0].name),
                            _normalize(e[1]),
                        )
                    ),
                    itertools.product(
                        properties,
                        keys,
                    )
                ),
                key=lambda e: e[2],
            )
            return [x] + _distances(
                list(filter(lambda e: e != x[0], properties)),
                list(filter(lambda e: e != x[1], keys)),
            )
        results = _distances(
            node.properties,
            df.columns,  # type: ignore
        )
        results = list(
            filter(
                lambda e: e[2] < tolerance * len(e[0].name),
                results,
            )
        )
        if len(results) == 0:
            return None
        properties = []
        for result in results:
            propery_schema = result[0]
            source = result[1]
            kind = None
            format = None

            series = df[source]

            def _match_phone(s: Any) -> bool:
                if isinstance(s, int) or isinstance(s, float):
                    s = str(s)
                if isinstance(s, str):
                    if phone_regex.search(s):
                        return True
                return False
            matches = series.map(_match_phone).value_counts(normalize=True)
            if True in matches and matches[True] >= 0.9:  # type: ignore
                kind = 'str'
                format = 'phone'

            def _match_date(s: Any) -> bool:
                if not isinstance(s, str):
                    return False
                dt = parse_date(s)
                return dt is not None
            matches = series.map(_match_date).value_counts(normalize=True)
            if True in matches and matches[True] >= 0.9:  # type: ignore
                kind = 'datetime'

            properties.append(
                PropertyMapping(
                    name=propery_schema.name,
                    source=source,
                    merge_behavior=preferred_merge_behavior,
                    kind=kind,
                    format=format,
                )
            )
        return Mapping(
            name=node.label,
            keys=[],
            label=node.label,
            properties=properties,
            edge_keys=[],
            edge_properties=[],
        )

    def generate_mappings(
        self,
        schema: Schema,
        df: pd.DataFrame,
        tolerance: float = 0.5,
        preferred_merge_behavior: str = merge_if_not_present,
        map_all: bool = True,
    ) -> Sequence[Mapping]:
        mappings = []
        for node in schema.nodes:
            mapping = self.generate_mapping(
                node=node,
                df=df,
                tolerance=tolerance,
                preferred_merge_behavior=preferred_merge_behavior,
                map_all=map_all,
            )
            if mapping is None:
                continue
            mappings.append(mapping)

        return mappings
