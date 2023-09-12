import MetaTrader5 as mt5
import pandas as pd

mt5.initialize()
ATIVOS = ['BOVA11', 'BOVAK115', 'BOVAW115', 'BOVAT114','BOVAJ112','BOVAV112','BOVAP25']

'''
mt5.symbol_select(ATIVOS, True)
data=pd.DataFrame()

for i in ATIVOS:
    rates = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_D1, 0, 5)
    data[i] = [y['close'] for y in rates]
mt5.shutdown()

data['total']=data['BOVAT114']-data['BOVAK115']-data['BOVAW115']

print(data)'''

# symbol_info_tick_dict = mt5.symbol_info_tick('BOVA11')._asdict()
# for prop in symbol_info_tick_dict:
#     print("  {}={}".format(prop, symbol_info_tick_dict[prop]))


lasttick = mt5.symbol_info_tick('BOVA11')
# converter para dicionário
tick_dict = lasttick._asdict() 
# criar DataFrame 
df = pd.DataFrame(tick_dict), columns=['attribute', 'value']

 
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()
