import gi
import os
gi.require_version("Gtk", "3.0")
from packages import search
from packages import page_01
from packages import page_00
from gi.repository import Gtk

if __name__ == "__main__" :
    # window0 = page_00.FileChooser()
    # try :
    #     os.mkdir("Pages")
    #     window0.show_all()
    #     Gtk.main()
    # except :
    #     pass
    # if window0.flag == 0 :
    window1 = page_01.MyWindow()
    window1.show_all()
    Gtk.main()
