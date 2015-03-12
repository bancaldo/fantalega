import wx
# from messages import ChoiceMessage, InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER \
    | wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewMercati(wx.Frame):
    """GUI per visualizzare lo storico dei mercati"""
    def __init__(self, parent, title):
        """
        ViewMercati(parent, title) -> ViewMercati object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewMercati, self).__init__(parent=self.parent, title=title,
                                          style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelMercati(parent=self)
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

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_COMBOBOX, self.on_squadra, self.panel.cb_squadre)

    # noinspection PyUnusedLocal
    def on_squadra(self, event):
        """
        on_squadra(self, event)

        Invoca il metodo del controller per ottenere le operazioni di mercato
        effettuate da quella squadra

            :param event: object wx.EVT_COMBOBOX
        """
        squadra = self.panel.cb_squadre.GetStringSelection()
        op_rim, op_eff = self.controller.get_operazioni_mercato(squadra)
        self.fill_controls(op_rim, op_eff)

    def fill_controls(self, op_rimanenti, op_effettuate):
        """
        fill_controls(self, op_rimanenti, op_effettuate)

        Setta il valore op_rimanenti nella textctrl di competenza
        Splitta le oerazioni di mercato effettuate, mettendo i giocatori in
        ingresso da una parte e quelli in uscita dall'altra

        :param op_rimanenti: int
        :param op_effettuate: list
        :return:
        """
        self.panel.op_rimanenti.SetLabel('%s' % op_rimanenti)
        self.panel.lb_uscita.Clear()
        self.panel.lb_entrata.Clear()
        if op_effettuate:
            in_uscita = [m.giocatore.nome for m in op_effettuate
                         if m.verso == 'OUT']
            in_entrata = [m.giocatore.nome for m in op_effettuate
                          if m.verso == 'IN']
            self.panel.lb_uscita.AppendItems(in_uscita)
            self.panel.lb_entrata.AppendItems(in_entrata)


class PanelMercati(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelMercati(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelMercati, self).__init__(parent)
        # Attributes
        squadre = [s.nome for s in parent.controller.get_squadre()]
        self.cb_squadre = wx.ComboBox(self, -1, "scegli la squadra...",
                                  choices=squadre, style=wx.CB_DROPDOWN)
        self.lb_uscita = wx.ListBox(self, choices=[], size=(150, 150))
        self.lb_entrata = wx.ListBox(self, choices=[], size=(150, 150))
        self.btn_quit = wx.Button(self, label='Quit')
        self.op_rimanenti = wx.StaticText(self)

        # Layout
        sizer = wx.FlexGridSizer(rows=10, cols=2, hgap=8, vgap=8)
        sizer.Add(wx.StaticText(self, label="squadra:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        sizer.Add(wx.StaticText(self, label="in uscita:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(self, label="in entrata:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.lb_uscita, 0, wx.EXPAND)
        sizer.Add(self.lb_entrata, 0, wx.EXPAND)
        sizer.Add(wx.StaticText(self, label="operazioni rimanenti:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.op_rimanenti, 0, wx.EXPAND)
        sizer.Add(self.btn_quit, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)