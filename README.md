# Offline ERP for BPHC 
Tired of making your timetable on paper ? Offline ERP is here to help you !!
This is a basic desktop application made using python which allows you to select courses (CDCs and Electives) for your timetable.  
 
## Features
It allows you to - 

  - Select your courses, and 
  - Save it in pdf format.
 
##### Note :
1. This app works only for python 2.x versions because tabula-py is not available for python 3.x versions
2. Please install Java as tabula requires it. 
    To verify if Java is installed , type 
    ```
    $ Java
    ```
    on your terminal/command prompt.
    You can install it from this [link.](https://java.com/en/download/help/download_options.xml)

## Getting Started
You are going to need :
- _python_ 
- _git_
- _pip_


Download python depending on your os from the given links :
- [Linux/Unix](https://www.python.org/downloads/source/)

    
To download the repo use : 
```
    git clone https://github.com/PranjalGupta2199/OFFLINE-ERP.git
```

To download pip, use this [link.](https://pip.pypa.io/en/stable/installing/)


##  Prerequisites
You are going to need the following libraries :
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

Run this command to install the remaining dependencies : 

    pip install -r requirements.txt --ignore-installed 

## Deployment 

After completing the above steps, move to the folder where repo has been downloaded.
Then type these commands :-
```git 
git checkout Develop
```

```python
python main.py 
```
Note :
1. You need run the above (python) command everytime you want to run the app.

## Author
-  **Pranjal Gupta**

## TODOs
- Add compre and midsem schedule 
- Extend support for other campuses 

