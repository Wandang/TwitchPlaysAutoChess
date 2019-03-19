# TwitchPlaysAutoChess
Twitch Plays AutoChess bot that lets twitch-chat play Dota AutoChess


![GUI](https://github.com/Wandang/TwitchPlaysAutoChess/blob/master/assets/GUI%20sample2.png)

- [REQUIREMENTS](#REQUIREMENTS)
- [INSTALL](#INSTALL)
- [USAGE](#USAGE)
- [COMMANDLIST](#COMMANDLIST)

# REQUIREMENTS

- python 3.x
- pynput (cross platform)
- twitch account (+ auth token)

# INSTALL

- Install python
- Install pynput with pip `pip install --user pynput` (--user is optional but keeps the package with user permissions)
- Download and Unzip this project package or if you want to stay up to date use git clone

# USAGE

- Start Dota2
- Go to settings and activate quickcast: 
![hotkeyssetup](https://github.com/Wandang/TwitchPlaysAutoChess/blob/master/assets/Dota_settings_example.png)
- Navigate to the project folder with a console
- Execute tpacLaunch.py with python `python tpacLaunch.py` (alternatively python3 if you have several python versions)
- Follow all the steps in the setup process of the program

After you have successfully started the bot the bot will write `Connected` into your chatroom

The generated text files can be loaded in OBS (and probably other streaming programs as well) to show the currently read commands

There is an example OBS scene/overlay inside the assets folder that can be imported into OBS.

## Important notes

- Only works on 1920x1080 resolution at the moment
- Only tested for Linux. Please create an issue for Windows
- Chicken abilities are fixed for now and need to be set in the Dota Client

# COMMANDLIST (These are written and recognized in Twitch Chat)

## Dota

* Search game: `!search` (search accepts once after 5s, if that lobby does not start you will need to use !accept)
* Accept game: `!accept`
* Calibrate cam: `!calib` (needed for mouse movements to be accurate/work)
* Quit current game: `!rq` (20s grace period. Can be aborted with !stay)
* Stay in current game: `!stay`

## AutoChess
* Picking a chess piece: `!p 1-5`
* Moving a chess piece: `!m source target` (AA, A1...H8)
* Simple version of move: `!aa` or `!cc`, etc (moves unit from bench AA,BB,CC,etc directly onto the chessboard)
* Benching a chess piece: `!b target` (A1...H8)
* Selling a chess piece: `!s target` (AA, A1...H8)
* Reroll chess pieces: `!r`
* Buy XP: `!x 1-4`
* Activate lock selection: `!l`
* Show shop: `!shop on/off`
* Grabbing items: `!g target` (AA, A1...H8)
* Grabbing items outside chessboard: `!run side` (left,right,top,bot)
* Item to hero: `!i slot target` (!i 4 AA will give the 4th item in the chicken to the hero on pos AA)
* Lock/Unlock Item: `!il / !iul slot`
* Checking the compositions of other players: `!tab (1-8)` (will check the player at pos 1-8 or if no pos given everyone in 5s)
* Write in allchat: !write message

## Examples:
* pick piece (1-5):
 !pick 2
* move simple (top/left/right/bot):
 !aa, !bb, !cc, etc
(optionally with direction):
 !aa top, !bb right, etc
* benching (target): 
 !bench A2
* selling (target): 
 !sell A2
* reroll:
 !reroll
* xp: 
 !xp 1
* grab item (target):
 !grab H8
* item to hero (1-9, target):
 !item 2 F2
* lock/unlock item (1-9):
 !itemlock 1
* show shop (on/off):
 !shop on
* show player on pos x(1-8):
 !tab 1
* moving precice (start,target): 
 !move AA A2
* write in allchat:
 !write Hello there

# Shoutout

Big thanks to TwitchPlaysPokemon developers: sunshinekitty, RDJ, MZ, AP, & Oriax

# Licence

```
# Copyright (C) 2019 : Carsten Demming

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

```