import wx
from messages import InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewAsta(wx.Frame):
    """
    SubFrame Asta dell'applicazione FantaLega
    Da qui gestisco l'Asta dei giocatori
    """
    def __init__(self, parent, title):
        """
        ViewAsta(parent, title) -> ViewAsta object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewAsta, self).__init__(parent=self.parent, title=title,
                                       style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelAsta(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSize((250, 600))
        self.SetSizer(sizer)

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe,
                  self.panel.btn_cancel)
        self.Bind(wx.EVT_BUTTON, self.acquista_giocatore,
                  self.panel.btn_save_giocatore)
        self.Bind(wx.EVT_RADIOBOX, self.on_ruoli)
        self.Bind(wx.EVT_COMBOBOX, self.on_ruoli,
                  self.panel.cb_squadre_reali)
        self.Bind(wx.EVT_COMBOBOX, self.on_giocatore,
                  self.panel.cb_giocatori)

    # noinspection PyUnusedLocal
    def acquista_giocatore(self, event):
        """
        acquista_giocatore(self, event)

        Invoca il metodo del controller, per l'acquisto del giocatore

            :param event: object wx.EVT_BUTTON
        """
        nome = self.panel.cb_giocatori.GetStringSelection()
        prezzo = self.panel.valore_asta.GetValue()
        acquirente = self.panel.cb_squadre.GetStringSelection()
        if acquirente and prezzo:
            msg = self.controller.acquista_giocatore(nome, prezzo, acquirente)
            InfoMessage(self, msg).get_choice()

        if prezzo == '0':
            InfoMessage(self, 'Manca il prezzo asta!').get_choice()

        if acquirente == '':
            InfoMessage(self, 'Scegli/Conferma Acquirente!').get_choice()

    # noinspection PyUnusedLocal
    def on_ruoli(self, event):
        """
        on_ruoli(self, event)

        Aggiorna i giocatori visualizzati nella combobox

            :param event: object wx.EVT_RADIOBOX
                          object wx.EVT_COMBOBOX
        """
        ruolo = self.panel.rb_ruoli.GetStringSelection()
        squadra_reale = self.panel.cb_squadre_reali.GetStringSelection()
        giocatori = self.controller.get_giocatori(ruolo=ruolo,
                                                  squadra_reale=squadra_reale)
        self.update_choice_giocatori(giocatori)

    # noinspection PyUnusedLocal
    def on_giocatore(self, event):
        """
        on_giocatore(self, event)

        Aggiorna i valori del giocatore selezionato

            :param event: object wx.EVT_COMBOBOX
        """
        nome = self.panel.cb_giocatori.GetStringSelection()
        objgiocatore = self.controller.get_giocatore_per_nome(nome)
        self.update_valori_giocatore(objgiocatore)

    def update_choice_giocatori(self, giocatori):
        """
        update_choice_giocatori(self, giocatori)

        Aggiorna la lista dei giocatori visualizzabili nella combobox

            :param giocatori: lista di oggetti Giocatore

        """
        self.panel.cb_giocatori.Clear()
        self.panel.cb_giocatori.AppendItems([g.nome for g in giocatori])

    def update_valori_giocatore(self, giocatore):
        """
        update_valori_giocatore(self, giocatore):

        Aggiorna le Textcontrols con gli attributi dell' oggetto 'Giocatore'

            :param event: object Giocatore
        """
        self.panel.nome.SetValue(giocatore.nome)
        self.panel.codice.SetValue(str(giocatore.codice))
        self.panel.valore.SetValue(str(giocatore.valore))
        self.panel.squadra_reale.SetValue(giocatore.squadra_reale)
        self.panel.valore_asta.SetValue(str(giocatore.valore_asta))
        if giocatore.squadra:
            self.panel.cb_squadre.SetValue(giocatore.squadra.nome)
        else:
            self.panel.cb_squadre.Clear()
            squadre = [''] + [s.nome for s in self.controller.get_squadre()]
            self.panel.cb_squadre.AppendItems(squadre)

    def update_choice_squadre_reali(self, squadre_reali):
        """
        update_choice_squadre_reali(self, squadre_reali)

        Aggiorna la lista delle squadre_reali visualizzabili dalla combobox
            :param event: lista di str
        """
        self.panel.cb_squadre_reali.Clear()
        self.panel.cb_squadre_reali.AppendItems(squadre_reali)


class PanelAsta(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelAsta(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelAsta, self).__init__(parent)
        ruoli = ['tutti', 'portiere', 'difensore', 'centrocampista',
                 'attaccante']
        self.giocatori = [g.nome for g in parent.controller.get_giocatori()]
        self.squadre = [s.nome for s in parent.controller.get_squadre()]
        self.squadre_reali = parent.controller.get_squadre_reali()
        self.nome = wx.TextCtrl(self)
        self.codice = wx.TextCtrl(self)
        self.squadra_reale = wx.TextCtrl(self)
        self.valore = wx.TextCtrl(self)
        self.valore_asta = wx.TextCtrl(self)
        self.cb_squadre_reali = wx.ComboBox(self, -1, "filtro squadra",
                                  choices=self.squadre_reali,
                                  style=wx.CB_DROPDOWN)
        self.cb_giocatori = wx.ComboBox(self, -1, "giocatori disponibili",
                                  choices=self.giocatori, style=wx.CB_DROPDOWN)
        self.cb_squadre = wx.ComboBox(self, -1, "associa squadra",
                                    choices=self.squadre, style=wx.CB_DROPDOWN)
        self.rb_ruoli = wx.RadioBox(self, -1, "ruoli", choices=ruoli,
                                    majorDimension=1, style=wx.RA_SPECIFY_COLS)
        box_ruoli = wx.BoxSizer(wx.VERTICAL)
        box_ruoli.Add(self.rb_ruoli, 0, wx.ALIGN_CENTER_HORIZONTAL, 15)
        box_ruoli.Add(wx.StaticText(self, label="Squadra Reale"),
                  1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)
        box_ruoli.Add(self.cb_squadre_reali,
                      0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        box_ruoli.Add(self.cb_giocatori, 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 15)
        text_sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=5)
        text_sizer.Add(wx.StaticText(self, label="Nome:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.nome, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Codice:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.codice, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Squadra Reale:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.squadra_reale, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Valore:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.valore, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Prezzo:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.valore_asta, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Acquirente:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        text_sizer.AddGrowableCol(1)

        button_sizer = wx.StdDialogButtonSizer()
        self.btn_save_giocatore = wx.Button(self, wx.ID_SAVE)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        self.btn_save_giocatore.SetDefault()
        button_sizer.AddButton(self.btn_save_giocatore)
        button_sizer.AddButton(self.btn_cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box_ruoli, 0, wx.EXPAND | wx.ALL, 20)
        sizer.Add(text_sizer, 0, wx.EXPAND | wx.ALL, 20)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        button_sizer.Realize()
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')
