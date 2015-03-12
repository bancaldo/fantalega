"""modulo View dell'applicazione Fantalega"""

import platform
import wx
from subviews.squadra import ViewNuovaSquadra, ViewEditSquadra
from subviews.squadra import ViewEditRosa, ViewEliminaSquadra
from subviews.giocatore import ViewEditGiocatore, ViewStatistiche
from subviews.voti import ViewImportVoti
from subviews.calendario import ViewCalendario, ViewCreaCalendario
from subviews.formazione import ViewFormazione, ViewPunteggio
from subviews.lega import ViewNuovaLega, ViewEditLega, ViewDeleteLega
from subviews.asta import ViewAsta
from subviews.classifica import ViewClassifica
from subviews.mercati import ViewMercati
from subviews.messages import RulesFrame, InfoFrame, HelpFrame, InfoMessage


IMGPATH = 'images/' if platform.system() == 'Linux' else 'images\\'


class Core(wx.Frame):
    """
    Core wxframe per FantaLega
    Da Qui gestisco tutta la App
    """
    def __init__(self, parent, controller, title):
        """
        Core(None parent, String title) -> Core frame

        Costruttore Core principale, eredita da wx.Frame.

        Args (object type):
            parent (None) Core e' un frame di primo livello
            controller (ControllerCore)
            title (String)
        """
        super(Core, self).__init__(parent=parent, title=title)
        self.controller = controller
        self.statusbar = self.CreateStatusBar()
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('Pink')
        self._create_widgets()
        self._bind_widgets()
        self.show()
        self.check_menus()

    def _create_widgets(self):
        """
        _create_widgets(self)

        Crea tutti i widgets
        """
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        # Menu Lega
        menu_lega = wx.Menu()
        self.menubar.Append(menu_lega, "Leghe")
        self.menu_nuova_lega = menu_lega.Append(-1, "Nuova Lega",
                        "Crea una nuova lega")
        self.menu_edit_lega = menu_lega.Append(-1, "Edit Lega",
                        "Modifica una lega esistente")
        self.menu_delete_lega = menu_lega.Append(-1, "Elimina Lega",
                        "Elimina una lega esistente")
        menu_lega.AppendSeparator()
        self.menu_asta = menu_lega.Append(-1, "Inizia Asta",
                        "Gestisce un'asta tra fanta-allenatori")
        menu_lega.AppendSeparator()
        self.menu_classifica = menu_lega.Append(-1, "Classifica",
                        "Visualizza la classifica di una lega")
        menu_lega.AppendSeparator()
        self.menu_esci = menu_lega.Append(-1, "Esci",
                        "Esce da FantaLega manager")
        # Menu Squadra
        self.menu_squadra = wx.Menu()
        self.menubar.Append(self.menu_squadra, "Squadre")
        self.menu_nuova_squadra = self.menu_squadra.Append(-1,
                        "Nuova Squadra",
                        "Crea una squadra e la associa alle leghe esistenti")
        self.menu_edit_squadra = self.menu_squadra.Append(-1,
                        "Modifica Squadra",
                        "Modifica i dati di una squadra esistente")
        self.menu_rosa = self.menu_squadra.Append(-1, "Rosa Squadra",
                        "Modifica la rosa di una squadra esistente")
        self.menu_mercato = self.menu_squadra.Append(-1, "Mercato Squadra",
                        "Visualizza le operazioni di mercato di una squadra")
        self.menu_squadra.AppendSeparator()
        self.menu_elimina_squadra = self.menu_squadra.Append(
            -1, "Elimina Squadra", "Elimina una squadra esistente")
        # Menu Giocatore
        menu_giocatore = wx.Menu()
        self.menubar.Append(menu_giocatore, "Giocatori")
        self.menu_modifica_giocatore = menu_giocatore.Append(-1,
                "Modifica Giocatore", "Modifica i dati di un giocatore")
        menu_giocatore.AppendSeparator()
        self.menu_statistiche = menu_giocatore.Append(-1,
                "Statistiche", "Visualizza le statistiche di un giocatore")
        # Menu Tools
        menu_tools = wx.Menu()
        self.menubar.Append(menu_tools, "Voti")
        self.menu_importa_voti = menu_tools.Append(-1, "Importa voti",
                "Importa i voti di giornata download \
                 da www.bancaldo.wordpress.com")
        # Menu Calendario
        menu_calendario = wx.Menu()
        self.menubar.Append(menu_calendario, "Calendario")
        self.menu_crea_calendario = menu_calendario.Append(-1,
                        "Crea Calendario", "Crea un calendario da zero")
        self.menu_vedi_calendario = menu_calendario.Append(-1,
                        "Risultati",
                        "Naviga attraverso il calendario creato ad inizio lega")
        # Menu Formazioni
        menu_formazioni = wx.Menu()
        self.menubar.Append(menu_formazioni, "Formazioni")
        self.menu_edit_formazione = menu_formazioni.Append(-1,
                "Edit Formazione", "Inserisce o modifica una formazione")
        menu_formazioni.AppendSeparator()
        self.menu_punteggio = menu_formazioni.Append(-1, "Vedi Punteggio",
                "Visualizza il punteggio di giornata di una formazione")
        # Menu info
        menu_info = wx.Menu()
        self.menubar.Append(menu_info, "info")
        self.menu_guida = menu_info.Append(-1,
                "Guida", "una breve guida passo passo")
        self.menu_regolamento = menu_info.Append(-1,
                "Regolamento", "Regolamento fantalega")
        menu_info.AppendSeparator()
        self.menu_about = menu_info.Append(-1,
                "about...", "Informazioni sul programma")

        img = wx.Image('{}Fantacalcio.bmp'.format(IMGPATH), wx.BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img))
        # ridimensiono il frame sulle dimensioni della figura
        # aggiungendo l'altezza della self.menubar e della statusbar
        self.SetSize((sb.GetSize().x, sb.GetSize().y +
                      self.statusbar.GetSize().y * 2))

    def _bind_widgets(self):
        """
        _bind_widgets(self)

        Crea i Bind con tutti i widgets utilizzati
        """
        self.Bind(wx.EVT_MENU, self.nuova_squadra, self.menu_nuova_squadra)
        self.Bind(wx.EVT_MENU, self.nuova_lega, self.menu_nuova_lega)
        self.Bind(wx.EVT_MENU, self.edit_lega, self.menu_edit_lega)
        self.Bind(wx.EVT_MENU, self.delete_lega, self.menu_delete_lega)
        self.Bind(wx.EVT_MENU, self.gestisci_asta, self.menu_asta)
        self.Bind(wx.EVT_MENU, self.classifica, self.menu_classifica)
        self.Bind(wx.EVT_MENU, self.quit, self.menu_esci)
        self.Bind(wx.EVT_MENU, self.edit_squadra, self.menu_edit_squadra)
        self.Bind(wx.EVT_MENU, self.elimina_squadra, self.menu_elimina_squadra)
        self.Bind(wx.EVT_MENU, self.edit_rosa, self.menu_rosa)
        self.Bind(wx.EVT_MENU, self.mercati, self.menu_mercato)
        self.Bind(wx.EVT_MENU, self.edit_giocatore,
                  self.menu_modifica_giocatore)
        self.Bind(wx.EVT_MENU, self.statistiche, self.menu_statistiche)
        self.Bind(wx.EVT_MENU, self.importa_voti, self.menu_importa_voti)
        self.Bind(wx.EVT_MENU, self.vedi_calendario, self.menu_vedi_calendario)
        self.Bind(wx.EVT_MENU, self.crea_calendario, self.menu_crea_calendario)
        self.Bind(wx.EVT_MENU, self.edit_formazione, self.menu_edit_formazione)
        self.Bind(wx.EVT_MENU, self.vedi_punteggio, self.menu_punteggio)
        self.Bind(wx.EVT_MENU, self.regolamento, self.menu_regolamento)
        self.Bind(wx.EVT_MENU, self.about, self.menu_about)
        self.Bind(wx.EVT_MENU, self.guida, self.menu_guida)

    def show(self):
        """
        show(self)

        Centra e mostra la window principale
        """
        self.Centre()
        self.Show()

    def abilita_tutti_menu(self, enable=True):
        """
        abilita_tutti_menu(self, enable=True)

        Abilita tutti i menu se enable=True, se enable=False li disabilita

        :param enable: boolean
        """
        menus = self.menubar.GetMenus()
        # per tenere un menu acceso, es. "calendario":
        # menus.pop(4) # 4 e' l'index 0-based del menu Calendario
        for menu in menus[:-1]:
            self.abilita_tutti_sottomenu(menu[0], enable)
        menu_leghe = self.get_topmenu('Leghe')
        for item_menu in ('Nuova Lega', 'Esci'):
            self.abilita_sottomenu(menu_leghe, item_menu)
        menu_voti = self.get_topmenu('Voti')
        self.abilita_tutti_sottomenu(menu_voti)

    def check_menus(self):
        """
        check_menus(self)

        Fa un check dei dati presenti a db ed in base a quelli abilita e
        disabilita i menu di competenza
        """
        if not self.controller.get_voti_inseriti():
            InfoMessage(self, 'Prima importare i voti').get_choice()
            menus = self.menubar.GetMenus()
            menus.pop(3)  # solo Voti acceso
            for menu in menus[:-1]:
                self.abilita_tutti_sottomenu(menu[0], False)
        else:
            self.abilita_tutti_menu(False)
            self.check_menu_giocatore()
            self.check_menu_lega()

    def check_menu_giocatore(self):
        """
        check_menu_giocatore(self)

        Fa il check dei giocatori e gestisce i menu correlati
        """
        giocatori = self.controller.get_giocatori()
        voti = self.controller.get_voti_inseriti()
        menu_g = self.get_topmenu('Giocatori')
        g_lbl = ('Modifica Giocatore',)
        self.controlla_sottomenu(menu=menu_g, labels=g_lbl, iterable=giocatori)
        v_lbl = ('Statistiche',)
        self.controlla_sottomenu(menu=menu_g, labels=v_lbl, iterable=voti)

    def check_menu_lega(self):
        """
        check_menu_lega(self)

        Fa il check delle leghe e gestisce i menu correlati
        """
        leghe = self.controller.get_leghe()
        menu_leghe = self.get_topmenu('Leghe')
        for item_menu in ('Nuova Lega', 'Esci'):
            self.abilita_sottomenu(menu_leghe, item_menu)
        lega_lbl = ('Edit Lega', 'Elimina Lega')
        self.controlla_sottomenu(menu=menu_leghe, labels=lega_lbl,
                                 iterable=leghe)
        if leghe:
            squadre = self.controller.get_squadre()
            sq_lbl = ('Inizia Asta', 'Classifica')
            self.controlla_sottomenu(menu=menu_leghe, labels=sq_lbl,
                                iterable=squadre)
            self.check_menu_squadra()

    def check_menu_squadra(self):
        """
        check_menu_squadra(self)

        Fa il check delle squadre e gestisce i menu correlati
        """
        squadre = self.controller.get_squadre()
        menu_squadre = self.get_topmenu('Squadre')
        menu_form = self.get_topmenu('Formazioni')
        self.abilita_sottomenu(menu_squadre, 'Nuova Squadra')
        sq_lbl = ('Modifica Squadra', 'Elimina Squadra', 'Rosa Squadra',
                  'Mercato Squadra')
        self.controlla_sottomenu(menu=menu_squadre, labels=sq_lbl,
                                 iterable=squadre)
        f_lbl = ('Edit Formazione', 'Vedi Punteggio')
        self.controlla_sottomenu(menu=menu_form, labels=f_lbl, iterable=squadre)
        if squadre:
            self.check_menu_calendario()

    def check_menu_calendario(self):
        """
        check_menu_calendario(self)

        Fa il check delle squadre e gestisce il menu calendario
        """
        squadre = self.controller.get_squadre()
        menu_cal = self.get_topmenu('Calendario')
        f_cal = ('Crea Calendario', 'Risultati')
        self.controlla_sottomenu(menu=menu_cal, labels=f_cal, iterable=squadre)

    def controlla_sottomenu(self, menu, labels, iterable):
        """
        controlla_sottomenu(self, menu, labels, iterable)

        Fa il check nel menu=menu per tutte le label presenti nella lista labels
        in base alla lista di dati di iterable

        :param menu: wx.Menu
        :param labels: list di label sottomenu
        :param iterable: list di oggetti db_models.*
        """
        for item_menu in labels:
            if iterable:
                self.abilita_sottomenu(menu, item_menu)
            else:
                self.abilita_sottomenu(menu, item_menu, False)

    def abilita_sottomenu(self, menu, label, enable=True):
        """
        abilita_sottomenu(self, menu, label, enable)

        Abilita il sottomenu con label=label nel menu=menu, se enable=True,
        altrimenti lo disabilita

        :param menu: wx.Menu
        :param label: str label sottomenu
        :param enable: boolean
        """
        submenu = self.get_submenu(menu, label)
        submenu.Enable(enable)

    def get_topmenu(self, label):
        """
        get_topmenu(self, label) -> object wx.Menu

        Ritorna l'oggetto Menu con label=label

        :param label: str nome menu
        :return: object wx.Menu
        """
        return [menu for menu, lbl in self.menubar.GetMenus()
                if lbl == label.capitalize()][0]

    @staticmethod
    def get_submenu(menu, label):
        """
        get_submenu(menu, label) -> wx.Menu item

        Ritorna l'item corrispondente al menu=menu con sottomenu=label

        :param menu: object wx.Menu
        :param label: str nome sottomenu
        :return: object wx.Menu item
        """
        return [submenu for submenu in menu.GetMenuItems()
                if submenu.GetItemLabel() == label][0]

    @staticmethod
    def abilita_tutti_sottomenu(menu, enable=True):
        """
        abilita_tutti_sottomenu(menu, enable)

        Abilita tutti i sottomenu del menu=menu se enable=True o li disabilita
        se enable=False

        :param menu: object wx.Menu
        :param enable: boolean
        """
        submenus = menu.GetMenuItems()
        for submenu in submenus:
            submenu.Enable(enable)

    # noinspection PyUnusedLocal
    def quit(self, event):
        """
        quit(self, event)

        Distrugge il frame ed esce dall'App.

        :param event: wx.EVT_BUTTON
        """
        self.Destroy()

    # noinspection PyUnusedLocal
    def nuova_lega(self, event):
        """
        nuova_lega(self, event) -> object ViewNuovaLega

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewNuovaLega(parent=self, title='Nuova Lega')

    # noinspection PyUnusedLocal
    def edit_lega(self, event):
        """
        edit_lega(self, event) -> object ViewEditLega

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewEditLega(parent=self, title='Edit Lega')

    # noinspection PyUnusedLocal
    def delete_lega(self, event):
        """
        delete_lega(self, event) -> object ViewDeleteLega

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewDeleteLega(parent=self, title='Delete Lega')

    # noinspection PyUnusedLocal
    def gestisci_asta(self, event):
        """
        gestisci_asta(self, event) -> object ViewAsta

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewAsta(parent=self, title='Asta')

    # noinspection PyUnusedLocal
    def classifica(self, event):
        """
        classifica(self, event) -> object ViewClassifica

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewClassifica(parent=self, title='Classifica')

    # noinspection PyUnusedLocal
    def nuova_squadra(self, event):
        """
        nuova_squadra(self, event) -> object ViewNuovaSquadra

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewNuovaSquadra(parent=self, title='Nuova Squadra')

    # noinspection PyUnusedLocal
    def edit_squadra(self, event):
        """
        edit_squadra(self, event) -> object ViewEditSquadra

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewEditSquadra(parent=self, title='Edit Squadra')

    # noinspection PyUnusedLocal
    def edit_rosa(self, event):
        """
        edit_rosa(self, event) -> object ViewEditRosa

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewEditRosa(parent=self, title='Edit Rosa')

    # noinspection PyUnusedLocal
    def elimina_squadra(self, event):
        """
        elimina_squadra(self, event) -> object ViewEliminaSquadra

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewEliminaSquadra(parent=self, title='Elimina Squadra')

    # noinspection PyUnusedLocal
    def mercati(self, event):
        """
        mercati(self, event) -> object ViewMercati

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewMercati(parent=self, title='Mercati')

    # noinspection PyUnusedLocal
    def edit_giocatore(self, event):
        """
        edit_giocatore(self, event) -> object ViewEditGiocatore

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewEditGiocatore(parent=self, title='Edit Giocatore')

    # noinspection PyUnusedLocal
    def statistiche(self, event):
        """
        statistiche(self, event) -> object ViewStatistiche

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewStatistiche(parent=self, title='Statistiche')

    # noinspection PyUnusedLocal
    def importa_voti(self, event):
        """
        importa_voti(self, event) -> object ViewImportVoti

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewImportVoti(parent=self, title='Importa Voti')

    # noinspection PyUnusedLocal
    def vedi_calendario(self, event):
        """
        vedi_calendario(self, event) -> object ViewCalendario

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewCalendario(parent=self, title='Calendario')

    # noinspection PyUnusedLocal
    def crea_calendario(self, event):
        """
        crea_calendario(self, event) -> object ViewCreaCalendario

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewCreaCalendario(parent=self, title='Crea Calendario')

    # noinspection PyUnusedLocal
    def edit_formazione(self, event):
        """
        edit_formazione(self, event) -> object ViewFormazione

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewFormazione(parent=self, title='Formazione')

    # noinspection PyUnusedLocal
    def vedi_punteggio(self, event):
        """
        vedi_punteggio(self, event) -> object ViewPunteggio

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        ViewPunteggio(parent=self, title='Punteggio')

    # noinspection PyUnusedLocal
    def regolamento(self, event):
        """
        regolamento(self, event) -> object RulesFrame

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        RulesFrame(parent=self, title='Regolamento FantaLega')

    # noinspection PyUnusedLocal
    def about(self, event):
        """
        about(self, event) -> object InfoFrame

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        InfoFrame(parent=self, title='about FantaLega 2.1')

    # noinspection PyUnusedLocal
    def guida(self, event):
        """
        guida(self, event) -> object HelpFrame

        :param event: wx.EVT_BUTTON
        """
        self.Disable()
        HelpFrame(parent=self, title='guida FantaLega 2.1')

    def quit_subframe(self, event):
        """
        _quit_subframe(self, event)

        Chiude il subframe aperto e riabilita il frame core.
        Viene creato il bind all'interno dei singoli subframe

        :param event: wx.EVT_BUTTON
        """
        subframe = event.GetEventObject().GetParent()
        if isinstance(subframe, wx.Panel):
            subframe = subframe.GetParent()
        self.Enable()
        subframe.Destroy()

    @staticmethod
    def show_subframe(child):
        """
        _show_subframe(child)

        staticmethod:
        Mostra e centra il subframe sullo schermo

        :param child: object wx.Frame
        """
        child.Centre()
        child.Show()