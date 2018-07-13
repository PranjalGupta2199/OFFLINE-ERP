import pandas
import sqlite3
import os

class Searching:
    '''
        Searches a match for the given query for the parameter

        METHODS : 
            __init__(self) 
            get_result (self, query) 
            get_course_details (self, match_parameter) 
            get_midsem_details (self, match_paramter) 
            __str__(self) :
 

    '''
    def __init__(self):
        '''
        Constructs the Searching class instance

            @variables :
                self.lecture, self.tutorial, self.practical : pandas.Dataframe
                            Contains the details of all the available sections
                db : sqlite3 connection object

                self.cursor : sqlite3 cursor object.
        '''
        self.lecture, self.tutorial, self.practical = [],[],[]  
        
        dirname = os.path.join(os.getcwd(),'packages/courses.db')
        db = sqlite3.connect(dirname)
        self.cursor = db.cursor()


    def get_result(self, query):
        '''
        Searches for a match in the database from the given query.

        '''

        self.cursor.execute ( "SELECT COURSE_CODE, COURSE_TITLE,COMPRE_DATE FROM \
         courses WHERE COURSE_CODE  LIKE ? OR COURSE_TITLE LIKE ? AND COURSE_CODE != ''",\
          ('%' + query + '%','%' + query + '%'))
        return self.cursor.fetchall()  #This will return all the matched strings 

    def get_course_details (self, match_parameter): #match_parameter is a tuple
        '''
        Retrives information (section details) from the database.

            @parameter : 
                match_parameter : tuple
                    contains tuple of strings having course_code and course_title as its 
                    elements
        '''
        match_id = self.cursor.execute("SELECT _rowid_ FROM courses \
            WHERE COURSE_CODE = ? AND COURSE_TITLE = ?",\
         match_parameter).fetchall()[0] 
        
        self.cursor.execute("SELECT * FROM courses WHERE _rowid_ >= ? ", match_id )
        result_list = [self.cursor.fetchone()] #contains the complete details of the course
        
        try:
            next_record = self.cursor.fetchone()
            while (not next_record[0]):
                result_list.append(next_record)
                next_record = self.cursor.fetchone()          
        except: 
            pass
        finally:
            pass

        details_df = pandas.DataFrame(result_list)
        tut_index, prac_index = -1, -1

        for index in range (len(details_df[1])) :
            if (details_df[1][index].lower() == 'practical') :
                prac_index = index
            elif (details_df[1][index].lower() == 'tutorial') :
                tut_index = index

        if (tut_index == -1) :
            if (prac_index == -1):
                self.practical = pandas.DataFrame([])
                self.tutorial = pandas.DataFrame([])
                self.lecture = details_df
            else :
                self.tutorial = pandas.DataFrame([])
                self.practical = details_df[prac_index : ]
                self.lecture = details_df[ : prac_index]
        else:
            if (prac_index == -1):
                self.practical = pandas.DataFrame([])
                self.lecture = details_df[ : tut_index]
                self.tutorial = details_df[tut_index : ]
            else :
                self.lecture = details_df[ : prac_index]
                self.practical = details_df[prac_index : tut_index]
                self.tutorial = details_df[tut_index : ]

    def get_midsem_details(self, match_parameter) :
        '''
        Searches for the midsem details of the course from 
        the 'midsem' table in courses database.
        
            @parameter : 
                match_paramter : tuple
                    A tuple of strings (course code, course title)

            @variables : 
                midsem_info : tuple 
                     A tuple of sting
                midsem_date : string
                    Of the form "DD/MM" or "*" (if unavailable in the pdf)
                midsem_time : string
                    A string giving the time details.

        '''

        midsem_info = self.cursor.execute(
            "SELECT * FROM midsem WHERE COURSE_CODE == ? \
            AND COURSE_TITLE == ?", match_parameter).fetchone()

        self.midsem_date, self.midsem_time = midsem_info[-2], midsem_info[-1]


    def __str__ (self) :
        '''
        Returns the string representation of the object.
        ''' 

        print self.lecture
        print self.practical
        print self.tutorial
        return ' '


if __name__ == '__main__':
    
    while True:
        search_object = Searching()
        print
        print 
        query = raw_input("Enter your query : ")
        search_object.search(query)
        print search_object
