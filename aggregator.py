import os
import re
from typing import Callable, List, Optional, Pattern, Tuple
import numpy as np
from numpy.lib.npyio import load
import pandas as pd
import io
import dateparser
import csv

xxtab_tim_prefix = r'(\d\dTab/|(f|F8)_\d\d).*/(Tim|tim|Telefonico|TIM).*/Package[0-9_]+'
xxtab_voda_prefix = r'\d\dTab/.*/(Vodafone|vOD|vODA|voda|Voda|vODAFONE|VOD|VODA).*/Package[a-zA-Z0-9_$]+'
xxtab_wind_prefix = r'\d\dTab/.*/(Telefonico wind|Wind|WIND).*'
xxtab_sparkle_prefix = r'\d\dTab/.*/(SPARKLE|Sparkle).*'
f8xx_tim_prefix = r'(f|F)8_\d\d/.*/(TIm|TIM|Tim|tim).*'
f8_bt_italia_prefix = r'(f|F)8_\d\d/.*/(BT Italia).*'
f8xx_iliad_prefix = r'(f|F)8_\d\d/.*/(Iliad|ILIAD|iliad).*'

ddp = dateparser.DateDataParser(languages=['it'], settings={
    'DATE_ORDER': 'DMY'
})


def parse_date(s: str):
    data = ddp.get_date_data(s)
    if data:
        return data['date_obj']
    return None


def clean_files(path: str, patterns: List[str], f: Optional[Callable[[str], bool]] = None) -> None:
    def _clean_files(path: str, patterns: List[Pattern[str]], f: Optional[Callable[[str], bool]] = None) -> None:
        def _del(filepath: str):
            print('deleting ' + filepath)
            os.unlink(filepath)
        files = os.listdir(path)
        for file in files:
            filepath = path + '/' + file
            if os.path.isdir(filepath):
                _clean_files(filepath, patterns, f)
            for pattern in patterns:
                if pattern.search(filepath):
                    if f == None:
                        _del(filepath)
                    elif f(filepath):
                        _del(filepath)
    _clean_files(path, [re.compile(p) for p in patterns], f)


def cleandirs(path: str) -> None:
    files = os.listdir(path)
    if len(files) == 0:
        print('deleting ' + path)
        os.rmdir(path)
        return
    for file in files:
        filepath = path + '/' + file
        if os.path.isdir(filepath):
            cleandirs(filepath)


def clean():
    clean_files('data', [
        # xxtab_tim
        r'{}/coverletter.pdf'.format(xxtab_tim_prefix),
        r'{}/Report[0-9_]+AnagraficaSemplice.*.(pdf|txt)'.format(
            xxtab_tim_prefix),
        r'.*/Anag Tim 8/Report.*AnagraficaSemplice.*.txt',
        r'{}/Report[0-9_]+Traffico.*.pdf'.format(xxtab_tim_prefix),
        r'{}/verbale.*.pdf'.format(xxtab_tim_prefix),
        # xxtab_voda
        r'{}/[0-9_]+intestatari.*.(pdf|txt)'.format(xxtab_voda_prefix),
        r'{}/[0-9_]+traffico.*.(pdf|xls)'.format(xxtab_voda_prefix),
        r'{}/Nota_Di_Consegna.pdf'.format(xxtab_voda_prefix),
        # xxtab_wind
        r'{}/.*ANAG_.*.TXT'.format(xxtab_wind_prefix),
        r'{}/.*\.asc'.format(xxtab_wind_prefix),
        r'{}/.*\.pdf'.format(xxtab_sparkle_prefix),
        r'{}/.*\.xls'.format(f8_bt_italia_prefix),
        r'{}/.*\.pdf'.format(f8xx_tim_prefix),
    ])

    def _contains_pattern(filepath: str, pattern: Pattern[str]):
        with open(filepath, 'r') as f:
            if pattern.search(f.read()):
                return True
            return False

    def _tim_no_conversations(filepath: str):
        return _contains_pattern(
            filepath,
            re.compile(
                r'\*\*\* NON SONO STATE RILEVATE CONVERSAZIONI \*\*\*',
            ),
        )
    clean_files('data', [
        r'{}/Report[0-9_]+_Traffico.*.txt'.format(xxtab_tim_prefix),
    ], _tim_no_conversations)

    def _tim_f8_no_conversations(filepath: str):
        return _contains_pattern(
            filepath,
            re.compile(
                r'\*\*\* NON SONO STATE RILEVATE CONVERSAZIONI \*\*\*',
            ),
        ) or _contains_pattern(
            filepath,
            re.compile(
                r"\*\*\* NON E' STATO RILEVATO TRAFFICO \*\*\*"
            )
        )
    clean_files('data', [
        r'{}/Report.*.txt'.format(f8xx_tim_prefix),
    ], _tim_f8_no_conversations)

    def _voda_no_conversations(filepath: str):
        return _contains_pattern(
            filepath,
            re.compile(
                r'Nessun movimento rilevato nel periodo indicato',
            ),
        )
    clean_files('data', [
        r'{}/[0-9_]+traffico.*.txt'.format(xxtab_voda_prefix),
    ], _voda_no_conversations)

    def _wind_no_conversations(filepath: str):
        return _contains_pattern(
            filepath,
            re.compile(
                r'SEZIONE DATI DI TRAFFICO: NESSUN RECORD TROVATO'
            )
        )
    clean_files('data', [
        r'{}/.*TRAFF_.*.TXT'.format(xxtab_wind_prefix),
    ], _wind_no_conversations)

    def _sparkle_no_conversations(filepath: str):
        with open(filepath, 'r') as f:
            matches = re.findall(
                r'\*\*\*\* la ricerca non ha prodotto risultati \*\*\*\*', f.read())
            return len(matches) == 2
    clean_files('data', [
        r'{}/.*TraffNum.*.txt'.format(xxtab_sparkle_prefix),
    ], _sparkle_no_conversations)
    cleandirs('data')


def detect_csvs(filepath: str, separator: str, fun: Callable[[str, Optional[str], str], Tuple[bool, str]]) -> List[str]:
    with open(filepath, 'r') as f:
        csvs: List[str] = []
        lines: List[str] = []
        while True:
            line = f.readline().rstrip('\n')
            if not line:
                break
            if len(line.strip()) == 0:
                continue
            pos = line.find(separator)
            if pos < 0:
                if len(lines) > 0:
                    csvs.append('\n'.join(lines))
                    lines = []
            else:
                match, line = fun(
                    line,
                    None if len(lines) == 0 else lines[0],
                    separator,
                )
                if not match:
                    csvs.append('\n'.join(lines))
                    lines = []
                lines.append(separator.join([
                    value.strip() for value in line.split(separator)
                ]))
        return csvs


def list_files(path: str, sort=True) -> List[str]:
    found = []
    files = os.listdir(path)
    for file in files:
        filepath = path + '/' + file
        if os.path.isdir(filepath):
            for f in list_files(filepath, sort=False):
                found.append(f)
        else:
            found.append(filepath)
    if sort:
        found.sort()
    return found


def load_xxtab_tim():
    pattern = re.compile(
        r'{}/Report[0-9_]+_Traffico.*.txt'.format(xxtab_tim_prefix)
    )

    def _match(line: str, header: Optional[str], separator: str) -> Tuple[bool, str]:
        if header is None:
            return (True, line+';')
        hcount = header.count(separator)
        count = line.count(separator)
        return (hcount == count, line)
    dfs: List[pd.DataFrame] = []
    for filepath in list_files('data'):
        if pattern.search(filepath):
            csvs = detect_csvs(filepath, separator=';', fun=_match)
            if len(csvs) > 0:
                df = pd.read_csv(io.StringIO(csvs[0]), sep=';')  # type: ignore
                df['nome_file_importato'] = filepath  # type: ignore
                dfs.append(df)  # type: ignore
    df = dfs[0]
    for i in range(1, len(dfs)):
        df = pd.concat([df, dfs[i]], axis=0)

    df = df[
        (df['DATA'] != '') & (df['ORA'] != '') &
        (df['Telefono Chte'] != '') & (df['Telefono Chto'] != '')
    ]

    df['data_ora'] = df['DATA'] + ' ' + df['ORA']
    del df['DATA']
    del df['ORA']

    df['durata'] = df['Durata']
    del df['Durata']

    def _map_tipo(e: str) -> str:
        mappings = {
            'S': [
                '0',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                'AP',
                'J',
                'N',
                'P',
                'PA',
                'Q',
                'R',
                'S',
                'W',
                'Z',
            ],
            'F': [
                '1',
                'X',
                'Y'
            ],
            'V': [
                '8',
                'E',
                'F',
                'FI',
                'FICS',
                'FIHO',
                'FIPS',
                'G',
                'I',
                'ICS',
                'IHO',
                'IPS',
                'L'
            ],
            'D': [
                '9',
                'C',
                'D',
                'H',
                'M',
                'V',
                'VI',
                'VIHO',
                'VIPS',
                'VK',
            ],
            'X': [
                'K'
            ],
        }
        for key in mappings:
            for value in mappings[key]:
                if value == e:
                    return key
        return ''

    df['tipo'] = df['Tipo Chta'].apply(_map_tipo)
    del df['Tipo Chta']

    df['da_torre_cell_inizio'] = ''

    df['da_torre_cell_fine'] = ''

    df['da_cgi_inizio'] = df['CGI/ECGI/LocNumber']
    del df['CGI/ECGI/LocNumber']

    df['da_cgi_fine'] = df['CGI end']
    del df['CGI end']

    df['da_numero'] = df['Telefono Chte']
    del df['Telefono Chte']

    df['da_imei'] = df['Imei Chte']
    del df['Imei Chte']

    df['da_imsi'] = df['Imsi Chte']
    del df['Imsi Chte']

    df['a_torre_cell_inizio'] = ''

    df['a_torre_cell_fine'] = ''

    df['a_cgi_inizio'] = ''
    df['a_cgi_fine'] = ''

    df['a_numero'] = df['Telefono Chto']
    del df['Telefono Chto']

    df['a_imei'] = df['Imei Chto']
    del df['Imei Chto']

    df['a_imsi'] = df['Imsi Chto']
    del df['Imsi Chto']

    df['operatore'] = 'TIM'

    df['esito_chiamata'] = ''

    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]

    df.to_csv('extracted_data/xxtab_tim.csv', sep=';')


def load_xxtab_voda():
    pattern = re.compile(
        r'{}/[0-9_]+traffico.*.txt'.format(xxtab_voda_prefix),
    )
    df: Optional[pd.DataFrame] = None
    for filepath in list_files('data'):
        if pattern.search(filepath):
            with open(filepath, 'r') as f:
                lines = []
                colspecs = []
                while True:
                    line = f.readline()
                    if not line or 'Legenda:' in line:
                        break
                    if line == '\n':
                        continue
                    if len(lines) > 0:
                        lines.append(line)
                        (start, end) = colspecs[len(colspecs) - 1]
                        if len(line) > end:
                            colspecs[len(colspecs) - 1] = (start, len(line))
                    elif 'Chiamato' in line and 'Chiamante' in line:
                        lines.append(line)
                        spaces = 0
                        start = 0
                        for i in range(1, len(line)):
                            current = line[i]
                            if current != ' ':
                                if spaces > 1:
                                    colspecs.append((start, i))
                                    start = i
                                spaces = 0
                            else:
                                spaces = spaces + 1
                        colspecs.append((start, len(line)))
                data = ''.join(lines)
                dataframe = pd.read_fwf(io.StringIO(data), colspecs=colspecs)
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])

    df['Data e Ora Inizio'] = df['Data e Ora Inizio'].combine_first(
        df['Data']).apply(parse_date)
    del df['Data']
    df['Data e Ora Fine'] = df['Data e Ora Fine'].combine_first(
        df['Data Fine']).apply(parse_date)
    del df['Data Fine']

    df['data_ora'] = df['Data e Ora Inizio']
    df['durata'] = (df['Data e Ora Fine'] - df['Data e Ora Inizio']
                    ).apply(lambda e: e.total_seconds())
    del df['Data e Ora Inizio']
    del df['Data e Ora Fine']

    def _map_tipo(e: str) -> str:
        mappings = {
            'S': [
                '6',
                '7',
                '8',
                '9',
                '55',
                '56',
                '63',
                'A20',
                'A21',
                'V6',
            ],
            'F': [
            ],
            'V': [
                '1',
                '2',
                '4',
                '5',
                '10',
                '24',
                '39',
                '44',
                '46',
                '47',
                '58',
                '60',
                '61',
                'A2',
                'A4',
                'A8',
                'A9',
                'A11',
                'M',
                'V',
                'V1',
                'V2',
            ],
            'D': [
                '23',
                '26',
                '29',
                '43',
                'N',
                'Q',
                'R',
                'U',
                'T',
            ],
            'X': [
                '3',
            ],
        }
        for key in mappings:
            for value in mappings[key]:
                if value == e:
                    return key
        return ''

    df['tipo'] = df['Tipo'].astype(str).apply(_map_tipo)
    del df['Tipo']

    df['da_torre_cell_inizio'] = ''

    df['da_torre_cell_fine'] = ''

    df['da_cgi_inizio'] = df['LAI-CI, Zona-Cella'].apply(
        lambda e: ''.join(e.split()[0:3]))

    df['da_cgi_fine'] = ''

    df['da_numero'] = df['Chiamante']
    del df['Chiamante']

    df['IMEI'] = df['IMEI'].combine_first(df['IMEI/SERIAL'])
    del df['IMEI/SERIAL']
    df['da_imei'] = df['IMEI']
    del df['IMEI']

    df['da_imsi'] = df['IMSI']
    del df['IMSI']

    df['a_torre_cell_inizio'] = ''

    df['a_torre_cell_fine'] = ''

    df['a_cgi_inizio'] = ''
    df['a_cgi_fine'] = ''

    df['a_numero'] = df['Chiamato']
    del df['Chiamato']

    df['a_imei'] = ''

    df['a_imsi'] = ''

    df['operatore'] = 'Vodafone'

    def _map_esito(s: str) -> str:
        if s == 'U1':
            return '0'
        elif s in ['U2', 'U3']:
            return '1'
        return ''
    df['esito_chiamata'] = df['UCA'].apply(_map_esito)

    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]
    # df.to_csv('extracted_data/xxtab_voda.csv', sep=';')


def load_xxtab_wind():
    pattern = re.compile(
        r'{}/.*TRAFF_.*.TXT'.format(xxtab_wind_prefix)
    )
    dtype = {
        'Imsi': str,
        'IMSI': str,
        'Imei': str,
        'IMEI': str,
        'Chiamante': str,
        'Chiamato': str
    }
    df: Optional[pd.DataFrame] = None
    for filepath in list_files('data'):
        if pattern.search(filepath):
            with open(filepath, 'r') as f:
                # if not 'Dettaglio Traffico MMS e SMS' in c:
                lines = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line == '\n' or line == ' \n':
                        if len(lines) > 0:
                            break
                        continue
                    if len(lines) > 0:
                        lines.append(line)
                    elif 'Chiamante' in line and 'Chiamato' in line:
                        if not line:
                            break
                        if '|' in line:
                            line = re.sub(r'\s*\|\s*', r'|', line)
                            lines.append(line)
                if len(lines) == 0:
                    continue
                data = ''.join(lines)
                dataframe: pd.DataFrame = pd.read_csv(
                    io.StringIO(data), sep='|', dtype=dtype, quoting=csv.QUOTE_NONE)  # type: ignore
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])
                lines = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line == '\n' or line == ' \n':
                        if len(lines) > 0:
                            break
                        continue
                    if len(lines) > 0:
                        lines.append(line)
                    elif 'Mittente' in line and 'Destinatario' in line:
                        if not line:
                            break
                        if '|' in line:
                            line = re.sub(r'\s*\|\s*', r'|', line)
                            lines.append(line)
                if len(lines) == 0:
                    continue
                data = ''.join(lines)
                dataframe: pd.DataFrame = pd.read_csv(
                    io.StringIO(data), sep='|', dtype=dtype, quoting=csv.QUOTE_NONE)  # type: ignore
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])

    del df['Rete']
    del df['Rete mittente']
    del df['Rete Mittente']
    del df['Rete destinatario']
    del df['Rete Destinatario']
    del df['Id Mvno']

    df['Imsi'] = df['Imsi'].combine_first(df['IMSI'])
    del df['IMSI']

    df['Imei'] = df['Imei'].combine_first(df['IMEI'])
    del df['IMEI']

    df['Cella Inizio/Fine'] = df['Cella Inizio/Fine'].combine_first(
        df['Cella inizio/fine'])
    del df['Cella inizio/fine']

    df['Redirect Num'] = df['Redirect Num'].combine_first(df['Redirect Num '])
    del df['Redirect Num ']

    df['Chiamante'] = df['Chiamante'].combine_first(df['Mittente'])
    del df['Mittente']

    df['Chiamato'] = df['Chiamato'].combine_first(df['Destinatario'])
    del df['Destinatario']

    df['Tipo'] = df['Tipo'].combine_first(df['Stato'])
    del df['Stato']

    def _map_cella(startstr: str, endstrs: List[str]) -> Callable[[str], Tuple[str, str]]:
        def __map_cella(e: str) -> Tuple[str, str]:
            if e.strip() == '' or e == 'nan':
                return (np.nan, np.nan)
            istart = 0
            iend = len(e)
            fstart = iend
            if startstr in e:
                istart = e.index(startstr)+len(startstr)
            for endstr in endstrs:
                if endstr in e:
                    iend = e.index(endstr)
                    fstart = iend+len(endstr)
                    break
            start = e[istart:iend]
            if start == '-':
                start = np.nan
            end = e[fstart:]
            if end == '-':
                end = np.nan
            return (start, end)
        return __map_cella

    cif = df['Cella Inizio/Fine'].astype(str).apply(
        _map_cella('Inizio:', ['TOP-Fine:', 'Fine:']))
    df['Cella inizio'] = cif.apply(lambda e: e[0])
    df['Cella fine'] = cif.apply(lambda e: e[1])
    del df['Cella Inizio/Fine']

    cmd = df['Cella'].astype(str).apply(
        _map_cella('Mittente:', ['Destinatario:'])
    )
    df['Cella inizio'] = df['Cella inizio'].combine_first(
        cmd.apply(lambda e: e[0])
    )
    df['Cella fine'] = df['Cella fine'].combine_first(
        cmd.apply(lambda e: e[1])
    )
    del df['Cella']

    df['Cella inizio'] = df['Cella inizio'].combine_first(df['Cella mittente'])
    del df['Cella mittente']
    df['Cella inizio'] = df['Cella inizio'].combine_first(df['Cella Mittente'])
    del df['Cella Mittente']

    df['Cella fine'] = df['Cella fine'].combine_first(
        df['Cella destinatario  ']
    )
    del df['Cella destinatario  ']
    df['Cella fine'] = df['Cella fine'].combine_first(
        df['Cella Destinatario']
    )
    del df['Cella Destinatario']

    df['data_ora'] = df['Data'].astype(str).apply(parse_date)
    del df['Data']

    df['durata'] = df['Durata Sec']
    del df['Durata Sec']

    ins = [
        'MTC',
        'SMST-2',
        'SMST-LTE',
        'UCA/MTC',
        'RCFW',
        'SMST',
        'UCA/RCFW-2',
        'MMST-S',
        'TAP-MTC',
        'TAP-SMST',
        'UCA/RCFW-1',
    ]
    outs = [
        'MOC',
        'CF-1',
        'SMSO-2',
        'UCA/MOC',
        'SMSO-LTE',
        'UCA/MOC-1',
        'SMSO',
        'TAP-MOC',
        'SCP-MOC',
        'SMSO-1',
        'UCA/CF-2',
        'InvioMsgDiOOO',
        'MMSO',
        'CF',
        'UCA/MOROC',
        'SCP-CF',
        'UCA/CF- 2',
        'UCA/CF-1',
    ]

    fails = [
        'CF-1',
        'UCA/MTC',
        'UCA/MOC',
        'UCA/CF-1',
        'UCA/MOC-1',
        'UCA/RCFW-2',
        'UCA/CF-2',
        'UCA/RCFW-1',
        'UCA/MOROC',
        'UCA/CF- 2',
    ]

    def _map_tipo(e: str) -> str:
        mappings = {
            'S': [
                'SMST-2',
                'SMST-LTE',
                'SMSO-2',
                'SMSO-LTE',
                'SMST',
                'SMSO',
                'TAP-SMST',
                'SMSO-1',
                'InvioMsgDiOOO',
            ],
            'F': [
            ],
            'V': [
                'MOC',
                'MTC',
                'UCA/MOC',
                'RCFW',
                'UCA/MOC-1',
                'UCA/RCFW-2',
                'TAP-MOC',
                'TAP-MTC',
                'SCP-MOC',
                'UCA/RCFW-1',
                'UCA/MOROC',
            ],
            'D': [
                'MMST-S',
                'MMSO',
            ],
            'X': [
                'CF-1',
                'UCA/CF-1',
                'UCA/CF-2',
                'CF',
                'SCP-CF',
                'UCA/CF- 2',
            ],
        }
        for key in mappings:
            for value in mappings[key]:
                if value == e:
                    return key
        return np.nan

    df['tipo'] = df['Tipo'].astype(str).apply(_map_tipo)
    df = df[df['tipo'].notna()]

    df['da_torre_cell_inizio'] = df['Cella inizio']
    del df['Cella inizio']

    df['da_torre_cell_fine'] = df['Cella fine']
    del df['Cella fine']

    df['da_cgi_inizio'] = ''

    df['da_cgi_fine'] = ''

    df['da_numero'] = df['Chiamante']
    del df['Chiamante']

    def _map_in_out(x: pd.Series):
        if x['Tipo'] in outs:
            x['da_imei'] = x['Imei']
            x['da_imsi'] = x['Imsi']
            x['a_imei'] = np.nan
            x['a_imsi'] = np.nan
        elif x['Tipo'] in ins:
            x['da_imei'] = np.nan
            x['da_imsi'] = np.nan
            x['a_imei'] = x['Imei']
            x['a_imsi'] = x['Imsi']
        else:
            raise Exception(x['Tipo'])
        x['esito_chiamata'] = '1' if x['Tipo'] in fails else '0'
        return x
    df = df.apply(_map_in_out, axis=1)
    del df['Tipo']

    df['a_torre_cell_inizio'] = ''

    df['a_torre_cell_fine'] = ''

    df['a_cgi_inizio'] = ''
    df['a_cgi_fine'] = ''

    df['a_numero'] = df['Chiamato']
    del df['Chiamato']

    df['operatore'] = 'WindTre'

    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]
    df.to_csv('extracted_data/xxtab_wind.csv', sep=';')
    return df


def load_xxtab_sparkle():
    pattern = re.compile(
        r'{}/.*TraffNum.*.txt'.format(xxtab_sparkle_prefix),
    )
    df: Optional[pd.DataFrame] = None
    for filepath in list_files('data'):
        if pattern.search(filepath):
            with open(filepath, 'r') as f:
                lines = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.strip() == '':
                        continue
                    if '|' in line:
                        line = '|'.join([l.strip() for l in line.split('|')])
                    if 'Centrale' in line and 'NDC' in line:
                        if not len(lines) > 0:
                            lines.append(line)
                    elif len(lines) > 0:
                        if not '|' in line:
                            continue
                        lines.append(line)
                data = '\n'.join(lines)
                dataframe: pd.DataFrame = pd.read_csv(
                    io.StringIO(data), delimiter='|', dtype=str)  # type: ignore
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])
    df['data_ora'] = df['Istante Impegno'].apply(parse_date)
    del df['Istante Impegno']

    df['durata'] = df['DurataConv(sec)']
    del df['DurataConv(sec)']

    df['tipo'] = 'V'

    def _map_cgi(x: pd.Series):
        origine = str(x['Ori']).strip()
        if origine != '':
            x['da_cgi_inizio'] = x['Centrale'] + ' ' + origine
        else:
            x['da_cgi_inizio'] = x['Centrale']
        return x
    df = df.apply(_map_cgi, axis=1)
    del df['Centrale']
    del df['Ori']

    df = df.rename(columns={
        'N. Chiamante': 'da_numero',
        'N. Chiamato': 'a_numero',
        'IMSI CTE': 'da_imsi',
        'IMSI CTO': 'a_imsi',
    })

    df['da_cgi_fine'] = ''
    df['da_imei'] = ''
    df['a_imei'] = ''
    df['da_torre_cell_inizio'] = ''
    df['a_torre_cell_inizio'] = ''
    df['da_torre_cell_fine'] = ''
    df['a_torre_cell_fine'] = ''
    df['a_cgi_inizio'] = ''
    df['a_cgi_fine'] = ''
    df['operatore'] = 'Sparkle'
    df['esito_chiamata'] = df['durata'].apply(lambda e: 1 if e == '0' else 0)
    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]
    df.to_csv('extracted_data/xxtab_sparkle.csv', sep=';')
    return df


def load_f8xx_bt_italia():
    pattern = re.compile(
        r'{}/SD.*\.csv'.format(f8_bt_italia_prefix),
    )
    df: Optional[pd.DataFrame] = None
    for filepath in list_files('data'):
        if pattern.search(filepath):
            with open(filepath, 'r') as f:
                data = f.read()
                pos = data.find('\n')
                if pos == -1:
                    continue
                data = data[pos+1:]
                dataframe: pd.DataFrame = pd.read_csv(
                    io.StringIO(data),
                    delimiter=',',
                    dtype=str,
                )  # type: ignore
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])

    df = df.rename(columns={
        'DURATA': 'durata',
        'ROUTEIN': 'da_cgi_inizio',
        'ROUTEOUT': 'a_cgi_inizio',
        'ANUMBER': 'da_numero',
    })

    df['data_ora'] = df['DATA (GMT+1)'].apply(parse_date)
    del df['DATA (GMT+1)']

    def _map(x: pd.Series):
        x['tipo'] = 'X' if not pd.isnull(x['CNUMBER']) else 'V'
        x['esito_chiamata'] = '0' if x['ESITO'] == 'effective' else '1'
        x['a_numero'] = x['CNUMBER'] if not pd.isnull(
            x['CNUMBER']) else x['BNUMBER']
        return x
    df = df.apply(_map, axis=1)

    df['a_cgi_inizio'] = ''
    df['da_torre_cell_inizio'] = ''
    df['da_torre_cell_fine'] = ''
    df['da_cgi_fine'] = ''
    df['da_imei'] = ''
    df['da_imsi'] = ''

    df['a_torre_cell_inizio'] = ''
    df['a_torre_cell_fine'] = ''
    df['a_cgi_fine'] = ''
    df['a_imei'] = ''
    df['a_imsi'] = ''
    df['operatore'] = 'BT Italia'

    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]
    df.to_csv('extracted_data/f8xx_bt_italia.csv', sep=';')
    return df


def load_f8xx_iliad():
    pattern = re.compile(
        r'{}/.*\.txt'.format(f8xx_iliad_prefix),
    )
    df: Optional[pd.DataFrame] = None
    for filepath in list_files('data'):
        if pattern.search(filepath):
            with open(filepath, 'r') as f:
                lines = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.strip() == '':
                        continue
                    if 'chiamante_originale' in line and 'chiamante' in line:
                        if len(lines) == 0:
                            lines.append(line)
                    elif len(lines) > 0:
                        if line.count(',') == lines[0].count(','):
                            lines.append(line)
                if len(lines) == 0 or len(lines) == 1:
                    continue
                data = ''.join(lines)
                dataframe: pd.DataFrame = pd.read_csv(
                    io.StringIO(data),
                    delimiter=',',
                    dtype=str,
                )  # type: ignore
                dataframe['nome_file_importato'] = filepath
                if df is None:
                    df = dataframe
                else:
                    df = pd.concat([df, dataframe])
    df = df.replace('-', np.nan)

    df = df.rename(columns={
        'durata[sec]': 'durata',
        'cgi_inizio': 'da_cgi_inizio',
        'cgi_fine': 'da_cgi_fine',
        'imei': 'da_imei',
        'imsi': 'da_imsi',
        'chiamato': 'a_numero'
    })

    df['data_ora'] = df['data'] + ' ' + df['ora']
    del df['data']
    del df['ora']

    def _map_chiamante(x: pd.Series):
        if x['tipo'] == 'forw' and pd.notnull(x['chiamante_originale']) and x['chiamante_originale'] != '':
            x['da_numero'] = x['chiamante_originale']
        return x
    df = df.apply(_map_chiamante, axis=1)

    def _map_tipo(e: str) -> str:
        mappings = {
            'S': [
                'smsc_smsmo',
                'smsc_smsmt',
                'smmt',
                'smsc_smsmt_report',
                'smmo',
                'smsc_smsmt_fwd',
            ],
            'F': [
            ],
            'V': [
                'moc',
                'mtc',
                'csr',
                'poc',
                'mtc-nr',
                'ptc',
            ],
            'D': [
            ],
            'X': [
                'forw',
            ],
        }
        for key in mappings:
            for value in mappings[key]:
                if value == e:
                    return key
        return np.nan
    df['tipo'] = df['tipo'].apply(_map_tipo)

    df['da_torre_cell_inizio'] = ''
    df['da_torre_cell_fine'] = ''
    df['a_torre_cell_inizio'] = ''
    df['a_torre_cell_fine'] = ''
    df['a_cgi_inizio'] = ''
    df['a_cgi_fine'] = ''
    df['a_imei'] = ''
    df['a_imsi'] = ''

    df['operatore'] = 'Iliad'
    df['esito_chiamata'] = df['durata'].apply(
        lambda e: '1' if e == '0' else '0')
    df = df[
        [
            'data_ora',
            'durata',
            'tipo',
            'da_torre_cell_inizio',
            'da_torre_cell_fine',
            'da_cgi_inizio',
            'da_cgi_fine',
            'da_numero',
            'da_imei',
            'da_imsi',
            'a_torre_cell_inizio',
            'a_torre_cell_fine',
            'a_cgi_inizio',
            'a_cgi_fine',
            'a_numero',
            'a_imei',
            'a_imsi',
            'operatore',
            'nome_file_importato',
            'esito_chiamata'
        ]
    ]
    df.to_csv('extracted_data/f8xx_iliad.csv', sep=';')
    return df


def main():
    clean()
    # load_xxtab_tim()
    # load_xxtab_voda()
    # load_xxtab_wind()
    # load_xxtab_sparkle()
    # load_f8xx_bt_italia()
    load_f8xx_iliad()


if __name__ == "__main__":
    main()
