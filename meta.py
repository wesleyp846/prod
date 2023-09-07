import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
import win32com.client as win32
import time

if not mt.initialize():
    print("initialize() failed, error code =", mt.last_error())
    quit()

def mandaemail(mensagem):
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    email.to = 'aventureiro-msn@hotmail.com'
    email.Subject = 'mt do wesley'
    email.HTMLBody = mensagem

    email.Send()
    return print('email enviado')

def historico():
    inicio = datetime(datetime.now().year, datetime.now().month, datetime.now().day) #YMD
    fim = datetime.now()
    df = mt.history_deals_get(inicio, fim, group="*,!*EUR*,!*GBP*")
    if df == None:
        print('Sem historico, error code={}'.format(mt.last_error()))
    elif len(df) > 0:
        df = pd.DataFrame(list(df), columns=df[0]._asdict().keys())
        df = df['profit'].cumsum()
    return df


while True:
    resu = historico()
    print(resu[-1:])
    try:
        if (resu[-1:] > 100).bool():
            print('ta quase')
        if (resu[-1:] > 250).bool():
            print('meta')
            mandaemail(f'<p>{resu[-1:]}</p>')
            break
    except: print('sem histórico')
    time.sleep(60)
quit()
mt.shutdown()