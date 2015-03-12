"""modulo Controller dell'applicazione Fantalega"""

import wx
from view import Core
from model import ModelFanta
from db_models import Squadra
from tools.imports import importa_txt, popola_calendario
from tools.calcoli import GestoreCalcoloPuntiFormazione as Calc
from tools.calcoli import calcola_ris as risultato


class ControllerCore(object):
    """Class Controller dell'applicazione Fantalega"""
    def __init__(self, model):
        """
        ControllerCore(model) -> object ControllerCore
        :param model: object model.ModelFanta
        """
        super(ControllerCore, self).__init__()
        self.model = model
        self.model.database_esistente()
        self.view = Core(parent=None, controller=self, title='FantaLega 2.1')

    def nuova_lega(self, nome):
        """
        nuova_lega(self, nome) -> db_models.Lega

        Salva una nuova lega e ne ritorna l'oggetto corrispondente

        :param nome: str nome lega
        :return: object db_models.Lega
        """
        return self.model.nuova_lega(nome)

    def salva_opzioni_lega(self, objlega, budget, max_mercati, max_portieri,
                           max_difensori, max_centrocampisti,
                           max_attaccanti, a_r):
        """
        salva_opzioni_lega(self, objlega, budget, max_mercati, max_portieri,
                           max_difensori, max_centrocampisti,
                           max_attaccanti, a_r)

        Invoca il metodo del model salva_opzioni_lega per il salvataggio delle
        opzioni di lega

        :param objlega: object db_models.Lega
        :param budget: str
        :param max_mercati: str
        :param max_portieri: str
        :param max_difensori: str
        :param max_centrocampisti: str
        :param max_attaccanti: str
        :param a_r: str
        """

        self.model.salva_opzioni_lega(objlega, budget, max_mercati,
                                      max_portieri, max_difensori,
                                      max_centrocampisti, max_attaccanti, a_r)

    def modifica_lega(self, nome, bd, me, mp, md, mc, ma, ar, offset):
        """
        modifica_lega(self, nome, bd, me, mp, md, mc, ma, ar, offset) -> list

        Modifica i valori della lega selezionata e ritorna la nuova lista delle
        leghe, dopo la modifica.

        :param nome: str
        :param bd: str
        :param me: str
        :param mp: str
        :param md: str
        :param mc: str
        :param ma: str
        :param ar: str
        :param offset: str
        :return: list di oggetti db_models.Lega
        """
        self.model.modifica_lega(nome, bd, me, mp, md, mc, ma, ar, offset)
        return self.model.get_leghe()

    def elimina_lega(self, lega):
        """
        elimina_lega(self, lega)

        Invoca il metodo del model elimina_lega per eliminare la lega dal db.

        :param lega: str nome lega
        :return: list di oggetti db_models.Lega
        """
        return self.model.elimina_lega(lega)

    def get_lega_nome(self, nome):
        """
        get_lega_nome(self, nome) -> object Lega

        Ritorna l'oggetto Lega con nome=nome

        :param nome: str nome Lega
        :return: object db_models.Lega
        """
        return self.model.get_lega_nome(nome)

    def get_leghe(self):
        """
        get_leghe(self) -> list

        Invoca il metodo model.get_leghe e ritorna tutte le leghe disponibili

        :return: list
        """
        return self.model.get_leghe()

    # Squadra
    def salva_nuova_squadra(self, nome, allenatore, budget, mercati, leghe):
        """
        salva_nuova_squadra(self, nome, allenatore, budget, mercati, leghe) ->
                                                                           msg
        invoca il metodo del model salva_nuova_squadra e ritorna il messaggio di
        esito alla view di competenza.

        :param nome: str
        :param allenatore: str
        :param budget: str
        :param mercati: str
        :param leghe: list di oggetti db_models.Lega
        :return:
        """
        return self.model.salva_nuova_squadra(nome, allenatore,
                                              budget, mercati, leghe)

    def get_squadre(self):
        """
        get_squadre(self) -> list di oggetti Squadra

        ritorna una lista di tutti gli oggetti Squadra

        :return: list di oggetti db_models.Squadra
        """
        return self.model.get_squadre()

    def get_giocatori(self, prefix=None, ruolo=None, squadra_reale=None):
        """
        get_giocatori(self) -> list di oggetti Giocatore

        ritorna una lista di tutti gli oggetti Giocatore che soddisfano
        i criteri prefix(nome parziale), ruolo, squadra_reale:

        :param prefix: str nome parziale
        :param ruolo: str ruolo
        :param squadra_reale: str squadra_reale
        :return: list di oggetti db_models.Giocatore
        """
        return self.model.get_giocatori(prefix, ruolo, squadra_reale)

    def get_giocatore_per_nome(self, nome):
        """
        get_giocatore_per_nome(self, nome) -> object Giocatore

        Invoca il metodo del model get_giocatore_per_nome per ottenere
        l'oggetto Giocatore con nome=nome

        :param nome: str nome Giocatore
        :return: object db_models.Giocatore
        """
        return self.model.get_giocatore_per_nome(nome)

    def giocatori_disponibili(self, ruolo=None, prefix=''):
        """
        giocatori_disponibili(self, ruolo, nome) -> list

        Ritorna una lista di stringhe 'nome > ruolo' dalla lista ottenuta
        invocando il metodo giocatori_disponibili del model

        :param ruolo: str ruolo
        :param prefix: str nome giocatore
        :return: list di str 'nome > ruolo'
        """
        disp = self.model.giocatori_disponibili(ruolo=ruolo, prefix=prefix)
        return ['%s > %s' % (g.nome, g.ruolo.lower()) for g in disp]

    def get_giocatore_values(self, nome):
        """
        get_giocatore_values(self, nome) -> tuple

        Ottiene l'oggetto Giocatore tramite il nome e ritorna la tupla dei suoi
        valori.

        :param nome: String nome giocatore
        :return: tuple di String (codice, nome, squadra_reale, valore,
                                  valore_asta, ruolo)
        """
        g = self.model.get_giocatore_per_nome(nome)
        if g:
            return g.codice, g.nome, g.squadra_reale,\
                g.valore, g.valore_asta, g.ruolo

    def get_squadra_default_values(self):
        """
        get_squadra_default_values(self) -> int, int

        Ritorna i valori di default per una squadra: max mercati e budget

        :return: int Option.max_mercati
        :return: int Option.budget
        """
        leghe = self.get_leghe()
        if leghe:
            return leghe[0].option.max_mercati, leghe[0].option.budget
        return '', ''

    def get_squadra_nome(self, nome):
        """
        get_squadra_nome(self, nome) -> object Squadra

        Invoca il metodo get_squadra_nome del model e ritorna l'oggetto Squadra
        con nome=nome

        :param nome: str nome squadra
        :return: object db_models.Squadra
        """
        return self.model.get_squadra_nome(nome)

    def get_rosa_squadra(self, nome):
        """
        get_rosa_squadra(self, nome) -> list

        Ritorna la lista dei giocatori della rosa di una squadra con nome=nome

        :param nome: str nome squadra
        :return: list ['nome > ruolo', ...]
        """
        obj_squadra = self.model.get_squadra_nome(nome)
        giocatori = obj_squadra.giocatori.all()
        giocatori.sort(key=lambda x: x.codice)
        return ['%s > %s' % (g.nome, g.ruolo.lower()) for g in giocatori]

    def get_mercati_rimanenti(self, squadra):
        """
        get_mercati_rimanenti(self, squadra)

        Ritorna i mercati rimanenti della squadra con nome=nome

        :param squadra: str nome squadra o object Squadra
        :return: int operazioni mercato rimanenti
        """
        if isinstance(squadra, Squadra):
            return self.model.get_mercati_rimanenti(squadra)
        else:
            objsquadra = self.model.get_squadra_nome(squadra)
            return self.model.get_mercati_rimanenti(objsquadra)

    def get_operazioni_mercato(self, squadra):
        """
        get_operazioni_mercato(self, squadra) -> int, list

        Ritorna alla view il valore di operazioni di mercato rimanenti e la
        lista dei giocatori IN e OUT della propria rosa.

        :param squadra: str
        :return: int op_rimanenti
        :return: list op_effettuate
        """
        op_rimanenti = self.get_mercati_rimanenti(squadra)
        op_effettuate = self.model.get_operazioni_effettuate(squadra)
        return op_rimanenti, op_effettuate

    def get_squadra_values(self, nome):
        """
        get_squadra_values(self, nome) -> tuple

        ritorna i valori della squadra con nome=nome

        :param nome: str nome di squadra
        :return: tuple dei valori di squadra
        """
        squadra = self.model.get_squadra_nome(nome)
        if squadra:
            values = (squadra.nome, squadra.allenatore, squadra.budget,
                      squadra.op_mercato)
            return values

    def get_squadre_reali(self):
        """
        get_squadre_reali(self)

        ritorna la lista dei nomi delle squadre reali disponibili

        :return: list di str
        """
        return self.model.get_squadre_reali()

    def elimina_squadra(self, squadra):
        """
        elimina_squadra(self, squadra) -> list di object Squadra

        Invoca il metodo elimina_squadra del model e ritorna la lista di
        oggetti Squadra rimanenti

        :param squadra: str nome squadra
        :return: list di oggetti db_models.Squadra
        """
        return self.model.elimina_squadra(squadra)

    def update_squadra_values(self, values):
        """
        update_squadra_values(self, values)

        Invoca il metodo del model update_squadra_values per salvare i valori
        degli attributi della squadra

        :param values: tuple
        """
        self.model.update_squadra_values(values)

    # Giocatore
    def salva_valori_giocatore(self, values):
        """
        salva_valori_giocatore(self, values)

        Invoca il metodo del model salva_valori_giocatore per salvare i valori
        modificati, del giocatore e ritorna il messaggio ottenuto dal model,
        alla view di competenza

        :param values: tuple di String
        :return: String message
        """
        return self.model.salva_valori_giocatore(values)

    def cedi_giocatore(self, nome):
        """

        :param nome: str nome giocatore
        :return: list di giocatori ['nome > ruolo', ...]
        """
        return ['%s > %s' % (g.nome, g.ruolo.lower())
                for g in self.model.cedi_giocatore(nome)]

    def rosa_acquista_giocatore(self, nome, squadra):
        """
        rosa_acquista_giocatore(self, nome, squadra) -> list rosa

        Invoca il metodo rosa_acquista_giocatore del model e ritorna la lista
        della rosa aggiornata post-acquisto

        :param nome: str nome giocatore
        :param squadra: str nome squadra
        :return: list ['nome > ruolo', ...]
        """
        return ['%s > %s' % (g.nome, g.ruolo.lower())
                for g in self.model.rosa_acquista_giocatore(nome, squadra)]

    def acquista_giocatore(self, nome, prezzo, squadra):
        """
        acquista_giocatore(self, nome, prezzo, squadra) -> str message

        Invoca il metodo del model acquista_giocatore e ritorna il messaggio
        di esito operazione

        :param nome: str nome Giocatore
        :param prezzo: str prezzo
        :param squadra: str nome squadra
        :return: str
        """
        return self.model.acquista_giocatore(nome, prezzo, squadra)

    def set_ruolo(self, ruolo):
        """
        set_ruolo(self, ruolo)

        Setta ruolo al valore ruolo

        :param ruolo: str ruolo
        """
        self.model.ruolo = ruolo

    def get_ruolo(self):
        """
        get_ruolo(self) -> str ruolo
        """
        return self.model.ruolo

    def break_limits(self, squadra):
        """
        break_limits(self, squadra) -> bool

        Ritorna True se l'oggetto squadra con nome=nome supera i limiti di
        rosa imposti dalla lega

        :param squadra: str nome squadra
        :return: boolean
        """
        obj_squadra = self.model.get_squadra_nome(squadra)
        mp, md, mc, ma = self.model.get_limiti_rosa(obj_squadra)
        pp = len([g for g in obj_squadra.giocatori.all()
                  if int(g.codice) < 200])
        dd = len([g for g in obj_squadra.giocatori.all()
              if 200 < int(g.codice) < 500])
        cc = len([g for g in obj_squadra.giocatori.all()
              if 500 < int(g.codice) < 800])
        aa = len([g for g in obj_squadra.giocatori.all()
                  if int(g.codice) > 800])
        return pp >= mp and dd >= md and cc >= mc and aa >= ma

    def get_classifica(self, lega):
        """
        get_classifica(self, lega) -> list

        Invoca il metodo model.get_classifica passando come argomento 'lega'.
        Ritorna alla view di competenza una lista di valori delle squadre,
        ordinati on modo decrescente in base ai punti in classifica.

        :param lega: String nome lega
        :return: sorted list [(nome, pts, v, n, p, gf, gs, dr, pr), ...]
        """
        classifica = self.model.get_classifica(lega)
        classifica.sort(key=lambda x: x[1], reverse=True)
        return classifica

    def ultima_giornata_importata(self):
        """
        ultima_giornata_importata(self) -> int

        ritorna l'ultima giornata importata

        :return: int
        """
        return self.model.ultima_giornata_importata()

    def get_valori_statistici(self, nome):
        """
        get_valori_statistici(self, nome) -> tuple uv, mv, presenze, aff, valore

        Ritorna la tupla dei valori statistici del giocatore di nome 'nome'

        :param nome: str nome del giocatore
        :return: tuple di str (uv, mv, presenze, aff, valore)
        """
        presenze = self.model.get_presenze(nome)
        giocatore = self.model.get_giocatore_per_nome(nome)
        valore = giocatore.valore
        gg_importate = len(self.get_voti_inseriti())
        aff = int(presenze) * 100.0 / gg_importate
        voti = [v.fanta_voto for v in giocatore.voti.all() if v.voto_nudo > 0]
        mv = sum(voti) / len(voti)
        try:
            uv = voti[-1]
        except IndexError:
            uv = 0.0
        return uv, mv, presenze, aff, valore

    @staticmethod
    def importa_voti(path, progressbar):
        """
        importa_voti(path, progressbar)

        Invoca la funzione imports.importa_txt per l'importazione dei voti

        :param path: str path del file voti da importare
        :param progressbar: object wx.ProgressBar
        """
        importa_txt(path, progressbar)

    def get_giornate_calendario(self, nome_lega):
        """
        get_giornate_calendario(self, nome_lega) -> list

        Invoca il metodo get_giornate_calendario con nome_lega come argomento
        e trasforma gli int della lista in stringhe per la view

        :param nome_lega: String nome lega
        :return: list String ['1', '2', ...]
        """
        return ['%s' % g for g in
                self.model.get_giornate_calendario(nome_lega)]

    def get_tutte_partite(self, nome_lega):
        """
        get_tutte_partite(self, nome_lega) -> list di oggetti Partita

        ritorna la lista delle partite della lega con nome=nome_lega

        :param nome_lega: str nome lega
        :return: list di oggetti db_models.Partita
        """
        return [p for p in reversed(self.model.get_tutte_partite(nome_lega))]

    def get_partite_per_giornata(self, nome_lega, giornata):
        """
        get_partite_per_giornata(self, nome_lega, giornata) -> list di
                                                               oggetti Partita

        ritorna la lista delle partite della giornata=giornata,
        della lega con nome=nome_lega

        :param nome_lega: str nome lega
        :param giornata: str giornata
        :return: list di oggetti db_models.Partita
        """
        return [p for p in reversed(self.model.get_partite_per_giornata(
            nome_lega, int(giornata)))]

    def cancella_calendario(self, partite, progressbar):
        """
        cancella_calendario(self, partite, progressbar)

        Cancella tutte le partite del calendario

        :param partite: list di oggetti Partita
        :param progressbar: object progressbar
        """
        count = 0
        for partita in partite:
            feedback = self.model.elimina_partita(partita)
            progressbar.progress(count, newmsg=feedback)
            count += 1

    def crea_calendario(self, lega, progressbar):
        """
        crea_calendario(self, lega, progressbar)

        invoca la funzione imports.popola_calendario e crea un nuovo calendario

        :param lega: str nome lega
        :param progressbar: object progressbar
        """
        objlega = self.get_lega_nome(lega)
        popola_calendario(objlega, progressbar)

    def get_squadre_lega(self, lega):
        """
        get_squadre_lega(self, lega) -> list

        Ritorna la lista dei nomi delle squadre associate ad una lega di nome
        'lega'

        :param lega: String nome lega
        :return: list
        """
        return [s.nome for s in self.model.get_squadre_lega(lega)]

    def get_formazione(self, lega, squadra, giornata):
        """
        get_formazione(self, lega, squadra, giornata) -> list, str message

        Invoca il metodo get_formazione del model e ritorna la lista dei
        giocatori presenti nella formazione di giornata=giornata, della squadra
        con nome=squadra, associata alla lega con nome=lega

        :param lega: str nome lega
        :param squadra: str nome squadra
        :param giornata: str giornata
        :return: list, str message
        """
        try:
            formazione, msg = self.model.get_formazione(lega,
                                                        squadra, giornata)
            giocatori = ['%s > %s' % (g.nome, g.ruolo)
                        for g in formazione]
            return giocatori, msg
        except AttributeError:
            return [], "Formazione non inserita!"

    def get_moduli(self):
        """
        get_moduli(self) -> list
        """
        return self.model.get_moduli()

    def modulo_corretto(self, titolari, modulo_scelto):
        """
        modulo_corretto(self, titolari, modulo_scelto) -> bool

        ritorna True se il modulo della formazione coincide con quello scelto

        :param titolari: list di str giocatori
        :param modulo_scelto: str modulo
        :return: bool
        """
        dd, cc, aa = 0, 0, 0
        for titolare in titolari:
            ruolo = self.get_giocatore_per_nome(titolare.split(' > ')[0]).ruolo
            if ruolo == 'difensore':
                dd += 1
            elif ruolo == 'attaccante':
                aa += 1
            elif ruolo == 'portiere':
                pass
            else:
                cc += 1
        modulo = '%s-%s-%s' % (dd, cc, aa)
        return modulo == modulo_scelto

    @staticmethod
    def duplicati_presenti(giocatori):
        """
        duplicati_presenti(giocatori) -> bool

        Ritorna True se ci sono duplicati nella lista passata come arg.

        :param giocatori: list
        :return: bool
        """
        for giocatore in giocatori:
            count = giocatori.count(giocatore)
            if count > 1:
                return True
        return False

    def salva_formazione(self, squadra, giornata, giocatori):
        """
        salva_formazione(self, squadra, giornata, giocatori) -> str message

        Invoca il metodo salva_formazione del model per salvare la formazione
        e ritorna il messaggio di esito

        :param squadra: str nome squadra
        :param giornata: str giornata
        :param giocatori: list giocatori
        :return: str message
        """
        return self.model.salva_formazione(squadra, giornata, giocatori)

    def get_voti_inseriti(self):
        """
        get_voti_inseriti(self) -> list

        ritorna la lista delle giornate dei voti inseriti

        :return: list
        """
        return [str(gg) for gg in self.model.get_voti_inseriti()]

    def get_punteggio(self, lega, squadra, giornata):
        """
        get_punteggio(self, lega, squadra, giornata) -> list, String,
                                                        dict, String

        Invoca il metodo model.get_formazione passando come argomenti 'lega',
        'squadra' e 'giornata'.
        Ottenuto l'oggetto formazione, viene passato all'handler punteggio,
        che restituisce un punteggio complessivo e un dizionario:
        giocatore: punteggio

        :param lega: String
        :param squadra: String
        :param giornata: int
        :return: list, String, dict, String
        """
        objlega = self.get_lega_nome(lega)
        offset = objlega.option.offset
        objform, msg = self.model.get_formazione(lega, squadra, int(giornata))
        if objform:
            form = ['%s > %s' % (g.nome, g.ruolo) for g in objform]
            calc = Calc(objform, giornata=giornata, offset=offset)
            res, dv = calc.calcola_punti_formazione()
            return form, res, dv, msg
        else:
            return [], '', {}, msg

    def quante_squadre_per_lega(self, lega):
        """
        quante_squadre_per_lega(self, lega) -> int

        :param lega: str nome lega
        """
        objlega = self.get_lega_nome(lega)
        return len(objlega.squadre_lega.all())

    def tutte_formazioni_inserite(self, lega, giornata):
        """
        tutte_formazioni_inserite(self, lega, giornata) -> bool

        Invoca il metodo tutte_formazioni_inserite del model e ne
        ritorna l'esito

        :param lega: str nome lega
        :param giornata: str giornata
        :return: bool
        """
        return self.model.tutte_formazioni_inserite(lega, giornata)

    def calcola_punteggi(self, lega, partite, giornata):
        """
        calcola_punteggi(self, lega, partite, giornata) -> list

        Invoca i metodi del model per il calcolo dei punteggi di giornata e
        ritorna alla view, i risultati

        :param lega: str nome lega
        :param partite: list partite
        :param giornata: str giornata
        :return: list
        """
        objlega = self.get_lega_nome(lega)
        offset = objlega.option.offset
        results = []
        for partita in partite:
            casa, fuori = partita
            form_casa, msg = self.model.get_formazione(lega=lega.upper(),
                                                  squadra=casa.upper(),
                                                  giornata=int(giornata))
            handler = Calc(form_casa, int(giornata), offset=offset)
            pts_casa = handler.calcola_punti_formazione()
            form_fuori, msg = self.model.get_formazione(lega=lega.upper(),
                                                   squadra=fuori.upper(),
                                                   giornata=int(giornata))
            pts_fuori = Calc(form_fuori, int(giornata),
                             offset=offset).calcola_punti_formazione()
            punteggio = risultato(pts_casa[0], pts_fuori[0])
            results.append((pts_casa[0], pts_fuori[0], punteggio))
            self.model.salva_punteggio_partita(lega, int(giornata),
                                               casa, punteggio)
            self.model.aggiorna_classifica(lega, int(giornata), casa,
                                           punteggio, pts_casa)
            invertito = [gol for gol in reversed(punteggio)]
            self.model.aggiorna_classifica(lega, int(giornata),
                                           fuori, invertito, pts_fuori)
        return results


def run():
    """App starter"""
    app = wx.App()
    model = ModelFanta()
    controller = ControllerCore(model)
    app.SetTopWindow(controller.view)
    app.MainLoop()


if __name__ == '__main__':
    run()