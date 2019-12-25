import sqlite3
import os
import re

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

db = sqlite3.connect('courses.db')
db.create_function("REGEXP", 2, regexp)
cursor = db.cursor()

cursor.execute("SELECT _rowid_,INSTRUCTOR FROM courses WHERE INSTRUCTOR LIKE '%G206'")
result = cursor.fetchall()
print(result)

for row in result:
    row_id = row[0]
    instructor = row[1][:-4]
    room = row[1][-4:]
    print((room, instructor, row_id))
    cursor.execute('''UPDATE courses SET ROOM = ?, INSTRUCTOR = ? WHERE _rowid_ = ?''', (room,instructor,row_id))

db.commit()