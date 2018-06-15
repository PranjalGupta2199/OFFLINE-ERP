import gi
import os
gi.require_version("Gtk", "3.0")
from packages import page_01
from packages import page_00
from packages import pdf_reader
from packages import search
from gi.repository import Gtk

if __name__ == "__main__" :
	try :
		flag = 1
		os.mkdir("Pages")
		window0 = page_00.FileChooser()
		window0.connect('delete-event', Gtk.main_quit)
		window0.show_all()
		Gtk.main()
	except :
		pass
	
	if flag == 1:
		window1 = page_01.MyWindow()
		window1.connect('delete-event', Gtk.main_quit)
		window1.show_all()
		Gtk.main()
