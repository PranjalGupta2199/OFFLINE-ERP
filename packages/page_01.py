import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from . import search
import pandas
import copy
import pickle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph



class MyWindow(Gtk.Window):
    '''
    This class is for creating gui for the second page of the application.
    The main window consists of 2 main pages (YOUR TIMETABLE , SEARCH, COURSE CATALOG). 

    The variables for the the pages are : 
        page00_window, page01

    The 1st page displays your timetable and two buttons (CLear All, Generate pdf). The clear all button 
    removes all the enteries from the timetable and Generate pdf saves your work in pdf format.

    The 2nd page allows you to search and select courses for your timetable. It contains 
    a SearchBar, a Search Button and another notebook which has 4 pages (COURSES, LECTURE, 
    PRACTICAL, TUTORIAL). 
    COURSES tab : Displays your matching results
    LECTURE tab : Displays the available lecture sections for your desired course
    PRACTICAL tab : Displays the availabe practical sections for your desired course 
    TUTORIAL tab : Displays the available tutorial sections for your desired course
        (all the above tabs will remain empty if there are no available sections)

    The 3rd page shows all the details of the courses which you have selected for your timetable.
    This page also allows you to delete some of them, if you don't want them in your timetable



    METHOS :
        __init__ :               
        create_timetable (self, grid) : 
        clear_timetable(self, widget, data = None) :
        gen_pdf(self, widget) :
        search(self, widget) :
        add_column_text(self, store, section_type, tab, callback_method, column_title_list ) :
        display_course_code (self, tab) :
        get_course_details (self, widget, path, data = None) :
        display_sections (self, dataframe, store, section_type) :
        update_timetable (self, widget, path, store, section_type) :
        add_to_timetable(self) :
        remove_course(self, widget, button) :
        set_active(self, widget, path, store, data) :
        add_to_catalog(self) :
        main_quit(self) :
    '''


    Label_list = []
    added_courses = []

    def __init__(self):
        '''
        Constructs a MyWindow instance . 
                
            @variables -
                
                (Gtk layout containers)

                header_bar :                                Gtk.HeaderBar       

                self.notebook :                             Gtk.NoteBook
-------------------------------------------------------------------------------                
YOUR TIMETABLE      page00_window :                         Gtk.ScrolledWindow 
                        page00 :                            Gtk.Grid
                            self.clear_all_button :         Gtk.Button
                            self.gen_pdf_button :           Gtk.Button
--------------------------------------------------------------------------------                            
SEARCH              page01 :                                Gtk.Grid
                        self.SearchBar :                    Gtk.Entry
                        self.SearchButton :                 Gtk.Button
                        self.page01_notebook :              Gtk.NoteBook
                            self.page01_courses_tab :       Gtk.ScrolledWindow
                            self.page01_lecture_tab :       Gtk.ScrolledWindow
                            self.page01_tutorial_tab :      Gtk.ScrolledWindow
                            self.page01_practical_tab :     Gtk.ScrolledWindow
--------------------------------------------------------------------------------                            
COURSE CATLOG       page02 :                                Gtk.Grid
                        self.page02_window :                Gtk.ScrolledWindow
                        self.remove_button :                Gtk.Button
---------------------------------------------------------------------------------
                
                Other variables : 
                    self.sobject : search.Searching () instance
                    self.lec_store, self.prac_store, self.tut_store  : Gtk.ListStore
                        (all are liststore for storing available course sections)
                    self.catalog_store : Gtk.Liststore 
                            This liststore contains information about the catalog page.
                    self.catalog_info : List
                            This is a list which also contains the information about the 
                            courses you are registered in.

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
        
        page00_window = Gtk.ScrolledWindow(hexpand = True, vexpand = True)
        page00 = Gtk.Grid()

        page00.set_row_homogeneous(True)
        page00.set_column_homogeneous(True)

        page00_window.add(page00)
        self.create_timetable(page00)
        self.notebook.append_page(page00_window, Gtk.Label("YOUR TIMETABLE"))

        
        page01 = Gtk.Grid()
        self.SearchBar = Gtk.Entry()
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

        
        self.lec_store = Gtk.ListStore(bool, str, str, str, str)
        self.prac_store = Gtk.ListStore(bool, str, str, str, str)
        self.tut_store = Gtk.ListStore(bool, str, str, str, str)

        self.page01_notebook.append_page(
            self.page01_course_tab, Gtk.Label("COURSE"))
        self.page01_notebook.append_page(
            self.page01_lec_tab, Gtk.Label("LECTURE") )
        self.page01_notebook.append_page(
            self.page01_prac_tab, Gtk.Label("PRACTICAL"))
        self.page01_notebook.append_page(
            self.page01_tut_tab, Gtk.Label("TUTORIAL"))

        self.notebook.append_page(page01, Gtk.Label("SEARCH"))

        self.page02 = Gtk.Grid()
        self.page02_window = Gtk.ScrolledWindow(hexpand = True, vexpand = True)
        self.page02.attach(child = self.page02_window, 
            left = 0, top = 0, width = 1, height = 1)

        self.remove_button = Gtk.Button(
            "SELECT THE COURSE YOU WANT TO DELETE AND PRESS THIS BUTTON TO CONTINUE")
        self.page02.attach_next_to(child = self.remove_button, 
            sibling = self.page02_window, 
            side = Gtk.PositionType(3), 
            width = 1, height = 1)


        
        self.remove_button.connect('clicked', self.remove_course)        
        self.catalog_store = Gtk.ListStore(bool, str, str, str, str, str, str)
        self.catalog_info = []
        self.notebook.append_page(self.page02, Gtk.Label('COURSE CATALOG'))


        self.menu = Gtk.Menu()

        clear_all_menu = Gtk.MenuItem("Clear all enteries")
        clear_all_menu.connect('activate', self.clear_timetable)

        gen_pdf_menu = Gtk.MenuItem('Generate pdf')
        gen_pdf_menu.connect('activate', self.gen_pdf)

        open_previous_menu = Gtk.MenuItem('Open your last work')
        open_previous_menu.connect('activate', self.open_last_work)

        self.menu.append(open_previous_menu)
        self.menu.attach(child = clear_all_menu,
            left_attach = 0, right_attach = 1,
            top_attach = 0, bottom_attach = 1)

        self.menu.attach(child = gen_pdf_menu,
            left_attach = 0, right_attach = 1,
            top_attach = 1, bottom_attach = 2)

        self.menu.attach(child = open_previous_menu,
            left_attach = 0, right_attach = 1,
            top_attach = 2, bottom_attach = 3)
        self.menu.show_all()

        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popup(self.menu)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('media/settings.png')
        pixbuf = pixbuf.scale_simple(32, 32, 2)
        
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.menu_button.set_image(image)

        self.notebook.append_page(Gtk.Label(), self.menu_button)

    def open_last_work(self, widget, *data) :
        self.clear_timetable(None)
        file = open('temp.txt', 'rb')

        data = pickle.load(file)
        for row in data :

            self.catalog_info.append(row)
            tt_info = row.split(';')

            days = tt_info[-2].split()
            hours = tt_info[-1].split()
            section = tt_info[2]
            course_code = tt_info[0]

            for i in range (len(hours)) :
                hours[i] = int(hours[i])

            self.text_to_display = course_code + '\n' + section
            self.add_to_timetable(hours, days)
            self.add_to_catalog()
            if course_code not in MyWindow.added_courses :
                MyWindow.added_courses.append(course_code)
            
        


    def create_timetable(self, grid) :
        '''
        Replaces your timetable to its initial state.
        This is a callback method for a Gtk.Button widget (self.clear_all_button). 

            @parameters :
                widget : Gtk widget object
                data : 
                    default = None 
                    Any additional data needed to be passed to the method.
        '''
        self.schedule = [
        ['HOURS/DAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        ['08 : 00 AM', '', '', '', '', '', ''],
        ['09 : 00 AM', '', '', '', '', '', ''],
        ['10 : 00 AM', '', '', '', '', '', ''],
        ['11 : 00 AM', '', '', '', '', '', ''],
        ['12 : 00 PM', '', '', '', '', '', ''],
        ['01 : 00 PM', '', '', '', '', '', ''],
        ['02 : 00 PM', '', '', '', '', '', ''],
        ['03 : 00 PM', '', '', '', '', '', ''],
        ['04 : 00 PM', '', '', '', '', '', '']]

        l = []
        for row in range (len(self.schedule)) :
            for col in range (len(self.schedule[row])) :
                label = Gtk.Label(label = self.schedule[row][col])
                grid.attach(child = label, left = col, top = row, width = 1, height = 1)
                l.append(label)
            MyWindow.Label_list.append(l)
            l = []

    def clear_timetable(self, widget, data = None) :
        '''
        Replaces your timetable to its initial state.
        This is a callback method for a Gtk.Button widget (self.clear_all_button). 

            @parameters :
                widget : Gtk widget object
                data : 
                    default = None 
                    Any additional data needed to be passed to the method.
        '''
        for row in range (len(MyWindow.Label_list)) :
            for col in range (len(MyWindow.Label_list[row])) :
                MyWindow.Label_list[row] [col].set_label(self.schedule[row][col]) 
        
        self.catalog_info = []
        self.catalog_store.clear()  
        MyWindow.added_courses = []   

    def gen_pdf(self, widget) :
        '''
        Saves your desired schedule in pdf format.
        This is a callback method for Gtk.Button widget (self.gen_pdf_button).

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
        if response == Gtk.ResponseType.ACCEPT :

            doc = SimpleDocTemplate(dialog.get_filename(), pagesize = letter)

            dialog.destroy()
            element = []

            headline = "WEEKLY SCHEDULE"

            style = getSampleStyleSheet()
            normal = style["Heading1"]

            para = Paragraph(headline, normal)
            element.append(para)

            user_data = copy.deepcopy(self.schedule)
            
            for row in range (len(MyWindow.Label_list)) :
                for col in range (len(MyWindow.Label_list[row])) :
                    user_data[row][col] =  MyWindow.Label_list[row][col].get_label()
                

            table = Table(data = user_data)
            table.setStyle(TableStyle([
                                    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                    ]))
            element.append(table)
            doc.build(element)
            self.save_list()
            self.clear_timetable(None)

        elif response == Gtk.ResponseType.CANCEL : 
            dialog.destroy()

    def search (self, widget) : 
        '''
        Usses self.sobject to search for courses matching your query.
        This is a callback method for a Gtk.Button widget (self.SearchButton).

        @variables :
            self.match_list : list 
                Contains a list of tuples having matching course_code and course_title as 
                tuple elements
                Returns self.match_list
        '''
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
                    Permitted values : LECTURE, PRACTICAL, TUTORIAL
            tab : Gtk.ScrolledWindow
                    Layout container in which details of the course is to be displayed.
            callback_method : callable method
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
        selection.set_mode(0)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.set_radio(False)
        renderer_toggle.connect("toggled", 
            callback_method, 
            store, section_type)


        radio_column  = Gtk.TreeViewColumn(" ", renderer_toggle)
        radio_column.add_attribute(renderer_toggle, 'active', 0)
        treeview.append_column(radio_column) 

        
        for i, column_title in enumerate(column_title_list) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(
                column_title, renderer, text=i+1)
            treeview.append_column(column)
        
        treeview.show_all()
        tab.add(treeview)

    def display_course_code(self, tab):
        '''
        Method for displaying course code on course_code tab on page01. 
            
            @variables :
                self.course_store : Gtk.ListStore 
                    store object for storing course details
        '''
        
        self.store = Gtk.ListStore(bool,str, str)
        self.add_column_text(
            self.store, ' ', tab, 
            self.get_course_details, 
            ["COURSE CODE", "COURSE TITLE"])
        
        for match in self.match_list :
            self.store.append([False] + list(match))        
        
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
        selected_path = Gtk.TreePath(path)
        for row in self.store:
            row[0] = (row.path == selected_path)

        self.selected_course_code = self.store[path][1]
        self.selected_course_title = self.store[path][2]
        match_parameter = (self.selected_course_code, self.selected_course_title)
        self.sobject.get_course_details(match_parameter)

        self.display_sections(
            dataframe = self.sobject.lecture, 
            tab = self.page01_lec_tab, 
            store = self.lec_store, 
            section_type = 'LEC')
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
            ["SECTION", "INSTRUCTOR", "DAYS", "HOURS"])
        if dataframe.empty :
            pass
            #store.append([False, ' ', ' ', ' ', ' '])

        else :
            count = 0   
            while count <= len(dataframe) - 1:  
                liststore_data_Section = dataframe.iloc[count][2] 
                liststore_data_Instructor = dataframe.iloc[count][3]
                liststore_data_days = dataframe.iloc[count][4]
                liststore_data_hours = dataframe.iloc[count][5]

                count += 1

                while count <= len(dataframe) - 1 and not dataframe.iloc[count][4]:
                    liststore_data_Instructor += '\n' + dataframe.iloc[count][3]
                    count += 1

                store.append([
                    False, liststore_data_Section, 
                    liststore_data_Instructor, 
                    liststore_data_days, 
                    liststore_data_hours])
                
    def update_timetable(self, widget, path, store, section_type) :
        '''
        This is a callback method for Gtk.CellRendererToggle object. This 
        method also adds dialog box if a course is clashing with other courses or 
        when you change sections of a already selected course. 

            @parameters :
                path : int
                    Row index of the treeview object which is selected.
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
        selected_path = Gtk.TreePath(path)
        for row in store:
            row[0] = (row.path == selected_path)
        
        self.selected_section = store[path][1]
        if not self.selected_section :
            self.selected_section = '1' 

        self.selected_instructor = store[path][2]
        self.selected_day = store[path][3].split()
        self.selected_hour = store[path][4].split()

        for i in range (len(self.selected_hour)) :
            self.selected_hour[i] = int(self.selected_hour[i])


        self.text_to_display = self.selected_course_code + '\n' + section_type + '-' + self.selected_section

        self.info = self.selected_course_code + ';' + \
         self.selected_course_title + ';' + \
         section_type + '-' + self.selected_section + ';' +\
         self.selected_instructor + ';' +\
         store[path][3] + ';' + store[path][4]


        if self.selected_course_code not in MyWindow.added_courses :
            flag = 0
            for row in self.selected_hour :
                for col in self.selected_day :
                    if col == 'M' : 
                        text = MyWindow.Label_list[row][1].get_label() 
                    elif col == 'T' :
                        text = MyWindow.Label_list[row][2].get_label() 
                    elif col == 'W' :
                        text = MyWindow.Label_list[row][3].get_label() 
                    elif col == 'Th' :
                        text = MyWindow.Label_list[row][4].get_label() 
                    elif col == 'F' :
                        text = MyWindow.Label_list[row][5].get_label() 
                    elif col == 'S' :
                        text = MyWindow.Label_list[row][6].get_label() 
                    if flag == 0 :
                        if text :
                            dialog = Gtk.MessageDialog(self, 0, 
                            Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.YES_NO, 
                            "Warning : You cannot have 2 classes at the same time !!")

                            dialog.format_secondary_text(
                                "Do you want to replace this course ?")

                            response = dialog.run()

                            if response == Gtk.ResponseType.YES :
                                MyWindow.added_courses.append(self.selected_course_code)
                                self.add_to_timetable(self.selected_hour, self.selected_day)

                                for index in self.catalog_info :
                                    if text.split('\n')[0] in index \
                                    and text.split('\n')[1] in index :
                                        self.catalog_info.remove(index)
                                        self.catalog_info.insert(0, self.info)
                                        break

                            elif response == Gtk.ResponseType.NO :
                                pass

                            flag = 1                            
                            dialog.destroy()
                        else :
                            MyWindow.added_courses.append(self.selected_course_code)
                            self.add_to_timetable(self.selected_hour, self.selected_day)
                            self.catalog_info.insert(0, self.info)
                            break
                    else :
                        break

        else :
            flag = 0
            for row in range (len(MyWindow.Label_list)) :
                for col in range (len(MyWindow.Label_list[row])) :
                    
                    text = MyWindow.Label_list[row][col].get_label()
                    
                    if self.selected_course_code in text \
                        and section_type in text :

                        flag = 1
                        break

            if flag == 1 :
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                    Gtk.ButtonsType.YES_NO, 
                    "Warning : You are about to change a section !")
                dialog.format_secondary_text("Do you wish to continue ?")

                response = dialog.run()

                if response == Gtk.ResponseType.YES :
                    
                    for row in range (len(MyWindow.Label_list)) :
                        for col in range (len(MyWindow.Label_list[row])) :
                            text = MyWindow.Label_list[row][col].get_label()

                            if self.selected_course_code in text \
                                and section_type in text :
                                MyWindow.Label_list[row][col].set_label(' ')
                                self.add_to_timetable(self.selected_hour, self.selected_day)

                                for index in self.catalog_info :
                                    if text.split('\n')[0] in index \
                                    and text.split('\n')[1] in index :
                                        self.catalog_info.remove(index)
                                        self.catalog_info.insert(0, self.info)
                                        break

                elif response == Gtk.ResponseType.NO :
                    pass


                dialog.destroy()
            
            else :
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)

        self.add_to_catalog()

    def add_to_timetable(self, hours, days) :
        '''
            Adds the selected section to the timetable.
        '''
        for row in hours :
            for col in days : 
                if col == 'M' : 
                    MyWindow.Label_list[row][1].set_label(self.text_to_display)
                elif col == 'T' : 
                    MyWindow.Label_list[row][2].set_label(self.text_to_display)
                elif col == 'W' : 
                    MyWindow.Label_list[row][3].set_label(self.text_to_display)
                elif col == 'Th' : 
                    MyWindow.Label_list[row][4].set_label(self.text_to_display)
                elif col == 'F' : 
                    MyWindow.Label_list[row][5].set_label(self.text_to_display)
                elif col == 'S' : 
                    MyWindow.Label_list[row][6].set_label(self.text_to_display)


    def remove_course(self, widget, data = None) :
        '''
        This method is called to remove the courses selected in the catalog page. This 
        is also a callback method for Gtk.Button (self.remove_button). This method also shows 
        dialog box warning the user to confirm before removing a course.
        '''

        for row in self.catalog_store :
            if row[0] == True :
                remove_course_code = row[1]
                remove_section = row[3]
                remove_hour = row[-1]
                remove_day = row[-2]

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
                                MyWindow.Label_list[int(row)][1].set_label('')
                            elif col == 'T' :
                                MyWindow.Label_list[int(row)][2].set_label('')
                            elif col == 'W' :
                                MyWindow.Label_list[int(row)][3].set_label('')
                            elif col == 'Th' :
                                MyWindow.Label_list[int(row)][4].set_label('')
                            elif col == 'F' :
                                MyWindow.Label_list[int(row)][5].set_label('')
                            elif col == 'S' :
                                MyWindow.Label_list[int(row)][6].set_label('')


                    count = 0
                    for strings in self.catalog_info :
                        if remove_course_code in strings :
                            count += 1

                        if remove_course_code in strings \
                        and remove_section in strings :
                            self.catalog_info.remove(strings)
                    
                    if count == 1:
                        MyWindow.added_courses.remove(remove_course_code)

                    self.add_to_catalog()
                    dialog.destroy()
                    break
                
                elif response == Gtk.ResponseType.CANCEL:
                    dialog.destroy()


    def set_active(self, widget, path, store, *data) :
        '''
        This method activates the desired row in the catalog_store. This is a callback 
        method for CellRendererToggle (in the Catalog page).

            @parameters :
                path : int 
                    Contains the index of the selected row from the catalog_store
                store : Gtk.ListStore
                data : default = None
                    Other data can be passed to this parameter if the method needs it.

            @variables :
                selected_path : Gtk.TreePath
        '''
        selected_path = Gtk.TreePath(path)
        for row in store:
            row[0] = (row.path == selected_path)
        


    def add_to_catalog(self) :
        '''
        This method updates content present in the catalog_info list to 
            catalog_store.
        '''
        self.add_column_text(
            self.catalog_store, None,
            self.page02_window, self.set_active,
            ['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR', 'DAYS', 'HOURS'])
    

        for row in self.catalog_info :
            self.catalog_store.append([False] + row.split(';'))

    def main_quit(self, widget, event) :
        '''
        Adds custom quit method for the application. 
        Shows a dialog box if there is unsaved work.
        '''
        if len(MyWindow.added_courses) != 0 :
            dialog = Gtk.MessageDialog(self, 0,
                Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                'You have unsaved work.')

            dialog.format_secondary_text(
                'Press YES to Save or No to Quit')

            response = dialog.run()

            if response == Gtk.ResponseType.YES :
                self.gen_pdf(None)
            elif response == Gtk.ResponseType.NO :
                self.save_list()

            dialog.destroy()
        else :
            pass

        Gtk.main_quit()

    def save_list(self) :
        with open('temp.txt', 'wb') as f :
            pickle.dump(self.catalog_info, f)                
            f.close()




        




        

