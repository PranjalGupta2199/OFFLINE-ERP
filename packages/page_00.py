import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf

from .pdf_parse import Pdf

class FileChooser(Gtk.Window, Pdf):
    '''
    This class is for creating gui for the first page of the application.
    The main window consists of a single page which contains 4 buttons.

    The purpose for this window is to get the location of the pdf on 
    user's system and to start parsing pdf and storing the 
    relevant information in a database.

    METHODS : 
        __init__(self) : 
        file_choose (self, widget, data = None)            
        pdf_parse(self, widget, data = None) :
        move_to_next_page(self, widget, data = None) :
        split_pdf(self, file_path) :
        to_database(self) :
        main_quit(self) :
.
    '''
    def __init__(self) :
        '''
        Constructs the FileChooser instance

            @variables :

                (Gtk Layout containers )
                header_bar  :               Gtk.HeaderBar 
                
                self.grid :                 Gtk.Grid
                    self.about_page         Gtk.ScrolledWindow
                        self.about_label :  Gtk.Label
                    file_label :            Gtk.Label
                    file_button :           Gtk.Button
                    okay_button :           Gtk.Button
                    self.spinner :          Gtk.Spinner
                    self.status_label       Gtk.Label
                    next_button :           Gtk.Button

            other variables :
                self.flag : int
                    Indicates wether the app has been used in the system before
                    so that pdf is not parsed again.

        '''
        super(Gtk.Window, self).__init__(title = 'OFFLINE ERP')
        self.connect('delete-event', self.main_quit)
        self.flag = 0
        self.set_border_width(10)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.set_resizable(False)

        self.set_icon_from_file('media/BITs.jpg')
        self.grid.set_row_homogeneous(True)
        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(5)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "OFFLINE ERP"
        self.set_titlebar(header_bar)

        self.about_page = Gtk.ScrolledWindow(vexpand = True, hexpand = True)
        self.about_label = Gtk.Label()
        self.about_label.set_justify(3)
        self.about_label.set_line_wrap(True)
        #self.about_label.set_markup()
        self.about_page.add(self.about_label)


        file_button = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('media/file_button.png')
        pixbuf = pixbuf.scale_simple(32, 32, 2)
        
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        file_button.set_image(image)

        file_button.connect('clicked', self.file_choose)
        
        file_label = Gtk.Label("Location :")
        self.file_path = ''

        self.okay_button = Gtk.Button("Okay")
        self.okay_button.connect('clicked', self.pdf_parse)

        self.entry = Gtk.Entry()
        self.entry.set_editable(False)

        self.spinner = Gtk.Spinner()

        next_button = Gtk.Button("Next")
        next_button.connect("clicked", self.move_to_next_page)

        self.grid.attach(
            child = self.about_page, left = 0,
            top = 0, width = 8, height = 9)


        self.grid.attach_next_to(
            child = file_label, sibling = self.about_page,
            side = Gtk.PositionType(3), width = 1, height = 1)

        self.grid.attach_next_to(
            child = self.entry, sibling = file_label,
            side = Gtk.PositionType(1), width = 6, height = 1)
        
        self.grid.attach_next_to(
            child = file_button, sibling = self.entry,
            side = Gtk.PositionType(1), width = 1, height = 1)

        self.grid.attach_next_to(
            child = self.okay_button, sibling = file_label,
            side = Gtk.PositionType(3), width = 1, height = 1)

        
        self.grid.attach_next_to(
            child = self.spinner, sibling = self.entry,
            side = Gtk.PositionType(3), width = 1, height = 1)

        self.grid.attach_next_to(
            child = next_button, sibling = file_button, 
            side = Gtk.PositionType(3), width = 1, height = 1)



    def file_choose(self, widget, data = None) :
        '''
        Used for specifying the file location of the pdf 

            @variables :
                dialog : Gtk.FileChooserDialog 
                    Creates a dialog box with action as OPEN.

                self.file_path : str
                    Contains the string value of the location of pdf file selected
        '''
        dialog = Gtk.FileChooserDialog("Please Choose Your File : ", self, 
            Gtk.FileChooserAction.OPEN, 
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            'SELECT', Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK :
            self.file_path = dialog.get_filename()
            self.entry.set_text(self.file_path)
        elif response == Gtk.ResponseType.CANCEL :
            pass

        dialog.destroy()

    def move_to_next_page(self, widget, data = None) :
        '''
        Destroys the current window returns the flow of execution to the main.py file.

        '''
        if self.okay_button.get_sensitive():
            dialog = Gtk.MessageDialog(self, 0,
                Gtk.MessageType.INFO, 
                Gtk.ButtonsType.OK,
                "You haven't created the database.")

            dialog.format_secondary_text(
                'Please select your file and then press Okay.')
            dialog.run()
            dialog.destroy()

        else :            
            self.destroy()
            Gtk.main_quit()

    def main_quit (self, widget, data = None) : 
        '''
        Overrides the Gtk.main_quit. This method is called only when
        the window is closed before going on to the next page.

        '''
        for file in os.listdir('Pages') :
            os.remove(os.path.join('Pages', file))
        os.rmdir("Pages")        
        try :
            os.remove(os.path.join(os.getcwd(),'packages/courses.db'))
        except : 
            pass
        self.flag = 1
        Gtk.main_quit()

if __name__ == "__main__" :
    window = FileChooser()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()