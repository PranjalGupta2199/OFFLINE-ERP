import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import search

class MyWindow(Gtk.Window):
    RadioButton_list = []

    def __init__(self):
        self.sobject = search.Searching()
        super(MyWindow, self).__init__(title = "OFFLINE ERP")
        self.set_size_request(400, 400)
     	self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        page00 = Gtk.Grid()
        page01 = Gtk.Grid()
        #page01.set_column_homogeneous(True)
        #page01.set_row_homogeneous(True)
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
        
        self.page01_notebook.append_page(self.page01_course_tab, Gtk.Label("COURSE"))
        self.page01_notebook.append_page(self.page01_lec_tab, Gtk.Label("LECTURE") )
        self.page01_notebook.append_page(self.page01_prac_tab, Gtk.Label("PRACTICAL"))
        self.page01_notebook.append_page(self.page01_tut_tab, Gtk.Label("TUTORIAL"))

        page01.attach_next_to(child = self.page01_notebook, sibling = self.SearchBar, side = Gtk.PositionType(3), width = 1, height = 1)

        self.notebook.append_page(page01, Gtk.Label("SEARCH"))
    
    def search (self, widget) : 
        self.match_list = self.sobject.get_result(query = self.SearchBar.get_text())
        self.display_course_code()

    def display_course_code(self):
        try:
            self.page01_course_tab.remove(self.page01_course_tab.get_child())
        except:
            pass
        
        
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.set_radio(False)
        renderer_toggle.connect("toggled", self.get_course_details)

        self.store = Gtk.ListStore(bool,str, str)

        for match in self.match_list :
            self.store.append([True] + list(match))

        treeview = Gtk.TreeView(model = self.store)
        selection = treeview.get_selection()
        selection.set_mode(0)

        selected_section = Gtk.TreeViewColumn("", renderer_toggle)
        treeview.append_column(selected_section)

        for i, column_title in enumerate(["COURSE CODE", "COURSE TITLE"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            treeview.append_column(column)
        

        treeview.show_all()
        self.page01_course_tab.add(treeview)
        

    def get_course_details(self, widget, path) :
        selected_course_code = self.store[path][1]
        selected_course_title = self.store[path][2]
        match_parameter = (selected_course_code, selected_course_title)
        self.sobject.get_course_details(match_parameter)

        self.display_sections(self.sobject.lecture, self.page01_lec_tab)
        self.display_sections(self.sobject.practical, self.page01_prac_tab)
        self.display_sections(self.sobject.tutorial, self.page01_tut_tab)

    def display_sections (self, dataframe, tab) :
        try:
            tab.remove(tab.get_child())
        except:
            pass
        self.sec_store = Gtk.ListStore(bool, str, str, str, str) ##Radio_button, sec, instructor(s), days, hours

        try :
            if not dataframe :
                self.sec_store.append([False, ' ', ' ', ' ', ' '])                
        except:
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

                self.sec_store.append([False, liststore_data_Section, liststore_data_Instructor, liststore_data_days, liststore_data_hours])


        treeview = Gtk.TreeView(model = self.sec_store)
        

        renderer_radio = Gtk.CellRendererToggle()
        renderer_radio.set_radio(True)
        renderer_radio.connect("toggled", self.add_to_timetable)

        column_radio = Gtk.TreeViewColumn(" ", renderer_radio)
        treeview.append_column(column_radio)
		
        for i, column_title in enumerate(["SECTION", "INSTRUCTOR", "DAYS", "HOURS"]) :
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            treeview.append_column(column)
        treeview.show_all()

        tab.add(treeview)


    def add_to_timetable(self, widget) :
        print 'working'








