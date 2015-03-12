import wx
from messages import ChoiceMessage, InfoMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewNuovaLega(wx.Frame):
    """GUI per creazione nuova Lega"""
    def __init__(self, parent, title):
        """
        ViewNuovaLega(parent, title) -> ViewNuovaLega object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewNuovaLega, self).__init__(parent=self.parent, title=title,
                                            style=STYLE)
        self.controller = self.parent.controller
        self.panel = None
        self.paneledit = None
        self.build()  # Build Layout with sizer, background and size
        self.bind_widgets()  # Bind widgets
        self.parent.show_subframe(self)  # Show and center the frame

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.panel = PanelNuovaLega(parent=self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSize((250, 550))

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.salva_lega, self.panel.btn_salva)

    def clear_fields(self):
        """
        clear_fields(self)

        Pulisce la textctrl dal valore precedente
        """
        self.panel.nome.SetValue('')

    def salva_lega(self, event):
        """
        salva_lega(self, event)

        Salva la lega con il nome inserito associandole le opzioni utente

            :param event: object wx.EVT_BUTTON
        """
        nome_lega = self.panel.nome.GetValue()
        if not nome_lega:
            InfoMessage(self, 'nessun nome inserito').get_choice()
        else:
            objlega = self.controller.nuova_lega(nome_lega)
            InfoMessage(self, 'Nuova Lega %s salvata!' % objlega.nome
                        ).get_choice()
            budget = int(self.panel.budget.GetValue())
            max_mercati = int(self.panel.mercati.GetValue())
            max_portieri = int(self.panel.max_portieri.GetValue())
            max_difensori = int(self.panel.max_difensori.GetValue())
            max_centrocampisti = int(self.panel.max_centrocampisti.GetValue())
            max_attaccanti = int(self.panel.max_attaccanti.GetValue())
            a_r = int(self.panel.a_r.GetValue())
            offset = int(self.panel.offset.GetValue())
            self.controller.salva_opzioni_lega(objlega, budget, max_mercati,
                                               max_portieri, max_difensori,
                                               max_centrocampisti,
                                               max_attaccanti, a_r, offset)
            InfoMessage(self, 'Impostazioni Lega %s salvate!' % objlega.nome
                        ).get_choice()
            self.clear_fields()
            self.parent.check_menus()


class PanelNuovaLega(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelNuovaLega(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelNuovaLega, self).__init__(parent)
        # Attributes
        self.nome = wx.TextCtrl(self)
        self.budget = wx.TextCtrl(self, value='500')
        self.mercati = wx.TextCtrl(self, value='6')
        self.max_portieri = wx.TextCtrl(self, value='3')
        self.max_difensori = wx.TextCtrl(self, value='9')
        self.max_centrocampisti = wx.TextCtrl(self, value='9')
        self.max_attaccanti = wx.TextCtrl(self, value='7')
        self.a_r = wx.TextCtrl(self, value='4')
        self.offset = wx.TextCtrl(self, value='1')
        # Layout
        text_sizer = wx.FlexGridSizer(rows=9, cols=2, hgap=5, vgap=5)

        text_sizer.Add(wx.StaticText(self, label="Nome:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.nome, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Budget:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.budget, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Mercati:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.mercati, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="n. portieri:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.max_portieri, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="n. difensori:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.max_difensori, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="n. ccampisti:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.max_centrocampisti, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="n. attaccanti:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.max_attaccanti, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="andate/ritorno:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.a_r, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="offset giornate:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.offset, 0, wx.EXPAND)
        text_sizer.AddGrowableCol(1)
        button_sizer = wx.StdDialogButtonSizer()
        self.btn_salva = wx.Button(self, wx.ID_SAVE)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.btn_salva.SetDefault()
        button_sizer.AddButton(self.btn_salva)
        button_sizer.AddButton(self.btn_quit)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Realize()
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)


class ViewEditLega(ViewNuovaLega):
    """GUI per creazione nuova Lega"""
    def __init__(self, parent, title):
        """
        ViewEditLega(parent, title) -> ViewEditLega object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewEditLega, self).__init__(parent=self.parent, title=title)
        self.additional_bindings()

    def additional_bindings(self):
        """
        additional_bindings(self)

        Aggiunge il Bind ai widgets non presenti nella classe padre
        """
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_leghe, self.paneledit.cb_leghe)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene i panels e stabilisce le dimensioni
        del subframe. In questo frame ci sono il panel ereditato ed uno
        ulteriore
        """
        self.paneledit = PanelEditLega(parent=self)
        self.panel = PanelNuovaLega(parent=self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.paneledit, 0, wx.EXPAND)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSize((250, 550))

    # noinspection PyUnusedLocal
    def on_combo_leghe(self, event):
        """
        on_combo_leghe(self, event)

        Invoca il metodo del controller per ottenere i valori della lega
        selezionata ed eventualmente modificarli

            :param event: object wx.EVT_COMBOBOX
        """
        nome = self.paneledit.cb_leghe.GetValue()
        lega = self.controller.get_lega_nome(nome)
        option = lega.option
        self.panel.nome.SetValue(lega.nome)
        self.panel.budget.SetValue(str(option.budget))
        self.panel.mercati.SetValue(str(option.max_mercati))
        self.panel.max_portieri.SetValue(str(option.max_portieri))
        self.panel.max_difensori.SetValue(str(option.max_difensori))
        self.panel.max_centrocampisti.SetValue(str(option.max_centrocampisti))
        self.panel.max_attaccanti.SetValue(str(option.max_attaccanti))
        self.panel.a_r.SetValue(str(option.a_r))
        self.panel.offset.SetValue(str(option.offset))

    def clear_fields(self):
        """
        clear_fields(self)

        Pulisce tutti i widgets dai valori visualizzati in precedenza
        """
        for w in [w for w in self.panel.GetChildren()
                  if isinstance(w, wx.TextCtrl)]:
            w.SetValue('')

    # noinspection PyUnusedLocal
    def salva_lega(self, event):
        """
        salva_lega(self, event)

        Invoca il metodo del controller per modificare i valori della lega
        selezionata

            :param event: object wx.EVT_BUTTON
        """
        nome = self.panel.nome.GetValue()
        try:
            bd = int(self.panel.budget.GetValue())
            me = int(self.panel.mercati.GetValue())
            mp = int(self.panel.max_portieri.GetValue())
            md = int(self.panel.max_difensori.GetValue())
            mc = int(self.panel.max_centrocampisti.GetValue())
            ma = int(self.panel.max_attaccanti.GetValue())
            ar = int(self.panel.a_r.GetValue())
            offset = int(self.panel.offset.GetValue())
            leghe = self.controller.modifica_lega(nome, bd, me, mp, md,
                                                  mc, ma, ar, offset)
            self.update_controls(leghe)
            InfoMessage(self, 'Lega %s e opzioni salvate!' % nome).get_choice()
            self.clear_fields()
        except ValueError:
            InfoMessage(self, 'Inserire valori numerici').get_choice()

    def update_controls(self, leghe):
        """
        update_controls(self, leghe)

        Aggiorna le leghe disponibili nella combobox relativa

        :param leghe: list di oggetti db_models.leghe
        """
        self.panel.nome.SetValue('')
        self.paneledit.cb_leghe.Clear()
        self.paneledit.cb_leghe.AppendItems([l.nome for l in leghe])


class PanelEditLega(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelEditLega(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelEditLega, self).__init__(parent)
        # Attributes
        self.leghe = [lega.nome for lega in parent.controller.get_leghe()]
        self.cb_leghe = wx.ComboBox(self, -1, "scegli la lega...",
                                    choices=self.leghe, style=wx.CB_DROPDOWN)
        self.cb_leghe.SetBackgroundColour('Yellow')
        self.cb_leghe.SetLabelText('Leghe...')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)


class ViewDeleteLega(wx.Frame):
    """GUI per creazione nuova Lega"""
    def __init__(self, parent, title):
        """
        ViewDeleteLega(parent, title) -> ViewDeleteLega object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewDeleteLega, self).__init__(parent=self.parent, title=title,
                                             style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelDeleteLega(parent=self)
        self.build()  # Build Layout with sizer, background and size
        self.bind_widgets()  # Bind widgets
        self.parent.show_subframe(self)  # Show and center the frame

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
        self.Bind(wx.EVT_BUTTON, self.elimina_lega, self.panel.btn_delete)

    # noinspection PyUnusedLocal
    def elimina_lega(self, event):
        """
        elimina_lega(self, event)

        Elimina la lega selezionata

            :param event: object wx.EVT_BUTTON
        """
        choice = ChoiceMessage(self, 'Sicuro di voler Eliminare la Lega?')
        if choice.is_yes():
            lega = self.panel.cb_leghe.GetValue()
            leghe_rimanenti = self.controller.elimina_lega(lega)
            self.update_choice_leghe(leghe_rimanenti)
            InfoMessage(self, '%s Eliminata!' % lega).get_choice()
            self.parent.check_menu_lega()
        else:
            choice.Destroy()

    def update_choice_leghe(self, leghe):
        """
        update_choice_leghe(self, leghe)

        Aggiorna le leghe disponibili nella combobox relativa

        :param leghe: list di oggetti db_models.leghe
        """
        self.panel.cb_leghe.Clear()
        self.panel.cb_leghe.AppendItems([l.nome for l in leghe])


class PanelDeleteLega(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelDeleteLega(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelDeleteLega, self).__init__(parent)
        self.leghe = [lega.nome for lega in parent.controller.get_leghe()]
        # Layout
        text_sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=5)
        text_sizer.Add(wx.StaticText(self, label="Leghe:"),
                       0, wx.ALIGN_CENTER_VERTICAL)
        self.cb_leghe = wx.ComboBox(self, -1, choices=self.leghe,
                                    style=wx.CB_DROPDOWN)
        text_sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        self.btn_delete = wx.Button(self, label="Delete")
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.btn_delete.SetDefault()
        text_sizer.Add(self.btn_delete, 0,)
        text_sizer.Add(self.btn_quit, 0,)
        text_sizer.AddGrowableCol(1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')
