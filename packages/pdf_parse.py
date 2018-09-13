import pandas
import threading
import sqlite3
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf, convert_into


class Pdf(object):
    def pdf_parse(self, widget, data = None) :
        '''
        Handles spinner events and multiprocessing when populating the database.
        '''
        if self.file_path :
        
            self.split_pdf(self.file_path)
            self.spinner.start()
            p3 = threading.Thread(target = self.to_database)
            p3.start()
        
        else :
            self.handle_no_file()

    def split_pdf(self, file_path):
        ''' 
        Splits the timetable pdf into individual pages 
        '''
        infile = PdfFileReader(open(file_path, 'rb'))
        

        for i in range(infile.getNumPages()):
            p = infile.getPage(i)
            
            outfile = PdfFileWriter()
            outfile.addPage(p)
            
            split_page_path = os.path.join(os.getcwd(), 'Pages/page-%02d.pdf' % i)

            with open(split_page_path, 'wb') as f:
                outfile.write(f)

    def to_database(self):
        ''' 
            Extracts table from the pdf and stores them in a database (courses.db)
        '''
        path = os.path.join(os.getcwd(), "Pages")
        self.database = sqlite3.connect(os.path.join(os.getcwd(), "packages/courses.db"))

        directory_files = os.listdir(path)
        directory_files.sort()

        for file in directory_files:
            page_no = int (file.split('.')[0].split('-')[1]) 
            
            
            if ( page_no >= 6 and page_no <= 50 ):
                
                data = read_pdf(
                    input_path = os.path.join(path, file), 
                    pandas_options = {
                    'header' : None, 
                    'skiprows' : [0,1,2,3,4,5], 
                    'keep_default_na' : False,
                    'usecols' : [1,2,4,5,7,8,10]})
               
                data.columns = ['COURSE_CODE', 'COURSE_TITLE', 'SECTION', 
                'INSTRUCTOR', 'DAY', 'HOURS', 'COMPRE_DATE']
                
                data.to_sql(name = 'courses', con = self.database, 
                    index = False, if_exists = 'append')

            if (page_no >= 51  and page_no <= 64 ) :
                data = read_pdf(
                    input_path = os.path.join(path, file),
                    pandas_options = {
                    'header' : None,
                    'skiprows' : [0],
                    'keep_default_na' : True,
                    })


                if len(data.columns) != 6 :
                    data = data.loc[:, [1,2,3,4]]
                else : 
                    data = data.loc[:, [1,2,4,5]]
                # This if statement is called only because of the 
                # errors caused when converting the pdf in dataframe
                # on same pages.
                
                data.columns = ['COURSE_CODE', 'COURSE_TITLE', 'DATES', 'TIME']
                data.to_sql(name = 'midsem', con = self.database,
                    index = False, if_exists = 'append')
              
        self.spinner.stop()
        self.okay_button.set_sensitive(False)
