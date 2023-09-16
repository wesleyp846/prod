import MetaTrader5 as mt5
from datetime import datetime
import re
import pandas as pd

dados = []
count = 0

def inicialize(): 
    # estabelecemos a conexão ao MetaTrader 5
    if not mt5.initialize():
        print("initialize() falhou, codigo de erro =",mt5.last_error())
        quit()

def converteData(data_era):
        converterData = data_era
        data = datetime.fromtimestamp(converterData)
        return data.strftime('%d/%m/%Y')

inicialize() 

bova_ativos=mt5.symbols_get("*BOVA*")
for ativo in bova_ativos:

    if re.match("BOVA\w{3}", ativo.name):

       linha = [ativo.name, ativo.option_strike, ativo.expiration_time]  
       dados.append(linha)

    #    count += 1
    #    if count==100: 
    #        break
           
df = pd.DataFrame(dados, columns=['Ativo', 'Strike', 'Vencimento'])
df = df.sort_values(by='Vencimento')
print(df['Vencimento'].dtype)
df['Vencimento'] = df['Vencimento'].apply(converteData)
df.to_csv('dados.csv', sep=";", index=False)

#print(df)

#converteData(ativo.expiration_time)
print()
mt5.shutdown()