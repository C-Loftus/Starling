# Intallation 
## Downloading the Code
 You can either download  the project from GitHub as a zip file or clone it with Git. It  is recommended to do the latter  in order to stay up to date with any project changes or bug fixes. You  must have Git  installed in order to run this command.
 ```bash
git clone https://github.com/C-Loftus/Starling
 ```

## Building
Once you have downloaded the code, you can then begin the process of setting it up.
You must have python3, pip3, and make installed. These should already be installed on most distributions. 
To build, type either your package manager name or OS name. (i.e. `ubuntu`, `pop-os`, `apt` all build the same)
```
make ubuntu 
```
 The installation process will install all python dependencies and download the model used for voice recognition.

To uninstall
```
make uninstall
```

## Running
pipenv installs all python packages for Starling in its own separate folder. That way they will not conflict with your existing python environments. `pipenv` before the command will run it in this environment.
```bash
cd Starling
pipenv run python3 src/main.py
```
