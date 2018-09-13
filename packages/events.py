import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Event(object) : 
    def handle_compre_date(self) : 
        '''
        This method is called when there are courses in your catalog 
        having same compre date. You need to remove the course whose 
        date is clashing with this one and then add this course.

        '''

        dialog = Gtk.MessageDialog(self, 0,
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK,
            "You have selected a course having same compre date !!" )

        dialog.format_secondary_text(
            "Please remove that course from your schedule to add this one.")

        response = dialog.run()
        if response == Gtk.ResponseType.OK :
            pass
        dialog.destroy()


                
    
    def handle_section_change(self, row, section_type) :
        '''
        This method is called when you try to change section of a course 
        you took.
            @parameters :
                row : string 
                    A string from self.catalog_info
                section_type : string 
                    A string which tells the type of class 
                    ('LEC', 'PRAC', 'TUT')
        '''

        section_list = row.split(';')
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, 
            "Warning : You are about to change a section !")
        dialog.format_secondary_text("Do you wish to continue ?")

        response = dialog.run()

        if response == Gtk.ResponseType.YES :
            self.catalog_info.remove(row)
            for row in section_list[-2].split() :
                for col in section_list[-3].split() :
                    if col == 'M' : 
                        self.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' : 
                        self.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' : 
                        self.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' : 
                        self.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' : 
                        self.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' : 
                        self.Label_list_weekly[int(row)][6].set_label('')

            self.update_timetable(None, None, None, None, section_type)
            
        elif response == Gtk.ResponseType.NO :
            pass    
        dialog.destroy()

        

    def handle_clash_time(self, row) :
        '''
        This method is called when there are two courses 
        occurring at the same time. This method shows a dialog box
        which asks you to either continue or cancel the replacement 
        of the course you want with the one already present in your timetable 
        at that same time slot.

            @parameter :
                row : string
                    A string from self.catalog_info

        '''

        section_list = row.split(';')
        dialog = Gtk.MessageDialog(self, 0, 
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, 
            "Warning : You cannot have 2 classes at the same time !!")
        dialog.format_secondary_text(
                "Do you want to replace this course ?")

        response = dialog.run()

        if section_list[0] == self.selected_course_code :
            response = Gtk.ResponseType.YES 

        if response == Gtk.ResponseType.YES :
            self.catalog_info.remove(row)
            for row in section_list[-2].split() :
                for col in section_list[-3].split() :
                    if col == 'M' : 
                        self.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' : 
                        self.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' : 
                        self.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' : 
                        self.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' : 
                        self.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' : 
                        self.Label_list_weekly[int(row)][6].set_label('')
            self.add_to_timetable(self.selected_hour, self.selected_day)
            self.catalog_info.insert(0, self.info)

        else :
            pass
        dialog.destroy()
