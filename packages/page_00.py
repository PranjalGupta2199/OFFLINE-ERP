import gi 
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import pdf_reader
import sqlite3

class FileChooser(Gtk.Window):
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
		self.grid.attach_next_to(child = file_button, sibling = file_label, side = Gtk.PositionType(1), width = 1, height = 1)
		self.grid.attach_next_to(child = okay_label, sibling = file_label, side = Gtk.PositionType(3), width = 1, height = 1)
		self.grid.attach_next_to(child = okay_button, sibling = file_button, side = Gtk.PositionType(3), width = 1, height = 1)
		self.grid.attach_next_to(child = next_button, sibling = okay_button, side = Gtk.PositionType(3), width = 2, height = 1)
		

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