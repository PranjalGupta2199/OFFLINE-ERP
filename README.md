# Offline ERP for BPHC 
Tired of making your timetable on paper ? Offline ERP is here to help you. This is a basic desktop application made using python which allows you to select courses (CDCs and Electives) for your timetable.  
You just need the pdf of the timetable booklet. Then you can 
  - Search courses based on your course code/title
  - Pop-up windows will appear in events of clashing time or when changing section
 

## Features
It allows you to - 

  - Select your courses, and 
  - Save it in pdf format.
 
## Getting Started
You are going to need :
- _python_
- _git_
- _pip or Anaconda/Miniconda_

Download python depending on your os from the given links :
- [Windows](https://www.python.org/downloads/windows)
- [Linux/Unix](https://www.python.org/downloads/source/)
- [MacOS](https://www.python.org/downloads/mac-osx/)
    
To download the repo use : 
```
    git clone https://github.com/PranjalGupta2199/OFFLINE-ERP.git
```
To download pip, use this [link.](https://pip.pypa.io/en/stable/installing/)
To download Anaconda/Miniconda, use this [link.](https://conda.io/docs/user-guide/install/index.html)

##  Prerequisites
You are going to need he following libraries :
- gi
- pandas 
- PyPDF2 
- tabula 
- reportlab

## Installation

##### gi 
- Linux 
    - [Ubuntu](http://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-getting-started)
    - [Fedora](http://pygobject.readthedocs.io/en/latest/getting_started.html#fedora-getting-started)
    - [OpenSUSE](http://pygobject.readthedocs.io/en/latest/getting_started.html#opensuse-getting-started) 
- [Windows](http://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started)
- [MacOS](http://pygobject.readthedocs.io/en/latest/getting_started.html#macosx-getting-started)

##### Pandas
Anaconda/Miniconda comes with this package installed. So you don't need to run this package.

    pip install pandas

##### PyPDF2
    pip install PyPDF2

##### Tabula 
    pip install tabula-py

##### Reportlab 
    pip install reportlab


## Deployment 

After completing the above steps,run this command : move to the directory where the git repo has been downloaded and run the following command on your terminal or command prompt : 

```python
python main.py 
```
Note :
1. You need run the above command everytime you want to run the app
2. Please add environment variable in your command line (Windows) if there is an error.

## Author
-  **Pranjal Gupta**

## TODOs
- Add compre and midsem schedule 
- Extend support for other campuses 

