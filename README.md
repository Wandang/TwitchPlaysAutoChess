# TwitchPlaysAutoChess
Twitch Plays AutoChess bot that lets twitch-chat play Dota AutoChess


![GUI](https://github.com/Wandang/TwitchPlaysAutoChess/blob/master/assets/GUI%20sample2.png)

- [REQUIREMENTS](#REQUIREMENTS)
- [INSTALL](#INSTALL)
- [USAGE](#USAGE)

# REQUIREMENTS

- python 3.x
- pynput (cross platform)
- twitch account (+ auth token)
- ~~xdotool (only works on Linux, I am working on a windows alternative)~~


# INSTALL

- Install python
- Install pynput with pip `pip install --user pynput` (--user is optional but keeps the package with user permissions)
- Download and Unzip this project package or if you want to stay up to date use git clone

# USAGE

- Start Dota2
- Go to settings and change the hotkeys like this (including quickcast!): 
![hotkeyssetup](https://github.com/Wandang/TwitchPlaysAutoChess/blob/master/assets/Dota_settings_example.png)
- Navigate to the project folder with a console
- Execute tpacLaunch.py with python `python tpacLaunch.py` (alternatively python3 if you have several python versions)
- Follow all the steps in the setup process of the program

After you have successfully started the bot the bot will write `Connected` into your chatroom

The generated text files can be loaded in OBS (and probably other streaming programs as well) to show the currently read commands


## Important notes

- Only works on 1920x1080 resolution at the moment
- Only tested for Linux. Please create an issue for Windows
- Chicken abilities are fixed for now and need to be set in the Dota Client