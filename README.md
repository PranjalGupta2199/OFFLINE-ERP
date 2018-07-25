# Offline ERP for BPHC 
Tired of making your timetable on paper ? Offline ERP is here to help you !!
This is a basic desktop application made using python which allows you to select courses (CDCs and Electives) for your timetable. 

**_Note : This App has been tested for linux systems only._**

**This app works only for python 2.x versions because tabula-py is not available for python 3.x versions**

**Please go through the Note Section at the end. It contains the most common errors and tips which you should keep in mind while using it.**

## Features
It allows you to - 

  - Select your courses 
  - Save it in pdf format
  - Open your last saved/unsaved work

You can view your :
  - Weekly Schedule
  - Compre Schedule
  - Midsem Schedule
  - List of all the available courses 
  - Opted courses

This app will give you warnings/ dialog box :
  - When you change a section of a class
  - When there is time clash
  - When you choose a course which has same compre date and session
  - When you don't create a database or exit your work without saving it


## How to Use :
1. Double click on the row to select any course, lecture, practical or tutorial.
2. If there are no sections available for a particular course, the list will display NA. You can select NA to automatically move onto the next page or
  you can manually select the class type.
3. You need to remove all the section(s) associated with a particular course to delete it from exam timetable.
4. If you want to change a section of a course which you have already opted, search the course and directly select the section you want.



## Getting Started
You need to install these :
- [_python_](https://www.python.org/downloads/source/)
- [_git_](https://git-scm.com/downloads/)
- [_pip_](https://pip.pypa.io/en/stable/installing/)


    
To download the repo use : 
```git
    git clone https://github.com/PranjalGupta2199/OFFLINE-ERP.git
```



##  Prerequisites
You are going to need the following libraries :
- gi
- pandas 
- PyPDF2 
- tabula 
- reportlab

## Installation
**GI** - Click on this [link](http://pygobject.readthedocs.io/en/latest/getting_started.html) to install the package for your os.

 
Move to repo's directory using the following command.
```bash
    cd OFFLINE-ERP/
 ```

Run this command to install the remaining dependencies : 

    pip install --user -r requirements.txt --ignore-installed 


## Deployment 
Run this command after following all the steps above.

```python
python2 main.py 
```
### Note :
1. Use only pip (for python 2.x version).
2. You need to run the above command everytime you want to use the app. 
3. The app will take sometime (usually 2-3 minutes) when using it for the first time. If it takes more time than that expected, close the window and run the python command again.
4. Please install Java as tabula requires it. 
    To verify if Java is installed , type 
    ```bash
    $ java 
    ```
    on your terminal/command prompt.
    You can install it from this [link.](https://java.com/en/download/help/download_options.xml)



5. If you face any difficulty related to tabula, please go through this [page.](https://github.com/chezou/tabula-py) If the problem persists, report it in the Issues Page.

6. If you want to run this app with a new pdf, run these commands : 
```bash
    $ rm -r Pages/
    $ rm packages/courses.db
    $ python2 main.py
```
  Please make sure you make appropriate changes to the files packages/search.py and packages/page_01.py so that te pdf can be parsed correctly or else some unexpected error might occur.

7. If you come across the error below, try the following links :
    1. [Link1](https://stackoverflow.com/questions/49836676/error-after-upgrading-pip-cannot-import-name-main) 
    2. [Link2](https://stackoverflow.com/questions/49881448/importerror-cannot-import-name-main-after-upgrading-to-pip-10-0-0-for-python)
```bash
  File "usr/bin/pip", line 9, in <module>
    from pip import main
  ImportError : cannot import name 'main'

```

8. If you come across this error, try installing Java. If the problem still persists, go to the link given in pt 3.
```bash
  File "/home/<username>/.local/lib/python2.7/site-packages/tabula/wrapper.py", line 87, in read_pdf
    output = subprocess.check_output(args)
  File "/usr/lib/python2.7/subprocess.py", line 394, in __init__
    errread, errwrite)
  File "/usr/lib/python2.7/subprocess.py", line 1047, in _execute_child
    raise child_exception
  OSError: [Errno 2] No such file or directory
```

9. You might come across something called as AbstractMethodError such as this :
```bash
    ImportError: cannot import name AbstractMethodEror
```
This is due to pandas version. Roll back to any previous version of pandas and try running the app.


## Author
-  [**Pranjal Gupta**](https://github.com/PranjalGupta2199/)

## TODOs
 
- Add credits to your timetable
- Extend support for other campuses 

