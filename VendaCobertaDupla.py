''' ativo abev 15,30 -10K
vende 10K a155 (0,75)
vende 5k de m155 (0,65)
compra  2,5K t170 (1,3)

---------------------
ABEV3    15,83              Dia 29/11
ABEVN164 16,47 17/02 (0,85) Dia 29/11
ABEVL161 15,64 16/12 (0,53) Dia 29/11 vendido
ABEVX151 15,14 16/12 (0,11) Dia 29/11 vendido
= -0,85 +0,53 +0,11 >> - 0,21 (paga -0,21  pra entrar) '''

import time
import MetaTrader5 as mt
import win32com.client as win32

ATIVO = 'ABEV3'
COMPRADO = 'ABEVN164'
VENDIDOCALL = 'ABEVL161'
VENDIDOPUT = 'ABEVX151'

def mandaemail(titulo, mensagem):
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    email.to = 'aventureiro-msn@hotmail.com'
    email.Subject = titulo
    email.HTMLBody = mensagem

    email.Send()
    return print('email enviado')
def inicializacao():
    try:
        if not mt.initialize():
            print('initialização falhou no Meta Trade 5', mt.last_error())
            quit()
    except:
        print('Erro grave na inicialização1', mt.last_error())
mt.symbol_select([ATIVO, COMPRADO, VENDIDOCALL, VENDIDOPUT], True)
inicializacao()

while True:
    print('')
    print('VENDA COBER DUPLA, <<<STRANGLLE LONGE PUT>>>')
    print('')
    ativo = mt.symbol_info_tick(ATIVO)
    comprado = mt.symbol_info_tick(COMPRADO)
    vendidocall = mt.symbol_info_tick(VENDIDOCALL)
    vendidoput = mt.symbol_info_tick(VENDIDOPUT)
    result = round((comprado.bid - vendidocall.ask - vendidoput.ask), 2)
    exercicocall = round((ativo.last - 15.64), 2)
    exercicoput = round((15.14 - ativo.last), 2)
    print(f'             {ATIVO} =  ', (ativo).last)
    print(f'Put Longa {COMPRADO}    +',(comprado).bid)
    print(f'Call vendida {VENDIDOCALL} -',(vendidocall).ask)
    print(f'Put vendida {VENDIDOPUT}  -',(vendidoput).ask)
    print(f'Ativo>>> {ativo.last} =        {result} pra sair')
    if ativo.last > 15.64:
        print('-' * 75)
        print(f'Sendo exercido na call  {VENDIDOCALL} excedendo em {exercicocall}')
        print(f'{COMPRADO} se desvalorizando, Rolar a call {VENDIDOCALL} e put {VENDIDOPUT} virando po')
        print(f'venda a Put do mes seguinte, comprando mais Put longa {COMPRADO}' )
        print('-' * 75)
        #mandaemail('VEnda coberta Dupla', f'<p>Abeve chegou a meta {result}</p>')
    elif ativo.last < 15.14:
        print(f'Sendo execido na put  {VENDIDOPUT} excedendo em {exercicoput}')
    time.sleep(60)
mt.shutdown()

