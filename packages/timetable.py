import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Timetable(object) :


    weekly_schedule = [
        ['HOURS/DAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        ['08 : 00 AM', '', '', '', '', '', ''],
        ['09 : 00 AM', '', '', '', '', '', ''],
        ['10 : 00 AM', '', '', '', '', '', ''],
        ['11 : 00 AM', '', '', '', '', '', ''],
        ['12 : 00 PM', '', '', '', '', '', ''],
        ['01 : 00 PM', '', '', '', '', '', ''],
        ['02 : 00 PM', '', '', '', '', '', ''],
        ['03 : 00 PM', '', '', '', '', '', ''],
        ['04 : 00 PM', '', '', '', '', '', ''],
        ['05 : 00 PM', '', '', '', '', '', '']]

    compre_schedule = [
        ['Sessions','01/12', '02/12', '03/12','04/12', '05/12', '06/12', \
        '07/12', '08/12' ,'09/12', '10/12', '11/12', '12/12', '13/12', '14/12'],
        ['Forenoon', '', '', '', '', '', '', '', '', '', '', '', '', '', '',],
        ['Afternoon', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]]

    midsem_schedule = [
        ['TIME/DATES', '08/10', '09/10', '10/10', '11/10', '12/10', '13/10'],
        ['9:00 - 10:30 AM', '', '', '', '', '', ''],
        ['11:00 - 12:30 AM', '', '', '', '', '', ''],
        ['1:30 - 3:00 PM', '', '', '', '', '', ''],
        ['3:30 - 5:00 PM', '', '', '', '', '', '']]

    def create_timetable(self) :
        '''
        Replaces your timetable to its initial state. 
            
            @variables :
                self.weekly_schedule : List
                    Labels in the weekly timetable
                compre_label : Gtk.Label
                    Displays "COMPREHENSIVE EXAMINATION"
                self.compre_schedule : List
                    Label in the compre schedule
                midsem_label : Gtk.Label
                    Displays "MID SEMESTER EXAMINATION"
                self.midsem_schedule : List
                    Label in the midsem schedule

        '''

        l = []
        for row in range (len(Timetable.weekly_schedule)) :
            for col in range (len(Timetable.weekly_schedule[row])) :
                label = Gtk.Label(label = Timetable.weekly_schedule[row][col])
                self.page00_weekly.attach(child = label, left = col, top = row,\
                width = 1, height = 1)
                l.append(label)
            self.Label_list_weekly.append(l)
            l = []        


        compre_label = Gtk.Label()
        compre_label.set_markup(
            "<big> <b> COMPREHENSIVE EXAMINATION </b> </big>")
        self.page00_compre.attach(child = compre_label,
            left = 0, top = 0, width = 3, height = 1)

        for row in range(len(Timetable.compre_schedule)) :
            for col in range (len(Timetable.compre_schedule[row])) :
                label = Gtk.Label(label = Timetable.compre_schedule[row][col])
                self.page00_compre.attach(child = label, left = row, top = col + 1,\
                    width = 1 , height = 1)
                l.append(label)
            self.Label_list_compre.append(l)
            l = []


        midsem_label = Gtk.Label()
        midsem_label.set_markup(
            "<big> <b> MID SEMESTER EXAMINATION </b> </big>")
        self.page00_midsem.attach(child = midsem_label,
            left = 0, top = 0, width = 5, height = 1)



        for row in range(len(Timetable.midsem_schedule)) :
            for col in range (len(Timetable.midsem_schedule[row])) :
                label = Gtk.Label(label = Timetable.midsem_schedule[row][col])
                self.page00_midsem.attach(child = label, left = row, top = col + 1,\
                    width = 1 , height = 1)
                l.append(label)
            self.Label_list_midsem.append(l)
            l = []


    def clear_timetable(self, widget, data = None) :
        '''
        Replaces your timetable to its initial state.
        This is a callback method for a Gtk.MenuItem widget (clear_all_menu). 

            @parameters :
                widget : Gtk widget object
                data : default = None 
                    Any additional data needed to be passed to the method.

            @variables :
                Label_list_weekly : List 
                    List of Gtk.Labels
                Label_list_compre : List
                    List of Gtk.Labels
                Label_list_midsem : List
                    List of Gtk.Labels
                added_courses : List
                    List of str containing course codes (distinct) in your timetable.
                save_count : int
                    Determines whether to use self.save_list method.
        '''
        for row in range (len(self.Label_list_weekly)) :
            for col in range (len(self.Label_list_weekly[row])) :
                self.Label_list_weekly[row] [col].set_label(
                    Timetable.weekly_schedule[row][col]) 
        
        for row in range(len(self.Label_list_compre)) :
            for col in range(len(self.Label_list_compre[row])) :
                self.Label_list_compre[row][col].set_label(
                    Timetable.compre_schedule[row][col])

        for row in range(len(self.Label_list_midsem)) :
            for col in range(len(self.Label_list_midsem[row])) :
                self.Label_list_midsem[row][col].set_label(
                    Timetable.midsem_schedule[row][col])

        self.catalog_info = []
        self.catalog_store.clear()  
        self.save_count = 0
        self.added_courses = []


    def update_compre_schedule(self, compre_date, label) :
        '''
        Adds entry to compre schedule.
            @parameter : 
                compre_date : str
                    str value of the form "DD/MM AN" or "DD/MM FN", 
                    where AN and FN are the afternoon and forenoon 
                    sessions respectively.
            
        '''

        date = compre_date.split()[0].split('/')
        session = compre_date.split()[-1]
        if session == 'AN' : session = 2
        elif session == 'FN' : session = 1

        try :
            self.Label_list_compre[session][int(date[0])].set_label(
            label)
            # these statements will catch an exception when, there is either
            # a null value or '*' in date or session variables. 

        except : 
            pass


    def update_midsem_schedule(self, match_parameter, label) :
        '''
        Adds entry to midsem schedule.
            @parameter :
                match_paramter : tuple
                    tuple of string (course code,)
                label : The text to be displayed in the schedule.
        '''
        self.sobject.get_midsem_details(match_parameter)
        date = self.sobject.midsem_date.split('/')[0]
        time = self.sobject.midsem_time

        if time == '9.00 -- 10.30 AM' : time = 1
        elif time == '11.00 -- 12.30 PM' : time = 2
        elif time == '1.30 -- 3.00 PM' : time = 3
        elif time == '3.30 -- 5.00 PM' : time = 4
        
        try :
            self.Label_list_midsem[time][int(date) - 7].set_label(
                label)
            # these statements will catch an exception when, there is either
                # a null value or '*' in date or session variables. 
        except :
            pass
 
    def update_timetable(self, widget, path, treecolumn, store, section_type) :
        '''
        This is a callback method for Gtk.CellRendererToggle object. This 
        method also adds dialog box if a course is clashing with other courses or 
        when you change sections of a already selected course. 

            @parameters :
                path : int
                    Row index of the treeview object which is selected.
                treecolumn : Gtk.TreeViewColumn
                store : Gtk.ListStore
                    Contains the details of all the available choices.
                section_type : str
                    Contains the string value of the type of section

            @variables :
                self.selected_section : str 
                    Contains selected section number
                self.selected_instructor : str 
                    Contains selected instructor names
                self.selected_hour : list
                    Contains a list of strings of times of the course section
                self.selected_day : list
                    Contains a list of strings of days of the course section

                self.added_course : list
                    Contains a list of all the course_code a user has opted for.  
        '''
        try :
            self.selected_section = store[path][0]
            if not self.selected_section :
                self.selected_section = '1' 

            self.selected_instructor = store[path][1]
            self.selected_day = store[path][2].split()
            self.selected_hour = store[path][3].split()

            for i in range (len(self.selected_hour)) :
                self.selected_hour[i] = int(self.selected_hour[i])


            self.text_to_display = self.selected_course_code + '\n' + \
            section_type + '-' + self.selected_section

            self.info = self.selected_course_code + ';' + \
             self.selected_course_title + ';' + \
             section_type + '-' + self.selected_section + ';' +\
             self.selected_instructor + ';' +\
             store[path][2] + ';' + store[path][3] +\
             ';' + self.selected_compre_date

        except :
            pass

    
        for row in self.catalog_info :
            list_ = row.split(';')

            if 0 in self.selected_hour :
                break
            
            flag = 0
            for hr in self.selected_hour :
                for dy in self.selected_day :
    
                    if str(hr) in list_[-2].split()  \
                    and dy in list_[-3].split() \
                    and self.selected_course_code != list_[0]:
                        self.handle_clash_time(row)
                        flag = 1
                        break 
                if flag == 1 :
                    break
            
            if flag == 1 :
                break

            if self.selected_course_code in self.added_courses :

                if section_type == list_[2].split('-')[0]\
                    and self.selected_course_code == list_[0] :
                    self.handle_section_change(row, section_type)
                    break
                    
                else :
                    pass

            else :
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)
                self.added_courses.append(self.selected_course_code)
                break               

        else :
            if 0 not in self.selected_hour:
                self.add_to_timetable(self.selected_hour, self.selected_day)
                self.catalog_info.insert(0, self.info)
                self.added_courses.append(self.selected_course_code)
        
        self.add_to_catalog()       
        self.page01_notebook.next_page()
        self.update_compre_schedule(self.selected_compre_date, \
                label = self.selected_course_code)
        self.update_midsem_schedule(
            match_parameter = (self.selected_course_code,),\
            label = self.selected_course_code)


    def add_to_timetable(self, hours, days) :
        '''
        Adds the selected section to the timetable.
            @variables :
                hours : list 
                    Contains a list of integers 
                days : list 
                    Contains a list of string objects.
                        (M, T, W, Th, F, S)
        '''
        for row in hours :
            for col in days : 
                if col == 'M' : 
                    self.Label_list_weekly[row][1].set_label(self.text_to_display)
                elif col == 'T' : 
                    self.Label_list_weekly[row][2].set_label(self.text_to_display)
                elif col == 'W' : 
                    self.Label_list_weekly[row][3].set_label(self.text_to_display)
                elif col == 'Th' : 
                    self.Label_list_weekly[row][4].set_label(self.text_to_display)
                elif col == 'F' : 
                    self.Label_list_weekly[row][5].set_label(self.text_to_display)
                elif col == 'S' : 
                    self.Label_list_weekly[row][6].set_label(self.text_to_display)


    def remove_course(self, widget, path, treeview, store, *data) :
        '''
        This method is called to remove the courses selected in the catalog page. This 
        is also a callback method for Gtk.Button (self.remove_label). This method also shows 
        dialog box warning the user to confirm before removing a course.
        '''

        row = store[path]
        remove_course_title = row[1]
        remove_course_code = row[0]
        remove_section = row[2]
        remove_hour = row[-2]
        remove_day = row[-3]
        remove_compre= row[-1]

        dialog = Gtk.MessageDialog(self, 0, 
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, 
            "You are about to remove the selected course")
        
        dialog.format_secondary_text(
            "Press OK to continue or CANCEL to abort")
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            for col in remove_day.split() :
                for row in remove_hour.split() :
                    if col == 'M' :
                        self.Label_list_weekly[int(row)][1].set_label('')
                    elif col == 'T' :
                        self.Label_list_weekly[int(row)][2].set_label('')
                    elif col == 'W' :
                        self.Label_list_weekly[int(row)][3].set_label('')
                    elif col == 'Th' :
                        self.Label_list_weekly[int(row)][4].set_label('')
                    elif col == 'F' :
                        self.Label_list_weekly[int(row)][5].set_label('')
                    elif col == 'S' :
                        self.Label_list_weekly[int(row)][6].set_label('')


            count = 0
            remove_string = ''
            for strings in self.catalog_info :
                if remove_course_code in strings :
                    count += 1

                if remove_course_code in strings \
                and remove_section in strings :
                    remove_string = strings


            if count == 1:
                self.added_courses.remove(remove_course_code)
            
            self.catalog_info.remove(remove_string)

            self.add_to_catalog()
            dialog.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        if remove_course_code not in self.added_courses :
            session = remove_compre.split()[-1]
            date = remove_compre.split()[0].split('/')[0]
            if session == 'AN' : session = 2
            elif session == 'FN' : session = 1

            self.Label_list_compre[session][int(date)].set_label('')

            self.update_midsem_schedule(
                match_parameter = (remove_course_code,),\
                label = '')
