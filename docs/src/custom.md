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