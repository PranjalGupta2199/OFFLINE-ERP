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
1. Go the official site of [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) and download the latest version of msys2 (x86_64 for 64 bit machines and i686 for 32bit machines).
2. Run the setup, go to the installed location and open the **msys2.exe** executable. Note that there are three applications in the installed directory : 
    - msys2.exe
    - mingw64.exe
    - mingw32.exe
    Make sure that you open **msys2.exe**.
3. In the MSYS2 shell, execute the following.
    ```bash
        pacman -Syuu
    ```
    **Close the shell once you are asked to.** Reopen MSYS2. **Repeatedly** run the following command until it says there are no further updates. You might have to restart your shell again.
    ```bash
        pacman -Syuu
    ```
    Now that msys2 is fully up-to-date, we will install the dependencies.
4. Run the following steps in sequence on the mingw64 shell (if 64bit machine):
    ```bash
        pacman -S mingw-w64-x86_64-python3-reportlab
    ```
    After installation, make sure that _reportlab_ is properly installed by typing these commands.
    ```python
        $ python
        >>> import reportlab
        >>> # If no error occurs, then success ! Else try again
        >>> exit()
    ```
    Now we need to install **pip** for installing other dependencies. Run the following command:
    ```bash
        pacman -S mingw-w64-x86_64-python-pip
    ```

    Ensure pip is properly installed by checking it's version.
    ```bash
        pip --version
    ```

    Now install **pandas** libaray by typing the following command:
    ```bash
        pacman -S mingw-w64-x86_64-python3-pandas
    ```
    Again ensure that pandas is properly installed by importing in a python shell.

    Install **tabula-py** and **PyPDF2** library by typing the following command:
    ```bash
        pip3 install tabula-py PyPDF2
    ```

    Instal **PyGObject** and **Gtk3** using the following commands:
    ```bash
        pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject
    ```
    **Ensure that all the libraries are properly installed.**

5. You can now either install **git** on the MSYS2 shell or simply download the zip of this repo and move it inside 
    ``` <path to installed directory>\home\<username>\ ``` (for example ``` C:\\msys64\\home\\Pranjal Gupta\\```). 

    Move to the repository directory
    ```bash
        cd OFFLINE-ERP-master
    ```
    and run the **main.py** file
    ```python
        python main.py
    ```

    To resolve any error, follow this [doc](docs/error.md). If the error still persists, please file an issue on the issue page.