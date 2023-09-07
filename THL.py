'''Se o mercado cair muito você sofre.
Fazer um pouco acima do ATM
Se virar pó a A30, pode virar uma borboleta (B26-2B28+B30) ZCC

Subiu mais de 7 ou 8% já deve sair que fico ruim.

Com 20 dias antes do vencimento.

Ex. ABEV3 = 15,50  1,3%= 15,50*0,013 = 0,21
saída 3% = 15,5*0,03 =0,47

BOVA11 ta entorno de 0,8% com saída em 2,5%
BOVA11 = 105,00*0,008=0,84 Saída 105,00*0,025=2,62

Calendar Butterfly é superior a THL

FLY HORIZONTAL (melhor rolagem)
Começamos com a THL B25-A25
Passamos para C25-2B25+A25 (Fly Horizontal) >>> Da THL compra 1 da A25, vende 2B25, pois já tinha uma, e compra a C25.

ABEV3    14,84              Dia 14/11
ABEVA155 15,57 20/01 (0,41) Dia 12/11
ABEVB154 15,47 17/02 (0,69) Dia 2/11 vendido
ABEVM148 14,82 17/02 (0,46)
= -0,69 +0,41 >> - 0,28 (paga -0,28  pra entrar) '''

from FUNCOES import *

ATIVO = 'ABEV3'
CALLVENDIDACURTA = 'ABEVA155'
CALLCOMPRADALONGA = 'ABEVB154'
VCPUT = 'ABEVM148'
STRIKECALLVENDIDA = 15.57
STRIKEPUTVENDIDA = 14.82
ATIVOENTRADA = 15.47

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

inicializacao()

while True:
    print('')
    print('THL, <<< ABEV3 DE JANEIRO PARA FEVEREIRO  >>>')
    print('')
    ativo = mt.symbol_info_tick(ATIVO)
    callcruta = mt.symbol_info_tick(CALLVENDIDACURTA)
    calllonga = mt.symbol_info_tick(CALLCOMPRADALONGA)
    vcput = mt.symbol_info_tick(VCPUT)

    result = round((calllonga.ask - callcruta.bid), 2)
    entrada = ATIVOENTRADA*0.013
    saida = ATIVOENTRADA*0.03
    explodiu = ATIVOENTRADA*1.09
    premio = round(0.46 - vcput.bid, 2)

    print('Gasto -0,28 pra montar')
    print(f'                      {ATIVO} =  ', (ativo).last)
    print(f'Call vendida curta {CALLVENDIDACURTA}    -',(callcruta).bid)
    print(f'Call comprada longa {CALLCOMPRADALONGA}   +',(calllonga).ask)
    print(f'Ativo >>> {ativo.last}  =               {result} pra sair')
    print(f'Total com VC {result} + {premio} =       ', round(result + premio, 2))

    if ativo.last < STRIKEPUTVENDIDA:
        print('-' * 75)
        print(f'Exercendo no mês seguinte pela {VCPUT} em ', round(ativo.last - STRIKEPUTVENDIDA, 2))
        print(f'Rolar a {VCPUT} com Fly Horizontal')
    if result <= entrada:
        print('-' * 75)
        print(f'A THL dando oportunidade abaixo de 1,3% no valor de {result}')
    if result >= saida:
        print('-' * 75)
        print(f'A THL ganhando 3% com ganho de {result}')
    if ativo.last > explodiu:
        print('-' * 75)
        print(f'Ativo com valor 8% acima do Strike da {CALLVENDIDACURTA} excedendo ', round(explodiu - ativo.last, 2))
        print(f'{CALLVENDIDACURTA} Sair pela Fly Horizontal')
        #mandaemail('VEnda coberta Dupla', f'<p>Abeve chegou a meta {result}</p>')
    if ativo.last > STRIKECALLVENDIDA:
        print('-' * 75)
        print(f'Exercendo no mês seguinte pela {CALLVENDIDACURTA} em ', round(STRIKECALLVENDIDA - ativo.last, 2))
        print(f'Rolar a {CALLVENDIDACURTA} com Fly Horizontal')
    print('-' * 75)
    time.sleep(60)
mt.shutdown()

