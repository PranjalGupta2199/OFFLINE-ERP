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

     	self.notebook.append_page(page00, Gtk.Label("YOUR TIMETABLE"))

     	self.SearchBar = Gtk.Entry()
        
        page01.attach(child = self.SearchBar, left = 1, top = 1, width = 7, height = 1)
     
        self.SearchButton = Gtk.Button("GO !")
        self.SearchButton.connect('clicked', self.search)
     	page01.attach_next_to(child = self.SearchButton, sibling = self.SearchBar, side = Gtk.PositionType(1), width = 2, height = 1)
     	

        self.page01_notebook = Gtk.Notebook()
        self.page01_course_tab = Gtk.Box()

        self.page01_lec_tab = Gtk.Box()
        self.display_sections(self.sobject.lecture, self.page01_lec_tab)
        self.page01_tut_tab = Gtk.Box()
        self.display_sections(self.sobject.tutorial, self.page01_tut_tab)
        self.page01_prac_tab = Gtk.Box()
        self.display_sections(self.sobject.practical, self.page01_prac_tab)
        
        self.page01_notebook.append_page(self.page01_course_tab, Gtk.Label("COURSE"))
        self.page01_notebook.append_page(self.page01_lec_tab, Gtk.Label("LECTURE") )
        self.page01_notebook.append_page(self.page01_prac_tab, Gtk.Label("PRACTICAL"))
        self.page01_notebook.append_page(self.page01_tut_tab, Gtk.Label("TUTORIAL"))

        page01.attach_next_to(child = self.page01_notebook, sibling = self.SearchBar, side = Gtk.PositionType(3), width = 2, height = 1)

        self.notebook.append_page(page01, Gtk.Label("SEARCH"))
    
    def search (self, widget) : 
        self.match_list = self.sobject.get_result(query = self.SearchBar.get_text())
        self.display_course_code(self.page01_course_tab)

    def display_course_code(self, tab):
        liststore = Gtk.ListStore(bool, str, str)

        liststore_data_course_code = ' '
        liststore_data_course_title = ' ' 
        for match in self.match_list : 
        	liststore_data_course_code = match[0]
        	liststore_data_course_title = match[1]
        	liststore.append([False, liststore_data_course_code, liststore_data_course_title])

        treeview = Gtk.TreeView(model = liststore)

        renderer_radio = Gtk.CellRendererToggle()
        renderer_radio.set_radio(True)
        renderer_radio.connect("toggled", self.get_course_details)

        column_radio = Gtk.TreeViewColumn(" ", renderer_radio)
        treeview.append_column(column_radio)

        for column in ["COURSE CODE", "COURSE_TITLE"] :
            renderer_text = Gtk.CellRendererText()
            column_text = Gtk.TreeViewColumn(column, renderer_text)
            treeview.append_column(column_text)
        
        tab.pack_start(treeview, False, False, 0)



    def get_course_details(self, widget) :
        text = widget.get_label()
        match_parameter = tuple(text.split(" "))
        
        self.sobject.get_course_details(match_parameter)

    def display_sections (self, list_, tab) :
		liststore = Gtk.ListStore(bool, str, str, str, str) ##Radio_button, sec, instructor(s), days, hours
		
		count = -1
		liststore_data_Section = " "
		liststore_data_Instructor = " "
		liststore_data_days = " "
		liststore_data_hours = " "

		while count < len(list_) - 1 :
			item = list_[count + 1]
			liststore_data_Section = list_[1]
			liststore_data_Instructor = list_[2]
			liststore_data_days = list_[3]
			liststore_data_hours = list_[4]

			try:
				while not next(item[1]) :
					liststore_data_Instructor += '\n' + next(item[2])
					item = next(item)
					count += 1
			except :
				pass

		liststore.append([False, liststore_data_Section, liststore_data_Instructor, liststore_data_days, liststore_data_hours])

		treeview = Gtk.TreeView(model = liststore)
		tab.pack_start(treeview, False, False, 0)

		renderer_radio = Gtk.CellRendererToggle()
		renderer_radio.set_radio(True)
		renderer_radio.connect("toggled", self.add_to_timetable)

		column_radio = Gtk.TreeViewColumn(" ", renderer_radio)
		treeview.append_column(column_radio)
		
		for column in ["SECTION", "INSTRUCTOR(S), DAYS, HOURS"] :
			renderer_text = Gtk.CellRendererText()
        	column_text = Gtk.TreeViewColumn(column, renderer_text)
        	treeview.append_column(column_text)



    def add_to_timetable(self, widget) :
    	pass








