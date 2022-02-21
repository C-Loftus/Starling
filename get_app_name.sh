#!/bin/bash
echo "Click on your window to get its name. This is the name that will be used in the config file.\nPress ctrl-c to stop\n"

while ["" == ""]; do
sleep 3
echo "Currently focused window is: "
pipenv run python3 src/Desktop/xdotool_wrappers.py 2>/dev/null
done