# model.py
"""modulo Model dell'applicazione Fantalega"""

import os
import time
from db_models import db, DB_NAME, MODULI
from db_models import Giocatore, Lega, Squadra, Partita, Formazione, Voto
from db_models import FormazioniGiocatori
from db_models import Mercato, Option, Punteggio
from werkzeug.exceptions import NotFound
from tools.imports import importa_txt, popola_squadre, popola_calendario
from tools.imports import inserisci_formazione_da_file


class ModelInterface(object):
    """Model Interface"""
    def __init__(self):
        super(ModelInterface, self).__init__()
        self.lega = None
        self._lega = None
        self._squadra = None
        self._leghe = []
        self._ruolo = None
        self.observers = []

    def database_esistente(self):
        """
        Controllo che il database esista altrimenti lo creo
        """
        path = os.getcwd()
        if DB_NAME in os.listdir(path):
            self.write_to_log("WARNING: Database esistente!")
        else:
            self.write_to_log("INFO: Creazione database...")
            db.create_all()

    def registra_observer(self, observer):
        """Registra un eventuale observer"""
        self.observers.append(observer)

    def update_observers(self):
        """esegue l'update di tutti gli observer legati"""
        for observer in self.observers:
            observer()

    @property
    def lega(self):
        return self._lega

    @lega.setter
    def lega(self, obj_lega):
        self._lega = obj_lega
        self.write_to_log('INFO: Lega memorizzata %s' % self._lega)

    @property
    def squadra(self):
        return self._squadra

    @squadra.setter
    def squadra(self, objsquadra):
        self._squadra = objsquadra
        self.write_to_log('INFO: Squadra memorizzata %s' % self._squadra)

    @property
    def ruolo(self):
        return self._ruolo

    @ruolo.setter
    def ruolo(self, ruolo):
        self._ruolo = ruolo.lower().strip()
        self.write_to_log('INFO: Ruolo modificato: %s' % self._ruolo)

    @property
    def leghe(self):
        return self._leghe

    @leghe.setter
    def leghe(self, iterable):
        self._leghe = iterable
        self.write_to_log('INFO: Leghe modificate: %s' % self._leghe)
        self.update_observers()

    @staticmethod
    def write_to_log(msg):
        """Scrivo sul LOG il messaggio passato come argomento"""
        with open('log.txt', 'a') as logger:
            t = time.localtime()
            time_string = '{}-{}-{} {}:{}:{}'.format(
                t.tm_mday, t.tm_mon, t.tm_year,
                t.tm_hour, t.tm_min, t.tm_sec)
            message = 'INFO: {} -> {}\n'.format(time_string, msg)
            logger.write(message)


class ModelFanta(ModelInterface):
    """Class Model dell'App FantaLega"""
    def __init__(self):
        super(ModelFanta, self).__init__()

    # Metodi Lega
    def nuova_lega(self, nome):
        """
        nuova_lega(self, nome) -> object Lega

        Salva una nuova lega con nome 'nome' controllando che questa non esista
        a database.

        :param nome: str nome lega
        :return: object db_models.Lega
        """
        try:
            self.lega = Lega.query.filter_by(
                nome=nome.upper()).first_or_404()
            self.write_to_log('WARNING: Lega "%s" esistente' % nome)
        except NotFound:
            self.lega = Lega(nome=nome.upper())
            db.session.add(self.lega)
            db.session.commit()
            self.leghe = self.get_leghe()
            self.write_to_log('INFO: Nuova Lega <%s> creata!' % nome)
            return self.lega

    @staticmethod
    def salva_opzioni_lega(objlega, budget, max_mercati, max_portieri,
                           max_difensori, max_centrocampisti,
                           max_attaccanti, a_r, offset):
        """
        salva_opzioni_lega(objlega, budget, max_mercati, max_portieri,
                           max_difensori, max_centrocampisti,
                           max_attaccanti, a_r, offset)

        Salva le opzioni della lega, associando un oggetto Object all' oggetto
        lega stesso

        :param objlega: object db_models.Lega
        :param budget: str
        :param max_mercati: str
        :param max_portieri: str
        :param max_difensori: str
        :param max_centrocampisti: str
        :param max_attaccanti: str
        :param a_r: str
        :param offset: str
        """
        option = Option(lega=objlega, budget=budget, max_mercati=max_mercati,
                        max_portieri=max_portieri, max_difensori=max_difensori,
                        max_centrocampisti=max_centrocampisti,
                        max_attaccanti=max_attaccanti, a_r=a_r, offset=offset)
        db.session.add(option)
        db.session.commit()

    @staticmethod
    def get_leghe():
        """
        get_leghe() -> list

        Staticmethod:
        ritorna la lista di tutte le leghe disponibili

        :return: list
        """
        return Lega.query.all()

    @staticmethod
    def get_lega_nome(nome):
        """
        get_lega_nome(self, nome) -> object Lega o None

        :param nome: str nome lega
        :return: object db_models.Lega
        """
        return Lega.query.filter_by(nome=nome.upper()).first()

    def get_lega(self):
        """
        get_lega(self) -> object Lega
        """
        return self.lega

    def elimina_lega(self, nome):
        """
        elimina_lega(self, nome) -> list

        Elimina la lega con nome=nome e ritorna la lista delle leghe rimanenti

        :param nome: str nome lega
        :return: list di oggetti db_models.Lega
        """
        lega = self.get_lega_nome(nome.upper())
        if lega:
            db.session.delete(lega)
            db.session.commit()
            self.write_to_log('INFO: Lega %s eliminata' % nome)
            return Lega.query.all()

    def elimina_partita(self, object_partita):
        """
        elimina_partita(self, object_partita) -> str message

        Elimina la partita e ritorna il messaggio di esito

        :param object_partita: object db_models.Partita
        :return: str message
        """
        lega = object_partita.lega
        msg = 'INFO: %s lega %s eliminata' % (object_partita, lega)
        db.session.delete(object_partita)
        db.session.commit()
        self.write_to_log(msg)
        return msg

    def modifica_lega(self, nuovo_nome, bd, me, mp, md, mc, ma, ar, offset):
        """
        modifica_lega(self, nuovo_nome, bd, me, mp, md, mc, ma, ar, offset)

        Modifica i valori della lega selezionata

        :param nuovo_nome: str
        :param bd: str
        :param me: str
        :param mp: str
        :param md: str
        :param mc: str
        :param ma: str
        :param ar: str
        :param offset: str
        """
        nome = self.lega.nome
        option = self.lega.option
        self.lega.nome = nuovo_nome
        db.session.commit()
        self.write_to_log('INFO: Lega %s modificata in %s' % (nome, nuovo_nome))
        option.budget = bd
        option.max_mercati = me
        option.max_portieri = mp
        option.max_difensori = md
        option.max_centrocampisti = mc
        option.max_attaccanti = ma
        option.a_r = ar
        option.offset = offset
        db.session.commit()
        self.write_to_log('INFO: Opzioni Lega %s salvate' % nuovo_nome)

    # Metodi Squadra

    def salva_nuova_squadra(self, nome, allenatore, budget, mercati, leghe):
        """
        salva_nuova_squadra(self, nome, allenatore, budget, mercati, leghe) ->
                                                                           msg

        Salva una nuova squadra con i valori passati come argomenti

        :param nome: str
        :param allenatore: str
        :param budget: str
        :param mercati: str
        :param leghe: list di oggetti db_models.Lega
        :return: str messaggio di esito operazione
        """
        try:
            self.squadra = Squadra.query.filter_by(
                nome=nome.upper()).first_or_404()
            msg = 'INFO: Squadra "%s" esistente' % nome
            self.write_to_log(msg)
        except NotFound:
            self.squadra = Squadra(nome=nome.upper())
            db.session.add(self.squadra)
            self.squadra.allenatore = allenatore.upper()
            self.squadra.op_mercato = mercati
            self.squadra.budget = budget
            msg = 'INFO: Nuova Squadra <%s> creata' % nome
            self.write_to_log(msg)
            if leghe:
                for lega in leghe:
                    lega.squadre_lega.append(self.squadra)
            msg = 'INFO: sq. <%s> creata e leghe/classifiche associate!' % nome
            self.write_to_log(msg)
            db.session.commit()
            return msg

    def elimina_squadra(self, nome):
        """
        elimina_squadra(self, nome) -> list object Squadra

        Elimina la squadra con nome=nome e ritorna la lista aggiornata
        di tutti gli oggetti Squadra rimanenti

        :param nome: str nome squadra
        :return: list di oggetti db_models.Squadre
        """
        squadra = self.get_squadra_nome(nome.upper())
        if squadra:
            db.session.delete(squadra)
            db.session.commit()
            self.write_to_log('INFO: Squadra %s eliminata' % nome)
            return Squadra.query.all()
        else:
            self.write_to_log('INFO: Squadra %s non trovata' % nome)

    @staticmethod
    def get_squadra_nome(nome):
        """
        get_squadra_nome(nome) -> object Squadra

        staticmethod:
        Ritorna l'oggetto Squadra con nome 'nome' o ritorna None

        :param nome: str nome squadra
        :return: object db_models.Squadra o None
        """
        return Squadra.query.filter_by(nome=nome.upper()).first()

    def cedi_giocatore(self, nome):
        """
        cedi_giocatore(self, nome) -> list di oggetti Giocatore

        Elimina il giocatore dalla squadra a cui appartiene e ritorna la rosa
        aggiornata, priva del giocatore stesso

        :param nome: str nome giocatore
        :return: list di oggetti db_models.Giocatore
        """
        obj_giocatore = self.get_giocatore_per_nome(nome)
        obj_squadra = obj_giocatore.squadra
        obj_squadra.giocatori.remove(obj_giocatore)
        db.session.commit()
        self.write_to_log(
            'INFO: %s eliminato da %s' % (obj_giocatore, obj_squadra))
        mercato = Mercato()
        db.session.add(mercato)
        obj_squadra.mercati.append(mercato)
        mercato.giocatore = obj_giocatore
        mercato.verso = 'OUT'
        db.session.commit()
        return obj_squadra.giocatori.all()

    def rosa_acquista_giocatore(self, nome, squadra):
        """
        rosa_acquista_giocatore(self, nome, squadra) -> list di oggetti
                                                                Giocatore

        Acquista il giocatore con nome=nome e lo associa alla squadra con
        nome=squadra. Ritorna la lista dei giocatori della rosa aggiornata

        :param nome: nome giocatore
        :param squadra: nome squadra
        :return: list
        """
        obj_giocatore = self.get_giocatore_per_nome(nome)
        obj_squadra = self.get_squadra_nome(squadra)
        if self.get_mercati_rimanenti(obj_squadra) > 0:

            obj_squadra.giocatori.append(obj_giocatore)
            self.write_to_log(
                'INFO: %s aggiunto a rosa %s' % (obj_giocatore, obj_squadra))
            mercato = Mercato()
            db.session.add(mercato)
            mercato.giocatore = obj_giocatore
            mercato.verso = 'IN'
            db.session.commit()
            obj_squadra.mercati.append(mercato)
            obj_squadra.op_mercato -= 1
            db.session.commit()
            self.write_to_log('INFO: Operazione marcato %s memorizzata'
                              % mercato)
            return obj_squadra.giocatori.all()
        else:
            self.write_to_log('ERROR: mercati esauriti o ruoli incompatibili')

    @staticmethod
    def get_squadre():
        """
        get_squadre()

        staticmethod:
        ritorna una lista di tutte le squadre esistenti

        :return: list object db_models.Squadra
        """
        return Squadra.query.all()

    @staticmethod
    def get_giocatori(prefix=None, ruolo=None, squadra_reale=None):
        """
        get_giocatori(prefix, ruolo, squadra_reale) -> list

        staticmethod:
        ritorna una lista di tutti i giocatori presenti a db che soddisfano i
        criteri prefix(nome parziale), ruolo e squadra_reale

        :param prefix: str nome parziale
        :param ruolo: str ruolo
        :param squadra_reale: str squadra reale
        :return: list object db_models.Giocatore
        """
        if prefix and not ruolo and not squadra_reale:
            return Giocatore.query.filter(
                Giocatore.nome.startswith(prefix)).all()
        elif prefix and ruolo and not squadra_reale:
            return Giocatore.query.filter(
                Giocatore.nome.startswith(prefix)).filter_by(ruolo=ruolo).all()
        elif prefix and ruolo and squadra_reale:
            return Giocatore.query.filter(
                Giocatore.nome.startswith(prefix)).filter_by(
                    ruolo=ruolo, squadra_reale=squadra_reale).all()
        elif ruolo and not squadra_reale and not prefix:
            return Giocatore.query.filter_by(ruolo=ruolo).all()
        elif ruolo and squadra_reale and not prefix:
            return Giocatore.query.filter_by(ruolo=ruolo,
                                             squadra_reale=squadra_reale).all()
        elif squadra_reale and not ruolo and not prefix:
            return Giocatore.query.filter_by(squadra_reale=squadra_reale).all()
        elif squadra_reale and prefix and not ruolo:
            return Giocatore.query.filter(
                Giocatore.nome.startswith(prefix)).filter_by(
                squadra_reale=squadra_reale).all()
        else:
            return Giocatore.query.all()

    def sotto_contratto(self):
        """
        sotto_contratto(self) -> list di oggetti Giocatore

        Ritorna la lista dei giocatori che sono sotto contratto, non liberi

        :return: list di oggetti db_models.Giocatore
        """
        return [g for g in self.get_giocatori() if g.squadra is not None]

    def giocatori_disponibili(self, ruolo=None, prefix=''):
        """
        giocatori_disponibili(self, ruolo, nome) -> list di oggetti Giocatore

        Ritorna la lista dei giocatori che sono liberi, con ruolo=ruolo e
        nome contenente prefix

        :param ruolo: str ruolo
        :param prefix: str nome parziale
        :return: list di oggetti db_models.Giocatore
        """
        liberi = [g for g in self.get_giocatori() if g.squadra is None]
        if ruolo is None and prefix == '':
            disp = liberi
        elif ruolo and prefix == '':
            disp = [g for g in liberi if g.ruolo == ruolo.strip()]
        elif prefix and ruolo is None:
            disp = [g for g in liberi
                    if g.nome.startswith(prefix.strip().upper())]
        else:
            disp = [g for g in liberi if g.ruolo == ruolo.strip()
                    and g.nome.startswith(prefix.upper().strip())]
        return disp

    def acquista_giocatore(self, nome, prezzo, nome_squadra):
        """
        acquista_giocatore(self, nome, prezzo, nome_squadra) -> str message

        Acquista il giocatore in asta, associandolo alla squadra acquirente
        e salvandone il prezzo d'asta

        :param nome: str nome giocatore
        :param prezzo: str prezzo
        :param nome_squadra: str nome squadra
        :return: str message
        """
        squadra = self.get_squadra_nome(nome_squadra)
        giocatore = self.get_giocatore_per_nome(nome)
        in_rosa = [g for g in squadra.giocatori.all()
                   if g.ruolo == giocatore.ruolo]

        if giocatore.squadra == squadra:
            vecchio_prezzo = int(giocatore.valore_asta)
            diff_prezzo = vecchio_prezzo - int(prezzo)
            squadra.budget += diff_prezzo
            giocatore.valore_asta = int(prezzo)
            db.session.commit()
            msg = 'WARNING: Giocatore acquistato precedentemente, aggiorno...'
            self.write_to_log(msg)
            msg = 'Valori %s aggiornati!' % giocatore.nome
        else:
            if giocatore.ruolo.lower() == 'portiere':
                max_g = squadra.leghe[0].option.max_portieri
            elif giocatore.ruolo.lower() == 'difensore':
                max_g = squadra.leghe[0].option.max_difensori
            elif giocatore.ruolo.lower() == 'centrocampista':
                max_g = squadra.leghe[0].option.max_centrocampisti
            else:
                max_g = squadra.leghe[0].option.max_attaccanti

            if len(in_rosa) < max_g:
                comprati = len(squadra.giocatori.all())
                rimanenti = self.get_max_giocatori_rosa() - comprati
                cassa = int(squadra.budget)
                if (cassa - rimanenti) > 0:
                    if giocatore in squadra.giocatori.all():
                        msg = 'ERROR: Giocatore acquistato precedentemente'
                    elif giocatore.squadra:
                        msg = 'ERROR: Giocatore acquistato da altra squadra'
                    else:
                        squadra.giocatori.append(giocatore)
                        squadra.budget -= int(prezzo)
                        db.session.commit()
                        msg = "INFO: salvo: %s %s %s " % (giocatore.nome,
                                                          prezzo, squadra.nome)
                        self.write_to_log(msg)
                else:
                    msg = 'ERROR: prezzo troppo elevato per completare la rosa'
                    self.write_to_log(msg)
            else:
                msg = "ERROR: limite giocatori raggiunto."
                self.write_to_log(msg)
        return msg

    def get_max_giocatori_rosa(self):
        """
        get_max_giocatori_rosa(self) -> int

        ritorna il massimo numero di giocatori per rosa
        """
        leghe = self.get_leghe()
        if leghe:
            p = int(leghe[0].option.max_portieri)
            d = int(leghe[0].option.max_difensori)
            c = int(leghe[0].option.max_centrocampisti)
            a = int(leghe[0].option.max_attaccanti)
            return sum([p, d, c, a])
        else:
            return 25  # Valore di default nelle fantaleghe

    # Metodi Giocatore

    @staticmethod
    def get_giocatore_per_nome(nome):
        """
        get_giocatore_per_nome(nome) -> object Giocatore

        Ritorna l'oggetto giocatore con nome=nome

        :param nome: str nome giocatore
        :return: object db_models.Giocatore
        """
        return Giocatore.query.filter_by(nome=nome.upper()).first()

    @staticmethod
    def get_squadre_reali():
        """
        get_squadre_reali() -> list

        ritorna la lista delle squadre reali
        """
        tuples = db.session.query(Giocatore.squadra_reale).distinct().all()
        return [t[0] for t in tuples]

    # noinspection PyUnusedLocal
    def update_squadra_values(self, values, legata=False):
        """
        update_squadra_values(self, values, legata=False)

        Modifica i valori degli attributi della squadra.
        il boolean 'legata' indica se la squadra deve essere associata o
        meno alle leghe esistenti

        :param values: tuple
        :param legata: boolean
        """
        nome, allenatore, budget, mercati, legata = values
        squadra = self.get_squadra_nome(nome)
        squadra.allenatore = allenatore
        squadra.budget = budget
        squadra.op_mercato = mercati
        if legata:
            squadra.leghe = self.get_leghe()
        db.session.commit()
        self.write_to_log('INFO: Squadra %s modificata' % nome)

    def salva_valori_giocatore(self, values):
        """
        salva_valori_giocatore(self, values) -> String

        Modifica gli attributi dell'oggetto giocatore di nome 'nome' e ritorna
        il messaggio di modifica avvenuta

        :param values: tuple di String
        :return: String message
        """
        codice, nome, squadra_reale, valore, valore_asta, ruolo = values
        giocatore = self.get_giocatore_per_nome(nome)
        giocatore.codice = codice
        giocatore.nome = nome.strip().upper()
        giocatore.squadra_reale = squadra_reale.strip().upper()
        giocatore.valore = valore
        giocatore.valore_asta = valore_asta
        giocatore.ruolo = ruolo.strip().lower()
        db.session.commit()
        msg = 'INFO: Giocatore <%s> modificato!' % nome
        self.write_to_log(msg)
        return msg

    def load_data(self, num):
        """
        load_data(self, num)

        Importa la giornata-voti con giornata=num
        Utilizzare solo in fase di debug

        :param num: int giornata
        """
        if len(str(num)) < 2:
            string = '0%s' % num
        else:
            string = '%s' % num
        try:
            importa_txt(string)
        except IOError:
            self.write_to_log('ERROR: File non trovato.')

    @staticmethod
    def load_squadra(lega):
        """
        load_squadra(lega)

        Popola l'oggetto lega con tutte le squadre presenti nel file teams.txt
        Utilizzare solo in fase di debug

        :param lega: object db_models.Lega
        """
        popola_squadre(lega)

    def load_formazione(self, nome_squadra, num):
        try:
            inserisci_formazione_da_file(nome_squadra, num)
        except IOError:
            self.write_to_log('ERROR: file "formazione.txt" non trovato')

    @staticmethod
    def crea_calendario(lega):
        """
        crea_calendario(lega)

        Popola il calendario con le squadre esistenti associate a lega

        :param lega: object db_models.Lega
        """
        popola_calendario(lega)

    @staticmethod
    def get_mercati_rimanenti(squadra):
        """
        get_mercati_rimanenti(squadra) -> int

        Ritorna le operazioni rimanenti dell'oggetto squadra

        :param squadra: object db_models.Squadra
        :return: int operazioni di mercato
        """
        return squadra.op_mercato

    def get_operazioni_effettuate(self, squadra):
        """
        get_operazioni_effettuate(self, squadra)

        Ritorna la lista dei mercati effettuati dalla squadra di nome 'squadra'

        :param squadra: str nome squadra
        :return: list oggetti db_models.Mercato
        """
        objsquadra = self.get_squadra_nome(squadra)
        return Mercato.query.filter_by(squadra=objsquadra).all()

    def get_classifica(self, lega):
        """
        get_classifica(self, lega) -> list

        Ottiene l'oggetto lega di nome 'lega' e ritorna tutti i valori
        utili alla classifica, delle squadre legate a tale oggetto lega.

        :param lega: object String
        :return: list [(squadra.nome, pts, v, n, p, gf, gs, dr, pr), ...]
        """
        objlega = self.get_lega_nome(lega)
        classifica = []
        for squadra in objlega.squadre_lega.all():
            v = sum([pt.vinta for pt in squadra.punteggi])
            n = sum([pt.pareggiata for pt in squadra.punteggi])
            p = sum([pt.persa for pt in squadra.punteggi])
            gf = sum([pt.gol_fatti for pt in squadra.punteggi])
            gs = sum([pt.gol_subiti for pt in squadra.punteggi])
            dr = sum([pt.differenza_reti for pt in squadra.punteggi])
            pr = sum([pt.punti_rosa for pt in squadra.punteggi])
            pts = sum([pt.punti for pt in squadra.punteggi])
            classifica.append((squadra.nome, pts, v, n, p, gf, gs, dr, pr))
        return classifica

    def get_presenze(self, nome):
        """
        get_presenze(self, nome) -> int

        Ritorna le presenze del giocatore con nome=nome

        :param nome: str nome giocatore
        :return: int presenze
        """
        giocatore = self.get_giocatore_per_nome(nome.strip().upper())
        return len([v.voto_nudo for v in giocatore.voti.all()
                    if v.voto_nudo > 0])

    def get_giornate_calendario(self, nome_lega):
        """
        get_giornate_calendario(self, nome_lega) -> list

        Ritorna la lista delle giornate disponibili nel calendario relativo
        alla lega di nome 'lega'

        :param nome_lega: String nome lega
        :return: list int giornate [1, 2, ...]
        """
        lega = self.get_lega_nome(nome_lega)
        return [item[0] for item in db.session.query(
            Partita.giornata).filter_by(lega=lega).distinct().all()]

    def get_tutte_partite(self, nome_lega):
        """
        get_tutte_partite(self, nome_lega) -> list di oggetti Partita

        Ritorna tutte le partite della lega con nome=nome_lega
        :param nome_lega: str nome lega
        :return: list di oggetti db_models.Partita
        """
        lega = self.get_lega_nome(nome_lega)
        return db.session.query(Partita).filter_by(lega=lega).all()

    def get_partite_per_giornata(self, nome_lega, giornata):
        """
        get_partite_per_giornata(self, nome_lega, giornata) -> list di
                                                               oggetti Partita

        Ritorna tutte le partite della lega con nome=nome_lega,
        per la giornata=giornata

        :param nome_lega: str nome lega
        :param giornata: str giornata
        :return: list di oggetti db_models.Partita
        """
        lega = self.get_lega_nome(nome_lega)
        return db.session.query(Partita).filter_by(
            lega=lega).filter_by(giornata=int(giornata)).all()

    def get_squadre_lega(self, lega):
        """
        get_squadre_lega(self, lega) -> list

        Ritorna la lista degli oggetti squadra correlati alla lega di nome
        'lega'

        :param lega: String nome lega
        :return: list object db_models.Squadra
        """
        lega = self.get_lega_nome(lega)
        return lega.squadre_lega.all()

    def get_formazione(self, lega, squadra, giornata):
        """
        get_formazione(self, lega, squadra, giornata) -> list, String

        ritorna la formazione in base agli argomenti 'lega', 'squadra',
        'giornata'. Se la formazione non esiste, ritorna una lista vuota.
        Oltre alle liste, vengono restituiti i relativi messaggi.

        :param lega: String
        :param squadra: String
        :param giornata: int
        :return: list, String
        """
        objlega = self.get_lega_nome(lega)
        objsquadra = objlega.squadre_lega.filter(
            Squadra.nome == squadra.upper()).first()
        objform = objsquadra.formazioni.filter(
            Formazione.giornata == giornata).first()
        if objform:
            form = [Giocatore.query.get(fg.giocatore_id)
                    for fg in FormazioniGiocatori.query.filter_by(
                    formazione_id=objform.id).order_by('position asc').all()]
            return form, 'WARNING: formazione esistente!'
        else:
            return [], 'INFO: formazione da inserire!'

    @staticmethod
    def get_moduli():
        """
        get_moduli() -> list
        """
        return MODULI

    def salva_formazione(self, squadra, giornata, giocatori):
        """
        salva_formazione(self, squadra, giornata, giocatori) -> str message

        Salva la formazione della squadra con nome=squadra, con
        giornata=giornata e ritorna il messaggio di esito

        :param squadra: str nome
        :param giornata: str giornata
        :param giocatori: list str giocatori
        :return: str message
        """
        objsquadra = self.get_squadra_nome(squadra)
        objform = objsquadra.formazioni.filter(
            Formazione.giornata == int(giornata)).first()
        objgiocatori = [self.get_giocatore_per_nome(g.split(' > ')[0])
                       for g in giocatori]
        if objform:
            db.session.delete(objform)
            db.session.commit()
            msg = 'INFO: cancello formazione %s gg %s [esistente]' % (
                objform.squadra, giornata)
            self.write_to_log(msg)

        print objsquadra
        print objgiocatori
        form = Formazione(squadra=objsquadra, giocatori=objgiocatori,
                          giornata=int(giornata))
        db.session.commit()
        msg = 'INFO: salvo formazione %s gg %s' % (squadra, giornata)
        n = 1
        for og in objgiocatori:
            association = FormazioniGiocatori.query.filter(
                FormazioniGiocatori.formazione_id == form.id,
                FormazioniGiocatori.giocatore_id == og.id).first()
            association.position = n
            n += 1
            db.session.commit()
        self.write_to_log(msg)
        return msg

    @staticmethod
    def get_voti_inseriti():
        """
        get_voti_inseriti() -> list

        staticmethod:
        Ritorna la lista delle giornate-voti inserite

        :return: list
        """
        giornate = db.session.query(Voto.giornata).distinct().all()
        return [v[0] for v in giornate] if giornate else []

    def ultima_giornata_importata(self):
        """
        ultima_giornata_importata(self) -> list

        ritorna l'ultima giornata-voti importata o None

        :return: int o None
        """
        try:
            return self.get_voti_inseriti()[-1]
        except IndexError:
            return ''

    def tutte_formazioni_inserite(self, lega, giornata):
        """
        tutte_formazioni_inserite(self, lega, giornata) -> bool

        Ritorna True se per la lega con nome=lega, alla giornata=giornata tutte
        le formazioni sono state inserite, altrimenti ritorna False

        :param lega: str nome lega
        :param giornata: str giornata
        :return: bool
        """
        obj_lega = self.get_lega_nome(lega)
        squadre = obj_lega.squadre_lega.all()
        for squadra in squadre:
            if not squadra.formazioni.filter(
                    Formazione.giornata == int(giornata)).first():
                return False
        return True

    def salva_punteggio_partita(self, lega, giornata, squadra_casa, punteggio):
        """
        salva_punteggio_partita(self, lega, giornata, squadra_casa, punteggio)

        Salva il punteggio nei dati della partita

        :param lega: str nome lega
        :param giornata: str giornata
        :param squadra_casa: str nome squadra
        :param punteggio: tuple
        """
        objlega = self.get_lega_nome(lega)
        objsquadracasa = self.get_squadra_nome(squadra_casa)
        objpartita = Partita.query.filter_by(lega=objlega).filter_by(
            giornata=giornata).filter(Partita.casa == objsquadracasa).first()
        objpartita.gol_casa = punteggio[0]
        objpartita.gol_fuori = punteggio[1]
        db.session.commit()

    def aggiorna_classifica(self, lega, giornata, squadra, punteggio, pts):
        """
        aggiorna_classifica(self, lega, giornata, squadra, punteggio, pts)

        Aggiorna i punteggi (object Punteggio) delle squadre
        per l'aggiornamento classifica

        :param lega: str nome lega
        :param giornata: str giornata
        :param squadra: str nome squadra
        :param punteggio: tuple
        :param pts: tuple punti rosa
        """
        objlega = self.get_lega_nome(lega)
        objsquadra = self.get_squadra_nome(squadra)
        gf, gs = punteggio
        dr = gf - gs
        if gf > gs:
            v, n, p, punti = 1, 0, 0, 3
        elif gs > gf:
            v, n, p, punti = 0, 0, 1, 0
        else:
            v, n, p, punti = 0, 1, 0, 1
        pt = Punteggio.query.filter_by(lega=objlega).filter_by(
            giornata=int(giornata)).filter(
            Punteggio.punteggio_squadre.contains(objsquadra)).first()
        if pt:
            msg = "INFO: cancello vecchio punteggio..."
            self.write_to_log(msg)
            db.session.delete(pt)
            db.session.commit()
        pt = Punteggio(lega=objlega)
        db.session.add(pt)
        db.session.commit()
        pt.punteggio_squadre.append(objsquadra)
        pt.punti = punti
        pt.lega = objlega
        pt.giornata = int(giornata)
        pt.vinta = v
        pt.pareggiata = n
        pt.persa = p
        pt.gol_fatti = gf
        pt.gol_subiti = gs
        pt.differenza_reti = dr
        pt.punti_rosa = float(pts[0])
        db.session.commit()
        msg = "INFO: nuovo punteggio gg.%s creato" % giornata
        self.write_to_log(msg)

    @staticmethod
    def get_limiti_rosa(objsquadra):
        """
        get_limiti_rosa(objsquadra) -> tuple

        ritorna i limiti della rosa derivanti dalle opzioni di lega

        :param objsquadra: object db_models.Squadra
        :return: tuple
        """
        opt = objsquadra.leghe[0].option
        return opt.max_portieri, opt.max_difensori, opt.max_centrocampisti, \
            opt.max_attaccanti
