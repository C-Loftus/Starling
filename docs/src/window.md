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
