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
        display_all_courses(self, column_title_list)                
        create_timetable (self) 
        clear_timetable(self, widget, data = None) 
        save_pdf(self, widget) 
        search(self, widget) 
        add_column_text(self, store, section_type, tab, 
            callback_method, column_title_list ) 
        display_course_code (self, tab) 
        get_course_details (self, widget, path, data = None)
        handle_compre_date (self) 
        display_sections (self, dataframe, store, section_type) 
        update_timetable (self, widget, path, treecolumn, store, section_type)
        update_compre_schedule (self, compre_date, label)
        update_midsem_schedule (self, match_parameter, label) 
        handle_section_change(self, row, section_type) 
        handle_clash_change(self, row)
        add_to_timetable(self) 
        remove_course(self, widget, path, treecolumn, store, *data) 
        add_to_catalog(self) 
        main_quit(self) 
        save_list(self) 
        open_last_work(self, widget, data) 

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
        self.SearchBar.connect('key-press-event', self.search)
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
        
        self.lec_store = Gtk.ListStore(str, str, str, str, str)
        self.prac_store = Gtk.ListStore(str, str, str, str, str)
        self.tut_store = Gtk.ListStore(str, str, str, str, str)

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


        self.catalog_store = Gtk.ListStore(str, str, str, str, str, str, str, str)
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

    def display_all_courses(self, column_title_list) :
        '''
        Displays all the available courses this semester. 
        The list consists only of course code and course title. 
            
            @parameter:
                column_title_list : List 
                    A list of string containing all the column names.
            
            @variables :
                self.all_course_list : List 
                    A list of tuples containing all course codes and titles
                
                self.all_course_store : Gtk.ListStore
                    A Gtk.ListStore containing items from all_course_list 

                treeview : Gtk.TreeView 
                    Gtk.TreeView with model as all_course_store to display 
                    the results.

                self.all_course_window : Gtk.ScrolledWindow 
                    Parent widget to which the treeview object is added.
                    This widget is visible as the 3rd page on the GUI.
        '''


        self.all_course_list = self.sobject.get_result(query = ' ')

        for course_code, course_title, compre_date in self.all_course_list :
            self.all_course_store.append([course_code, course_title, compre_date])

        treeview = Gtk.TreeView(model = self.all_course_store)
        for i, column_title in enumerate(column_title_list) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(
                column_title, renderer, text=i)
            treeview.append_column(column)
        self.all_course_window.add(treeview)
        
    def create_timetable(self) :
        '''
        Replaces your timetable to its initial state. 
            
            @variables :
                self.weekly_schedule : List
                    Labels in the weekly timetable
                compre_label : Gtk.Label
                    Displays "COMPREHENSIVE EXAMINATION"
                self.compre_schedule : List
                    Label in the compre schedule
                midsem_label : Gtk.Label
                    Displays "MID SEMESTER EXAMINATION"
                self.midsem_schedule : List
                    Label in the midsem schedule

        '''
        self.weekly_schedule = [
        ['HOURS/DAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        ['08 : 00 AM', '', '', '', '', '', ''],
        ['09 : 00 AM', '', '', '', '', '', ''],
        ['10 : 00 AM', '', '', '', '', '', ''],
        ['11 : 00 AM', '', '', '', '', '', ''],
        ['12 : 00 PM', '', '', '', '', '', ''],
        ['01 : 00 PM', '', '', '', '', '', ''],
        ['02 : 00 PM', '', '', '', '', '', ''],
        ['03 : 00 PM', '', '', '', '', '', ''],
        ['04 : 00 PM', '', '', '', '', '', ''],
        ['05 : 00 PM', '', '', '', '', '', '']]

        l = []
        for row in range (len(self.weekly_schedule)) :
            for col in range (len(self.weekly_schedule[row])) :
                label = Gtk.Label(label = self.weekly_schedule[row][col])
                self.page00_weekly.attach(child = label, left = col, top = row,\
                width = 1, height = 1)
                l.append(label)
            MyWindow.Label_list_weekly.append(l)
            l = []        


        compre_label = Gtk.Label()
        compre_label.set_markup(
            "<big> <b> COMPREHENSIVE EXAMINATION </b> </big>")
        self.page00_compre.attach(child = compre_label,
            left = 0, top = 0, width = 3, height = 1)

        self.compre_schedule = [
        ['Sessions','01/05', '02/05', '03/05','04/05', '05/05', '06/05', \
        '07/05', '08/05' ,'09/05', '10/05', '11/05', '12/05', '13/05', '14/05'],
        ['Forenoon', '', '', '', '', '', '', '', '', '', '', '', '', '', '',],
        ['Afternoon', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]]

        for row in range(len(self.compre_schedule)) :
            for col in range (len(self.compre_schedule[row])) :
                label = Gtk.Label(label = self.compre_schedule[row][col])
                self.page00_compre.attach(child = label, left = row, top = col + 1,\
                    width = 1 , height = 1)
                l.append(label)
            MyWindow.Label_list_compre.append(l)
            l = []


        midsem_label = Gtk.Label()
        midsem_label.set_markup(
            "<big> <b> MID SEMESTER EXAMINATION </b> </big>")
        self.page00_midsem.attach(child = midsem_label,
            left = 0, top = 0, width = 5, height = 1)

        self.midsem_schedule = [
        ['TIME/DATES', '11/03', '12/03', '13/03', '14/03', '15/03', '16/03'],
        ['9:00 - 10:30 AM', '', '', '', '', '', ''],
        ['11:00 - 12:30 AM', '', '', '', '', '', ''],
        ['1:30 - 3:00 PM', '', '', '', '', '', ''],
        ['3:30 - 5:00 PM', '', '', '', '', '', '']]

        for row in range(len(self.midsem_schedule)) :
            for col in range (len(self.midsem_schedule[row])) :
                label = Gtk.Label(label = self.midsem_schedule[row][col])
                self.page00_midsem.attach(child = label, left = row, top = col + 1,\
                    width = 1 , height = 1)
                l.append(label)
            MyWindow.Label_list_midsem.append(l)
            l = []


    def clear_timetable(self, widget, data = None) :
        '''
        Replaces your timetable to its initial state.
        This is a callback method for a Gtk.MenuItem widget (clear_all_menu). 

            @parameters :
                widget : Gtk widget object
                data : default = None 
                    Any additional data needed to be passed to the method.

            @variables :
                Label_list_weekly : List 
                    List of Gtk.Labels
                Label_list_compre : List
                    List of Gtk.Labels
                Label_list_midsem : List
                    List of Gtk.Labels
                added_courses : List
                    List of str containing course codes (distinct) in your timetable.
                save_count : int
                    Determines whether to use self.save_list method.
        '''
        for row in range (len(MyWindow.Label_list_weekly)) :
            for col in range (len(MyWindow.Label_list_weekly[row])) :
                MyWindow.Label_list_weekly[row] [col].set_label(
                    self.weekly_schedule[row][col]) 
        
        for row in range(len(MyWindow.Label_list_compre)) :
            for col in range(len(MyWindow.Label_list_compre[row])) :
                MyWindow.Label_list_compre[row][col].set_label(
                    self.compre_schedule[row][col])

        for row in range(len(MyWindow.Label_list_midsem)) :
            for col in range(len(MyWindow.Label_list_midsem[row])) :
                MyWindow.Label_list_midsem[row][col].set_label(
                    self.midsem_schedule[row][col])

        self.catalog_info = []
        self.catalog_store.clear()  
        self.save_count = 0
        MyWindow.added_courses = []

    def save_pdf(self, widget) :
        '''
        Saves your desired schedule in pdf format.
        This is a callback method for Gtk.MenuItem widget (save_pdf_menu).

        This method uses a special Python library known as 'reportlab' which is 
        used for writing/reading in pdf files. For more information  :
            
            http://www.blog.pythonlibrary.org/2010/09/21/reportlab-tables-creating-tables-in-pdfs-with-python/
            https://www.reportlab.com/opensource/installation/
            https://www.reportlab.com/docs/reportlab-userguide.pdf
        ''' 
        dialog = Gtk.FileChooserDialog("Choose your destination :", self,
            Gtk.FileChooserAction.SAVE,
            ('Cancel', Gtk.ResponseType.CANCEL,
             'SAVE', Gtk.ResponseType.ACCEPT))

        dialog.set_current_name('Untitled Document.pdf')
        
        response = dialog.run()

        doc = SimpleDocTemplate(dialog.get_filename(), \
            pagesize = landscape(letter))

        if response == Gtk.ResponseType.ACCEPT :
            self.write (
                doc, "WEEKLY SCHEDULE", \
                self.weekly_schedule, MyWindow.Label_list_weekly)
            
            self.write (
                doc, "COMPREHENSIVE EXAMINATION", \
                self.compre_schedule, MyWindow.Label_list_compre)

            self.element.append(PageBreak())
            
            self.write (
                doc, "MID SEMESTER SCHEDULE", \
                self.midsem_schedule, MyWindow.Label_list_midsem)
        
            style = getSampleStyleSheet()
            normal = style["Heading1"]

            para = Paragraph("LEGEND", normal)
            self.element.append(para)
            user_data = [['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR', 'ROOM']]
            for row in self.catalog_info :
                data = row.split(';')
                user_data.append([data[0], data[1], data[2], data[3], data[4]])
            table = Table(data = user_data)
            table.setStyle(TableStyle([
                                    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                    ]))     
            self.element.append(table)

            doc.multiBuild(self.element)
            self.save_list()
            self.save_count = 1
            
        elif response == Gtk.ResponseType.CANCEL : 
            pass

        dialog.destroy()

    def write(self, doc, headline, schedule, class_label_list) :        
        '''
        Writes data to a pdf file.
            @paramter :
                doc : 
                    reportlab.platypus.doctemplate.SimpleDocTemplate instance
                headline : string
                    string which to be written as a heading
                schedule : list 
                    list of strings containing labels for the timetable
                class_label_list : list 
                    list of Gtk.Label objects 
            @variables : 
                user_data : list
                    list of string to be written on the pdf
                table : 
                    reportlab.platypus.doctemplate.Table instance
        '''

        style = getSampleStyleSheet()
        normal = style["Heading1"]

        para = Paragraph(headline, normal)
        self.element.append(para)

        user_data = copy.deepcopy(schedule)
        
        for row in range (len(class_label_list)) :
            for col in range (len(class_label_list[row])) :
                user_data[row][col] =  class_label_list[row][col].get_label()
            

        table = Table(data = user_data)
        table.setStyle(TableStyle([
                                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                ]))
        self.element.append(table)


    def search (self, widget, event = None) : 
        '''
        Usses self.sobject to search for courses matching your query.
        This is a callback method for a Gtk.Button widget (self.SearchButton). This method
        is also activated when any key is pressed and the SearchBar is active.

        @variables :
            self.SearchBar : Gtk.Entry 
            self.match_list : list 
                Contains a list of tuples having matching course_code and course_title as 
                tuple elements
        
        Returns self.match_list
        '''
        if self.SearchBar.get_text() != '':   
            self.match_list = self.sobject.get_result(query = self.SearchBar.get_text())
            self.display_course_code(self.page01_course_tab)

    def add_column_text(
        self, store, 
        section_type, tab, 
        callback_method, column_title_list) :
        '''
    This method adds column_title to the treeview object.

        @parameters :
            store : Gtk.ListStore 
                    Store objects which contains details of the section(s)
            section_type : str
                    String value used for displaying the type of class of a class.
                    Permitted values : LEC, PRAC, TUT
            tab : Gtk.ScrolledWindow
                    Layout container in which details of the course is to be displayed.
            callback_method : callable object
                    The treeview contains a togglebutton (Gtk.CellRendererToggle), which when 
                    activated calls this method.
            column_title_list : list 
                    A list of strings containing the column_title for the tabular data to 
                    be displayed.
        @variables :
            treeview : Gtk.TreeView (model = store)
                Object which displays data on the window
            
            selection : Gtk.TreeSelection Object
                Allows you to the change selection_mode and get selected row(s) of the 
                treeview object
            
            renderer_toggle: Gtk.CellRendererToggle()
                Object for adding radiobutton on rows of the treeview
            
            radio_column : Gtk.TreevViewColumn(label, renderer_toggle)
                            label - text to be displayed on the columns
            
            renderer : Gtk.CellRendererText()
                Object for adding text object in the treeview.
            
            column :    Gtk.TreeViewColumn(label, renderer)
                            label - element of column_title_list
        '''
        
        try:
            if tab.get_child() != None :
                store.clear()
                tab.remove(tab.get_child())
        except :
            pass            
        
        treeview = Gtk.TreeView(model = store)
        selection = treeview.get_selection()
        selection.set_mode(1)

        
        for i, column_title in enumerate(column_title_list) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(
                column_title, renderer, text=i)
            treeview.append_column(column)
        
        treeview.show_all()
        treeview.connect("row-activated", 
            callback_method, 
            store, section_type)
        tab.add(treeview)

    def display_course_code(self, tab):
        '''
        Method for displaying course code on course_code tab on page01. 
            
            @variables :
                self.store : Gtk.ListStore 
                    store object for storing course details
        '''
        
        self.store = Gtk.ListStore(str, str, str)
        self.add_column_text(
            self.store, ' ', tab, 
            self.get_course_details, 
            ["COURSE CODE", "COURSE TITLE", "COMPRE DATES"])
        
        for match in self.match_list :
            self.store.append(list(match))        
        
    def get_course_details(self, widget, path, *data) :
        '''
        Uses sobject to get lecture, tutorial and practical dataframe objects.
        This is a callback method for Gtk.CellRendererToggle Object.

            @variables :
                selected_path : Gtk.TreePath object
                    Changes the state (True/False) of the selected row of treeview.

            @parameters :
                path : int
                    Integer whose value is the row index of the treeview object.
        '''

        self.selected_course_code = self.store[path][0]
        self.selected_course_title = self.store[path][1]
        self.selected_compre_date = self.store[path][2]
        match_parameter = (self.selected_course_code, self.selected_course_title)
        self.sobject.get_course_details(match_parameter)

        for row in self.catalog_store :
            compre_date = row[-1]
            if compre_date == self.selected_compre_date\
            and self.selected_course_code != row[0] and compre_date != '':
                self.handle_compre_date()
                break

        else :  
            self.display_sections(
                dataframe = self.sobject.practical, 
                tab = self.page01_prac_tab, 
                store = self.prac_store, 
                section_type = 'PRAC')
            self.display_sections(
                dataframe = self.sobject.tutorial, 
                tab = self.page01_tut_tab, 
                store = self.tut_store, 
                section_type = 'TUT')
            self.display_sections(
                dataframe = self.sobject.lecture, 
                tab = self.page01_lec_tab, 
                store = self.lec_store, 
                section_type = 'LEC')

        self.page01_notebook.next_page()


    def handle_compre_date(self) : 
        '''
        This method is called when there are courses in your catalog 
        having same compre date. You need to remove the course whose 
        date is clashing with this one and then add this course.

        '''

        dialog = Gtk.MessageDialog(self, 0,
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK,
            "You have selected a course having same compre date !!" )

        dialog.format_secondary_text(
            "Please remove that course from your schedule to add this one.")

        response = dialog.run()
        if response == Gtk.ResponseType.OK :
            pass
        dialog.destroy()


    def display_sections (self, dataframe, tab, store, section_type) :
        '''
        This method is used for displaying all the data of a course.

            @parameters :
                dataframe : pandas.DataFrame object
                    Contains details of the all the available sections 
                store : Gtk.ListStore object

                section_type : str
                    Contains the string value for type of section 
        '''

        self.add_column_text(
            store, section_type, 
            tab, self.update_timetable, 
            ["SECTION", "INSTRUCTOR", "ROOM", "DAYS", "HOURS"])
        if dataframe.empty :
            store.append(['NA', 'NA', 'NA', 'NA', '0'])

        else :
            count = 0   
            while count <= len(dataframe) - 1:  
                liststore_data_Section = dataframe.iloc[count][2] 
                liststore_data_Instructor = dataframe.iloc[count][3]
                liststore_data_room = dataframe.iloc[count][4]
                liststore_data_days = dataframe.iloc[count][5]
                liststore_data_hours = dataframe.iloc[count][6]


                count += 1

                while count <= len(dataframe) - 1 and not dataframe.iloc[count][2]:
                    liststore_data_Instructor += '\n' + dataframe.iloc[count][3]
                    #liststore_data_hours += '\n' + dataframe.iloc[count][6]
                    #liststore_data_days += '\n' + dataframe.iloc[count][5]
                    #liststore_data_room += '\n' + dataframe.iloc[count][4]
                    count += 1

                store.append([
                    str(liststore_data_Section), 
                    liststore_data_Instructor, 
                    liststore_data_room,
                    liststore_data_days, 
                    liststore_data_hours])
                
    def update_compre_schedule(self, compre_date, label) :
        '''
        Adds entry to compre schedule.
            @parameter : 
                compre_date : str
                    str value of the form "DD/MM AN" or "DD/MM FN", 
                    where AN and FN are the afternoon and forenoon 
                    sessions respectively.
            
        '''

        try :
            date = compre_date.split()[0].split('/')
            session = compre_date.split()[-1]
            
            if session == 'AN' : session = 2
            elif session == 'FN' : session = 1

            MyWindow.Label_list_compre[session][int(date[0])].set_label(
            label)
            # these statements will catch an exception when, there is either
            # a null value or '*' in date or session variables. 

        except : 
            pass


    def update_midsem_schedule(self, match_parameter, label) :
        '''
        Adds entry to midsem schedule.
            @parameter :
                match_paramter : tuple
                    tuple of string (course code,)
                label : The text to be displayed in the schedule.
        '''
        self.sobject.get_midsem_details(match_parameter)
        date = self.sobject.midsem_date.split('/')[0]
        time = self.sobject.midsem_time

        if time == '9.00 - 10.30AM' : time = 1
        elif time == '11.00 -12.30 PM' : time = 2
        elif time == '1.30 -3.00 PM' : time = 3
        elif time == '3.30 - 5.00 PM' : time = 4
        
        try :
            MyWindow.Label_list_midsem[time][int(date) - 10].set_label(
                label)
            # these statements will catch an exception when, there is either
                # a null value or '*' in date or session variables. 
        except :
            pass
 
    def update_timetable(self, widget, path, treecolumn, store, section_type) :
        '''
        This is a callback method for Gtk.CellRendererToggle object. This 
        method also adds dialog box if a course is clashing with other courses or 
        when you change sections of a already selected course. 

            @parameters :
                path : int
                    Row index of the treeview object which is selected.
                treecolumn : Gtk.TreeViewColumn
                store : Gtk.ListStore
                    Contains the details of all the available choices.
                section_type : str
                    Contains the string value of the type of section

            @variables :
                self.selected_section : str 
                    Contains selected section number
                self.selected_instructor : str 
                    Contains selected instructor names
                self.selected_hour : list
                    Contains a list of strings of times of the course section
                self.selected_day : list
                    Contains a list of strings of days of the course section

                MyWindow.added_course : list
                    Contains a list of all the course_code a user has opted for.  
        '''
        try :
            self.selected_section = store[path][0]
            if not self.selected_section :
                self.selected_section = '1' 

            self.selected_room = store[path][2]
            self.selected_instructor = store[path][1]
            self.selected_day = store[path][3].split()
            self.selected_hour = store[path][4].split()

            for i in range (len(self.selected_hour)) :
                self.selected_hour[i] = int(self.selected_hour[i])


            self.text_to_display = self.selected_course_code + '\n' + \
            self.selected_room

            #self.text_to_display = self.selected_course_code + '\n' + \
            #section_type + '-' + self.selected_section

            self.info = self.selected_course_code + ';' + \
             self.selected_course_title + ';' + \
             section_type + '-' + self.selected_section + ';' +\
             self.selected_instructor + ';' +\
             self.selected_room + ';' +\
             store[path][3] + ';' + store[path][4] +\
             ';' + self.selected_compre_date

        except :
            pass

    
        for row in self.catalog_info :
            list_ = row.split(';')

            if 0 in self.selected_hour :
                break
            
            flag = 0
            for hr in self.selected_hour :
                for dy in self.selected_day :
    
                    if str(hr) in list_[-2].split()  \
                    and dy in list_[-3].split() \
                    and self.selected_course_code != list_[0]:
                        self.handle_clash_time(row)
                        flag = 1
                        
                #if flag == 1 :
                    #break
            
            if flag == 1 :
                break

            if self.selected_course_code in MyWindow.added_courses :

                if section_type == list_[2].split('-')[0]\
                    and self.selected_course_code == list_[0] :
                    self.handle_section_change(row, section_type)
                    break
                    
                else :
                    pass

            else :
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)
                MyWindow.added_courses.append(self.selected_course_code)
                break               

        else :
            if 0 not in self.selected_hour:
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)
                MyWindow.added_courses.append(self.selected_course_code)
        
        self.add_to_catalog()       
        self.page01_notebook.next_page()
        self.update_compre_schedule(self.selected_compre_date, \
                label = self.selected_course_code)
        self.update_midsem_schedule(
            match_parameter = (self.selected_course_code,),\
            label = self.selected_course_code)
    
    def handle_section_change(self, row, section_type) :
        '''
        This method is called when you try to change section of a course 
        you took.
            @parameters :
                row : string 
                    A string from self.catalog_info
                section_type : string 
                    A string which tells the type of class 
                    ('LEC', 'PRAC', 'TUT')1
        '''

        section_list = row.split(';')
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, 
            "Warning : You are about to change a section !")
        dialog.format_secondary_text("Do you wish to continue ?")

        response = dialog.run()

        if response == Gtk.ResponseType.YES :
            self.catalog_info.remove(row)
            for row in section_list[-2].split() :
                for col in section_list[-3].split() :
                    if col == 'M' : 
                        MyWindow.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' : 
                        MyWindow.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' : 
                        MyWindow.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' : 
                        MyWindow.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' : 
                        MyWindow.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' : 
                        MyWindow.Label_list_weekly[int(row)][6].set_label('')

            self.update_timetable(None, None, None, None, section_type)
            
        elif response == Gtk.ResponseType.NO :
            pass    
        dialog.destroy()

        

    def handle_clash_time(self, row) :
        '''
        This method is called when there are two courses 
        occurring at the same time. This method shows a dialog box
        which asks you to either continue or cancel the replacement 
        of the course you want with the one already present in your timetable 
        at that same time slot.

            @parameter :
                row : string
                    A string from self.catalog_info

        '''

        section_list = row.split(';')
        dialog = Gtk.MessageDialog(self, 0, 
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, 
            "Warning : You cannot have 2 classes at the same time !!")
        dialog.format_secondary_text(
                "Do you want to replace this course ?")

        response = dialog.run()

        if section_list[0] == self.selected_course_code :
            response = Gtk.ResponseType.YES 

        if response == Gtk.ResponseType.YES :
            self.catalog_info.remove(row)
            
            for row in section_list[-2].split() :
                for col in section_list[-3].split() :
                    if col == 'M' : 
                        MyWindow.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' : 
                        MyWindow.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' : 
                        MyWindow.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' : 
                        MyWindow.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' : 
                        MyWindow.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' : 
                        MyWindow.Label_list_weekly[int(row)][6].set_label('')
            
            for rows in self.catalog_info : 

                row_item = rows.split(';')
                section = row_item[2].split('-')[0]
                course = row_item[0]

                if (self.selected_course_code == course \
                    and self.info.split(';')[2].split('-')[0] == section) :
                    self.handle_section_change(rows, section)
                    

            else :
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)

        else :
            pass
        dialog.destroy()

    def add_to_timetable(self, hours, days) :
        '''
        Adds the selected section to the timetable.
            @variables :
                hours : list 
                    Contains a list of integers 
                days : list 
                    Contains a list of string objects.
                        (M, T, W, Th, F, S)
        '''
        for row in hours :
            for col in days : 
                if col == 'M' : 
                    MyWindow.Label_list_weekly[row][1].set_label(self.text_to_display)
                elif col == 'T' : 
                    MyWindow.Label_list_weekly[row][2].set_label(self.text_to_display)
                elif col == 'W' : 
                    MyWindow.Label_list_weekly[row][3].set_label(self.text_to_display)
                elif col == 'Th' : 
                    MyWindow.Label_list_weekly[row][4].set_label(self.text_to_display)
                elif col == 'F' : 
                    MyWindow.Label_list_weekly[row][5].set_label(self.text_to_display)
                elif col == 'S' : 
                    MyWindow.Label_list_weekly[row][6].set_label(self.text_to_display)


    def remove_course(self, widget, path, treeview, store, *data) :
        '''
        This method is called to remove the courses selected in the catalog page. This 
        is also a callback method for Gtk.Button (self.remove_label). This method also shows 
        dialog box warning the user to confirm before removing a course.
        '''

        row = store[path]
        remove_course_title = row[1]
        remove_course_code = row[0]
        remove_section = row[2]
        remove_hour = row[-2]
        remove_day = row[-3]
        remove_compre= row[-1]

        dialog = Gtk.MessageDialog(self, 0, 
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, 
            "You are about to remove the selected course")
        
        dialog.format_secondary_text(
            "Press OK to continue or CANCEL to abort")
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            for col in remove_day.split() :
                for row in remove_hour.split() :
                    if col == 'M' :
                        MyWindow.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' :
                        MyWindow.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' :
                        MyWindow.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' :
                        MyWindow.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' :
                        MyWindow.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' :
                        MyWindow.Label_list_weekly[int(row)][6].set_label('')


            count = 0
            remove_string = ''
            for strings in self.catalog_info :
                if remove_course_code in strings :
                    count += 1

                if remove_course_code in strings \
                and remove_section in strings :
                    remove_string = strings


            if count == 1:
                MyWindow.added_courses.remove(remove_course_code)
            
            self.catalog_info.remove(remove_string)

            self.add_to_catalog()
            dialog.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        if remove_course_code not in MyWindow.added_courses :
            session = remove_compre.split()[-1]
            date = remove_compre.split()[0].split('/')[0]
            if session == 'AN' : session = 2
            elif session == 'FN' : session = 1

            MyWindow.Label_list_compre[session][int(date)].set_label('')

            self.update_midsem_schedule(
                match_parameter = (remove_course_code,),\
                label = '')

    def add_to_catalog(self) :
        '''
        This method updates content present in the catalog_info list to 
            catalog_store.
        '''
        self.add_column_text(
            self.catalog_store, None,
            self.page02_window, self.remove_course,
            ['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR', 'ROOM', 'DAYS', 'HOURS', 'COMPRE DATE'])

        self.catalog_info.sort()
        for row in self.catalog_info :
            self.catalog_store.append(row.split(';'))

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

    def save_list(self) :
        '''
        Creates a file (if it doesn't exist) and writes the data in the 
        self.catalog_info for future use.
        '''
        with open('temp.txt', 'wb') as f :
            pickle.dump(self.catalog_info, f)                
            f.close()

    def open_last_work(self, widget, *data) :
        '''
        Method for loading the data from 'temp.txt' file in the directory.
        Uses pickle module which is used for serializing/de-serializing an
        object in a file. This is also a callback method for Gtk.MenuItem 
        (open_previous_menu).

            @variables :
                file : file object
                    Used for reading/writing in a file.
                data : 2D array
                    Contains the values of self.catalog_info (of your last work.)

        '''
        self.clear_timetable(None)
        try :
        
            file = open('temp.txt', 'rb')

            data = pickle.load(file)
            for row in data :

                self.catalog_info.append(row)
                tt_info = row.split(';')

                days = tt_info[-3].split()
                hours = tt_info[-2].split()
                section = tt_info[2]
                course_code = tt_info[0]
                course_title = tt_info[1]
                compre_date = tt_info[-1]

                for i in range (len(hours)) :
                    hours[i] = int(hours[i])

                self.text_to_display = course_code + '\n' + section
                self.add_to_timetable(hours, days)
                self.update_compre_schedule(compre_date, 
                    label = course_code)
                
                self.update_midsem_schedule(
                    match_parameter = (course_code,),
                    label = course_code)

                if course_code not in MyWindow.added_courses :
                    MyWindow.added_courses.append(course_code)

            self.add_to_catalog()
        
        except IOError :
            pass
