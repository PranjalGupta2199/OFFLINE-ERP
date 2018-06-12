import gi
gi.require_version("Gtk", "3.0")
import pandas 
import sqlite3
import os
from packages import gui
from packages import pdf_reader
from packages import search
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf, convert_into
from gi.repository import Gtk

if __name__ == "__main__" :
	db = sqlite3.connect('/home/pranjal/Python/repos/Projects/TimeTable@BPHC/packages/courses.db')
	pdf_reader.split_pdf()
	pdf_reader.to_database(db)
	window = gui.MyWindow()
	window.connect('delete-event', Gtk.main_quit)
	window.show_all()
	Gtk.main()
