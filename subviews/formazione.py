import wx
from messages import InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewFormazione(wx.Frame):
    """GUI per creazione nuova squadra"""
    def __init__(self, parent, title):
        """
        ViewFormazione(parent, title) -> ViewFormazione object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewFormazione, self).__init__(parent=self.parent,
                                             title=title, style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelFormazione(parent=self)
        self.build()  # Build Layout with sizer, background and size
        self.bind_widgets()  # Bind widgets
        self.parent.show_subframe(self)  # Show and center the frame

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((400, 700))
        self.panel.SetBackgroundColour('Pink')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.panel.btn_salva.Disable()
        self.panel.cb_squadre.Disable()
        self.panel.cb_giornate.Disable()
        self.panel.cb_moduli.Disable()

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.salva_formazione, self.panel.btn_salva)
        self.Bind(wx.EVT_COMBOBOX, self.on_lega, self.panel.cb_leghe)
        self.Bind(wx.EVT_COMBOBOX, self.on_modulo, self.panel.cb_moduli)
        self.Bind(wx.EVT_COMBOBOX, self.on_squadra, self.panel.cb_squadre)
        self.Bind(wx.EVT_COMBOBOX, self.on_giornata, self.panel.cb_giornate)

    # noinspection PyUnusedLocal
    def on_lega(self, event):
        """
        on_lega(self, event)

        Seleziona la lega della quale visualizzare le giornate disponibili.

            :param event: object wx.EVT_COMBOBOX
        """
        lega = self.panel.cb_leghe.GetStringSelection()
        squadre = self.controller.get_squadre_lega(lega)
        self.fill_squadre(squadre)
        giornate = self.controller.get_giornate_calendario(lega)
        if giornate:
            self.fill_giornate(giornate)
        else:
            InfoMessage(self, 'Devi creare il calendario di lega!').get_choice()

    # noinspection PyUnusedLocal
    def on_squadra(self, event):
        """
        on_squadra(self, event)

        Seleziona la squadra della quale visualizzare le formazioni disponibili
        ed eventualmente modificarle, o creare la formazione della giornata
         successiva.

            :param event: object wx.EVT_COMBOBOX
        """
        self.panel.cb_giornate.Enable()
        self.panel.cb_giornate.SetValue('')
        self.clean_combos()

    # noinspection PyUnusedLocal
    def on_giornata(self, event):
        """
        on_giornata(self, event)

        Seleziona la giornata della quale visualizzare la formazione, se
        disponibile, oppure crearla da zero.

            :param event: object wx.EVT_COMBOBOX
        """
        squadra = self.panel.cb_squadre.GetStringSelection()
        lega = self.panel.cb_leghe.GetStringSelection()
        giornata = self.panel.cb_giornate.GetStringSelection()
        rosa = self.controller.get_rosa_squadra(squadra)
        form, msg = self.controller.get_formazione(lega, squadra, giornata)
        if not form:
            InfoMessage(self, msg).get_choice()
        self.fill_giocatori(form, rosa)
        self.panel.cb_moduli.Enable()

    # noinspection PyUnusedLocal
    def on_modulo(self, event):
        """
        on_modulo(self, event)

        Seleziona il modulo con il quale si faranno i controlli e abilita
        il bottone 'Salva'.

            :param event: object wx.EVT_COMBOBOX
        """
        self.panel.btn_salva.Enable()

    def fill_squadre(self, iterable):
        """
        fill_squadre(self, iterable)

        Riempe la combobox squadre con le squadre disponibili per quella lega

            :param iterable: object list
        """
        self.panel.cb_squadre.Clear()
        self.panel.cb_squadre.AppendItems(iterable)
        self.panel.cb_squadre.Enable()

    def fill_giornate(self, iterable):
        """
        fill_giornate(self, iterable)

        Riempe la combobox giornate con le giornate disponibili per quella lega

            :param iterable: object list
        """
        self.panel.cb_giornate.Clear()
        self.panel.cb_giornate.AppendItems(iterable)

    def fill_giocatori(self, iterable, rosa):
        """
        fill_giocatori(self, iterable, rosa)

        Riempe la listbox rosa con i giocatori della rosa della squadra
        selezionata e la listbox della formazione, con la eventuale formazione
        esistente

            :param rosa: object list giocatori
            :param iterable: object list giocatori
        """
        if iterable:
            for n, giocatore in enumerate(iterable):
                combobox = self.get_combobox(index=n + 1)
                combobox.Clear()
                combobox.AppendItems(rosa)
                combobox.SetValue(giocatore)
        else:
            for n in range(1, 22):
                combobox = self.get_combobox(index=n)
                combobox.Clear()
                combobox.AppendItems(rosa)

    def get_combobox(self, index):
        """
        get_combobox(self, index) -> object combobox

        Ritorna la combobox con indice index iterando sui children del panel
        :param index: object int
        :return: object wx.ComboBox
        """
        return [cb for cb in self.panel.GetChildren() if isinstance(
            cb, wx.ComboBox) and cb.GetId() == index][0]

    # noinspection PyUnusedLocal
    def salva_formazione(self, event):
        """
        salva_formazione(self, event)

        Controlla che la formazione rispetti il modulo selezionato e non ci
        siano dei duplicati presenti nei giocatori, poi invoca il metodo del
        controller per il salvataggio della formazione.
        In caso di errori visualizza un Alert.

            :param event: object wx.EVT_BUTTON
        """
        modulo = self.panel.cb_moduli.GetStringSelection()
        cb_giocatori = [cb for cb in self.panel.GetChildren() if isinstance(
            cb, wx.ComboBox) and cb.GetId() > -1]
        giocatori = [cb.GetValue() for cb in cb_giocatori]
        if self.controller.modulo_corretto(giocatori[:11], modulo):
            if self.controller.duplicati_presenti(giocatori):
                InfoMessage(self, 'Duplicati presenti!').get_choice()
            else:
                squadra = self.panel.cb_squadre.GetStringSelection()
                giornata = self.panel.cb_giornate.GetStringSelection()
                msg = self.controller.salva_formazione(squadra, giornata,
                                                       giocatori)
                InfoMessage(self, msg).get_choice()
                self.clean_widgets()
        else:
            InfoMessage(self, 'Errore nel Modulo!').get_choice()

    def clean_widgets(self):
        """
        clean_widgets(self)

        Pulisce tutti i widgets dai valori precedenti
        """
        self.panel.cb_giornate.SetValue('')
        self.panel.cb_squadre.SetValue('')
        self.panel.cb_moduli.SetValue('')
        self.panel.cb_giornate.Disable()
        self.panel.cb_moduli.Disable()
        self.panel.btn_salva.Disable()
        self.clean_combos()

    def clean_combos(self):
        """
        clean_combos(self)

        Pulisce tutte le comboboxes
        """
        cbs = [cb for cb in self.panel.GetChildren() if isinstance(
            cb, wx.ComboBox) and cb.GetId() > -1]
        for cb in cbs:
            cb.Clear()
            cb.SetValue('')


class PanelFormazione(wx.Panel):
    """Contiene tutti i sizers principali e i widgets"""
    def __init__(self, parent):
        """
        PanelFormazione(parent) -> wx.Panel object

            :param parent: object frame
        """

        super(PanelFormazione, self).__init__(parent)
        # Attributes
        try:
            leghe = [l.nome for l in parent.controller.get_leghe()]
            moduli = parent.controller.get_moduli()
        except AttributeError:  # for debug
            leghe = ['FANTALEGA 2014-2015']
            moduli = ['3-4-3']
        rosa = []
        self.cb_leghe = wx.ComboBox(self, -1, "leghe...", choices=leghe,
                                    style=wx.CB_DROPDOWN)
        self.cb_giornate = wx.ComboBox(self, -1, "giornate...", choices=[],
                                       style=wx.CB_DROPDOWN)
        self.cb_squadre = wx.ComboBox(self, -1, "squadra...", choices=[],
                                      style=wx.CB_DROPDOWN)
        self.cb_moduli = wx.ComboBox(self, -1, "moduli...", choices=moduli,
                                     style=wx.CB_DROPDOWN)
        self.btn_salva = wx.Button(self, label='Salva')
        self.btn_quit = wx.Button(self, label='Quit')
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        sizer.Add(self.cb_giornate, 0, wx.EXPAND)
        sizer.Add(self.cb_moduli, 0, wx.EXPAND)
        sizer.Add(wx.StaticText(self, label="titolari:"),
                  0, wx.ALIGN_CENTER_HORIZONTAL)
        for n in range(21):
            string = "titolare %s" if n < 11 else "sostituto %s"
            cb_giocatore = wx.ComboBox(self, n + 1, string % (n + 1),
                                       choices=rosa, style=wx.CB_DROPDOWN)
            sizer.Add(cb_giocatore, 0, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Add(self.btn_salva, 0, wx.EXPAND, 10)
        sizer.Add(self.btn_quit, 0, wx.EXPAND)


class ViewPunteggio(wx.Frame):
    """GUI per creazione nuova squadra"""
    def __init__(self, parent, title):
        # Attribs
        self.parent = parent
        # Layout
        super(ViewPunteggio, self).__init__(parent=self.parent,
                                            title=title, style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelPunteggio(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((300, 650))
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
        self.Bind(wx.EVT_COMBOBOX, self.on_lega, self.panel.cb_leghe)
        self.Bind(wx.EVT_COMBOBOX, self.on_squadra, self.panel.cb_squadre)
        self.Bind(wx.EVT_COMBOBOX, self.on_giornata, self.panel.cb_giornate)
        self.panel.cb_squadre.Disable()
        self.panel.cb_giornate.Disable()

    # noinspection PyUnusedLocal
    def on_lega(self, event):
        """
        on_lega(self, event)

        Seleziona la lega della quale visualizzare le squadre e le giornate.

            :param event: object wx.EVT_COMBOBOX
        """
        lega = self.panel.cb_leghe.GetStringSelection()
        squadre = self.controller.get_squadre_lega(lega)
        self.fill_squadre(squadre)
        self.fill_giornate(self.controller.get_voti_inseriti())

    # noinspection PyUnusedLocal
    def on_squadra(self, event):
        """
        on_squadra(self, event)

        Seleziona la squadra della quale visualizzare le formazioni.

            :param event: object wx.EVT_COMBOBOX
        """
        self.panel.cb_giornate.Enable()
        self.panel.cb_giornate.SetValue('')

    # noinspection PyUnusedLocal
    def on_giornata(self, event):
        """
        on_giornata(self, event)

        Seleziona la giornata della quale visualizzare la formazione ed invoca
        il metodo del controller per ottenere il punteggio complessivo.

            :param event: object wx.EVT_COMBOBOX
        """
        squadra = self.panel.cb_squadre.GetStringSelection()
        lega = self.panel.cb_leghe.GetStringSelection()
        giornata = self.panel.cb_giornate.GetStringSelection()
        form, res, dv, msg = self.controller.get_punteggio(
            lega, squadra, giornata)
        if form:
            self.fill_giocatori(form, res, dv)
        else:
            InfoMessage(self, msg).get_choice()
            self.clean_widgets()

    def fill_squadre(self, iterable):
        """
        fill_squadre(self, iterable)

        Aggiorna la combobox squadre con tutte le squadre legate alla lega
        scelta.

            :param iterable: list
        """
        self.panel.cb_squadre.Clear()
        self.panel.cb_squadre.AppendItems(iterable)
        self.panel.cb_squadre.Enable()

    def fill_giornate(self, iterable):
        """
        fill_giornate(self, iterable)

        Aggiorna la combobox giornate con tutte le giornate della lega.

            :param iterable: list
        """
        self.panel.cb_giornate.Clear()
        self.panel.cb_giornate.AppendItems(iterable)

    def fill_giocatori(self, giocatori, res, dv):
        """
        fill_giocatori(self, giocatori, res, dv)

        Aggiorna la listctrlbox con i nomi dei giocatori ed il relativo
        punteggio, selezionato dal dizionario 'dv'.
        Poi viene settato il punteggio totale della formazione,
        nella Textctrl di competenza

            :param giocatori: list
            :param res: int
            :param dv: dict
        """
        self.panel.lc_pts.DeleteAllItems()
        for n, item in enumerate(giocatori):
            giocatore = item.split(' > ')[0]
            index = self.panel.lc_pts.InsertStringItem(n, giocatore)
            if giocatore in dv:
                self.panel.lc_pts.SetStringItem(index, 1, str(dv[giocatore]))
        self.panel.totale.SetValue(str(res))

    def clean_widgets(self):
        """
        clean_widgets(self)

        Pulisce i widgets dai valori precedenti
        """
        self.panel.cb_giornate.SetValue('')
        self.panel.cb_squadre.SetValue('')
        self.panel.cb_giornate.Disable()
        self.panel.lc_pts.DeleteAllItems()


class PanelPunteggio(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelPunteggio(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelPunteggio, self).__init__(parent)
        # Attributes
        leghe = [l.nome for l in parent.controller.get_leghe()]
        self.cb_leghe = wx.ComboBox(self, -1, "leghe...", choices=leghe,
                                    style=wx.CB_DROPDOWN)
        self.cb_giornate = wx.ComboBox(self, -1, "voti giornate...", choices=[],
                                       style=wx.CB_DROPDOWN)
        self.cb_squadre = wx.ComboBox(self, -1, "squadra...", choices=[],
                                      style=wx.CB_DROPDOWN)
        self.lc_pts = wx.ListCtrl(self, -1, style=wx.LC_REPORT, size=(260, 450))
        self.lc_pts.InsertColumn(1, 'giocatore', wx.LIST_AUTOSIZE, 225)
        self.lc_pts.InsertColumn(2, 'fv', wx.LIST_AUTOSIZE, 35)

        self.totale = wx.TextCtrl(self)
        self.btn_quit = wx.Button(self, label='Quit')
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        sizer.Add(self.cb_giornate, 0, wx.EXPAND)
        sizer.Add(self.lc_pts, 0, wx.EXPAND)
        sizer.Add(wx.StaticText(self, label="totale:"), 0,
                  wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.totale, 0, wx.EXPAND)
        sizer.Add(self.btn_quit, 0, wx.EXPAND)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)