from FUNCOESs import *

PAPEL = ['BOVA11', 'BOVAK115', 'BOVAW115', 'BOVAT114','BOVAJ112','BOVAV112','BOVAP25']

ATIVO = 'BOVA11'
CALLVENDIDACURTA = 'BOVAJ112'
PUTVENDIDACURTA = 'BOVAV112'
PUTLONGA = 'BOVAP25'

inicializacao()
ativosvisiveis(PAPEL)

while True:
    print('')
    ativo = mt.symbol_info_tick(ATIVO)
    callcruta = mt.symbol_info_tick(CALLVENDIDACURTA)
    putcurta = mt.symbol_info_tick(PUTVENDIDACURTA)
    putlonga = mt.symbol_info_tick(PUTLONGA)

    result = round((callcruta.ask + putcurta.ask), 2)
    saida = round((putlonga.bid - result), 2)
    
    print(f'                  {ATIVO} =  ', (ativo).last)
    print(f'Call vendida curta {CALLVENDIDACURTA}   -',(callcruta).ask)
    print(f'Put  vendida curta {PUTVENDIDACURTA}   -',(putcurta).ask)
    print(f'put longa  {PUTLONGA}         +',(putlonga).bid)

    print(f'Total das vendidas {result}')
    print(f'Total da reverssão {saida}')
    time.sleep(60)
mt.shutdown()

