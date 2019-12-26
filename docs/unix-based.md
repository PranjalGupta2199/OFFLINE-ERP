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

Virtual Environment - [pipenv](https://github.com/pypa/pipenv)

## Installation 
Go to this [link](https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-getting-started), find your OS and install gi on your system.

Move to repo's directory using the following command.
```bash
    cd OFFLINE-ERP/
 ```

Install the virtual environment 
```bash
    pip3 install pipenv
```
Activate the virtual env
```bash
    pipenv shell
```
Download the dependencies 
```bash
    pipenv install
```

## Deployment 
Run this command after activating your virtual environment.

```python
python3 main.py 
```
