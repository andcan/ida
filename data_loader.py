import itertools
from data import merge_if_not_present, Mapping, PropertyMapping, PropertySchema, Schema, NodeSchema
from typing import Any, Dict, List, Optional, Sequence, Tuple
import pandas as pd
import re
import Levenshtein as levenshtein
import pandas as pd
import dateparser
import datetime
import xmltodict
import json
import jsonpath_ng
import datetime
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

preferred_case_match_source = 'preferred_case_match_source'
preferred_case_snake_case = 'preferred_case_snake_case'
preferred_case_camel_case = 'preferred_case_camel_case'

phone_regex = re.compile(r'((\d{2}|\+)?\d{2})?(\d[ -]*){8,15}')


ddp = dateparser.DateDataParser(languages=['it'], settings={
    'DATE_ORDER': 'DMY'
})


def parse_date(s: str):
    data = ddp.get_date_data(s)
    if data:
        return data['date_obj']
    return None

class DataLoader(object):

    def dataframe_from_csv(self, filename: str, dtype=str) -> pd.DataFrame:
        return pd.read_csv(filename, delimiter=';', dtype=dtype)

    def dataframe_from_xml(self, filename: str, path: str) -> pd.DataFrame:
        with open(filename, 'r') as f:
            # convert xml to a dictionary
            d = xmltodict.parse(f.read())
            pathexpr = jsonpath_ng.parse(path)
            matches = pathexpr.find(d)
            if len(matches) == 0:
                raise Exception('no matches fot path <{}>'.format(path))
            return pd.json_normalize(matches[0].value) # flatten data

    def dataframe_from_json(self, filename: str, path: Optional[str] = None) -> pd.DataFrame:
        with open(filename, 'r') as f:
            d = json.loads(f.read())
            # optionally apply path
            if path is not None and path != '':
                pathexpr = jsonpath_ng.parse(path)
                matches = pathexpr.find(d)
                if len(matches) == 0:
                    # cml 1 rt text="invalid path"
                    raise Exception('no matches fot path <{}>'.format(path))
                d = matches[0].value
            return pd.json_normalize(d) # flatten data

    def load(self, filename, query: Optional[str] = None, path: Optional[str] = None, dtype: Optional[Any] = str) -> pd.DataFrame:
        """
        Loads filename and applies query if provided.

        path parameter is used only for json and xml files, and mandatory for xml.
        """
        if filename.endswith('.csv'):
            df = self.dataframe_from_csv(filename, dtype=dtype)
        elif filename.endswith('.xml'):
            if path is None or path == '':
                # cml 1 rt text="path is required"
                raise Exception('path is required')
            df = self.dataframe_from_xml(filename, path=path)
        elif filename.endswith('.json'):
            df = self.dataframe_from_json(filename, path=path)
        else:
            # cml 1 rt text="unsupported file type"
            raise Exception('unsupported file type')
        if query != None:
            df = df.query(query)
        # drop completely empty rows and columns
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
            """
            Remove noise to get better matching
            """
            s = s.lower()
            return re.sub(r'[^A-Za-z0-9]', '', s)

        def _gen_name(s: str) -> str:
            """
            Generates a safe name for given property
            """
            s = re.sub(r'[^A-Za-z0-9 ]', '', s)
            s = '_'.join(s.split(' '))
            while True:
                matches = re.findall('_{2,}', s)
                if len(matches) == 0:
                    break
                s = s.replace(max(matches), '_')
            return s

        def _distances(properties: Sequence[PropertySchema], keys: Sequence[str]) -> List[Tuple[PropertySchema, str, int]]:
            """
            Generates Lehvenstein distances forgiven properties
            """
            if len(keys) == 0:
                return []
            if len(properties) == 0:
                if not map_all: # there is no need to map all
                    return []
                # return a list containing all remaining keys
                return list(
                    map(
                        lambda e: (
                            PropertySchema(
                                name=_gen_name(e),
                                kind='str'
                            ),
                            e,
                            -1,
                        ),
                        keys,
                    )
                )
            # find best match
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
            # build list of distances recursively
            return [x] + _distances(
                list(filter(lambda e: e != x[0], properties)),
                list(filter(lambda e: e != x[1], keys)),
            )
        # get all matches
        results = _distances(
            node.properties,
            df.columns,
        )
        # filter out matches that do not satisfy tolerance 
        results = list(
            filter(
                lambda e: e[2] < tolerance * len(e[0].name),
                results,
            )
        )
        if len(results) == 0:
            return None
        # type recognition
        properties = []
        for result in results:
            propery_schema = result[0]
            source = result[1]
            kind = None
            format = None

            # extract series for source column
            series = df[source]

            def _match_phone(s: Any) -> bool:
                """
                Matches strings or numbers that look like phones
                """
                if isinstance(s, int) or isinstance(s, float):
                    s = str(s)
                if isinstance(s, str):
                    if phone_regex.search(s):
                        return True
                return False
            matches = series.map(_match_phone).value_counts(normalize=True)
            # if at least 90% of values match phones, column is very likely to contain phones
            if True in matches and matches[True] >= 0.9:
                kind = 'str'
                format = 'phone'

            if not kind:
                def _match_date(s: Any) -> bool:
                    """
                    Matches strings that look like dates
                    """
                    if not isinstance(s, str):
                        return False
                    dt = parse_date(s)
                    return dt is not None
                matches = series.map(_match_date).value_counts(normalize=True)
                # if at least 90% of values match dates, column is very likely to contain dates
                if True in matches and matches[True] >= 0.9:
                    kind = 'datetime'

            if not kind:
                if is_numeric_dtype(series):
                    kind = str(series.dtype)

            if not kind:
                try:
                    if is_string_dtype(series.dtype):
                        matches = (series.apply(
                            lambda e: 0 if pd.isnull(e) else e)).astype(int)
                        counts = matches.value_counts(normalize=True)
                        # if at least 90% of values match 0's and 1's, column is very likely to contain bools
                        if 0 in counts and 1 in counts and counts[0] + counts[1] >= 0.9:
                            kind = 'bool'
                        else:
                            kind = 'int'
                except:
                    # nothing wrong do not break
                    pass

            if not kind:
                matches = (series.str.isdecimal() == True).value_counts()
                # if at least 90% of values match decimals, column is very likely to contain decimals
                if True in matches and matches[True] >= 0.9:
                    kind = 'float'

            if not kind:
                # fallback to string
                kind = 'str'

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
