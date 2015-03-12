__author__ = 'banchellia'


def scegli_sostituti_over(nv):
    scelti = []
    sostituiti = []
    iterable = [102, 203, 204, 205, 501, 502, 901][:]
    ps = False
    ds = False
    cs = False
    ats = False
    while True:
        for non_votato in nv:
            if 200 < non_votato < 500:
                p = cerca_difensore(iterable)
                if ds is False:
                    scelti.append(iterable.pop(iterable.index(p)))
                    sostituiti.append(nv.pop(nv.index(non_votato)))
                    ds = True
                    ps = False
                    cs = False
                    ats = False
            elif 500 < non_votato < 800:
                p = cerca_ccampista(iterable)
                if cs is False:
                    scelti.append(iterable.pop(iterable.index(p)))
                    sostituiti.append(nv.pop(nv.index(non_votato)))
                    cs = True
                    ps = False
                    ds = False
                    ats = False
            elif non_votato > 800:
                p = cerca_attaccante(iterable)
                if ats is False:
                    scelti.append(iterable.pop(iterable.index(p)))
                    sostituiti.append(nv.pop(nv.index(non_votato)))
                    ats = True
                    ps = False
                    ds = False
                    cs = False
            else:
                p = cerca_portiere(iterable)
                if ps is False:
                    scelti.append(iterable.pop(iterable.index(p)))
                    sostituiti.append(nv.pop(nv.index(non_votato)))
                    ps = True
                    ats = False
                    ds = False
                    cs = False
        if len(scelti) == 3:
            return scelti
    return scelti


def scegli_sostituti(nv):
    scelti = []
    iterable = [102, 203, 204, 205, 501, 502, 901][:]
    for non_votato in nv:
        if 200 < non_votato < 500:
            p = cerca_difensore(iterable)
            scelti.append(iterable.pop(iterable.index(p)))
        elif 500 < non_votato < 800:
            p = cerca_ccampista(iterable)
            scelti.append(iterable.pop(iterable.index(p)))
        elif non_votato > 800:
            p = cerca_attaccante(iterable)
            scelti.append(iterable.pop(iterable.index(p)))
        else:
            p = cerca_portiere(iterable)
            scelti.append(iterable.pop(iterable.index(p)))
            
    return scelti


def cerca_difensore(iterable):
    dif = [d for d in iterable if 200 < d < 500]
    if dif:
        return dif[0]


def cerca_ccampista(iterable):
    cc = [c for c in iterable if 500 < c < 800]
    if cc:
        return cc[0]


def cerca_attaccante(iterable):
    att = [a for a in iterable if a > 800]
    if att:
        return att[0]


def cerca_portiere(iterable):
    por = [p for p in iterable if p < 200]
    if por:
        return por[0]


if __name__ == '__main__':
    nonv = [201, 202, 230, 604]
    gscelti = scegli_sostituti_over(nonv)
    print gscelti
    nonv = [201, 202]
    gscelti = scegli_sostituti(nonv)
    print gscelti
    nonv = [201, 202, 601]
    gscelti = scegli_sostituti(nonv)
    print gscelti
    nonv = [501, 502, 801]
    gscelti = scegli_sostituti(nonv)
    print gscelti
