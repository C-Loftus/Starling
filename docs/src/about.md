# About
Starling is a general purpose voice control program for Linux. It was especially created with the goal of helping people with disabilities or hand injuries.  It seeks to be easily customizable  and functionally robust. It can 
* start, close, minimize, maximize, and focus windows
*  execute custom natural language commands defined in the config.yaml file
*   automatically type spoken input through speech-to-text
*    execute shell commands
*    and be used along other specialized voice control programs to serve as a general-purpose orchestrator

All speech recognition is done locally on your own device. No cloud APIs are used and there is no third-party interaction with your data whatsoever. After Starling is installed,  it does not need  internet access for any reason.

##  Development Background
 This project was the result of my junior year independent work at Princeton University. 
 
The goal of this project has been to try and reimagine voice control.  For many disabled users, voice control appears to be a second rate solution.  It is often seen as a crutch that feels unnatural and slow.  Many voice control solutions are produced as an afterthought and do not naturally interact with the surrounding system.

As such my goals have been to create a program with:
 *   generalizable behavior that can control the entire system
 *  a clear and verifiable policy of no data collection
 *   clear documentation for customizing
 *   intuitive behavior for new users
 *   full support on many Linux distributions
 *  free and open source licensing

My goal is to have the program be as easy or complex as the user wanted it to be. Namely, if a user  doesn't have any programming experience,  the program can be entirely customized in a config file. However, if a user does have programming experience, the program can  draw upon all existing scripts or aliases  sourced in default shell.

## Help


For a detailed list of program functionality please consult this website. If you have a technical problem or found a bug please feel free to create a [Github issue](https://github.com/C-Loftus/Starling/issues).