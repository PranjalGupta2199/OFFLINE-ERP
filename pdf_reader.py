import pandas 
import sqlite3
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf, convert_into
#import tabula 

def split_pdf(path):
	''' Splits the timetable pdf into individual pages 
		path here is the pdf path of timetable.
	'''
	infile = PdfFileReader(open(path, 'rb'))
	

	for i in xrange(infile.getNumPages()):
	   	p = infile.getPage(i)
		outfile = PdfFileWriter()
		outfile.addPage(p)
		with open('Pages/pdf/page-%02d.pdf' % i, 'wb') as f:
			outfile.write(f)

split_pdf('/home/pranjal/Python/repos/Projects/TimeTable@BPHC/TIMETABLE II SEM 2017-18 .pdf')

def extract_to_csv():
	''' Index is the starting page containing the coursewise timetable.
		and path is the path of pages (split pages)
		cursor.execute( CREATE TABLE courses ( 
		COURSE_CODE text, 
		COURSE_TITLE text, 
		INSTRUCTOR text, 
		DAY text, HOURS text, 
		COMPRE_DATE text) )
	'''
	path = '/home/pranjal/Python/repos/Projects/TimeTable@BPHC/Pages/pdf'
	
	db = sqlite3.connect('courses.db')
	cursor = db.cursor() 

	


	directory_files = os.listdir(path)
	directory_files.sort()

	for file in directory_files:
		page_no = int (file.split('.')[0].split('-')[1]) 
		print page_no
		if ( page_no >= 6 and page_no <= 45 ):
			data = read_pdf(
				input_path = os.path.join(path, file), 
				pandas_options = {'header' : None, 
				'skiprows' : [0,1,2,3,4,5], 
				'keep_default_na' : False,
				'usecols' : [1,2,5,7,8,10]})
			data.to_sql(name = 'courses', con = db, index = False, index_label = None, if_exists = 'append')

			

extract_to_csv()	


