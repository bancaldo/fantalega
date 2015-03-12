__author__ = 'banchellia'

import wx
import sys


class ViewClassifica(wx.Frame):
    """GUI per classifica"""
    def __init__(self, parent, title):
        """
        ViewClassifica(parent, title) -> ViewClassifica object

            :param parent: object frame Core
            :param title: object str
        """
        self.parent = parent
        super(ViewClassifica, self).__init__(parent=self.parent, title=title)
        self.controller = self.parent.controller
        self.panel = PanelClassifica(parent=self)
        self.build()
        self.bind_widgets()
        self.parent.show_subframe(self)

    def build(self):
        """
        build(self)
        Crea il sizer che contiene il panel e stabilisce le dimensioni
        del subframe
        """
        self.SetSize((800, 400))
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

    # noinspection PyUnusedLocal
    def on_lega(self, event):
        """
        on_lega(self, event)
        Seleziona la lega della quale visualizzare la classifica.

            :param event: object wx.EVT_COMBOBOX
        """
        lega = self.panel.cb_leghe.GetStringSelection()
        values = self.controller.get_classifica(lega)
        self.fill_controls(values)

    def fill_controls(self, values):
        """
        fill_controls(self, values)
        Riempie i vari campi della listctrlbox con i dati delle squadre.

            :param values: list [(nome, pts, v, n, p, gf, gs, dr, pr), ...]
        """
        for col, item in enumerate(values):
            index = self.panel.lc_pts.InsertStringItem(sys.maxint, item[0])
            for n in range(1, len(item)):
                self.panel.lc_pts.SetStringItem(index, n, str(item[n]))


class PanelClassifica(wx.Panel):
    """Contiene i sizers principali e tutti i widgets"""
    def __init__(self, parent):
        """
        PanelClassifica(parent) -> wx.Panel object

            :param parent: object frame
        """
        super(PanelClassifica, self).__init__(parent)
        # Attributes
        leghe = [l.nome for l in parent.controller.get_leghe()]
        self.cb_leghe = wx.ComboBox(self, -1, "leghe disponibili...",
                                  choices=leghe, style=wx.CB_DROPDOWN)
        self.lc_pts = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL)
        self.lc_pts.InsertColumn(1, 'squadra', wx.LIST_AUTOSIZE, 175)
        self.lc_pts.InsertColumn(2, 'pts', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(3, 'V', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(4, 'N', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(5, 'P', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(6, 'GF', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(7, 'GS', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(8, 'DR', wx.LIST_AUTOSIZE, 65)
        self.lc_pts.InsertColumn(9, 'tot', wx.LIST_AUTOSIZE, 100)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb_leghe, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.lc_pts, 1, wx.EXPAND | wx.ALL, 20)
        sizer.Add(self.btn_quit, 0, wx.CENTRE)
        self.SetSizer(sizer)
        self.SetBackgroundColour('Pink')