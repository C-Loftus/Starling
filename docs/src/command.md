# Command Mode
Command mode executes key presses, commands defined in the config file,  shorter dictations, or window control commands.
## Raw Keyboard Input
Raw input from the keyboard is the easiest way to control your computer with Starling. Simply say the name of the keys that you wish to press.

You can press any keyboard combination by saying the name of a key. Since many of the letters  of the alphabet are very similar, Starling defines an alphabet in the config file. For instance 
`super cap` will  be decoded as a press of super and c at the same time. 
 the following is the alphabet as it is defined in the default config file, config.toml in the Starling project root directory.
 You can change any of these key value pairs to a different word if you  prefer the use of other words.


```yaml
alphabet: 
  - air       : "a" 
  - bat       : "b" 
  - cap       : "c" 
  - drum      : "d" 
  - each      : "e" 
  - fine      : "f" 
  - gust      : "g" 
  - harp      : "h" 
  - sit       : "i" 
  - jury      : "j" 
  - crunch    : "k" 
  - look      : "l" 
  - made      : "m" 
  - near      : "n" 
  - odd       : "o" 
  - pit       : "p" 
  - quench    : "q" 
  - red       : "r" 
  - sun       : "s" 
  - trap      : "t" 
  - urge      : "u" 
  - vest      : "v" 
  - whale     : "w" 
  - plex      : "x" 
  - yank      : "y" 
  - zip       : "z"    
  - enter     : "enter"
  - escape    : "escape"
  - home      : "home"
```

## Window Commands
 window commands are the  second type of commands built into command mode. 
 Window comands can  launch ,  close, maximize, minimize, or focus a window. Window command syntax is as follows
```
(window_action) (window_target)
```
#### Window Actions
 * `start`
 * `close`
 * `maximize`
 * `minimize`
 * `focus`
#### Window Targets
 the best way to achieve maximum accuracy with window targets is to define alias is in the  config file. This is since there are many programs on Linux with unnatural sounding names. For instance, it is much quicker and more natural to say `terminal`  instead of `urxvt`.  

 if you wish to launch a  window based on its name, you must define the `exe_path`  for the application in the config file. Otherwise, Starling does not know where you want to launch the application from.

  The built in alias `this`  will always alias to the currently focused window.
  ```bash
  #  Example  when firefox is the currently focused window
  #  this command will minimize firefox
  minimize this
  ```

   You can define your own aliases in the config file by specifying a key and a application name that corresponds to it.  It is best to pick key names that are simple and distinct. This improves accuracy and reduces command length.

## Dictations Without Switching Mode
 sometimes you will want to dictate short sentences without needing to switch mode two dictation mode. If you want this behavior say `sentence`  before the words you wish to say.
 ```toml
 #example to print the words "this is a test that will be input as text  even in command mode
sentence this is a test that will be input as text even in command mode
 ```


## Custom Natural Language Shortcuts
If you wish to define custom commands, it can be easily done in the config file. All you need to do is give the name of the application and list of key value pairs.
 In order to avoid commands being miscategorized as window actions or key presses, you should avoid any of the window action keywords or words you have defined to be in your alphabet.
#### A Bad Example
 ```yaml
 # AVOID COMMANDS LIKE THIS
 Google Chrome:
 #  focus is a window action keyword so it should be avoided.
 - focus tab: "ctrl \t"
 #  air and cap correspond to  key presses of "a" and "c" respectively in the predefined alphabet.
 - air cap: "alt left"
 ```
#### A Good Example
```yaml
#  Good examples for mozilla firefox
Mozilla Firefox:
- exe_path : "firefox"
- go foward: "alt right"
- go back: "alt left"
- next tab: "ctrl \t"
- private tab: "ctrl shift p"
- new bookmark: "ctrl d"
- search bar: "ctrl j"
- fold window: "ctrl w"
```

#### Help
 If you do not know the official name of the application you wish to define custom shortcuts for, run the following command and then click on the window you wish to know the name of.  The sleep command is needed so it doesn't just give you the name of the terminal before you can click off it.
 ```bash
 sleep 3; xdotool getactivewindow getwindowname
 ```
 xdotool   should already be installed once you install starling. this command above will give you the name of the window that you should put in the config file.

