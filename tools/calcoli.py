from db_models import Voto


class BadInputError(Exception):
    pass


def calcola_numero_goal(pts):
    """
    calcola_numero_goal(pts) -> int
    Calcola il numero di goal in base al punteggio float complessivo della rosa,
    passato come argomento
       --> calcola_numero_goal(66)
           1

    :param pts: str punteggio rosa
    """
    if isinstance(pts, float):
        return (float(pts) - 60) // 6
    else:
        raise BadInputError('Need a Float as input')


def calcola_ris(ptsa, ptsb):
    """
    calcola_ris(ptsa, ptsb) -> tuple

    Trasforma i pts in gol in una sfida a scontri diretti
       --> calcola('66', '62')
           (1, 0)
    :param ptsa: str punti rosa squadra A
    :param ptsb: str punti rosa squadra B
    """
    gola, golb = calcola_numero_goal(ptsa), calcola_numero_goal(ptsb)
    if gola == golb:
        if ptsa - ptsb >= 4:  # +4 in fascia squadra a
            gola += 1
        elif ptsb - ptsa >= 4:  # +4 in fascia squadra b
            golb += 1
    if ptsa < 60:  # autogol squadra a
        gola = 0
        golb += 1
    elif ptsb < 60:  # autogol squadra b
        golb = 0
        gola += 1
    if ptsa - ptsb > 9.5:  # +10 squadra a
        gola += 1
    elif ptsb - ptsa > 9.5:  # +10 squadra b
        golb += 1
    return int(gola), int(golb)


class GestoreCalcoloPuntiFormazione(object):
    """Handler Calcolo punti formazione"""
    def __init__(self, formazione, giornata, offset=1):
        """
        GestoreCalcoloPuntiFormazione(formazione, giornata, offset)

        Gestisce il calcolo dei punti di formazione
        :param formazione: object db_models.Formazione
        :param giornata: int giornata
        :param offset: int differenza giornate reali - giornate fantalega
        """
        self.offset = offset
        self.formazione = formazione
        self.titolari = self.formazione[:11]
        self.panchinari = self.formazione[11:]
        self.giornata = int(giornata) + self.offset
        self.valutati = []
        self.titolari_senza_voto = []
        self.panchinari_con_voto = []
        self.scelti = []
        self.iterable = []
        self.pts = 0.0

    def calcola_punti_formazione(self):
        """
        calcola_punti_formazione(self) -> res, dict

        Calcola i punti della formazione e ritorna una tupla formata dal
        risultato cumulativo della rosa e un dizionario nel formato
        giocatore.nome: fanta_voto

        :return res: float risultato totale formazione
        :return dv: dict Giocatore.nome: Voto.fanta_voto
        """
        for giocatore in self.titolari:
            voto = Voto.query.filter_by(giocatore=giocatore,
                                        giornata=self.giornata).first()
            if not voto.voto_nudo == 0.0:
                self.valutati.append((giocatore, voto))
                # print '+++ {} {} ok!'.format(#giocatore.nome, voto.fanta_voto)
            else:
                # smetto di accumulare sostituzioni dopo la terza
                self.titolari_senza_voto.append(giocatore)
                # print '-----> {} non valutato!'.format(giocatore)
        # se la lista dei titolari con voto e' di lunghezza 11 ritorno
        # la somma dei fanta_voti
        if len(self.valutati) == 11:
            res = sum([v.fanta_voto for g, v in self.valutati])
            # print '[CORE] +++++ nessuna sostituzione +++++'

        # PANCHINARI: controllo sostituzioni
        # se i senza voto sono 3, chiamo il metodo scegli_sostituti
        # altrimenti il metodo scegli_sostituti_ciclico
        else:
            # print '[CORE] *** controllo sostituzioni ***'
            if len(self.titolari_senza_voto) < 4:
                # print '[CORE] sostituzioni entro il limite concesso di 3...'
                self.scelti = self.scegli_sostituti()
            else:
                # print '[CORE] sostituzioni OLTRE il limite concesso di 3...'
                self.scelti = self.scegli_sostituti_ciclico()
            self.valutati += self.scelti
            res = sum([v.fanta_voto for g, v in self.valutati])
            # print '[CORE] +-+-+ risultato finale con sostituzioni +-+-+'

        # for p, v in self.valutati:
        #     print '{} - {}'.format(p.nome, v.fanta_voto)

        self.pts = res
        dv = {item[0].nome: item[1].fanta_voto for item in self.valutati}
        # return res, self.valutati
        # print res, dv
        return res, dv

    def filtra_panchinari_con_voto(self):
        """
        filtra_panchinari_con_voto(self) -> list di object Giocatore

        Filtra i panchinari ed estrapola quelli che hanno preso il voto

        :return: list di oggetti db_models.Giocatore
        """
        panchinari_con_voto = []
        for panchinaro in self.panchinari:
            voto = Voto.query.filter_by(giocatore=panchinaro,
                                    giornata=self.giornata).first()
            if voto.voto_nudo > 0.0:
                panchinari_con_voto.append((panchinaro, voto))
        return panchinari_con_voto

    def scegli_sostituti(self):
        """
        scegli_sostituti(self) -> list di object Giocatore

        Sceglie i sostituti, se possibile, tra i panchinari con voto, se il
        titolare non prende il voto e le sostituzioni da fare sono massimo 3.

        :return self.scelti: list di oggetti db_models.Giocatore
        """
        self.panchinari_con_voto = self.filtra_panchinari_con_voto()

        for non_votato in self.titolari_senza_voto:
            if 200 < non_votato.codice < 500:
                disponibile = self.cerca_difensore()
                if disponibile:
                    self.scelti.append(self.panchinari_con_voto.pop(
                        self.panchinari_con_voto.index(disponibile)))
            elif 500 < non_votato.codice < 800:
                disponibile = self.cerca_ccampista()
                if disponibile:
                    self.scelti.append(self.panchinari_con_voto.pop(
                        self.panchinari_con_voto.index(disponibile)))
            elif non_votato.codice > 800:
                disponibile = self.cerca_attaccante()
                if disponibile:
                    self.scelti.append(self.panchinari_con_voto.pop(
                        self.panchinari_con_voto.index(disponibile)))
            else:
                disponibile = self.cerca_portiere()
                if disponibile:
                    self.scelti.append(self.panchinari_con_voto.pop(
                        self.panchinari_con_voto.index(disponibile)))
        return self.scelti

    def scegli_sostituti_ciclico(self):
        """
        scegli_sostituti_ciclico(self) -> list di object Giocatore

        Se ci sono da effettuare piu' sostituzioni in piu' ruoli, scorre
        ciclicamente dal difensore all'attaccante, fino ad effettuare tutte
        le sostituzioni possibili.


        :return scelti: list di oggetti db_models.Giocatore
        """
        self.panchinari_con_voto = self.filtra_panchinari_con_voto()
        scelti = []
        sostituiti = []
        ps = False
        ds = False
        cs = False
        ats = False
        while True:
            for non_votato in self.titolari_senza_voto:
                if 200 < non_votato.codice < 500:
                    disponibile = self.cerca_difensore()
                    if ds is False:
                        scelti.append(self.panchinari_con_voto.pop(
                            self.panchinari_con_voto.index(disponibile)))
                        sostituiti.append(self.titolari_senza_voto.pop(
                            self.titolari_senza_voto.index(non_votato)))
                        ds = True
                        ps = False
                        cs = False
                        ats = False
                elif 500 < non_votato.codice < 800:
                    disponibile = self.cerca_ccampista()
                    if cs is False:
                        scelti.append(self.panchinari_con_voto.pop(
                            self.panchinari_con_voto.index(disponibile)))
                        sostituiti.append(self.titolari_senza_voto.pop(
                            self.titolari_senza_voto.index(non_votato)))
                        cs = True
                        ps = False
                        ds = False
                        ats = False
                elif non_votato.codice > 800:
                    disponibile = self.cerca_attaccante()
                    if ats is False:
                        scelti.append(self.panchinari_con_voto.pop(
                            self.panchinari_con_voto.index(disponibile)))
                        sostituiti.append(self.titolari_senza_voto.pop(
                            self.titolari_senza_voto.index(non_votato)))
                        ats = True
                        ps = False
                        ds = False
                        cs = False
                else:
                    disponibile = self.cerca_portiere()
                    if ps is False:
                        scelti.append(self.panchinari_con_voto.pop(
                            self.panchinari_con_voto.index(disponibile)))
                        sostituiti.append(self.titolari_senza_voto.pop(
                            self.titolari_senza_voto.index(non_votato)))
                        ps = True
                        ats = False
                        ds = False
                        cs = False

            if len(scelti) == 3:
                return scelti
        return scelti

    def cerca_difensore(self):
        """
        cerca_difensore(self) -> object Giocatore

        Cerca un difensore per la sostituzione tra quelli con voto

        :return: object Giocatore
        """
        difensori = [(dif, v) for dif, v in self.panchinari_con_voto
                     if 200 < dif.codice < 500]
        # print difensori
        if difensori:
            return difensori[0]

    def cerca_ccampista(self):
        """
        cerca_ccampista(self) -> object Giocatore

        Cerca un centrocampista per la sostituzione tra quelli con voto

        :return: object Giocatore
        """
        ccampisti = [(cc, v) for cc, v in self.panchinari_con_voto
                     if 500 < cc.codice < 800]
        if ccampisti:
            return ccampisti[0]

    def cerca_attaccante(self):
        """
        cerca_attaccante(self) -> object Giocatore

        Cerca un attaccante per la sostituzione tra quelli con voto

        :return: object Giocatore
        """
        attaccanti = [(a, v) for a, v in self.panchinari_con_voto
                      if a.codice > 800]
        if attaccanti:
            return attaccanti[0]

    def cerca_portiere(self):
        """
        cerca_portiere(self) -> object Giocatore

        Cerca un portiere per la sostituzione tra quelli con voto

        :return: object Giocatore
        """
        portieri = [(p, v) for p, v in self.panchinari_con_voto
                    if p.codice < 200]
        if portieri:
            return portieri[0]

    def quanti_punti(self):
        """
        quanti_punti(self) -> int

        Invoca il metodo calcola_punti_formazione e ritorna il numero di gol

        :return: int punti formazione
        """
        self.calcola_punti_formazione()
        return self.pts