import pandas as pd

from FUNCOES import *
from datetime import datetime as dt

PAPEL = ['HASH11', 'ITSA4', 'BOVA11', 'ABEV3', 'ITSAM873', 'ABEVA155', 'ABEVB154', 'ABEVM148',
         'BOVAA103', 'BOVAM103', 'BOVAA109']

inicializacao()
ativosvisiveis(PAPEL)

df1 = pd.DataFrame()
for ativo in PAPEL:
    info = mt.symbol_info(ativo)._asdict()
    dict = {'ativo': [info['name']],
            'ultimo': [info['last']],
            'venda': [info['bid']],
            'compra': [info['ask']],
            'strike': [info['option_strike']],
            'vencimento': [dt.strftime(dt.fromtimestamp(info['expiration_time']), '%d/%m/%Y')]}
    df = pd.DataFrame(dict)
    df1 = pd.concat([df1, df])
    df1 = df1.sort_values('ativo')
print(df1)
print('-'*75)
#Thl
print('                      THL')
thl = ['ABEV3', 'ABEVA155', 'ABEVB154', 'ABEVM148']
print(f'ABEVA155 pg -0,41 >>> atual -{df1["ultimo"].iloc[-10]} Strike {df1["strike"].iloc[-10]}')
print(f'ABEVB154 pg +0,69 >>> atual +{df1["ultimo"].iloc[-9]} Strike {df1["strike"].iloc[-9]}')
print('Entrada da operação -0,41 +0,69 = 0,28')
resultadothl = df1["ultimo"].iloc[-9] - df1["ultimo"].iloc[-10]
print(f'Saida da operação -{df1["ultimo"].iloc[-10]}+{df1["ultimo"].iloc[-9]} = {resultadothl}')
print(f'ABEVM148 pg -0,46 >>> atual +{df1["ultimo"].iloc[-8]} Strike {df1["strike"].iloc[-8]}')
'''ABEVM148 14,82 17/02 (0,46)'''