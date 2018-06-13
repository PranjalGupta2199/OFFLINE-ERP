import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import search
import pandas

class MyWindow(Gtk.Window):
    Label_list = []

    def __init__(self):
        self.sobject = search.Searching()
        super(MyWindow, self).__init__(title = "OFFLINE ERP")
        self.set_size_request(400, 400)
     	self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        page00 = Gtk.Grid()
        page01 = Gtk.Grid()

        page00.set_row_homogeneous(True)
        page00.set_column_homogeneous(True)


        self.create_timetable(page00)
        self.notebook.append_page(page00, Gtk.Label("YOUR TIMETABLE"))

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





    def search (self, widget) : 
        self.match_list = self.sobject.get_result(query = self.SearchBar.get_text())
        self.display_course_code(self.page01_course_tab)


    def add_column_text(self, store, tab, callback_method, column_title_list) :
        if tab.get_child() != None :
            store.clear()
            tab.remove(tab.get_child())
            
        
        treeview = Gtk.TreeView(model = store)
        selection = treeview.get_selection()
        selection.set_mode(0)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.set_radio(True)
        renderer_toggle.connect("toggled", callback_method, store)


        selected_section = Gtk.TreeViewColumn(" ", renderer_toggle)
        selected_section.add_attribute(renderer_toggle, 'active', 0)
        treeview.append_column(selected_section) 

        
        for i, column_title in enumerate(column_title_list) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            treeview.append_column(column)
        
        treeview.show_all()
        tab.add(treeview)


    def display_course_code(self, tab):
        
        self.store = Gtk.ListStore(bool,str, str)
        self.add_column_text(self.store, tab, self.get_course_details, ["COURSE CODE", "COURSE TITLE"])
        
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

        self.display_sections(dataframe = self.sobject.lecture, tab = self.page01_lec_tab, store = self.lec_store)
        self.display_sections(dataframe = self.sobject.practical, tab = self.page01_prac_tab, store = self.prac_store)
        self.display_sections(dataframe = self.sobject.tutorial, tab = self.page01_tut_tab, store = self.tut_store)

    def display_sections (self, dataframe, tab, store) :
         ##Radio_button, sec, instructor(s), days, hours
        self.add_column_text(store, tab, self.update_timetable, ["SECTION", "INSTRUCTOR", "DAYS", "HOURS"])
        if dataframe.empty :
            store.append([False, ' ', ' ', ' ', ' '])

        else :
            count = 0   
            while count <= len(dataframe) - 1:  
                liststore_data_Section = dataframe.iloc[count][2] 
                liststore_data_Instructor = dataframe.iloc[count][3]
                liststore_data_days = dataframe.iloc[count][4]
                liststore_data_hours = dataframe.iloc[count][5]

                count += 1

                while count < len(dataframe) - 1 and not dataframe.iloc[count][4]:
                    liststore_data_Instructor += '\n' + dataframe.iloc[count][3]
                    count += 1

                store.append([False, liststore_data_Section, liststore_data_Instructor, liststore_data_days, liststore_data_hours])
                



    def update_timetable(self, widget, path, store) :
        selected_path = Gtk.TreePath(path)
        for row in store:
            row[0] = (row.path == selected_path)
        
        self.selected_instructor = store[path][2]
        self.selected_hour = store[path][4].split()
        self.selected_day = store[path][3].split()

        for i in range (len(self.selected_hour)) :
            self.selected_hour[i] = int(self.selected_hour[i])


        self.text = self.selected_course_code + '\n' + self.selected_course_title + '\n' + self.selected_instructor 

        for row in self.selected_hour : 
            for col in self.selected_day : 
                if col == "M" : MyWindow.Label_list[row][1].set_label(self.text)
                elif col == 'T' : MyWindow.Label_list[row][2].set_label(self.text)
                elif col == 'W' : MyWindow.Label_list[row][3].set_label(self.text)
                elif col == 'Th' : MyWindow.Label_list[row][4].set_label(self.text)
                elif col == 'F' : MyWindow.Label_list[row][5].set_label(self.text)
                elif col == 'S' : MyWindow.Label_list[row][6].set_label(self.text)

        

