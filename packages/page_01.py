import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import search
import pandas
import copy

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph



class MyWindow(Gtk.Window):
    '''
    This class is for creating gui for the second page of the application.
    The main window consists of 2 main pages (YOUR TIMETABLE , SEARCH). 

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



    METHOS :
        __init__ : 

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
                
        create_timetable (self, grid) : 
            Creates the schedule and displays on the window 
                    
                    @variables :
                        self.schedule : An array containing the basic 
                                structure of your timetable

                        MyWindow.Label_list : <class-variables>
                                Stores Gtk.Label() objects which display 
                                your schedule on the window

        clear_timetable(self, widget, data = None) :
            Replaces your timetable to its initial state.
            This is a callback method for a Gtk.Button widget (self.clear_all_button). 

                @parameters :
                    widget : Gtk widget object
                    data : 
                        default = None 
                        Any additional data needed to be passed to the method.

        gen_pdf(self, widget) :
            Saves your desired schedule in pdf format.
            This is a callback method for Gtk.Button widget (self.gen_pdf_button).
            
            This method uses a special Python library known as 'reportlab' which is 
            used for writing/reading in pdf files. For more information  :
                
                http://www.blog.pythonlibrary.org/2010/09/21/reportlab-tables-creating-tables-in-pdfs-with-python/
                https://www.reportlab.com/opensource/installation/
                https://www.reportlab.com/docs/reportlab-userguide.pdf

        
        search(self, widget) :
            Usses self.sobject to search for courses matching your query.
            This is a callback method for a Gtk.Button widget (self.SearchButton).

            @variables :
                self.match_list : list 
                    Contains a list of tuples having matching course_code and course_title as 
                    tuple elements
                    Returns self.match_list

        add_column_text(self, store, section_type, tab, callback_method, column_title_list ) :
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

        display_course_code (self, tab) :
            Method for displaying course code on course_code tab on page01. 
                
                @variables :
                    self.course_store : Gtk.ListStore 
                        store object for storing course details

        get_course_details (self, widget, path, data = None) :
            Uses sobject to get lecture, tutorial and practical dataframe objects.
            This is a callback method for Gtk.CellRendererToggle Object.

                @variables :
                    selected_path : Gtk.TreePath object
                        Changes the state (True/False) of the selected row of treeview.

                @parameters :
                    path : int
                        Integer whose value is the row index of the treeview object.

        display_sections (self, dataframe, store, section_type) :
            This method is used for displaying all the data of a course.

                @parameters :
                    dataframe : pandas.DataFrame object
                        Contains details of the all the available sections 
                    store : Gtk.ListStore object

                    section_type : str
                        Contains the string value for type of section 

        update_timetable (self, widget, path, store, section_type) :
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
        
        add_to_timetable(self) :
            Adds the selected section to the timetable.
        
        remove_course(self, widget, button) :
            This method is called to remove the courses selected in the catalog page. This 
            is also a callback method for Gtk.Button (self.remove_button). This method also shows 
            dialog box warning the user to confirm before removing a course.

        set_active(self, widget, path, store, data) :
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

        add_to_catalog(self) :
            This method updates content present in the catalog_info list to 
            catalog_store.
    '''


    Label_list = []
    added_courses = []

    def __init__(self):
        super(MyWindow, self).__init__(title = "OFFLINE ERP")
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

        self.clear_all_button = Gtk.Button("Clear All")
        self.clear_all_button.connect('clicked', self.clear_timetable)
        page00.attach(child = self.clear_all_button, left = 0, 
                    top = 11, width = 2, height = 1)

        self.gen_pdf_button = Gtk.Button("Generate pdf")
        self.gen_pdf_button.connect('clicked', self.gen_pdf)
        page00.attach(child = self.gen_pdf_button, left = 6, 
                    top = 11, width = 2, height = 1)

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
            "Select the coure you want to delete and press this button to continue")
        self.page02.attach_next_to(child = self.remove_button, 
            sibling = self.page02_window, 
            side = Gtk.PositionType(3), 
            width = 1, height = 1)


        
        self.remove_button.connect('clicked', self.remove_course)        
        self.catalog_store = Gtk.ListStore(bool, str, str, str, str, str, str)
        self.catalog_info = []
        self.notebook.append_page(self.page02, Gtk.Label('COURSE CATALOG'))

    def create_timetable(self, grid) :
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
        for row in range (len(MyWindow.Label_list)) :
            for col in range (len(MyWindow.Label_list[row])) :
                MyWindow.Label_list[row] [col].set_label(self.schedule[row][col]) 
        
        self.catalog_info = []
        self.catalog_store.clear()     

    def gen_pdf(self, widget) : 
        doc = SimpleDocTemplate("TIMETABLE.pdf", pagesize = letter)
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

    def search (self, widget) : 
        self.match_list = self.sobject.get_result(query = self.SearchBar.get_text())
        self.display_course_code(self.page01_course_tab)

    def add_column_text(
        self, store, 
        section_type, tab, 
        callback_method, column_title_list) :
        
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
        
        self.store = Gtk.ListStore(bool,str, str)
        self.add_column_text(
            self.store, ' ', tab, 
            self.get_course_details, 
            ["COURSE CODE", "COURSE TITLE"])
        
        for match in self.match_list :
            self.store.append([False] + list(match))        
        
    def get_course_details(self, widget, path, *data) :
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
                                self.add_to_timetable()

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
                            self.add_to_timetable()
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
                                self.add_to_timetable()

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
                self.add_to_timetable()
                self.catalog_info.insert(0, self.info)

        self.add_to_catalog()

    def add_to_timetable(self) :

        for row in self.selected_hour : 
            for col in self.selected_day : 
                if col == "M" : 
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
        selected_path = Gtk.TreePath(path)
        for row in store:
            row[0] = (row.path == selected_path)
        


    def add_to_catalog(self) :
        self.add_column_text(
            self.catalog_store, None,
            self.page02_window, self.set_active,
            ['COURSE CODE', 'COURSE TITLE', 'INSTRUCTOR', 'SECTION', 'DAYS', 'HOURS'])
    

        for row in self.catalog_info :
            self.catalog_store.append([False] + row.split(';'))



        




        

