# Global Behavior
This behavior is universal to Starling no matter what mode you are in.
## Switching Modes
To switch to a different mode, say one of the following phrases.
` Command mode`
` Shell mode`
` Dictation mode`
` Sleep mode`

## Timer
For many users fighting repetitive strain injury, having a system timer to remind them to take breaks  is particularly useful. As result, I have included a timer by default in Starling.  The following two commands can be used to start and stop the timer respectively
`start timer`
`end timer `

 This timer will automatically print a message to the screen if you have been working for longer than the time specified in the config file.  This message will not go away until you have taken a break. A break is detected if you have ben idle at the computer for longer than the specified amount of time in the config file.
## Tray Indicator
Starling  uses a tray indicator that is compatible with most system trays on Linux.  This tray indicator can be used to quit the application, start a timer, or end a timer. Sleep mode  is represented with a moon icon. 

 All communications with the tray is done using a local socket.  You do not need to understand how this works in order to use Starling. However,  you should avoid using local port 9999  since this is where the Starling messages are sent.