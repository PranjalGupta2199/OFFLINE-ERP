### Note :
1. Use pip (for python 3.x version).
2. You need to run the above command everytime you want to use the app. 
3. The app will take sometime (usually 2-3 minutes) when using it for the first time. If it takes more time than expected, close the window and run the python command again.
4. Please install Java as tabula requires it. (Confirmed working with Java 7 and 8)

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
    $ python3 main.py
```
  Please make sure you make appropriate changes to the files packages/search.py and packages/page_01.py so that the pdf can be parsed correctly or else some unexpected error might occur.

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
    ImportError: cannot import name AbstractMethodError
```
  Roll back to any previous version of pandas and try running the app.
