
import pandas as pd
import time
from Funcoes import *

PAPEL = 'WDOZ22'
LOTE = float(1)
TEMPO_GRAFICO = mt.TIMEFRAME_M1
MAGICO = int(6)
COMENT = 'dol1MR2S2'
HORA_INICIO = '0904'
HORA_FIM = '1820'
LOSS = 3000
GAIM = 5000


def get_ohlc(n=5):
    ativo = mt.copy_rates_from_pos(PAPEL, TEMPO_GRAFICO, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo['Pivot'] = (ativo['high'] + ativo['low'] + ativo['close']) / 3
    ativo['R1'] = 2 * ativo['Pivot'] - ativo['low']
    ativo['S1'] = 2 * ativo['Pivot'] - ativo['high']
    ativo['R2'] = ativo['Pivot'] + (ativo['high'] - ativo['low'])
    ativo['S2'] = ativo['Pivot'] - (ativo['high'] - ativo['low'])
    ativo.set_index('time', inplace=True)
    return ativo
def compra():
    lot=LOTE
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
def posicao(ativo):
    pos = mt.positions_get(symbol=ativo)
    if pos == ():
        return 0
    if pos != ():
        if pos != None and pos[0][5] == 0:
            return 1
        if pos != None and pos[0][5] >= 1:
            return 2

inicializacao(PAPEL)
print('inicialização completa...')

while True:
    ativo = get_ohlc()
    pos = posicao(PAPEL)
    tick = mt.symbol_info_tick(PAPEL)
   # print(ativo['R1'][-1 - 2], 'r1')
    #print(ativo['R2'][-1 - 2], 'r2')
    # Bloco não posicionando
    if posicao(PAPEL) == 0:
        # bloco de compra
        if tick.last > ativo['R2'][-1 - 1]:
            compra()
        # bloco de venda
        if tick.last < ativo['S2'][-1 - 1]:
            venda()

    # bloco se ja tiver comprado
    if posicao(PAPEL) == 1:
        if tick.last < ativo['R1'][-2 - 2]:
            print('stop da Compra')
            venda()

    # bloco se ja tiver vendido
    if posicao(PAPEL) == 2:
        if tick.last > ativo['S1'][-2 - 2]:
            print('stop da venda')
            compra()

    time.sleep(0.5)