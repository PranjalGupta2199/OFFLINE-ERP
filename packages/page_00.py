import gi 
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from . import pdf_reader
import sqlite3

class FileChooser(Gtk.Window):
	'''
	This class is for creating gui for the first page of the application.
	The main window consists of a single page which contains 4 buttons.

	The purpose for this window is to get the location of the pdf on 
	user's system and to start parsing pdf and storing the 
	relevant information in a database.

	METHODS : 
		__init__(self) : 
			Constructs the FileChooser instance

			@variables :

				(Gtk Layout containers )
				header_bar  : 				Gtk.HeaderBar 
				
				self.grid :					Gtk.Grid
					self.about_page 		Gtk.ScrolledWindow
						self.about_label : 	Gtk.Label
					file_label : 			Gtk.Label
					file_button :			Gtk.Button
					okay_button :			Gtk.Button
					self.spinner : 			Gtk.Spinner
					self.status_label		Gtk.Label
					next_button :			Gtk.Button

				Other variables :
					self.flag : int
						Indicates wether the app has been used in the system before
						so that pdf is not parsed again.

		file_choose (self, widget, data = None):
			Used for specifying the file location of the pdf 

			@variables :
				dialog : Gtk.FileChooserDialog 
					Creates a dialog box with action as OPEN.

				self.file_path : str
					Contains the string value of the location of pdf file selected

		move_to_database(self, widget, data = None) :
			This method uses pdf_reader file and parses and stores information from 
			the pdf file. This is a callback method used for Gtk.Button (okay_button).

			@variables :
				self.database : sqlite3 connection object
					Creates a database 'courses.db' in the packages directory of the repo.

		move_to_next_page(self, widget, data = None) :
			Destroys the current window returns the flow of execution to the main.py file.

			@variables :
				self.flag  : int
					Indicates that this window has succesfully worked.
	'''
	def __init__(self) :
		super(Gtk.Window, self).__init__(title = 'OFFLINE ERP')
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
		self.about_label.set_markup(

"<big>Say hello to your own <b> OFFLINE ERP  </b>!! </big>" + "\n" + 
"\n" + "This Desktop Application is designed to \
help you decide what courses (CDCs and Electives)\
you wish to opt for in the coming semester." + "\n" + "\n" +
"You can search your desired course, add them to your catalog \
or even remove them if you want. If you are unhappy with \
your timetable you can clear all the enteries at once and start afresh. \
To save your work, you can generate the pdf version of your timetable." + "\n" + "\n" + 
"Well, for now you just need to specify the path of your pdf file. For that, \
click on the folder icon, a window pops-up. Select your file and click OPEN. \
Then when you have verified the path, click on OKAY button. This process may take some time depending on your system,\
so wait as long as the spinner shows on the pop-up window.Then click on NEXT to move onto the main page ... " + "\n" + "\n" +
"<b> Hope you enjoy my application. </b>"
			)
		self.about_page.add(self.about_label)


		file_button = Gtk.Button()
		pixbuf = GdkPixbuf.Pixbuf.new_from_file('media/file_button.png')
		pixbuf = pixbuf.scale_simple(32, 32, 2)
		
		image = Gtk.Image()
		image.set_from_pixbuf(pixbuf)
		file_button.set_image(image)

		file_button.connect('clicked', self.file_choose)
		
		file_label = Gtk.Label("Location :")
		
		okay_button = Gtk.Button("Okay")
		okay_button.connect('clicked', self.move_to_pdf_reader)

		self.entry = Gtk.Entry()
		self.entry.set_editable(False)

		self.spinner = Gtk.Spinner()

		next_button = Gtk.Button("Next")
		next_button.connect("clicked", self.move_to_next_page)

		self.status_label = Gtk.Label("Status :")

		self.grid.attach(
			child = self.about_page, left = 0,
			top = 0, width = 8, height = 5)


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
			child = okay_button, sibling = file_label,
			side = Gtk.PositionType(3), width = 1, height = 1)

		
		self.grid.attach_next_to(
			child = self.spinner, sibling = self.entry,
			side = Gtk.PositionType(3), width = 1, height = 1)

		self.grid.attach_next_to(
			child = self.status_label, sibling = self.spinner,
			side = Gtk.PositionType(1), width = 1, height = 1)		


		self.grid.attach_next_to(
			child = next_button, sibling = file_button, 
			side = Gtk.PositionType(3), width = 1, height = 1)



	def file_choose(self, widget, data = None) :
		dialog = Gtk.FileChooserDialog("Please Choose Your File : ", self, 
			Gtk.FileChooserAction.OPEN, 
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		response = dialog.run()

		if response == Gtk.ResponseType.OK :
			self.file_path = dialog.get_filename()
			self.entry.set_text(self.file_path)
		elif response == Gtk.ResponseType.CANCEL :
			pass

		dialog.destroy()



	def move_to_pdf_reader(self, widget, data = None) :
		self.spinner.start()
		self.database = sqlite3.connect(os.path.join(os.getcwd(), "packages/courses.db"))
		pdf_reader.split_pdf(
			file_path = self.file_path)

		pdf_reader.to_database(
			connection_object = self.database)
		self.spinner.stop()
		self.status_label.set_label("Status : Done")

	def move_to_next_page(self, widget, data = None) :
		self.flag += 1
		self.destroy()
		Gtk.main_quit()
		return



if __name__ == "__main__" :
	window = FileChooser()
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()