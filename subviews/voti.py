import wx
import os
import platform
from messages import ProgressBar


STYLE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN


if platform.system() == 'Linux':
    IMPORT_PATH = r'/giornate/'
else:
    IMPORT_PATH = r'\\giornate\\'


class ViewImportVoti(wx.Frame):
    """GUI per importazione Voti"""
    def __init__(self, parent, title):
        """
        ViewImportVoti(parent, title) -> ViewImportVoti object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewImportVoti, self).__init__(parent=self.parent, title=title,
                                             style=STYLE)
        self.controller = self.parent.controller
        self.panel = PanelImportVoti(parent=self)
        self.pb = None
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)

        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((250, 175))
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
        self.Bind(wx.EVT_BUTTON, self.on_import, self.panel.btn_import)

    # noinspection PyUnusedLocal
    def on_import(self, event):
        """
        on_import(self, event)

        Invoca il metodo importa_voti del controller per importare i voti e
        crea una ProgressBar che ne visualizzi l'avanzamento

        :param event: wx.EVT_BUTTON
        """
        browser = FileBrowser(parent=self)
        path = browser.get_file()
        with open(path) as txt_file:
            max_limit = len(txt_file.readlines())
        if path:
            self.pb = ProgressBar(parent=None, maximum=max_limit)
            self.controller.importa_voti(path, self.pb)
            self.refresh()
        self.parent.check_menu_giocatore()
        self.parent.check_menu_lega()
        if self.controller.get_leghe():
            self.parent.check_menu_squadra()

    def refresh(self):
        """
        refresh(self)

        Esegue un refresh dei widgets
        """
        self.panel.cb_giornate.Clear()
        giornate = self.controller.get_voti_inseriti()
        self.panel.cb_giornate.AppendItems(giornate)
        ultima = self.controller.ultima_giornata_importata()
        self.panel.ultima_giornata.SetValue(str(ultima))


class PanelImportVoti(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelImportVoti(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelImportVoti, self).__init__(parent)
        giornate = parent.controller.get_voti_inseriti()
        ultima = parent.controller.ultima_giornata_importata()
        self.cb_giornate = wx.ComboBox(self, -1, "giornate importate...",
                                       choices=giornate, style=wx.CB_DROPDOWN)
        self.ultima_giornata = wx.TextCtrl(self, value='%s' % ultima)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.btn_import = wx.Button(self, label='Importa voti')
        # Layout
        text_sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=8, vgap=8)
        text_sizer.Add(wx.StaticText(self, label="Giornate:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.cb_giornate, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="ultima giornata:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        text_sizer.Add(self.ultima_giornata, 0, wx.EXPAND)
        # wrapper sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_import, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_quit, 0, wx.EXPAND | wx.ALL, 5)
        self.SetBackgroundColour('Pink')
        self.SetSizer(sizer)


class FileBrowser(wx.FileDialog):
    """Class for file browser"""
    def __init__(self, parent):
        wildcard = "File Voti (*.txt)|*.txt|" "Tutti i files (*.*)|*.*"
        super(FileBrowser, self).__init__(parent=parent, message='',
                                          defaultDir=os.getcwd() + IMPORT_PATH,
                                          wildcard=wildcard, style=wx.OPEN)

    def get_file(self):
        """
        get_file(self) -> str path

        Ritorna il path del file selezionato per l'apertura

        :return: str
        """
        return self.GetPath() if self.ShowModal() == wx.ID_OK else None