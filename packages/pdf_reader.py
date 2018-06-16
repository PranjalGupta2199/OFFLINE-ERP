import pandas 
import sqlite3
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf, convert_into


def split_pdf(file_path, folder_path):
	''' Splits the timetable pdf into individual pages 
	'''
	infile = PdfFileReader(open(file_path, 'rb'))
	

	for i in xrange(infile.getNumPages()):
	   	p = infile.getPage(i)
		
		outfile = PdfFileWriter()
		outfile.addPage(p)
		
		split_page_path = os.path.join(folder_path, 'Pages/page-%02d.pdf' % i)

		with open(split_page_path, 'wb') as f:
			outfile.write(f)

def to_database(folder_path, connection_object):
	''' 
		Extracts table from the pdf and stores them in a database (courses.db)
	'''
	path = os.path.join(folder_path, "Pages")

	directory_files = os.listdir(path)
	directory_files.sort()

	for file in directory_files:
		page_no = int (file.split('.')[0].split('-')[1]) 
		
		#print page_no
		
		if ( page_no >= 6 and page_no <= 45 ):
			
			data = read_pdf(
				input_path = os.path.join(path, file), 
				pandas_options = {
				'header' : None, 
				'skiprows' : [0,1,2,3,4,5], 
				'keep_default_na' : False,
				'usecols' : [1,2,4,5,7,8,10]})
			
			data.columns = ['COURSE_CODE', 'COURSE_TITLE', 'SECTION', 
			'INSTRUCTOR', 'DAY', 'HOURS', 'COMPRE_DATE']
			
			data.to_sql(name = 'courses', con = connection_object, 
				index = False, if_exists = 'append')

if __name__ == '__main__':
	db = sqlite3.connect('courses.db')
	split_pdf()
	to_database(db)	


