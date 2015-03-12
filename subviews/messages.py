# -*- coding: utf-8 -*-#
import wx
import wx.html as wxhtml


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class InfoMessage(wx.MessageDialog):
    """Simple message Dialog"""
    def __init__(self, parent, message):
        wx.MessageDialog.__init__(self, parent, message, 'core info', wx.OK |
                                  wx.ICON_EXCLAMATION)

    def get_choice(self):
        """get the state of the user choice"""
        if self.ShowModal() == wx.ID_OK:
            self.Destroy()


class ChoiceMessage(wx.MessageDialog):
    """Simple choice message Dialog"""
    def __init__(self, parent, message):
        wx.MessageDialog.__init__(self, parent, message, 'Core question',
                                  wx.YES_NO | wx.ICON_QUESTION)

    def is_yes(self):
        """get True if YES is clicked"""
        if self.ShowModal() == wx.ID_YES:
            return True
        else:
            self.Destroy()


class EntryDialog(wx.TextEntryDialog):
    """Simple Text Entry Dialog"""
    def __init__(self, parent, msg, value):
        wx.TextEntryDialog.__init__(self, parent, msg, 'Core request',
                                    defaultValue=value, style=wx.OK)

    def get_choice(self):
        """get the state of the user choice"""
        if self.ShowModal() == wx.ID_OK:
            response = self.GetValue()
            self.Destroy()
            return response


class InfoFrame(wx.Frame):
    """Frame for Abuot text"""
    def __init__(self, parent, title):
        super(InfoFrame, self).__init__(parent=parent, title=title,
                                        style=STYLE)
        self.parent = parent
        self.text = """
<html>
<center><h1>FantaManager</h1> versione 2.1<br>
by Bancaldo</td></center><br><br>
<b>Fantamanager</b> e' una semplice applicazione per la creazione<br>
e gestione di una FantaLega<br>
<br>
<b>pacchetti utilizzati:</b><br>
- wxPython</b> for Graphics<br>
- Flask-SQLAlchemy</b> for database and Object Ralation Mapping<br>
<br>
<b>link utili:</b><br>
web-site: www.bancaldo.wordpress.com<br>
web-site: www.bancaldo.altervista.org<br>
<br>
<b>last revision:</b> Feb 22, 2015</p><br>
<b>author:</b> bancaldo
</html>
"""
        self.SetSize((400, 600))
        html = wxhtml.HtmlWindow(self)
        html.SetPage(self.text)
        self.btn_quit = wx.Button(self, -1, 'quit', (25, 150), (150, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.btn_quit)
        self.Centre()
        self.Show()


class HelpFrame(wx.Frame):
    """Frame for Abuot text"""
    def __init__(self, parent, title):
        super(HelpFrame, self).__init__(parent=parent, title=title,
                                        style=STYLE)
        self.parent = parent
        self.text = """
<html>
<center><b>FantaLega</b></center><br><br>
<b>1) Importare i voti</b><br>
I voti sono reperibili sul mio blog: www.bancaldo.wordpress.com<br>
<b>2) Creare una nuova Lega</b><br>
Dal menu Leghe, impostando le opzioni di lega:<br>
budget squadra, massimo numero di cambi, offset giornate<br>
(indica l'offset di giornata tra campionato reale e fantalega), ecc.<br>
<b>3) Creare le Squadre</b><br>
Dal menu Squadre, associandole alle leghe esistenti, cliccando<br>
l'apposita checkbox 'Associa a Leghe esistenti'.<br>
<b>4) Iniziare l'asta</b><br>
Create le squadre e' necessario eseguire l'Asta.<br>
Dal menu lega scegliere Inizia Asta e comporre le squadre.<br>
Ad ogni giocatore associare la squadra acquirente ed il prezzo d'asta,<br>
per aggiornare il budget della squadra stessa e non rischiare di sforare
dal monte fantamilioni.<br>
<b>5) Calendario</b><br>
Creare un nuovo calendario per la lega creata<br>
dal menu calendario > crea calendario<br>
E' possibile consultare anche le giornate di lega selezionando la giornata.<br>
<b>6) Formazioni</b><br>
Inserire le formazioni per ogni squadra dal menu Formazione, scegliendo<br>
la giornata ed il modulo, con il quale verranno calcolati i punteggi.<br>
E' possibile consultare il punteggio di una formazione per una determinata<br>
giornata, dallo stesso menu, o modificare la formazione inserita.<br>
<b>7) Punteggi</b><br>
I punteggi si calcolano scegliendo la giornata da menu calendario > punteggi<br>
e premendo il pulsante <Calcola>. In caso di punteggi gia' calcolati,<br>
questi verranno sovrascritti<br>
<b>8) Restart</b><br>
Per ricominciare tutto da capo, e' sufficiente eliminare il file fantalega.db,
ad applicazione spenta.<br>
L'applicazione puo' gestire piu' leghe contemporaneamente.<br><br>
bancaldo<br>
</html>
        """
        self.SetSize((600, 800))
        html = wxhtml.HtmlWindow(self)
        html.SetPage(self.text)
        self.btn_quit = wx.Button(self, -1, 'quit', (25, 150), (150, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.btn_quit)
        self.Centre()
        self.Show()


class RulesFrame(wx.Frame):
    """Frame for rules text"""
    def __init__(self, parent, title):
        super(RulesFrame, self).__init__(parent=parent, title=title,
                                         style=STYLE)
        self.parent = parent
        self.text = """
<html>
<b>consegna formazioni</b><br><br>
La formazione va consegnata entro 1min dall'inizio del primo anticipo.<br>
FA TESTO L'ORA DEL MESSAGGIO DEL BLOG  o l'ora INTERNET di whatsapp.<br>
<b>votazioni partite</b><br>
come previsto dal regolamento della Gazzetta<br><br>

<b>Fantamercato</b><br>
Il mercato tra fantaallenatori e' limitato a 6 giocatori fino
a tutto febbraio.<br>
Le operazioni effettuate al mercato di riparazione sono contate a parte.<br>
Gli scambi devono essere comunicati entro  Venerdi ore 15:00.<br>
(Operazioni di sabato non valgono!).<br>
Se un giocatore e' conteso tra piu' fantaallenatori, si ricorre alle buste.<br>
Finito il mercato di riparazione Ufficiale, termina anche il Fantamercato<br>
NON E' PREVISTO IL CAMBIO DI UN GIOCATORE INFORTUNATO
(solo al mercato di rip.)<br>
Non si puo' riprendere un giocatore precedentemente venduto<br><br>

<b>conferme per anno successivo</b><br>
Al termine della fantalega si potranno confermare 1 giocatore per ruolo<br>
eccetto il portiere, per la stagione successiva<br><br>

<b>Sostituzioni</b><br>
NON ESISTE IL CAMBIO MODULO<br>
in caso di consegna di 11 panchinari, verranno esclusi quelli in esubero,<br>
dall '11o in poi. Per evitare disordine, la panchina va consegnata
nell'ordine<br>
in cui si vuole che entrino i  sostituti, non necessariamente portiere,<br>
3 difensori, 3 ccampsti ecc. Di norma si procede dal ruolo più basso al
piu' alto<br>
prima entra un difensore poi un ccampista poi un attaccante,<br>
in caso manchino più di tre titolari.<br><br>

<b>Fasce Goals</b><br>
66 (1), 72 (2), 78 (3)...stessa fascia con +4 (1), +10 (1), <60 (-1)<br><br>

<b>Premi FantaLega</b><br>
Campione 225e. ViceCampione 125e. Terzo classificato 75e<br><br>

<b>Premi Fantachampions</b><br>
Campione 75e
</html>
        """
        self.SetSize((700, 725))
        html = wxhtml.HtmlWindow(self)
        html.SetPage(self.text)
        self.btn_quit = wx.Button(self, -1, 'quit', (25, 150), (150, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.btn_quit)
        self.SetSizer(sizer)
        self.Centre()
        self.Show()


class ProgressBar(wx.ProgressDialog):
    """Class per la gestione di una progressbar"""
    def __init__(self, parent, title='', message='loading...', maximum=550):
        super(ProgressBar, self).__init__(parent=parent, title=title,
                                          message=message, maximum=maximum,
            style=wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

    def progress(self, value, newmsg=''):
        """

        :param value: int valore di avanzamento della pb
        :param newmsg: str messaggio da visualizzare sulla pb
        """
        wx.MicroSleep(1)  # for slow processes use wx.MilliSleep(1)
        self.Update(value, newmsg)
