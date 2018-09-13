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
            and self.selected_course_code != row[0] :
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
            store.append(['NA', 'NA', 'NA', '0'])

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
                    liststore_data_Section, 
                    liststore_data_Instructor, 
                    liststore_data_days, 
                    liststore_data_hours])


    def add_to_catalog(self) :
        '''
        This method updates content present in the catalog_info list to 
            catalog_store.
        '''
        self.add_column_text(
            self.catalog_store, None,
            self.page02_window, self.remove_course,
            ['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR', 'DAYS', 'HOURS', 'COMPRE DATE'])

        self.catalog_info.sort()
        for row in self.catalog_info :
            self.catalog_store.append(row.split(';'))


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
