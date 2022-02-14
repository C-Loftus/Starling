# Command Mode
Command mode executes key presses, commands defined in the config file,  short dictations, or window control commands. Command mode is indicated with an orange icon on the system tray.


## Dictations Without Switching Mode
 Sometimes you will want to dictate short sentences without needing to switch mode two dictation mode. If you want this behavior say `sentence`  before the words you wish to say.
 ```toml
 # prints the words "test of dictating text even in command mode"
sentence test of dictating text even in command mode
 ```

#### Help
 If you do not know the official name of the application you wish to define custom shortcuts for, run the following command and then click on the window you wish to know the name of.  The sleep command is needed so it doesn't just give you the name of the terminal before you can click off it.
 ```bash
 sleep 3; xdotool getactivewindow getwindowname
 ```
 xdotool  should already be installed once you install starling. this command above will give you the name of the window that you should put in the config file.

