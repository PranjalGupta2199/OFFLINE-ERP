import gi
gi.require_version('Gtk','3.0')
gi.require_version('Gdk','3.0')
from gi.repository import Gtk, GdkPixbuf


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Offline ERP")
        #self.set_size_request(400,400)
        self.connect('delete-event', Gtk.main_quit)


        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.grid.set_row_homogeneous(True)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_spacing(5)

        welcome_label = Gtk.Label()
        welcome_label.set_label ('''WELCOME TO YOUR OFFILINE ERP ''')
        self.grid.attach(welcome_label, 0, 0, 2, 2)


        pb = GdkPixbuf.Pixbuf.new_from_file_at_size('BITs.jpg',200,200)
        img = Gtk.Image()
        img.set_from_pixbuf(pb)
        self.grid.attach (img, 3, 1, 2, 4)


        Name_label = Gtk.Label()
        Name_label.set_label("Name :")
        Name_label.set_xalign(0)

        Name_entry = Gtk.Entry()
        Name_entry.set_editable(True)



        ID_label = Gtk.Label()
        ID_label.set_label("ID Number :")
        ID_label.set_xalign(0)

        ID_entry = Gtk.Entry()
        ID_entry.set_editable(True)

        Pdf_label = Gtk.Label()
        Pdf_label.set_label("Add path to your file")
        Pdf_label.set_xalign(0)

        Pdf_entry = Gtk.Entry()
        Pdf_entry.set_editable(True)

        self.grid.attach(Name_label, 1, 2, 1, 1)
        self.grid.attach_next_to(Name_entry, Name_label, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach(ID_label, 1, 3, 1, 1)
        self.grid.attach_next_to(ID_entry, ID_label, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach(Pdf_label, 1, 4, 1, 1)
        self.grid.attach_next_to(Pdf_entry, Pdf_label, Gtk.PositionType.RIGHT, 1, 1)


        Next_button = Gtk.Button()
        Next_button.set_label("Next")

        Exit_button = Gtk.Button()
        Exit_button.set_label("Exit")

        self.grid.attach(Next_button, 4, 5, 1, 1)
        self.grid.attach(Exit_button, 0, 5, 1, 1)


        Exit_button.connect('clicked', Gtk.main_quit)



window = MyWindow()
window.show_all()
Gtk.main()
