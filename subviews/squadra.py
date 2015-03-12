import wx
from messages import ChoiceMessage, InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewNuovaSquadra(wx.Frame):
    """GUI per creazione nuova squadra"""
    def __init__(self, parent, title):
        """
        ViewNuovaSquadra(parent, title) -> ViewNuovaSquadra object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        self.controller = self.parent.controller
        # Layout
        super(ViewNuovaSquadra, self).__init__(parent=self.parent, title=title,
                                               style=STYLE)
        self.panel = PanelNuovaSquadra(parent=self)
        self.paneledit = None
        self.build()  # Build Layout with sizer, background and size
        self.bind_widgets()  # Bind widgets
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((350, 300))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.set_default_values()

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.salva_squadra, self.panel.btn_save)

    def set_default_values(self):
        """
        set_default_values(self)

        setta i valori di default di una squadra: max_mercati e budget
        """
        mercati, budget = self.controller.get_squadra_default_values()
        self.panel.mercati.SetValue('%s' % mercati)
        self.panel.budget.SetValue('%s' % budget)

    # noinspection PyUnusedLocal
    def salva_squadra(self, event):
        """
        salva_squadra(self, event)

        Invoca il metodo del controlle per salvare una squadra.
        Se il checkbox 'Associa Leghe' e' attivo, la squadra viene associata
        alle leghe esistenti

        :param event: wx.EVT_BUTTON
        """
        nome = self.panel.nome.GetValue()
        allenatore = self.panel.allenatore.GetValue()
        mercati = self.panel.mercati.GetValue()
        budget = self.panel.budget.GetValue()
        if self.panel.option.Get3StateValue():
            leghe = self.controller.get_leghe()
        else:
            leghe = []
        msg = self.controller.salva_nuova_squadra(nome, allenatore, budget,
                                                  mercati, leghe)
        self.clear_controls()
        InfoMessage(self, msg).get_choice()
        self.parent.check_menus()

    def clear_controls(self):
        """
        clear_controls(self)

        Pulisce le textctrl dai valori precedentemente visualizzati
        """
        self.panel.nome.SetValue('')
        self.panel.allenatore.SetValue('')


class PanelNuovaSquadra(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelNuovaSquadra(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelNuovaSquadra, self).__init__(parent)
        # Attributes
        self.nome = wx.TextCtrl(self)
        self.allenatore = wx.TextCtrl(self)
        mercati, budget = parent.controller.get_squadra_default_values()
        self.budget = wx.TextCtrl(self, value=str(budget))
        self.mercati = wx.TextCtrl(self, value=str(mercati))
        self.option = wx.CheckBox(self, -1, 'Associa alle leghe esistenti')
        # Layout
        text_sizer = wx.FlexGridSizer(rows=10, cols=2, hgap=8, vgap=8)

        text_sizer.Add(wx.StaticText(self, label="Nome:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.nome, 0, wx.EXPAND)

        text_sizer.Add(wx.StaticText(self, label="Allenatore:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.allenatore, 0, wx.EXPAND)

        text_sizer.Add(wx.StaticText(self, label="budget:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.budget, 0, wx.EXPAND)

        text_sizer.Add(wx.StaticText(self, label="Mercati:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.mercati, 0, wx.EXPAND)
        text_sizer.AddGrowableCol(1)

        cb_sizer = wx.BoxSizer(wx.VERTICAL)
        cb_sizer.Add(self.option, 1)
        # button sizer
        button_sizer = wx.StdDialogButtonSizer()
        self.btn_save = wx.Button(self, wx.ID_SAVE)
        self.btn_save.SetDefault()
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(self.btn_save)
        button_sizer.AddButton(self.btn_quit)
        button_sizer.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(cb_sizer, 1, wx.EXPAND | wx.ALL, 2)
        sizer.Add(button_sizer, 1, wx.ALIGN_CENTER | wx.ALL, 2)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')


class ViewEditSquadra(ViewNuovaSquadra):
    """GUI per modifica Squadra"""
    def __init__(self, parent, title):
        """
        ViewEditSquadra(parent, title) -> ViewEditSquadra object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewEditSquadra, self).__init__(parent=self.parent, title=title)
        self.additional_bindings()

    def additional_bindings(self):
        """
        additional_bindings(self)

        Crea i bind dei widgets aggiuntivi
        """
        self.Bind(wx.EVT_COMBOBOX, self.on_squadra, self.paneledit.cb_squadre)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.paneledit = PanelEditSquadra(parent=self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.paneledit, 0, wx.EXPAND)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSize((350, 300))

    # noinspection PyUnusedLocal
    def salva_squadra(self, event):
        """
        salva_squadra(self, event)

        Salva i valori della squadra selezionata

        :param event: wx.EVT_BUTTON
        """
        try:
            nome = self.panel.nome.GetValue()
            allenatore = self.panel.allenatore.GetValue()
            budget = int(self.panel.budget.GetValue())
            mercati = int(self.panel.mercati.GetValue())
            legata = self.panel.option.Get3StateValue()

        except ValueError:
            InfoMessage(self, 'Seleziona una squadra').get_choice()

        else:
            values = (nome, allenatore, budget, mercati, legata)
            self.controller.update_squadra_values(values)
            msg = 'Modifica a squadra %s salvata!' % nome
            InfoMessage(self, msg).get_choice()
            self.parent.check_menu_squadra()

    # noinspection PyUnusedLocal
    def on_squadra(self, event):
        """
        on_squadra(self, event)

        Invoca il metodo del controller get_squadra_values per visualizzare
        i valori della squadra scelta

        :param event: wx.EVT_COMBOBOX
        """
        nome_squadra = self.paneledit.cb_squadre.GetValue()
        values = self.controller.get_squadra_values(nome_squadra)
        self.fill_fields(*values)
        self.panel.option.Set3StateValue(False)
        if self.controller.get_squadra_nome(nome_squadra).leghe:
            self.panel.option.Disable()
        else:
            self.panel.option.Enable()

    def fill_fields(self, n, a, b, m):
        """
        fill_fields(self, n, a, b, m)

        Riempe i textctrl con i valori corrispondenti agli attributi di squadra

        :param n: str nome squadra
        :param a: str nome allenatore
        :param b: str budget
        :param m: str max mercati
        """
        self.panel.nome.SetValue(n)
        self.panel.allenatore.SetValue(a)
        self.panel.budget.SetValue(str(b))
        self.panel.mercati.SetValue(str(m))


class PanelEditSquadra(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelEditSquadra(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelEditSquadra, self).__init__(parent)
        self.squadre = [s.nome for s in parent.controller.get_squadre()]
        self.cb_squadre = wx.ComboBox(self, -1, "scegli la squadra...",
                                      choices=self.squadre,
                                      style=wx.CB_DROPDOWN)
        self.cb_squadre.SetBackgroundColour('Yellow')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)


class ViewEliminaSquadra(wx.Frame):
    """GUI per Eliminazione Squadra"""
    def __init__(self, parent, title):
        """
        ViewEliminaSquadra(parent, title) -> ViewEliminaSquadra object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewEliminaSquadra, self).__init__(parent=self.parent,
                                                 title=title, style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelEliminaSquadra(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((250, 150))
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
        self.Bind(wx.EVT_BUTTON, self.elimina_squadra, self.panel.btn_delete)

    # noinspection PyUnusedLocal
    def elimina_squadra(self, event):
        """
        elimina_squadra(self, event)

        Invoca il metodo elimina_squadra del controller, per eliminare la
        squadra selezionata

        :param event: wx.EVT_BUTTON
        """
        choice = ChoiceMessage(self, 'Sicuro di voler Eliminare la Squadra?')
        if choice.is_yes():
            squadra = self.panel.cb_squadre.GetValue()
            sq_rimanenti = self.controller.elimina_squadra(squadra)
            self.update_choice_squadre(sq_rimanenti)
            InfoMessage(self, '%s Eliminata!' % squadra).get_choice()
            self.parent.check_menu_squadra()
        else:
            choice.Destroy()

    def update_choice_squadre(self, squadre):
        """
        update_choice_squadre(self, squadre)

        Aggiorna la combobox squadre con la lista passata come argomento

        :param squadre: list
        """
        self.panel.cb_squadre.Clear()
        self.panel.cb_squadre.AppendItems([sq.nome for sq in squadre])


class PanelEliminaSquadra(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelEliminaSquadra(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelEliminaSquadra, self).__init__(parent)
        self.squadre = [sq.nome for sq in parent.controller.get_squadre()]
        # Layout
        text_sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=5)

        text_sizer.Add(wx.StaticText(self, label="Squadre:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        self.cb_squadre = wx.ComboBox(self, -1, choices=self.squadre,
                                      style=wx.CB_DROPDOWN)
        text_sizer.Add(self.cb_squadre, 0, wx.EXPAND)
        self.btn_delete = wx.Button(self, label="Delete")
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.btn_delete.SetDefault()
        text_sizer.Add(self.btn_delete, 0,)
        text_sizer.Add(self.btn_quit, 0,)
        text_sizer.AddGrowableCol(1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)


class ViewEditRosa(wx.Frame):
    def __init__(self, parent, title):
        """
        ViewEditRosa(parent, title) -> ViewEditRosa object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewEditRosa, self).__init__(parent=parent, title=title,
                                           style=STYLE)
        self.controller = parent.controller
        self.panel = PanelEditRosa(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.panel.filtro.Disable()
        self.SetSize((550, 750))

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_TEXT, self.on_filtro, self.panel.filtro)
        self.Bind(wx.EVT_COMBOBOX, self.on_squadra, self.panel.cb_squadre)
        self.Bind(wx.EVT_LISTBOX, self.on_giocatore, self.panel.lb_rosa)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.cedi, self.panel.btn_cedi)
        self.Bind(wx.EVT_BUTTON, self.acquista, self.panel.btn_acquista)

    # noinspection PyUnusedLocal
    def on_squadra(self, event):
        """
        on_squadra(self, event)

        Invoca i metod get_rosa_squadra e liberi, del controller e
        popola i widgets di competenza

        :param event: wx.EVT_COMBOBOX
        """
        nome_squadra = self.panel.cb_squadre.GetStringSelection()
        rosa = self.parent.controller.get_rosa_squadra(nome_squadra)
        self.fill_rosa(rosa)
        disponibili = self.parent.controller.giocatori_disponibili()
        self.fill_disponibili(disponibili)

    def fill_rosa(self, iterable):
        """
        fill_rosa(self, iterable)

        popola la listbox 'rosa' con i giocatori dell'argomento iterable

        :param iterable: list di giocatori presenti in rosa
        """
        self.panel.lb_rosa.Clear()
        self.panel.lb_rosa.AppendItems(iterable)

    def fill_disponibili(self, iterable):
        """
        fill_disponibili(self, iterable)

        popola la listbox 'disponibili' con i giocatori dell'argomento iterable

        :param iterable: list di giocatori disponibili
        """
        self.panel.filtro.Enable()
        self.panel.lb_disponibili.Clear()
        self.panel.lb_disponibili.AppendItems(iterable)

    # noinspection PyUnusedLocal
    def on_giocatore(self, event):
        """
        on_giocatore(self, event)

        Seleziona il giocatore che puo' essere ceduto
        e setta il ruolo come filtro per i disponibili

        :param event: wx.EVT_COMBOBOX
        """
        try:
            nome, ruolo = self.panel.lb_rosa.GetStringSelection().split(' > ')
            self.controller.set_ruolo(ruolo)
            prefix = self.panel.filtro.GetValue()
            self.fill_disponibili(self.controller.giocatori_disponibili(
                ruolo, prefix))
        except ValueError:
            pass

    # noinspection PyUnusedLocal
    def on_filtro(self, event):
        """
        on_filtro(self, event)

        Invoca il metodo giocatori_disponibili del controller e filtra i
        disponibili in base al testo digitato nella textctr 'filtro'
        e in base al ruolo

        :param event: wx.EVT_TEXT
        """
        ruolo = self.controller.get_ruolo()
        prefix = self.panel.filtro.GetValue()
        self.fill_disponibili(self.controller.giocatori_disponibili(
            ruolo, prefix))

    # noinspection PyUnusedLocal
    def cedi(self, event):
        """
        cedi(self, event)

        Invoca il metodo cedi_giocatore del controller per eliminare il
        giocatore dalla rosa

        :param event: wx.EVT_BUTTON
        """
        da_cedere = self.panel.lb_rosa.GetStringSelection()
        if da_cedere:
            nome, ruolo = da_cedere.split(' > ')
            msg = 'Sicuro di voler eliminare %s' % nome
            if ChoiceMessage(self, msg).is_yes():
                restanti = self.controller.cedi_giocatore(nome.strip().upper())
                disp = self.controller.giocatori_disponibili(
                    ruolo=ruolo.strip().lower())
                self.panel.filtro.SetValue('')
                self.fill_rosa(restanti)
                self.fill_disponibili(disp)
        else:
            InfoMessage(self, 'nessun giocatore selezionato').get_choice()

    # noinspection PyUnusedLocal
    def acquista(self, event):
        """
        acquista(self, event)

        Invoca il metodo rosa_acquista_giocatore del controller per acquistare
        il giocatore scelto dai disponibili. Se il limite di giocatori in rosa
        viene superato, si ottiene un Alert.

        :param event: wx.EVT_BUTTON
        """
        da_acquistare = self.panel.lb_disponibili.GetStringSelection()
        if da_acquistare:
            nome, ruolo = da_acquistare.split(' > ')
            msg = 'Sicuro di voler acuistare %s' % nome
            if ChoiceMessage(self, msg).is_yes():
                squadra = self.panel.cb_squadre.GetStringSelection()
                if not self.controller.break_limits(squadra):
                    nuova_rosa = self.controller.rosa_acquista_giocatore(
                        nome.strip().lower(), squadra.strip())
                    self.fill_rosa(nuova_rosa)
                    disp = self.controller.giocatori_disponibili(
                        ruolo.strip().lower())
                    self.fill_disponibili(disp)
                    self.panel.filtro.SetValue('')
                else:
                    InfoMessage(self, 'limite rosa superato').get_choice()
        else:
            InfoMessage(self, 'nessun giocatore selezionato').get_choice()


class PanelEditRosa(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelEditRosa(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelEditRosa, self).__init__(parent=parent)
        self.parent = parent
        self.squadre = [sq.nome for sq in self.parent.controller.get_squadre()]
        self.SetBackgroundColour('Pink')
        self.filtro = wx.TextCtrl(self)
        self.cb_squadre = wx.ComboBox(self, -1, choices=self.squadre,
                                      style=wx.CB_DROPDOWN)
        self.lb_rosa = wx.ListBox(self, choices=[], size=(250, 500))
        self.lb_disponibili = wx.ListBox(self, choices=[], size=(250, 500))
        self.btn_cedi = wx.Button(self, label='Cessione')
        self.btn_acquista = wx.Button(self, label='Acquisto')
        self.btn_quit = wx.Button(self, label='Quit')

        sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=5)

        sizer.Add(wx.StaticText(self, label="Squadre disponibili:"),
                  1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(wx.StaticText(self, label="filtro disponibili:"),
                  1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.cb_squadre, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.filtro, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(wx.StaticText(self, label="Rosa squadra"),
                  1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(wx.StaticText(self, label="Giocatori disponibili"),
                  1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.lb_rosa, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.lb_disponibili, 1,
                  wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.btn_cedi, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.btn_acquista, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(self.btn_quit, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(sizer)