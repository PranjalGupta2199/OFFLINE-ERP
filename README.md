# Offline ERP for BPHC 
Tired of making your timetable on paper ? Offline ERP is here to help you !!
This is a basic desktop application made using python which allows you to select courses (CDCs and Electives) for your timetable.  
 
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
  - Opted courses.

##### Note :
1. This app works only for python 2.x versions because tabula-py is not available for python 3.x versions
2. Please install Java as tabula requires it. 
    To verify if Java is installed , type 
    ```
    $ java
    ```
    on your terminal/command prompt.
    You can install it from this [link.](https://java.com/en/download/help/download_options.xml)

## Getting Started
You are going to need :
- [_python_](https://www.python.org/downloads/source/)
- [_git_](https://git-scm.com/downloads/)
- [_pip_](https://pip.pypa.io/en/stable/installing/)


    
To download the repo use : 
```
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
gi - Click on this [link](http://pygobject.readthedocs.io/en/latest/getting_started.html) to install the package for your os.

 
Move to repo's directory for the following command.
```
    cd OFFLINE-ERP/
 ```

Run this command to install the remaining dependencies : 

    pip install -r requirements.txt --ignore-installed 

## Deployment 
Run this command after following all the steps above.

```python
python main.py 
```
Note :
1. You need to run the above command everytime you want to use the app. 
2. The app will take sometime when using it for the first time. If you close the window during the process, run these commands :
    ```
        $ rm -r Pages/
        $ rm packages/courses.db
    ```
    Run the python command again.
3. If you face any difficulty, please go through this [page.](https://github.com/chezou/tabula-py) If the problem persists, report it in the Issues Page.
4. If you want to run this app with a new pdf, follow Note pt 2.

## Author
-  [**Pranjal Gupta**](https://github.com/PranjalGupta2199/)

## TODOs

- Add compre and midsem schedule 
- Add credits to your timetable
- Extend support for other campuses 

