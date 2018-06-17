import gi 
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import pdf_reader
import sqlite3

class FileChooser(Gtk.Window):
	'''
	This class is for creating gui for the first page of the application.
	The main window consists of a single page which contains 4 buttons.

	The purpose for this window is to get the location of the repo and pdf 
	of the timetable on user's system and to start parsing pdf and storing 
	the relevant information in a database.

	METHODS : 
		__init__(self) : 
			Constructs the FileChooser instance

			@variables :

				(Gtk Layout containers ) 
				
				self.grid :				Gtk.Grid
					file_label : 		Gtk.Label
					file_button :		Gtk.Button
					folder_label :		Gtk.Label
					folder_button :		Gtk.Button
					okay_label :		Gtk.Label
					okay_button :		Gtk.Button
					next_button :		Gtk.Button

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
		
		folder_choose(self, widget, data = None) :
			Used for specifying the folder location of this repo.
			
			@variables :
				dialog : Gtk.FileChooserDialog
					Creates a dialog box with action as SELECT_FOLDER

				self.folder_path : str 
					Contains the string value of the location of the repo folder
					in user's system

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

		self.grid = Gtk.Grid()
		self.add(self.grid)

		file_label = Gtk.Label("Choose Your File :")

		file_button = Gtk.Button("icon")
		file_button.connect('clicked', self.file_choose)

		okay_label = Gtk.Label("After selecting the path press okay.")

		okay_button = Gtk.Button("Okay")
		okay_button.connect('clicked', self.move_to_pdf_reader)

		next_button = Gtk.Button("Next")
		next_button.connect("clicked", self.move_to_next_page)

		
		self.grid.attach(child = file_label, left = 0, top = 0, width = 2, height = 1)
		self.grid.attach_next_to(
			child = file_button, sibling = file_label, 
			side = Gtk.PositionType(1),  width = 1, height = 1)
		
		self.grid.attach_next_to(
			child = okay_label, sibling = file_label, 
			side = Gtk.PositionType(3), width = 1, height = 1)
		
		self.grid.attach_next_to(
			child = okay_button, sibling = file_button, 
			side = Gtk.PositionType(3), width = 1, height = 1)
		
		self.grid.attach_next_to(
			child = next_button, sibling = okay_button, 
			side = Gtk.PositionType(3), width = 2, height = 1)
		

	def file_choose(self, widget, data = None) :
		dialog = Gtk.FileChooserDialog("Please Choose Your File : ", self, 
			Gtk.FileChooserAction.OPEN, 
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		response = dialog.run()

		if response == Gtk.ResponseType.OK :
			self.file_path = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL :
			pass

		dialog.destroy()



	def move_to_pdf_reader(self, widget, data = None) :
		self.database = sqlite3.connect(os.path.join(os.getcwd(), "packages/courses.db"))
		pdf_reader.split_pdf(
			file_path = self.file_path)

		pdf_reader.to_database(
			connection_object = self.database)

	def move_to_next_page(self, widget, data = None) :
		self.flag = 1
		self.destroy()
		Gtk.main_quit()
		return



if __name__ == "__main__" :
	window = FileChooser()
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()