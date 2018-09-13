import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from . import search
import pandas
import time
import copy
import pickle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak



class MyWindow(Gtk.Window):
    '''
    This class is for creating UI for the second page of the application.
    The main window consists of 4 main pages 
    (YOUR SCHEDULE , COURSE CATALOG, MY COURSES, OPTIONS). 

    The variables for the the pages are : 
        self.pane, page01

    The 1st page displays your schedule and lets you search your courses. 
    This page contains 2 panes.The 1st pane has three tabs -
    WEEKLY, COMPRE AND MISEM, containing their respective schedules.

    The 2nd pane allows you to search and select courses for your timetable.
    It contains a SearchBar, a Search Button and another notebook which has 
    4 pages (COURSES, LECTURE, PRACTICAL, TUTORIAL). 
    COURSES tab : Displays your matching results
    LECTURE tab : Displays the available lecture sections for your desired course
    PRACTICAL tab : Displays the availabe practical sections for your desired course 
    TUTORIAL tab : Displays the available tutorial sections for your desired course
        (all the above tabs will remain empty if there are no available sections)
    

    The 2nd page shows all the courses available, i.e. all the courses offered
    to students this sem.

    The 3rd page shows all the details of the courses which you have selected
    for your timetable. This page also allows you to delete some of them, if 
    you don't want them in your timetable

    The 4th page in the window opens a dropdown menu with options such clear_all 
    (if you want to start afresh), save_pdf (if you want to save your work), 
    open_last_work (if you plan to work on your last timetable).


    METHOS :
        __init__ 
        main_quit(self) 


    '''


    Label_list_weekly = []
    added_courses = []
    Label_list_compre = []
    Label_list_midsem = []

    def __init__(self):
        '''
        Constructs a MyWindow instance . 
                
            @variables -
                
                (Gtk layout containers)

                header_bar :                                Gtk.HeaderBar       

                self.notebook :                             Gtk.NoteBook
-------------------------------------------------------------------------------                
YOUR SCHEDULE   self.pane :                                 Gtk.Paned            
                    page00_notebook :                       Gtk.Notebook
                        page00_weekly_window :              Gtk.ScrolledWindow
                            self.page00_weekly :                Gtk.Grid
                        page00_weekly_window :              Gtk.ScrolledWindow
                            self.page00_compre :                Gtk.Grid
                                compre_label   :                Gtk.Label
                        page00_weekly_window :              Gtk.ScrolledWindow
                            self.page00_midsem :                Gtk.Grid
                                midsem_label   :                Gtk.Label

                        x-x-x-x-x-x-x HORIZONTAL PANE x-x-x-x-x-x-x

SEARCH              page01 :                                Gtk.Grid
                        self.SearchBar :                    Gtk.SearchEntry
                        self.SearchButton :                 Gtk.Button
                        self.page01_notebook :              Gtk.NoteBook
                            self.page01_courses_tab :       Gtk.ScrolledWindow
                            self.page01_lecture_tab :       Gtk.ScrolledWindow
                            self.page01_tutorial_tab :      Gtk.ScrolledWindow
                            self.page01_practical_tab :     Gtk.ScrolledWindow
--------------------------------------------------------------------------------                            
COURSE CATALOG      self.all_courses_window :               Gtk.ScrolledWindow
                        self.all_course_store :             Gtk.ListStore
---------------------------------------------------------------------------------                          
MY COURSES       page02 :                                Gtk.Grid
                        self.page02_window :                Gtk.ScrolledWindow
                        self.remove_label :                Gtk.Button
--------------------------------------------------------------------------------
OPTIONS             self.menu_button :                      Gtk.MenuButton
                        self.menu :                         Gtk.Menu
                            clear_all_menu :                Gtk.MenuItem
                            save_pdf_menu :                  Gtk.MenuItem
                            open_previous_menu :            Gtk.MenuItem
---------------------------------------------------------------------------------

                
                Other variables : 
                    self.sobject : search.Searching () instance
                    
                    self.save_count : int
                        Int value which acts a flag for using save_list method.

                    self.lec_store, self.prac_store, self.tut_store  : Gtk.ListStore
                        (all are liststore for storing available course sections)
                    
                    self.catalog_store : Gtk.Liststore 
                            This liststore contains information about the catalog page.
                    
                    self.catalog_info : List
                            This is a list which also contains the information about the 
                            courses you are registered in.
                    
                    self.all_course_list : List 
                            This is a list containing tuples (COURSE CODE, COURSE TITLE)

        '''

        super(MyWindow, self).__init__(title = "OFFLINE ERP")
        self.connect('delete-event', self.main_quit)
        self.notebook = Gtk.Notebook()
        self.set_size_request(width = 1000, height = 700)
        self.add(self.notebook)
        self.maximize()

        self.set_icon_from_file('media/BITs.jpg')

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "OFFLINE ERP"
        self.set_titlebar(header_bar)
        self.connect('key-press-event', self.search)

        self.sobject = search.Searching()
        self.save_count = 0
        self.element = []

        self.pane = Gtk.Paned()
        page00_notebook = Gtk.Notebook()

        page00_weekly_window = Gtk.ScrolledWindow(hexpand=True)
        self.page00_weekly = Gtk.Grid()
        self.page00_weekly.set_row_homogeneous(True)
        self.page00_weekly.set_column_homogeneous(True)
        page00_weekly_window.add(self.page00_weekly)

        page00_compre_window = Gtk.ScrolledWindow(hexpand=True)
        self.page00_compre = Gtk.Grid()
        self.page00_compre.set_row_homogeneous(True)
        self.page00_compre.set_column_homogeneous(True)
        page00_compre_window.add(self.page00_compre)

        page00_midsem_window = Gtk.ScrolledWindow(hexpand=True)
        self.page00_midsem = Gtk.Grid()
        self.page00_midsem.set_row_homogeneous(True)
        self.page00_midsem.set_column_homogeneous(True)
        page00_midsem_window.add(self.page00_midsem)


        page00_notebook.append_page(page00_weekly_window, 
            Gtk.Label('WEEKLY SCHEDULE'))
        page00_notebook.append_page(page00_compre_window, 
            Gtk.Label('COMPRE SCHEDULE'))
        page00_notebook.append_page(page00_midsem_window, 
            Gtk.Label('MIDSEM SCHEDULE'))

        self.notebook.append_page(self.pane, Gtk.Label("MY SCHEDULE"))
        self.create_timetable()

        page01 = Gtk.Grid()
        self.SearchBar = Gtk.SearchEntry()
        self.SearchBar.set_placeholder_text('Search your courses here')
        page01.attach(child = self.SearchBar, left = 1, 
                    top = 1, width = 4, height = 1)
     
        self.SearchButton = Gtk.Button("GO !")
        self.SearchButton.connect('clicked', self.search)
        page01.attach_next_to(
                    child = self.SearchButton, 
                    sibling = self.SearchBar,
                    side = Gtk.PositionType(1), 
                    width = 1, height = 1)
        
        self.page01_notebook = Gtk.Notebook()
        self.page01_course_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_lec_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_tut_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_prac_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)

        page01.attach_next_to(child = self.page01_notebook, sibling = self.SearchBar, 
                    side = Gtk.PositionType(3), width = 1, height = 1)

        self.pane.pack1(page00_notebook, True, False)
        self.pane.pack2(page01, True, False)
        
        self.lec_store = Gtk.ListStore(str, str, str, str)
        self.prac_store = Gtk.ListStore(str, str, str, str)
        self.tut_store = Gtk.ListStore(str, str, str, str)

        self.page01_notebook.append_page(
            self.page01_course_tab, Gtk.Label("COURSE"))
        self.page01_notebook.append_page(
            self.page01_lec_tab, Gtk.Label("LECTURE") )
        self.page01_notebook.append_page(
            self.page01_prac_tab, Gtk.Label("PRACTICAL"))
        self.page01_notebook.append_page(
            self.page01_tut_tab, Gtk.Label("TUTORIAL"))

        self.all_course_window = Gtk.ScrolledWindow(hexpand = True, vexpand = True)
        self.all_course_store = Gtk.ListStore(str, str, str)
        self.display_all_courses(['COURSE CODE', 'COURSE TITLE', 'COMPRE DATES'])
        self.notebook.append_page(self.all_course_window, Gtk.Label('COURSE CATALOG'))
        
        self.page02 = Gtk.Grid()
        self.page02_window = Gtk.ScrolledWindow(hexpand = True, vexpand = True)

        self.remove_label = Gtk.Label(
            "DOUBLE CLICK ON THE COURSE YOU WANT TO DELETE")

        self.page02.attach(child = self.remove_label, 
            left = 0, top = 0, width = 1, height = 1)

        self.page02.attach_next_to(child = self.page02_window, 
            sibling = self.remove_label, 
            side = Gtk.PositionType(3), 
            width = 1, height = 1)


        self.catalog_store = Gtk.ListStore(str, str, str, str, str, str, str)
        self.catalog_info = []
        self.notebook.append_page(self.page02, Gtk.Label('MY COURSES'))

        
        self.menu = Gtk.Menu()

        clear_all_menu = Gtk.MenuItem("Clear all enteries")
        clear_all_menu.connect('activate', self.clear_timetable)

        save_pdf_menu = Gtk.MenuItem('Generate pdf')
        save_pdf_menu.connect('activate', self.save_pdf)

        open_previous_menu = Gtk.MenuItem('Open your last work')
        open_previous_menu.connect('activate', self.open_last_work)

        self.menu.append(clear_all_menu)
        self.menu.append(save_pdf_menu)
        self.menu.append(open_previous_menu)
        self.menu.show_all()

        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popup(self.menu)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('media/settings.png')
        pixbuf = pixbuf.scale_simple(32, 32, 2)
        
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.menu_button.set_image(image)

        self.notebook.append_page(Gtk.Label(), self.menu_button)


    def main_quit(self, widget, event) :
        '''
        Adds custom quit method for the application. 
        Shows a dialog box if there is any unsaved work.
        '''
        if len(MyWindow.added_courses) != 0 and \
            self.save_count == 0:
            dialog = Gtk.MessageDialog(self, 0,
                Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                'Your Timetable has been saved. You can resume this' +\
               ' work again next time.')

            dialog.format_secondary_text(
                'Do you want to save it in pdf format ?')

            response = dialog.run()

            if response == Gtk.ResponseType.YES :
                self.save_pdf(None)
            elif response == Gtk.ResponseType.NO :
                self.save_list()

            dialog.destroy()
        else :
            pass

        Gtk.main_quit()

