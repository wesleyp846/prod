import MetaTrader5 as mt
import win32com.client as win32
import pandas as pd
import time

PAPEL = 'WINZ22'
LOTE = float(1)
TEMPO_GRAFICO = mt.TIMEFRAME_M15
MAGICO = int(1)
COMENT = 'ProdW15M100-100'
HORA_INICIO = '0917'
HORA_FIM = '1659'
LOSS = 500
GAIM = 500

def inicializacao():
    try:
        if not mt.initialize():
            print('initialização falhou no Meta Trade 5', mt.last_error())
            quit()
    except:
        print('Erro grave na inicialização', mt.last_error())
    symbol = PAPEL
    symbol_info = mt.symbol_info(symbol)
    try:
        if symbol_info is None:
            print(symbol, 'Não encontrato')
            quit()
    except:
        print('Erro grave na inicialização', mt.last_error())
    try:
        if not symbol_info.visible:
            print('Papel Não visivel, tentnado adicionar')
            if not mt.symbol_select(symbol, True):
                print(f'Papel selecionando({symbol}) não cadastrado', symbol)
                quit()
    except:
        print('Erro grave na inicialização', mt.last_error())


def horainicioefim():
    tempo_atual = time.localtime()
    hora = str(tempo_atual[3])
    minuto = str(tempo_atual[4])
    if len(hora) < 2:
        hora = str(0) + hora
    if len(minuto) < 2:
        minuto = str(0) + minuto
    hora_atual = (hora) + (minuto)
    if not HORA_INICIO <= hora_atual:
        return False
    if HORA_FIM <= hora_atual:
        return False


def get_ohlc(n=2):
    ativo = mt.copy_rates_from_pos(PAPEL, TEMPO_GRAFICO, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo['Pivot'] = (ativo['high'] + ativo['low'] + ativo['close']) / 3
    ativo['R1'] = 2 * ativo['Pivot'] - ativo['low']
    ativo['S1'] = 2 * ativo['Pivot'] - ativo['high']
    ativo.set_index('time', inplace=True)
    return ativo
def mandaemail():
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.to = 'aventureiro-msn@hotmail.com'
    email.Subject = 'mt do wesley'
    email.HTMLBody = '<p>robo funcionando</p>'
    email.Send()
    return print('email enviado')
def compra():
    lot = LOTE
    symbol = PAPEL
    point = mt.symbol_info(symbol).point
    price = mt.symbol_info_tick(symbol).ask
    desviation = 1
    tp = price + GAIM * point
    sl = price - LOSS * point
    request = {
        'action': mt.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': lot,
        'type': mt.ORDER_TYPE_BUY,
        'price': price,
        'tp': tp,
        'sl': sl,
        'magic': MAGICO,
        'desviation': desviation,
        'comment': COMENT,
        'type_time': mt.ORDER_TIME_GTC,
        'type_filling': mt.ORDER_FILLING_RETURN,
    }
    return mt.order_send(request), \
           print(f'>>>Comprando {lot} de {symbol} preço {price} com tp {tp} e sl {sl}')
def venda():
    lot = LOTE
    symbol = PAPEL
    point = mt.symbol_info(symbol).point
    price = mt.symbol_info_tick(symbol).bid
    desviation = 1
    tp = price - GAIM * point
    sl = price + LOSS * point
    request2 = {
        'action': mt.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': lot,
        'type': mt.ORDER_TYPE_SELL,
        'price': price,
        'tp': tp,
        'sl': sl,
        'deviation': desviation,
        'magic': MAGICO,
        'comment': COMENT,
        'type_time': mt.ORDER_TIME_GTC,
        'type_filling': mt.ORDER_FILLING_RETURN,
    }
    return mt.order_send(request2), \
           print(f'>>>Vendendo {lot} de {symbol} preço {price} com tp {tp} e sl {sl}')

inicializacao()
print('inicialização completa...')

while True:
    ativo = get_ohlc()
    tick = mt.symbol_info_tick(PAPEL)
    if tick.last > ativo['R1'][-1 - 1] and horainicioefim() != False:
        if mt.positions_get(symbol=PAPEL) == () or mt.positions_get(symbol=PAPEL)[0][5] == 1:
            result = compra()
            print('codigo de erro', mt.TRADE_RETCODE_DONE)
    if tick.last < ativo['S1'][-1 - 1] and horainicioefim() != False:
        if mt.positions_get(symbol=PAPEL) == () or mt.positions_get(symbol=PAPEL)[0][5] == 0:
            result = venda()
            print('codigo de erro', mt.TRADE_RETCODE_DONE)
    time.sleep(0.5)