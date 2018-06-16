import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import search
import pandas


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph



class MyWindow(Gtk.Window):
    Label_list = []
    added_courses = []

    def __init__(self):

        super(MyWindow, self).__init__(title = "OFFLINE ERP")
        self.set_size_request(1000, 500)
     	self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.maximize()



        self.sobject = search.Searching()

        page00_window = Gtk.ScrolledWindow(hexpand = True, vexpand = True)
        page00 = Gtk.Grid()
        page00_window.add(page00)
        
        page01 = Gtk.Grid()


        self.page02 = Gtk.Grid()

        page00.set_row_homogeneous(True)
        page00.set_column_homogeneous(True)

        self.clear_all_button = Gtk.Button("Clear All")
        self.clear_all_button.connect('clicked', self.clear_timetable)
        page00.attach(child = self.clear_all_button, left = 0, top = 11, width = 2, height = 1)

        self.gen_pdf_button = Gtk.Button("Generate pdf")
        self.gen_pdf_button.connect('clicked', self.gen_pdf)
        page00.attach(child = self.gen_pdf_button, left = 6, top = 11, width = 2, height = 1)

        self.create_timetable(page00)
        self.notebook.append_page(page00_window, Gtk.Label("YOUR TIMETABLE"))

        self.SearchBar = Gtk.Entry()
        
        page01.attach(child = self.SearchBar, left = 1, top = 1, width = 4, height = 1)
     
        self.SearchButton = Gtk.Button("GO !")
        self.SearchButton.connect('clicked', self.search)

        page01.attach_next_to(child = self.SearchButton, sibling = self.SearchBar, side = Gtk.PositionType(1), width = 1, height = 1)
     	
        self.page01_notebook = Gtk.Notebook()
        self.page01_course_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_lec_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_tut_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        self.page01_prac_tab = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        
        self.lec_store = Gtk.ListStore(bool, str, str, str, str)
        self.prac_store = Gtk.ListStore(bool, str, str, str, str)
        self.tut_store = Gtk.ListStore(bool, str, str, str, str)

        self.page01_notebook.append_page(self.page01_course_tab, Gtk.Label("COURSE"))
        self.page01_notebook.append_page(self.page01_lec_tab, Gtk.Label("LECTURE") )
        self.page01_notebook.append_page(self.page01_prac_tab, Gtk.Label("PRACTICAL"))
        self.page01_notebook.append_page(self.page01_tut_tab, Gtk.Label("TUTORIAL"))

        page01.attach_next_to(child = self.page01_notebook, sibling = self.SearchBar, side = Gtk.PositionType(3), width = 1, height = 1)

        self.notebook.append_page(page01, Gtk.Label("SEARCH"))
        self.notebook.append_page(self.page02, Gtk.Label("YOUR COURSES"))
    
    def create_timetable(self, grid) :
        self.schedule = [
        ['HOURS/DAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        ['08:00 AM', ' ', ' ', ' ', ' ', ' ',' '],
        ['09:00 AM', ' ', ' ', ' ', ' ', ' ',' '],
        ['10 : 00 AM', ' ', ' ', ' ', ' ', ' ',' '],
        ['11 : 00 AM', ' ', ' ', ' ', ' ', ' ',' '],
        ['12 : 00 PM', ' ', ' ', ' ', ' ', ' ',' '],
        ['01 : 00 PM', ' ', ' ', ' ', ' ', ' ',' '],
        ['02 : 00 PM', ' ', ' ', ' ', ' ', ' ',' '],
        ['03 : 00 PM', ' ', ' ', ' ', ' ', ' ',' '],
        ['04 : 00 PM', ' ', ' ', ' ', ' ', ' ',' ']]

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

        self.page02_info = []
        self.update_page()
    def gen_pdf(self, widget) : 
        doc = SimpleDocTemplate("TIMETABLE.pdf", pagesize = letter)
        element = []

        headline = "WEEKLY SCHEDULE"

        style = getSampleStyleSheet()
        normal = style["Heading1"]

        para = Paragraph(headline, normal)
        element.append(para)

        user_data = self.schedule
        
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


    def add_column_text(self, store, section_type,tab, callback_method, column_title_list) :
        if tab.get_child() != None :
            store.clear()
            tab.remove(tab.get_child())
            
        
        treeview = Gtk.TreeView(model = store)
        selection = treeview.get_selection()
        selection.set_mode(0)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.set_radio(True)
        renderer_toggle.connect("toggled", callback_method, store, section_type)


        radio_column  = Gtk.TreeViewColumn(" ", renderer_toggle)
        radio_column.add_attribute(renderer_toggle, 'active', 0)
        treeview.append_column(radio_column) 

        
        for i, column_title in enumerate(column_title_list) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            treeview.append_column(column)
        
        treeview.show_all()
        tab.add(treeview)


    def display_course_code(self, tab):
        
        self.store = Gtk.ListStore(bool,str, str)
        self.add_column_text(self.store, ' ', tab, self.get_course_details, ["COURSE CODE", "COURSE TITLE"])
        
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

        self.display_sections(dataframe = self.sobject.lecture, tab = self.page01_lec_tab, store = self.lec_store, section_type = 'LECTURE')
        self.display_sections(dataframe = self.sobject.practical, tab = self.page01_prac_tab, store = self.prac_store, section_type = 'PRACTICAL')
        self.display_sections(dataframe = self.sobject.tutorial, tab = self.page01_tut_tab, store = self.tut_store, section_type = 'TUTORIAL')

    def display_sections (self, dataframe, tab, store, section_type) :
         ##Radio_button, sec, instructor(s), days, hours
        self.add_column_text(store, section_type, tab, self.update_timetable, ["SECTION", "INSTRUCTOR", "DAYS", "HOURS"])
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

                store.append([False, liststore_data_Section, liststore_data_Instructor, liststore_data_days, liststore_data_hours])
                



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


        self.text_to_display = self.selected_course_code + '\n' + section_type[0] + '-' + self.selected_section
        
        info = self.selected_course_code + '-' + self.selected_course_title + '-' + section_type[0]  + self.selected_section + '-' + self.selected_instructor + '-' + store[path][3] + '-' + store[path][4] 

        for row in self.page02_info :
            row_list = row.split('-')
            row_list_sec_info = row_list[2] 

            if self.selected_course_code == row_list[0] :
                if row_list_sec_info[0] == section_type[0] :
                    self.page02_info.remove(row)
                    self.page02_info.append(info)
                    break
        else :
            self.page02_info.append(info)

        if self.selected_course_code not in MyWindow.added_courses : 
            MyWindow.added_courses.append(self.selected_course_code)
        else :
            for row in range (len(MyWindow.Label_list)) :
                for col in range (len(MyWindow.Label_list[row])) :
                    if self.selected_course_code in MyWindow.Label_list[row][col].get_label()\
                    and section_type in MyWindow.Label_list[row][col].get_label() :
                        MyWindow.Label_list[row][col].set_label(' ')

        for row in self.selected_hour : 
            for col in self.selected_day : 
                if col == "M" : MyWindow.Label_list[row][1].set_label(self.text_to_display)
                elif col == 'T' : MyWindow.Label_list[row][2].set_label(self.text_to_display)
                elif col == 'W' : MyWindow.Label_list[row][3].set_label(self.text_to_display)
                elif col == 'Th' : MyWindow.Label_list[row][4].set_label(self.text_to_display)
                elif col == 'F' : MyWindow.Label_list[row][5].set_label(self.text_to_display)
                elif col == 'S' : MyWindow.Label_list[row][6].set_label(self.text_to_display)
        self.update_page()


    def update_page(self) :
        page02_store = Gtk.ListStore(str, str, str, str, str, str)

        for info in self.page02_info :
            page02_store.append(info.split('-'))

        treeview = Gtk.TreeView(model = page02_store)
        selection = treeview.get_selection()
        selection.set_mode(1)
        
        for i, column_title in enumerate(['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR', 'DAYS', 'HOURS']) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            treeview.append_column(column)
        
        treeview.show_all()
        if self.page02.get_children() :
            self.page02.remove(self.page02.get_children()[0])
        self.page02.attach(child = treeview, left = 0, top = 0, width = 1, height = 1)
        
        self.remove_button = Gtk.Button('Remove selected')
        self.remove_button.connect('clicked', self.remove_course, selection)
        self.page02.attach_next_to(child = self.remove_button, sibling = treeview, side = Gtk.PositionType(3), width = 3, height = 1)


    def remove_course(self, widget, selection) :
        tree_model, tree_iter = selection.get_selected()

        if tree_iter is not None :
            row_contents = tree_model[tree_iter]
            print row_contents










        

