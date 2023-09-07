import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))
count=0

for s in symbols:
    count+=1
    print("{}. {}".format(count,s.name))
    if count==5: break
print()
ab_symbols=mt5.symbols_get("*BOVA*")
print('len(*ABE*): ', len(ab_symbols))
for s in ab_symbols:
    print(s.name, s.last)
print()
#obtemos símbolos cujos nomes não contêm USD, EUR, JPY e GBP
# group_symbols=mt5.symbols_get(group="*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
# print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(group_symbols))
# for s in group_symbols:
#     print(s.name,":",s.last)