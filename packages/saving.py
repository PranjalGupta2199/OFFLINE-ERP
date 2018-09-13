import gi
import pickle
import copy
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak


class Save(object): 
    def save_pdf(self, widget) :
        '''
        Saves your desired schedule in pdf format.
        This is a callback method for Gtk.MenuItem widget (save_pdf_menu).

        This method uses a special Python library known as 'reportlab' which is 
        used for writing/reading in pdf files. For more information  :
            
            http://www.blog.pythonlibrary.org/2010/09/21/reportlab-tables-creating-tables-in-pdfs-with-python/
            https://www.reportlab.com/opensource/installation/
            https://www.reportlab.com/docs/reportlab-userguide.pdf
        ''' 
        dialog = Gtk.FileChooserDialog("Choose your destination :", self,
            Gtk.FileChooserAction.SAVE,
            ('Cancel', Gtk.ResponseType.CANCEL,
             'SAVE', Gtk.ResponseType.ACCEPT))

        dialog.set_current_name('Untitled Document.pdf')
        
        response = dialog.run()

        doc = SimpleDocTemplate(dialog.get_filename(), \
            pagesize = landscape(letter))

        if response == Gtk.ResponseType.ACCEPT :
            self.write (
                doc, "WEEKLY SCHEDULE", \
                self.weekly_schedule, self.Label_list_weekly)
            
            self.write (
                doc, "COMPREHENSIVE EXAMINATION", \
                self.compre_schedule, self.Label_list_compre)

            self.element.append(PageBreak())
            
            self.write (
                doc, "MID SEMESTER SCHEDULE", \
                self.midsem_schedule, self.Label_list_midsem)
        
            style = getSampleStyleSheet()
            normal = style["Heading1"]

            para = Paragraph("LEGENDS", normal)
            self.element.append(para)
            user_data = [['COURSE CODE', 'COURSE TITLE', 'SECTION', 'INSTRUCTOR']]
            for row in self.catalog_info :
                data = row.split(';')
                user_data.append([data[0], data[1], data[2], data[3]])
            table = Table(data = user_data)
            table.setStyle(TableStyle([
                                    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                    ]))     
            self.element.append(table)

            doc.multiBuild(self.element)
            self.save_list()
            self.save_count = 1
            
        elif response == Gtk.ResponseType.CANCEL : 
            pass

        dialog.destroy()

    def write(self, doc, headline, schedule, class_label_list) :        
        '''
        Writes data to a pdf file.
            @paramter :
                doc : 
                    reportlab.platypus.doctemplate.SimpleDocTemplate instance
                headline : string
                    string which to be written as a heading
                schedule : list 
                    list of strings containing labels for the timetable
                class_label_list : list 
                    list of Gtk.Label objects 
            @variables : 
                user_data : list
                    list of string to be written on the pdf
                table : 
                    reportlab.platypus.doctemplate.Table instance
        '''

        style = getSampleStyleSheet()
        normal = style["Heading1"]

        para = Paragraph(headline, normal)
        self.element.append(para)

        user_data = copy.deepcopy(schedule)
        
        for row in range (len(class_label_list)) :
            for col in range (len(class_label_list[row])) :
                user_data[row][col] =  class_label_list[row][col].get_label()
            

        table = Table(data = user_data)
        table.setStyle(TableStyle([
                                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                ]))
        self.element.append(table)

    def save_list(self) :
        '''
        Creates a file (if it doesn't exist) and writes the data in the 
        self.catalog_info for future use.
        '''
        with open('temp.txt', 'wb') as f :
            pickle.dump(self.catalog_info, f)                
            f.close()

    def open_last_work(self, widget, *data) :
        '''
        Method for loading the data from 'temp.txt' file in the directory.
        Uses pickle module which is used for serializing/de-serializing an
        object in a file. This is also a callback method for Gtk.MenuItem 
        (open_previous_menu).

            @variables :
                file : file object
                    Used for reading/writing in a file.
                data : 2D array
                    Contains the values of self.catalog_info (of your last work.)

        '''
        self.clear_timetable(None)
        try :
        
            file = open('temp.txt', 'rb')

            data = pickle.load(file)
            for row in data :

                self.catalog_info.append(row)
                tt_info = row.split(';')

                days = tt_info[-3].split()
                hours = tt_info[-2].split()
                section = tt_info[2]
                course_code = tt_info[0]
                course_title = tt_info[1]
                compre_date = tt_info[-1]

                for i in range (len(hours)) :
                    hours[i] = int(hours[i])

                self.text_to_display = course_code + '\n' + section
                self.add_to_timetable(hours, days)
                self.add_to_catalog()
                self.update_compre_schedule(compre_date, 
                    label = course_code)
                
                self.update_midsem_schedule(
                    match_parameter = (course_code,),
                    label = course_code)

                if course_code not in self.added_courses :
                    self.added_courses.append(course_code)

        
        except IOError :
            pass
