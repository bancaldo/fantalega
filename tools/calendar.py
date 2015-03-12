# -*- coding: utf-8 -*-#
"""FantaCalendario v 2.0
   Controller Module for FantaCalendario Application:
   All the binding method to frame widget are defined here"""

from copy import copy
from random import shuffle


class Team(object):
    """A team class"""
    def __init__(self, name, status=True):
        self.name = name
        self.casa = status
        
    def set_casa(self):
        """set the status 'casa' to True"""
        self.casa = True

    def set_fuori(self):
        """set the status 'fuori' to True"""
        self.casa = False


def crea_calendario(lista):
    """crea gli accoppiamenti da una lista"""
    matrix = []
    cont = 0
    while cont < len(lista):
        matrix.append([None] * len(lista))
        cont += 1
    matrix[0] = lista  # intestazione

    # Riga Intestazione invertita meno l'ultima squadra
    row2 = copy(lista)
    row2.pop()
    row2.reverse()
    matrix[1][0:(len(lista) - 1)] = row2[0:(len(lista) - 1)]

    # Composizione tabella prima FASE
    i = 1
    while i < len(lista):
        k = 1
        for item in matrix[i]:
            try:
                matrix[i + 1][k] = item
                matrix[i + 1][0] = matrix[i + 1][(len(lista) - 1)]
                matrix[i + 1][(len(lista) - 1)] = None
                k += 1
            except IndexError:
                break
        i += 1

    # Composizione tabella seconda FASE
    row_m = 1
    while row_m < len(lista):
        for item_a in matrix[0]:
            for item_b in matrix[row_m]:
                if matrix[0].index(item_a) == matrix[row_m].index(item_b):
                    if item_a == item_b:
                        matrix[row_m][matrix[row_m].index(item_b)] = lista[-1]
                        matrix[row_m][(len(lista) - 1)] = item_b
        row_m += 1

    # Stampa giornata
    cal = []
    gg = 1
    while gg < len(lista):
        andata = []
        for sq_a in matrix[0]:
            for sq_b in matrix[gg]:
                if matrix[0].index(sq_a) == matrix[gg].index(sq_b):
                    if sq_b not in andata or sq_a not in andata:
                        if sq_a.casa is True:
                            andata.append(sq_a)
                            andata.append(sq_b)
                            cal.append('{},{},{}'.format(gg, sq_a.name,
                                                         sq_b.name))
                            sq_a.set_fuori()
                            sq_b.set_casa()
                        else:
                            andata.append(sq_b)
                            andata.append(sq_a)
                            cal.append('{},{},{}'.format(gg, sq_b.name,
                                                         sq_a.name))
                            sq_a.set_casa()
                            sq_b.set_fuori()
        gg += 1
    return cal


def crea_ritorno(cal, teams):
    ritcal = []
    for match in cal:
        n, sa, sb = match.split(',')
        ritcal.append('{},{},{}'.format(int(n) + len(teams) - 1, sb, sa))
    return ritcal


def componi_stagione(teams, num):
    """Iterable sono le squadre a db, num il numero di andate e ritorni
       Questa funzione viene chiamata dalla shell di django:
       from models import Squadra
       from tools.calendar import comopni_stagione as cs

       teams = [s.nome for s in Squadra.query.all()
       cal = cs(teams, 4) # 4 sta per 2 andate e 2 ritorni]
    """
    shuffle(teams)
    tobj = [Team(name) for name in teams]
    cal = crea_calendario(tobj)
    ar = 1
    full_cal = cal
    while ar < num:
        cal = crea_ritorno(cal, teams)
        full_cal += cal
        ar += 1
    return full_cal
    
    
if __name__ == '__main__':
    squadre = ['a', 'b', 'c', 'd', 'e', 'f']
    calendar = componi_stagione(squadre, 4)
