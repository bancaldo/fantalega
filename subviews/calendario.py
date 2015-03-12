import wx
from messages import ProgressBar, InfoMessage, ChoiceMessage


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


class ViewCalendario(wx.Frame):
    """
    SubFrame Calendario dell'applicazione FantaLega
    Da qui gestisco Il calendario.
    """
    def __init__(self, parent, title):
        """
        ViewCalendario(parent, title) -> ViewCalendario object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        self.controller = self.parent.controller
        super(ViewCalendario, self).__init__(parent=self.parent, title=title,
                                             style=STYLE)
        self.panel = PanelCalendario(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((450, 600))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe,
                  self.panel.btn_cancel)
        self.Bind(wx.EVT_BUTTON, self.calcola, self.panel.btn_calcola)
        self.Bind(wx.EVT_COMBOBOX, self.on_lega, self.panel.cb_leghe)
        self.Bind(wx.EVT_COMBOBOX, self.on_giornata, self.panel.cb_giornate)

    # noinspection PyUnusedLocal
    def calcola(self, event):
        """
        calcola(self, event)

        Calcola i punteggi della giornata selezionata se tutte le formazioni
        per quella giornata sono state inserite, o restituisce un Alert.

            :param event: object wx.EVT_BUTTON
        """
        partite = [(self.panel.calendario.GetItem(itemId=row, col=2).GetText(),
                    self.panel.calendario.GetItem(itemId=row, col=3).GetText())
                   for row in range(self.panel.calendario.GetItemCount())]
        giornata = self.panel.cb_giornate.GetStringSelection()
        lega = self.panel.cb_leghe.GetStringSelection()
        if self.controller.tutte_formazioni_inserite(lega, giornata):
            punteggi = self.controller.calcola_punteggi(lega, partite, giornata)
            self.fill_punteggi(punteggi)
        else:
            msg = 'Non tutte le formazioni sono state inserite'
            InfoMessage(self, msg).get_choice()

    # noinspection PyUnusedLocal
    def on_lega(self, event):
        """
        on_lega(self, event)

        Seleziona la lega della quale visualizzare il calendario.

            :param event: object wx.EVT_COMBOBOX
        """
        lega = self.panel.cb_leghe.GetStringSelection()
        gg = self.controller.get_giornate_calendario(lega)
        self.fill_giornate(['tutte'] + gg)

    # noinspection PyUnusedLocal
    def on_giornata(self, event):
        """
        on_giornata(self, event)

        Seleziona la giornata di lega della quale visualizzare le partite.

            :param event: object wx.EVT_COMBOBOX
        """
        nome_lega = self.panel.cb_leghe.GetStringSelection()
        giornata = self.panel.cb_giornate.GetStringSelection()
        if giornata.lower() == 'tutte':
            partite = self.controller.get_tutte_partite(nome_lega)
            self.panel.btn_calcola.Disable()
        else:
            partite = self.controller.get_partite_per_giornata(
                nome_lega, giornata)
            self.panel.btn_calcola.Enable()
        self.fill_fields(partite)

    def fill_giornate(self, iterable):
        """
        fill_giornate(self, iterable)

        Aggiorna la combobox giornate con tutte le giornate del calendario,
        in modo da poter selezionare una giornata specifica.

            :param iterable: lista di str giornate ['tutte', '1', '2', ...]
        """
        self.panel.cb_giornate.Clear()
        self.panel.cb_giornate.AppendItems(iterable)

    def fill_fields(self, partite):
        """
        fill_fields(self, partite)

        Riempie i vari campi della listctrlbox con i dati delle partite.

            :param partite: lista di oggetti partite
        """
        self.panel.calendario.DeleteAllItems()
        for partita in partite:
            giornata = unicode(partita.giornata)
            row = self.panel.calendario.InsertStringItem(0, giornata)
            self.panel.calendario.SetStringItem(row, 1, str(partita.id))
            self.panel.calendario.SetStringItem(row, 2, partita.casa.nome)
            self.panel.calendario.SetStringItem(row, 3, partita.fuori.nome)
            self.panel.calendario.SetStringItem(row, 4, str(partita.gol_casa))
            self.panel.calendario.SetStringItem(row, 5, str(partita.gol_fuori))

    def fill_punteggi(self, punteggi):
        """
        fill_punteggi(self, punteggi)

        Riempie i campi punteggio della listctrlbox con i punteggi calcolati

            :param punteggi: lista di str punteggi
        """
        for index, punteggio in enumerate(punteggi):
            self.panel.calendario.SetStringItem(index, 4, str(punteggio[2][0]))
            self.panel.calendario.SetStringItem(index, 5, str(punteggio[2][1]))


class PanelCalendario(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelCalendario(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelCalendario, self).__init__(parent)
        # Attributes
        leghe = [l.nome for l in parent.controller.get_leghe()]
        self.cb_leghe = wx.ComboBox(self, -1, "leghe attive...", choices=leghe,
                                    style=wx.CB_DROPDOWN)
        self.cb_giornate = wx.ComboBox(self, -1, "giornate...", choices=[],
                                       style=wx.CB_DROPDOWN)
        self.calendario = wx.ListCtrl(self, wx.NewId(), size=(400, 400),
                style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.calendario.Show(True)
        self.calendario.InsertColumn(0, "gg", wx.LIST_AUTOSIZE, 30)
        self.calendario.InsertColumn(1, "n", wx.LIST_FORMAT_CENTER, 30)
        self.calendario.InsertColumn(2, "casa", wx.LIST_AUTOSIZE, 130)
        self.calendario.InsertColumn(3, "fuori", wx.LIST_FORMAT_CENTER, 130)
        self.calendario.InsertColumn(4, "gc", wx.LIST_FORMAT_CENTER, 30)
        self.calendario.InsertColumn(5, "gf", wx.LIST_FORMAT_CENTER, 30)

        self.btn_calcola = wx.Button(self, label='Calcola Punteggio')
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        self.btn_calcola.Disable()
        # Layout
        text_sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=8, vgap=8)
        text_sizer.Add(wx.StaticText(self, label="Lega:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="giornata:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_giornate, 0, wx.EXPAND)
        # wrapper sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.calendario, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_calcola, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')


class ViewCreaCalendario(wx.Frame):
    """GUI per consultazione Calendario"""
    def __init__(self, parent, title):
        """
        ViewCreaCalendario(parent, title) -> ViewCreaCalendario object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewCreaCalendario, self).__init__(parent=self.parent,
                                                 title=title, style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelCreaCalendario(parent=self)
        self.lega = None
        self.partite = []

        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((300, 200))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.panel.btn_crea.Disable()
        self.panel.btn_delete.Disable()

    def bind_widgets(self):
        """
        bind_widgets(self)

        Crea tutti i bind dei widgets contenuti nel panel, con le
        corrispondenti callbacks
        """
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe,
                  self.panel.btn_cancel)
        self.Bind(wx.EVT_BUTTON, self.delete_calendario, self.panel.btn_delete)
        self.Bind(wx.EVT_BUTTON, self.crea_calendario, self.panel.btn_crea)
        self.Bind(wx.EVT_COMBOBOX, self.on_lega, self.panel.cb_leghe)

    # noinspection PyUnusedLocal
    def on_lega(self, event):
        """
        on_lega(self, event)

        Seleziona la lega per la quale creare il calendario.
        Se il calendario esiste gia', viene abilitato il bottone 'Elimina',
        se non esiste viene abilitato il bottone 'Crea'

            :param event: object wx.EVT_COMBOBOX
        """
        self.lega = self.panel.cb_leghe.GetStringSelection()
        self.partite = self.controller.get_tutte_partite(self.lega)
        if self.partite:
            self.panel.btn_delete.Enable()
        else:
            self.panel.btn_crea.Enable()

    # noinspection PyUnusedLocal
    def delete_calendario(self, event):
        """
        delete_calendario(self, event)

        Invoca il metodo del controller per la cancellazione del calendario
        Poi abilita il bottone 'Crea' e disabilita il bottone 'Elimina'

            :param event: object wx.EVT_BUTTON
        """
        msg = 'Calendario esistente, cancello?'
        if ChoiceMessage(self, msg).is_yes():
            max_a = len(self.partite)
            self.Disable()
            pba = ProgressBar(parent=self, title='Cancellazione calendario...',
                              maximum=max_a)
            self.controller.cancella_calendario(self.partite, pba)
            pba.Destroy()
            self.Enable()
            self.panel.btn_crea.Enable()
            self.panel.btn_delete.Disable()

    # noinspection PyUnusedLocal
    def crea_calendario(self, event):
        """
        crea_calendario(self, event)

        Invoca il metodo del controller per la creazione del calendario
        seguendo la formula:
        (n.squadre - 1) * n.squadre / 2 * n andata e ritorno
        Poi abilita il bottone 'Elimina' e disabilita il bottone 'Crea'

            :param event: object wx.EVT_BUTTON
        """
        max_b = (self.controller.quante_squadre_per_lega(
            self.lega) - 1) * 4 * 5
        self.Disable()
        pbb = ProgressBar(parent=self, title='Crazione nuovo calendario...',
                          maximum=max_b)
        self.controller.crea_calendario(self.lega, pbb)
        pbb.Destroy()
        self.Enable()
        self.panel.btn_delete.Enable()
        self.panel.btn_crea.Disable()


class PanelCreaCalendario(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelCreaCalendario(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelCreaCalendario, self).__init__(parent)
        # Attributes
        leghe = [l.nome for l in parent.controller.get_leghe()]
        self.cb_leghe = wx.ComboBox(self, -1, "leghe attive...", choices=leghe,
                                    style=wx.CB_DROPDOWN)
        self.btn_crea = wx.Button(self, label='Crea nuovo calendario')
        self.btn_delete = wx.Button(self, label='Elimina calendario')
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Lega:"),
                  0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.cb_leghe, 0, wx.EXPAND)
        sizer.Add(self.btn_delete, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_crea, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')
