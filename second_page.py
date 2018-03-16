import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Offline ERP")
        self.connect('delete-event', Gtk.main_quit)
        #self.set_size_request(200, 500)
        #self.set_default_size(500, 800)
        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.set_border_width(20)
        self.grid.set_row_homogeneous(False)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)

        course_list = Gtk.ListStore(str)  # contains only the subject name
        '''create a parsed list from the pdf and then append them to the ListStore'''

        course_combo = Gtk.ComboBox.new_with_model(course_list)
        # course_combo.connect('changed', #call_back_method)
        course_combo.set_entry_text_column(0)
        self.grid.attach(course_combo, 0, 0, 8, 1)

        sub_code = Gtk.Label('Course Number :')
        sub_code_value = Gtk.Label()  # will contain the course number of the selected course from course_combo
        course_name = Gtk.Label("Course Title :")
        course_name_value = Gtk.Label()  # same as sub_code_value

        self.grid.attach(sub_code, 0, 1, 1, 1)
        self.grid.attach(sub_code_value, 1, 1, 1, 1)
        self.grid.attach(course_name, 2, 1, 1, 1)
        self.grid.attach(course_name_value, 3, 1, 1, 1)
        #self.grid.attach_next_to(sub_code_value, sub_code, Gtk.PositionType.RIGHT, 1, 1)
        #self.grid.attach_next_to(course_name, sub_code_value, Gtk.PositionType.RIGHT, 1, 1)
        #self.grid.attach_next_to(course_name_value, course_name, Gtk.PositionType.RIGHT, 1, 1)

        self.parent_box = Gtk.Box()
        self.window = Gtk.ScrolledWindow(hexpand = True , vexpand = True)

        self.window.set_size_request(150,150)


        tutorial_view, tutorial_store = 0, 0
        lecture_store, lecture_view = 0, 0
        practical_store, practical_view = 0, 0

        lecture = self.selection_view(lecture_store, lecture_view)
        tutorial = self.selection_view(tutorial_store, tutorial_view)
        practical = self.selection_view(practical_store, practical_view)

        self.window.add(self.parent_box)
        self.grid.attach(self.window, 0, 2, 8, 5)
        self.timetable_view()

        empty_label = Gtk.Label()
        self.grid.attach(empty_label, 0, 17, 1 , 1)
        Exit_button = Gtk.Button()
        Exit_button.set_label("Exit")
        self.grid.attach(Exit_button, 0, 18, 1, 1)

        pdf_generate_button = Gtk.Button()
        pdf_generate_button.set_label("Generate Pdf of your timetable")
        self.grid.attach_next_to(pdf_generate_button, Exit_button, Gtk.PositionType.RIGHT, 3, 1)

        credits_label = Gtk.Label("Total credits : 30 " + " ID : F2017A7PS0124H " + " NAME : PRANJAL GUPTA")
        self.grid.attach_next_to(credits_label, pdf_generate_button, Gtk.PositionType.RIGHT, 5, 2)

    def selection_view(self, store, view):
        renderer_text = Gtk.CellRendererText()
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.set_radio(True)
        store = Gtk.ListStore(int, str, bool, bool, bool, bool)  # sec, instructor, day, hrs

        store.append([1, "DebianT", False, False, False, False])
        store.append([2, "OpenSuseT", False, False, False, False])
        store.append([3, "FedoraT", False, False, False, False])
        store.append([1, "DebianT", False, False, False, False])
        store.append([2, "OpenSuseT", False, False, False, False])
        store.append([3, "FedoraT", False, False, False, False])
        store.append([1, "DebianT", False, False, False, False])
        store.append([2, "OpenSuseT", False, False, False, False])
        store.append([3, "FedoraT", False, False, False, False])


        #column_toggle = Gtk.TreeViewColumn("Toggle", renderer_toggle, active=5)


        view = Gtk.TreeView(model=store)

        section_column_text = Gtk.TreeViewColumn("Section", renderer_text, text=0)
        instructor_column_text = Gtk.TreeViewColumn("Instructor", renderer_text, text=1)
        day_column_text = Gtk.TreeViewColumn("Day", renderer_text, text=2)
        hrs_column_text = Gtk.TreeViewColumn("Hours", renderer_text, text=3)
        selected_section = Gtk.TreeViewColumn("", renderer_toggle, active=5)

        view.append_column(section_column_text)
        view.append_column(instructor_column_text)
        view.append_column(day_column_text)
        view.append_column(hrs_column_text)
        view.append_column(selected_section)

        #tutorial_box.pack_start(tutorial_view, False, False, False)
        self.parent_box.pack_start(view, False, False, 10)

    def timetable_view(self):
        for hours in range (7, 16):
            for days in range (0,7):
                button = Gtk.Button()
                self.grid.attach(button, hours-7, days+10, 1, 1)


window = MyWindow()
window.show_all()
Gtk.main()
