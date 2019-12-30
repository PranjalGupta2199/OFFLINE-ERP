import sqlite3
import os
import re

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

db = sqlite3.connect('courses.db')
db.create_function("REGEXP", 2, regexp)
cursor = db.cursor()


def rectify_courses(room_num):
    cursor.execute("SELECT _rowid_,INSTRUCTOR,ROOM FROM courses WHERE INSTRUCTOR LIKE ?", ('%' + room_num + '%',))
    result = cursor.fetchall()
    print(result)

    for row in result:
        row_id = row[0]
        instructor = row[1][:-1*len(room_num)]
        room = row[1][-1*len(room_num):] + row[2]
        print((room, instructor, row_id))
        cursor.execute('''UPDATE courses SET ROOM = ?, INSTRUCTOR = ? WHERE _rowid_ = ?''', (room,instructor,row_id))

    db.commit()

def rectify_midsems():
    cursor.execute("SELECT _rowid_ FROM midsem WHERE TIME IS NULL OR DATES IS NULL")
    result = cursor.fetchall()
    print (result)

    for row in result:
        row_id = row[0]
        cursor.execute("UPDATE midsem SET DATES = ?, TIME = ? WHERE _rowid_ = ?", ('*', '*', row_id))
    
    db.commit()
    
def main():
    for block in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
        for floor in ['0', '1', '2', '3']:
            for room_num in range (0, 50):
                room_num = block + floor + '0'*(2 - len(str(room_num)))+str(room_num)
                # print (room_num)
                rectify_courses(room_num)
    rectify_midsems()

if __name__ == "__main__":
    main()