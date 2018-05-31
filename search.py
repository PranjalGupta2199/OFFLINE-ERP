import sqlite3

def Print_ (list_):
	for i in range(len(list_)):
		print i, list_[i]

	if not list_ : 
		print 'Sorry, No searches where found.'

def course_code_search (query, cursor) : 

	cursor.execute ( "SELECT COURSE_CODE FROM courses WHERE COURSE_CODE LIKE ? ", ('%' + query + '%',))
	list_ = cursor.fetchall()
	##After the user selects the desired result
	##Only for command-line
	Print_(list_)
	
	prompt = input(' match number :')	
	result = list_[prompt]

	result_id = cursor.execute("SELECT _rowid_ FROM courses WHERE COURSE_CODE = ?", result).fetchall()[0]

	cursor.execute("SELECT * FROM courses WHERE _rowid_ >= ? ", result_id )
	List = [cursor.fetchone()]
	try:
		item = cursor.fetchone()
		while (not item[0]):
			List.append(item)
			item = cursor.fetchone()		  
	except: ##add excpetion type
		pass
	finally:
		Print_(List)

db = sqlite3.connect('courses.db')
cursor = db.cursor()

while True:
	print
	print 
	query = raw_input("Enter your query : ")
	course_code_search(query, cursor)


def course_title_search (query, cursor) :
	cursor.execute( "SELECT COURSE_TITLE FROM courses WHERE COURSE_TITLE LIKE ?", ('%' + query + '%',))
	Print_ (cursor.fetchall())

def instructor_search (query, cursor) :
	a = cursor.execute( "SELECT DISTINCT INSTRUCTOR FROM courses WHERE INSTRUCTOR LIKE ?", ('%' + query + '%',))
	Print_ (cursor.fetchall())