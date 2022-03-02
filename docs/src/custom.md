## Custom Natural Language Shortcuts
If you wish to define custom commands, it can be easily done in the config file. All you need to do is give the name of the application and list of key value pairs.
 In order to avoid commands being miscategorized as window actions or key presses, you should avoid any of the window action keywords or words you have defined to be in your alphabet.
You should also refer to applications by their aliases  as they are defined in the config file. This reduces any miscategorization chance,  especially with applications that have unusual names.


The  config file is set up as follows
* aliases to app names
* app names as they are seen by the os
*  natural language commands which are ran in the context only when a window with that app name is focused

#### How to get the proper application names
When customizing, you must used the proper name for the application as it is seen within the OS.  Otherwise, Starling will not know  exactly which application you're referring to.

To do this you can use the following script. Simply  Run the script and click on the window that you want to know the proper name of.
```bash
cd Starling
# use chmod to make sure it is executable. Only need to do this once
chmod +x get_app_name.sh
./get_app_name.sh
```

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

#### Best Practices
 I recommend using an editor  like visual studio code in order to make sure you don't have any errors in your yaml syntax. yaml is parsed  in any order but I recommend keeping the order as it is defined in the given sample config. Namely, aliases, names, then commands.