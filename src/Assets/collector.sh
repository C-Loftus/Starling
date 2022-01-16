#!/bin/bash
# Ansi color code variables
red="\e[0;91m"
blue="\e[0;94m"
expand_bg="\e[K"
blue_bg="\e[0;104m${expand_bg}"
red_bg="\e[0;101m${expand_bg}"
green_bg="\e[0;102m${expand_bg}"
green="\e[0;92m"
white="\e[0;97m"
bold="\e[1m"
uline="\e[4m"
reset="\e[0m"


arr=(
"editor"
"browser"
"terminal"
"air"
"bat"
"cap"
"drum"
"each"
"fine"
"gust"
"harp"
"sit"
"jury"
"crunch"
"look"
"made"
"near"
"odd"
"pit"
"quench"
"red"
"sun"
"trap"
"urge"
"vest"
"whale"
"plex"
"yank"
"zip"
"zero"
"one"
"two"
"three"
"four"
"five"
"six"
"seven"
"eight"
"nine"
"focus_editor"
"close_editor"
"focus_browser"
"close_browser"
"focus_terminal"
"close_terminal"
"control_shift_each"
"super_alt_cap"
"control_alt_whale"
"control_page_up"
)

echo 'gender: m/f'
read gender

echo 'age'
read age

echo 'dialect'
read dialect

d=$(date +%Y-%m-%d-%I)

dir="training/${gender}_${age}_${dialect}_${d}"

mkdir -p $dir

for i in ${arr[@]};do
    echo -e "\n\n Next Word- >: ${green}${bold}  $i ${reset} \n\n"
    sleep 2
    echo "STARTING RECORDING"
    arecord -vv -fdat $dir/"${i}".wav  >> /dev/null 2>&1
    echo "-e RECORDING DONE"

done