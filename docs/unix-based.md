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
1. Install gi according to your OS:
    * Ubuntu:
    ```bash
        sudo apt libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
    ```
    * Fedora:
    ```bash
        sudo dnf install python3-gobject gtk3
    ```
    * Arch Linux
    ```bash
        sudo pacman -S python cairo pkgconf gobject-introspection gtk3
    ```
    * OpenSUSE
    ```bash
        sudo zypper install cairo-devel pkg-config python3-devel gcc gobject-introspection-devel
    ```
    * macOS
    ```bash
        brew install pygobject3 gtk+3
    ```

2. Move to repo's directory using the following command.
```bash
    cd OFFLINE-ERP/
 ```

3. Install the virtual environment
```bash
    pip3 install pipenv
```
4. Activate the virtual env
```bash
    pipenv shell
```
5. Download the dependencies
```bash
    pipenv install
```

## Deployment 
Run this command after activating your virtual environment (Step 4).

```python
python3 main.py 
```
