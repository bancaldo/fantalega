import wx
from messages import InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewEditGiocatore(wx.Frame):
    """GUI per modifica giocatore"""
    def __init__(self, parent, title):
        """
        ViewEditGiocatore(parent, title) -> ViewEditGiocatore object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewEditGiocatore, self).__init__(parent=self.parent, title=title,
                                                style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelEditGiocatore(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((350, 500))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.modifica_giocatore, self.panel.btn_save)
        self.Bind(wx.EVT_COMBOBOX, self.on_giocatore, self.panel.cb_giocatori)
        self.Bind(wx.EVT_TEXT, self.on_filtro, self.panel.filtro)

    # noinspection PyUnusedLocal
    def on_filtro(self, event):
        """
        on_filtro(self, event)

        Invoca il metodo giocatori_disponibili del controller e filtra i
        disponibili in base al testo digitato nella combotextctr 'filtro'

        :param event: wx.EVT_TEXT
        """
        prefix = self.panel.filtro.GetValue().upper()
        disponibili = [g.nome
                       for g in self.controller.get_giocatori(prefix=prefix)]
        self.panel.cb_giocatori.Clear()
        self.panel.cb_giocatori.SetValue("scegli giocatore...")
        self.panel.cb_giocatori.AppendItems(disponibili)

    # noinspection PyUnusedLocal
    def modifica_giocatore(self, event):
        """
        modifica_giocatore(self, event)

        Invoca il metodo del controller per la modifica dei valori del
        giocatore selezionato. Solleva un'eccezione se nessun giocatore
        viene selezionato

            :param event: object wx.EVT_BUTTON
        """
        try:
            codice = int(self.panel.codice.GetValue())
            nome = self.panel.nome.GetValue()
            squadra_reale = self.panel.squadra_reale.GetValue()
            valore = int(self.panel.valore.GetValue())
            valore_asta = int(self.panel.valore_asta.GetValue())
            ruolo = self.panel.ruolo.GetValue()
            values = (codice, nome, squadra_reale, valore, valore_asta, ruolo)
            msg = self.controller.salva_valori_giocatore(values)
            InfoMessage(self, msg).get_choice()
            self.clear_fields()
        except ValueError:
            InfoMessage(self, 'Seleziona un giocatore').get_choice()

    # noinspection PyUnusedLocal
    def on_giocatore(self, event):
        """
        on_giocatore(self, event)

        Invoca il metodo del controller per ottenere i valori del giocatore
        selezionato. Tali valori vengono passati a metodo fill_fields

            :param event: object wx.EVT_COMBOBOX
        """
        nome = self.panel.cb_giocatori.GetValue()
        values = self.controller.get_giocatore_values(nome)
        self.fill_fields(*values)

    def fill_fields(self, c, n, sv, v, va, r):
        """
        fill_fields(self, c, n, sv, v, va, r)

        Riempe i corrispondenti widgets con i parametri passati come arg.

        :param c: str
        :param n: str
        :param sv: str
        :param v: str
        :param va: str
        :param r: str
        """
        if va is None:
            va = 0
        self.panel.codice.SetValue(str(c))
        self.panel.nome.SetValue(n)
        self.panel.squadra_reale.SetValue(sv)
        self.panel.valore.SetValue(str(v))
        self.panel.valore_asta.SetValue(str(va))
        self.panel.ruolo.SetValue(r)

    def clear_fields(self):
        """
        clear_fields(self)

        svuota tutti i widgets dai valori ottenuti in precedenza
        """
        self.fill_fields('', '', '', '', '', '')
        self.panel.cb_giocatori.SetValue('')


class PanelEditGiocatore(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelEditGiocatore(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelEditGiocatore, self).__init__(parent)
        self.filtro = wx.TextCtrl(self)
        giocatori = [g.nome for g in parent.controller.get_giocatori()]
        self.cb_giocatori = wx.ComboBox(self, -1, "scegli giocatore...",
                                        choices=giocatori, style=wx.CB_DROPDOWN)
        self.codice = wx.TextCtrl(self)
        self.nome = wx.TextCtrl(self)
        self.squadra_reale = wx.TextCtrl(self)
        self.valore = wx.TextCtrl(self)
        self.valore_asta = wx.TextCtrl(self)
        self.valore_asta.Disable()
        self.ruolo = wx.TextCtrl(self)
        text_sizer = wx.FlexGridSizer(rows=9, cols=2, hgap=8, vgap=8)
        text_sizer.Add(wx.StaticText(self, label="Filtro:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.filtro, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Giocatori:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_giocatori, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Codice:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.codice, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Nome:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.nome, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="squadra reale:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.squadra_reale, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="valore:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.valore, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="valore asta:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.valore_asta, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="ruolo:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.ruolo, 0, wx.EXPAND)
        text_sizer.AddGrowableCol(1)
        # button sizer
        button_sizer = wx.StdDialogButtonSizer()
        self.btn_save = wx.Button(self, wx.ID_SAVE)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.btn_save.SetDefault()
        button_sizer.AddButton(self.btn_save)
        button_sizer.AddButton(self.btn_quit)
        button_sizer.Realize()
        # wrapper sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 12)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')


class ViewStatistiche(wx.Frame):
    """GUI per statistiche giocatore"""
    def __init__(self, parent, title):
        """
        ViewStatistiche(parent, title) -> ViewStatistiche object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewStatistiche, self).__init__(parent=self.parent, title=title,
                                              style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelStatistiche(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((350, 375))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_COMBOBOX, self.on_giocatore, self.panel.cb_giocatori)
        self.Bind(wx.EVT_TEXT, self.on_filtro, self.panel.filtro)

    # noinspection PyUnusedLocal
    def on_filtro(self, event):
        """
        on_filtro(self, event)

        Invoca il metodo giocatori_disponibili del controller e filtra i
        disponibili in base al testo digitato nella combotextctr 'filtro'

        :param event: wx.EVT_TEXT
        """
        prefix = self.panel.filtro.GetValue().upper()
        disponibili = [g.nome
                       for g in self.controller.get_giocatori(prefix=prefix)]
        self.panel.cb_giocatori.Clear()
        self.panel.cb_giocatori.SetValue("scegli giocatore...")
        self.panel.cb_giocatori.AppendItems(disponibili)

    # noinspection PyUnusedLocal
    def on_giocatore(self, event):
        """
        on_giocatore(self, event)

        Seleziona il giocatore per mostrarne le statistiche individuali.
        La tupla di valori ottenuti dal controller viene passata al metodo
        fill_fields

            :param event: object wx.EVT_COMBOBOX
        """
        nome = self.panel.cb_giocatori.GetValue()
        values = self.controller.get_valori_statistici(nome)
        self.fill_fields(*values)

    def fill_fields(self, uv, mv, pr, aff, va):
        """
        fill_fields(self, uv, mv, pr, aff, va)

        Riempe i widgets corrispondenti, con i valori ottenuti dalla callback
        on_giocatore

        :param uv: str
        :param mv: str
        :param pr: str
        :param aff: str
        :param va: str
        """
        self.panel.ultimo_voto.SetValue(str(uv))
        self.panel.media_voto.SetValue(str(mv))
        self.panel.presenze.SetValue(str(pr))
        self.panel.affidabilita.SetValue(str(aff))
        self.panel.valore.SetValue(str(va))

    def clear_fields(self):
        """
        clear_fields(self)

        Pulisce tutti i widgets dai valori precedentemente visualizzati
        """
        self.fill_fields('', '', '', '', '')
        self.panel.cb_giocatori.SetValue('')


class PanelStatistiche(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelStatistiche(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelStatistiche, self).__init__(parent)
        self.filtro = wx.TextCtrl(self)
        giocatori = [g.nome for g in parent.controller.get_giocatori()]
        self.cb_giocatori = wx.ComboBox(self, -1, "scegli giocatore...",
                                        choices=giocatori, style=wx.CB_DROPDOWN)
        self.ultimo_voto = wx.TextCtrl(self)
        self.media_voto = wx.TextCtrl(self)
        self.presenze = wx.TextCtrl(self)
        self.affidabilita = wx.TextCtrl(self)
        self.valore = wx.TextCtrl(self)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        # Layout
        text_sizer = wx.FlexGridSizer(rows=8, cols=2, hgap=8, vgap=8)
        text_sizer.Add(wx.StaticText(self, label="Filtro:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.filtro, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Giocatore:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_giocatori, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="ultimo voto:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.ultimo_voto, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="media voto:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.media_voto, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="presenze:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.presenze, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="affidabilita' (%):"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.affidabilita, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="valore:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.valore, 0, wx.EXPAND)
        # button sizer
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self.btn_quit)
        button_sizer.Realize()
        # wrapper sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 12)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')
