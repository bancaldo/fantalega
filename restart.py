from db_models import *
from model import ModelFanta
from tools.imports import importa_txt as it
from tools.imports import popola_squadre as ps
from tools.imports import popola_calendario as pc
from tools.imports import _import_formazioni_da_file as imfo


m = ModelFanta()

m.database_esistente()

print "Inserimento voti 1..."
it('giornate/MCC01.txt')
print "***** fatto!"
print "Inserimento voti 2..."
it('giornate/MCC02.txt')
print "***** fatto!"

print "Creo Lega..."

lega = Lega('FANTALEGA 2014-2015')
db.session.add(lega)
db.session.commit()
option = Option(lega=lega, budget=500, max_mercati=6,
                max_portieri=3, max_difensori=9,
                max_centrocampisti=9, max_attaccanti=7,
                a_r=4, offset=1)
db.session.add(option)
db.session.commit()


print "***** Lega creata"

ps(lega)
print "***** Squadre popolate"
for s in Squadra.query.all():
    s.budget = 500
    s.op_mercato = 6
    s.allenatore = ''
    db.session.commit()

pc(lega)
print "***** calendario creato"

imfo(m, 1, lega)
