# Command Mode
Command mode executes key presses, commands defined in the config file,  short dictations, or window control commands. Command mode is indicated with an orange icon on the system tray.

## Usage and customizing
Starling comes with a sample config file. If you just want to use keyboard commands you do not need to modified anything. If you want to use custom natural language commands, you will need to edit the config file to include the applications you will be using and what words you wish to do what actions.

When setting up the config file  you will need to know the names of the applications as they appear to the OS. If you do not know this, you can use a provided script.
`get_app_name.sh`

This simple script  will print out the name the application as it will be read in the config file. For more detail on how to use these names to customize, please see [the custom chapter](custom.md).

## Dictations Without Switching Mode
 Sometimes you will want to dictate short sentences without needing to switch mode two dictation mode. If you want this behavior say `sentence`  before the words you wish to say.
 ```toml
 # prints the words "test of dictating text even in command mode"
sentence test of dictating text even in command mode
 ```

#### Help
Please feel free to submit any issues on [Github](https://github.com/C-Loftus/Starling/issues)



