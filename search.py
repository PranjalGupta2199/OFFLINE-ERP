import sqlite3

def Print_ (list_):
	for i in list_:
		print i

	if not list_ : 
		print 'Sorry, No searches where found.'

def course_code_search (query, cursor) : 
	c = cursor
	c.execute ( "SELECT COURSE_CODE FROM courses WHERE COURSE_CODE LIKE ? ", ('%' + query + '%',))
	Print_ (c.fetchall())

def course_title_search (query, cursor) :
	c = cursor
	c.execute( "SELECT COURSE_TITLE FROM courses WHERE COURSE_TITLE LIKE ?", ('%' + query + '%',))
	Print_ (c.fetchall())

def instructor_search (query, cursor) :
	c = cursor
	c.execute( "SELECT DISTINCT INSTRUCTOR FROM courses WHERE INSTRUCTOR LIKE ?", ('%' + query + '%',))
	Print_ (c.fetchall())


db = sqlite3.connect('courses.db')
cursor = db.cursor()

while True:
	print
	print 
	query = raw_input("Enter your query : ")
	instructor_search(query, cursor)


