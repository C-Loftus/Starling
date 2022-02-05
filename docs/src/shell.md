# Shell Mode

Shell mode executes user input as a shell command. Shell commands are sourced from the config file of the default shell. Therefore, aliases and functions can both be called from shell model with natural language names that the user can define.

```bash
## example: Saying "dim" will automatically lower system brightness
## located in ~/.bashrc
alias dim="xrandr --output eDP --brightness .3"
## example: Saying "mute" will automatically mute system volume
alias mute="amixer -q sset Master toggle"
```

This functionality allows the power and flexibility of the shell in conjunction with natural language commands the user can define. In order to gain the maximum flexibility from Starling,  users are encouraged to extend behavior in this way. 

Shell mode sources commands from the default shell. Therefore it should work with bash, zsh, fish, and more.

## Safety
By default, Starling  has a safety feature which will alert the user and give a warning before executing a command. This is since the shell is very powerful, it has the ability to manipulate many things on the system, even without root. However, the alert buffer time can be reduced in the config file if  it is a nuisance.

 Since Starling  sources from the confit file of the shell, there is no risk of calling arbitrary shell commands like `rm`  unless it is specifically aliased or used in a function within the config file.

### Indicator

 Shell mode is represented with a green circle in the dock.