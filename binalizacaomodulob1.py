import MetaTrader5 as mt5
import pandas as pd
mt5.initialize()

#ativos=['ITSA4', 'ITSAJ828', 'ITSAV100', 'ITSAJ920', 'ITSAV920']
ativos=['ITSA4', 'ITSAK887', 'ITSAW108', 'ITSAK980', 'ITSAW980']
mt5.symbol_select(ativos, True)
data=pd.DataFrame()
for i in ativos:
    rates = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_D1, 0, 5)
    data[i] = [y['close'] for y in rates]
mt5.shutdown()
#print(data)
#data['total']=data['ITSAJ828']+data['ITSAV100']-2*data['ITSAJ920']-float(0.44) #-2*data['ITSAV920']
data['total']=data['ITSAK887']+data['ITSAW108']-2*data['ITSAK980']-2*data['ITSAW980']
print(data)
