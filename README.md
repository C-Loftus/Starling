## About
This program is a general purpose voice control program for Linux. It was especially created with the goal of helping people with disabilities or hand injuries.  It seeks to be easily customizable  and functionally robust. It can control  windows, execute commands defined in the config.yaml  file,  automatically type spoken input through speech-to-text, execute shell commands,  or serve as a general-purpose orchestrator between other application-specific voice control programs.

All speech recognition is done locally on your own device. No cloud APIs are used and there is no third-party interaction with your data whatsoever.
## Building
You must have python3, pip3, and make installed. These should already be installed on most distributions. 
To build, type either your package manager name or OS name. (i.e. `ubuntu`, `pop-os`, `apt` all build the same)
```
make ubuntu 
```
To uninstall
```
make uninstall
```
## Running
pipenv installs all python packages in this folder. That way they will not conflict with your existing python environments. `pipenv` before the command will run it in this environment.
```
pipenv python3 src/main.py
```
## Help
For a detailed list of program functionality please consult the project's website here: https://c-loftus.github.io/StarlingDocs/

If you have a technical problem or found a bug please feel free to create a Github issue.

