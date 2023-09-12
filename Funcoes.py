import MetaTrader5 as mt
import pandas as pd
import time
#import win32com.client as win32

def inicializacao(PAPEL):
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

def get_ohlc(PAPEL, TEMPO_GRAFICO, n=5):
    ativo = mt.copy_rates_from_pos(PAPEL, TEMPO_GRAFICO, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo['Pivot'] = (ativo['high'] + ativo['low'] + ativo['close']) / 3
    ativo['R1'] = 2 * ativo['Pivot'] - ativo['low']
    ativo['S1'] = 2 * ativo['Pivot'] - ativo['high']
    ativo.set_index('time', inplace=True)
    return ativo

def compra(PAPEL, LOTE, GAIM, LOSS, MAGICO, COMENT):
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

def venda(PAPEL, LOTE, GAIM, LOSS, MAGICO, COMENT):
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

