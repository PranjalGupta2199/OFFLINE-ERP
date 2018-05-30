import pandas 
import sqlite3
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf, convert_into


def split_pdf():
	''' Splits the timetable pdf into individual pages 
	'''
	path = '/home/pranjal/Python/repos/Projects/TimeTable@BPHC/TIMETABLE II SEM 2017-18 .pdf'
	infile = PdfFileReader(open(path, 'rb'))
	
	##Remove absolute path

	for i in xrange(infile.getNumPages()):
	   	p = infile.getPage(i)
		
		outfile = PdfFileWriter()
		outfile.addPage(p)
		
		with open('Pages/page-%02d.pdf' % i, 'wb') as f:
			outfile.write(f)

def extract_to_csv():
	''' 
		Extracts table from the pdf and stores them in a database (courses.db)
	'''
	path = '/home/pranjal/Python/repos/Projects/TimeTable@BPHC/Pages/'
	
	db = sqlite3.connect('courses.db')
	#cursor = db.cursor() 

	##Remove absolute path


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
			
			data.to_sql(name = 'courses', con = db, 
				index = False, if_exists = 'append')

			
split_pdf()
extract_to_csv()	


