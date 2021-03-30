TIM
---
* `data_ora`: `DATA` + `ORA`
* `durata`: `Durata`
* `tipo`:
```
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
```
* `da_torre_cell_inizio`: `None`
* `da_torre_cell_fine`: `None`
* `da_cgi_inizio`: `CGI/ECGI/LocNumber`
* `da_cgi_fine`: `'CGI end`
* `da_numero`: `Telefono Chte`
* `da_imei`: `Imei Chte`
* `da_imsi`: `Imsi Chte`
* `a_cgi_inizio`: `None`
* `a_cgi_fine`: `None`
* `a_numero`: `Telefono Chto`
* `a_imei`: `Imei Chto`
* `a_imsi`: `Imsi Chto`
* `operatore`: '`TIM`'
* `esito_chiamata`: `durata == 0 ? 1 : 0`

Vodafone
---
* `data_ora`: `Data e Ora Inizio` | `Data`
* `durata`: (`Data e Ora Fine` - `data_ora`).seconds()
* `tipo`:
```
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
```
* `da_torre_cell_inizio`: `'-'.join('LAI-CI, Zona-Cella').split()[2:] if 'LAI-CI, Zona-Cella'.count(',') >= 2 else 'LAI-CI, Zona-Cella'`
* `da_torre_cell_fine`: `None`
* `da_cgi_inizio`: `'-'.join('LAI-CI, Zona-Cella').split()[0:2] if 'LAI-CI, Zona-Cella'.count(',') >= 2 else None`
* `da_cgi_fine`: `None`
* `da_numero`: `Chiamante`
* `da_imei`: `IMEI | IMEI/SERIAL`
* `da_imsi`: `Imsi Chte`
* `a_cgi_inizio`: `None`
* `a_cgi_fine`: `None`
* `a_numero`: `Chiamato`
* `a_imei`: `None`
* `a_imsi`: `None`
* `operatore`: '`Vodafone`'
* `esito_chiamata`: `'UCA' == 'U1' ? 0 : ('UCA' in ['U2', 'U3'] ? 1 : ('durata' == 0 ? 1 : 0) )`

Wind
---
A seconda che il tipo di chiamata sia entrante o uscente sono fornite solo le informazioni del chiamante(in uscita) o del chiamato(in entrata)
Tabella di conversione:
```
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
```
* `data_ora`: `Data`
* `durata`: `Durata Sec`
* `tipo`:
```
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
```
* `da_torre_cell_inizio`: `Cella Inizio/Fine`
* `da_torre_cell_fine`: `Cella Inizio/Fine`
* `da_cgi_inizio`: `None`
* `da_cgi_fine`: `None`
* `da_numero`: `Chiamante`
* `da_imei`: `Imei`
* `da_imsi`: `Imsi`
* `a_torre_cell_inizio`: `Cella Inizio/Fine`
* `a_torre_cell_fine`: `Cella Inizio/Fine`
* `a_cgi_inizio`: `None`
* `a_cgi_fine`: `None`
* `a_numero`: `Chiamato`
* `a_imei`: `Imei`
* `a_imsi`: `Imsi`
* `operatore`: '`Wind`'
* `esito_chiamata`: 
```
tipo in [
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
] ? 1 : 0
```

Sparkle
---
* `data_ora`: `Istante Impegno`
* `durata`: `DurataConv(sec)`
* `tipo`: '`V`'
* `da_torre_cell_inizio`: `None`
* `da_torre_cell_fine`: `None`
* `da_cgi_inizio`: `Centrale` + `Ori` if `Ori` != '' else `Centrale`
* `da_cgi_fine`: `None`
* `da_numero`: `N. Chiamante`
* `da_imei`: `None`
* `da_imsi`: `IMSI CTE`
* `a_torre_cell_inizio`: `None`
* `a_torre_cell_fine`: `None`
* `a_cgi_inizio`: `None`
* `a_cgi_fine`: `None`
* `a_numero`: `N. Chiamato`
* `a_imei`: `Imei`
* `a_imsi`: `IMSI CTO`
* `operatore`: '`Sparkle`'
* `esito_chiamata`: 1 if `durata` == 0 else 0


BT Italia
---
* `data_ora`: `DATA (GMT+1)`
* `durata`: `DURATA`
* `tipo`: `'X' if not isnull(CNUMBER) else 'V'`
* `da_torre_cell_inizio`: `None`
* `da_torre_cell_fine`: `None`
* `da_cgi_inizio`: `ROUTEIN`
* `da_cgi_fine`: `None`
* `da_numero`: `ANUMBER`
* `da_imei`: `None`
* `da_imsi`: `None`
* `a_torre_cell_inizio`: `None`
* `a_torre_cell_fine`: `None`
* `a_cgi_inizio`: `ROUTEOUT`
* `a_cgi_fine`: `None`
* `a_numero`: `CNUMBER if not isnull(CNUMBER) else BNUMBER`
* `a_imei`: `None`
* `a_imsi`: `None`
* `operatore`: '`BT Italia`'
* `esito_chiamata`: `0 if ESITO == 'effective' else 1`

Iliad
---
* `data_ora`: `data` + `ora`
* `durata`: `durata[sec]`
* `tipo`: 
```
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
```
* `da_torre_cell_inizio`: `None`
* `da_torre_cell_fine`: `None`
* `da_cgi_inizio`: `cgi_inizio`
* `da_cgi_fine`: `cgi_fine`
* `da_numero`: `chiamante` if tipo != 'forw' else `chiamante originale`
* `da_imei`: `imei`
* `da_imsi`: `imsi`
* `a_torre_cell_inizio`: `None`
* `a_torre_cell_fine`: `None`
* `a_cgi_inizio`: `None`
* `a_cgi_fine`: `None`
* `a_numero`: `chiamato`
* `a_imei`: `None`
* `a_imsi`: `None`
* `operatore`: '`Iliad`'
* `esito_chiamata`: `1 if Durata == 0 else 0`