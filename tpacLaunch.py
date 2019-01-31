#!/usr/bin/env python3

# tpacLaunch.py
# Copyright (C) 2019 : Carsten Demming
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#

import configparser
import os
import subprocess
import sys
import string
import time
import socket
import re
import random
from collections import OrderedDict
from enum import Enum
from threading import Thread


class GameStates(Enum):
    searching = 0
    calibration = 1
    gaming = 2


settings = []
commands = []
delayBetweenActions = 0.3
dota2WindowID = ''
readbuffer = ""
#gameState = GameStates.searching
isCamCalibrated = False
isDebug = False

COORDMAP = {
    'a1': {'x': 633, 'y': 620},
    'a2': {'x': 651, 'y': 548},
    'a3': {'x': 669, 'y': 471},
    'a4': {'x': 683, 'y': 402},
    'a5': {'x': 695, 'y': 346},
    'a6': {'x': 708, 'y': 293},
    'a7': {'x': 715, 'y': 240},
    'a8': {'x': 727, 'y': 194},
    'b1': {'x': 734, 'y': 624},
    'b2': {'x': 744, 'y': 545},
    'b3': {'x': 750, 'y': 472},
    'b4': {'x': 761, 'y': 408},
    'b5': {'x': 769, 'y': 347},
    'b6': {'x': 778, 'y': 292},
    'b7': {'x': 783, 'y': 241},
    'b8': {'x': 793, 'y': 195},
    'c1': {'x': 824, 'y': 625},
    'c2': {'x': 831, 'y': 542},
    'c3': {'x': 835, 'y': 475},
    'c4': {'x': 842, 'y': 409},
    'c5': {'x': 846, 'y': 348},
    'c6': {'x': 853, 'y': 290},
    'c7': {'x': 856, 'y': 240},
    'c8': {'x': 862, 'y': 192},
    'd1': {'x': 913, 'y': 621},
    'd2': {'x': 917, 'y': 542},
    'd3': {'x': 919, 'y': 473},
    'd4': {'x': 920, 'y': 405},
    'd5': {'x': 923, 'y': 346},
    'd6': {'x': 926, 'y': 289},
    'd7': {'x': 928, 'y': 238},
    'd8': {'x': 927, 'y': 189},
    'e1': {'x': 1006, 'y': 621},
    'e2': {'x': 1004, 'y': 546},
    'e3': {'x': 1000, 'y': 476},
    'e4': {'x': 999, 'y': 409},
    'e5': {'x': 998, 'y': 346},
    'e6': {'x': 996, 'y': 288},
    'e7': {'x': 994, 'y': 240},
    'e8': {'x': 994, 'y': 188},
    'f1': {'x': 1098, 'y': 621},
    'f2': {'x': 1091, 'y': 541},
    'f3': {'x': 1084, 'y': 471},
    'f4': {'x': 1081, 'y': 404},
    'f5': {'x': 1072, 'y': 342},
    'f6': {'x': 1069, 'y': 288},
    'f7': {'x': 1066, 'y': 238},
    'f8': {'x': 1061, 'y': 192},
    'g1': {'x': 1193, 'y': 620},
    'g2': {'x': 1180, 'y': 543},
    'g3': {'x': 1167, 'y': 469},
    'g4': {'x': 1159, 'y': 405},
    'g5': {'x': 1149, 'y': 344},
    'g6': {'x': 1142, 'y': 293},
    'g7': {'x': 1137, 'y': 241},
    'g8': {'x': 1134, 'y': 191},
    'h1': {'x': 1278, 'y': 619},
    'h2': {'x': 1265, 'y': 539},
    'h3': {'x': 1248, 'y': 468},
    'h4': {'x': 1235, 'y': 405},
    'h5': {'x': 1227, 'y': 346},
    'h6': {'x': 1213, 'y': 290},
    'h7': {'x': 1204, 'y': 241},
    'h8': {'x': 1195, 'y': 194},

    'aa': {'x': 592, 'y': 807},
    'bb': {'x': 699, 'y': 809},
    'cc': {'x': 804, 'y': 809},
    'dd': {'x': 908, 'y': 808},
    'ee': {'x': 1014, 'y': 807},
    'ff': {'x': 1115, 'y': 809},
    'gg': {'x': 1224, 'y': 805},
    'hh': {'x': 1329, 'y': 806},

    'pick1': {'x': 464, 'y': 276},
    'pick2': {'x': 712, 'y': 257},
    'pick3': {'x': 973, 'y': 265},
    'pick4': {'x': 1220, 'y': 271},
    'pick5': {'x': 1458, 'y': 256},
    'lock': {'x': 313, 'y': 445},
    'close': {'x': 1610, 'y': 344},
    'nothing': {'x': 1547, 'y': 77},

    'chickSlot1': {'x': 1158, 'y': 964},
    'chickSlot2': {'x': 1224, 'y': 964},
    'chickSlot3': {'x': 1288, 'y': 965},
    'chickSlot4': {'x': 1158, 'y': 1012},
    'chickSlot5': {'x': 1223, 'y': 1010},
    'chickSlot6': {'x': 1286, 'y': 1010},
    'chickSlot7': {'x': 1159, 'y': 1057},
    'chickSlot8': {'x': 1223, 'y': 1057},
    'chickSlot9': {'x': 1286, 'y': 1057},

    'resetChicken': {'x': 914, 'y': 712},

    'dotaMenu': {'x': 32, 'y': 27},
    'dotaDisconnectBtn': {'x': 1627, 'y': 1035},
    'dotaLeaveBtn': {'x': 1648, 'y': 985},
    'dotaLeaveAcceptBtn': {'x': 874, 'y': 603},
    'dotaSearchBtn': {'x': 1530, 'y': 866},
    'dotaAcceptBtn': {'x': 901, 'y': 529}
}

CHICKENLOOP = OrderedDict([
    ('A1L', {'x': 565, 'y': 612}),
    ('A2L', {'x': 583, 'y': 541}),
    ('A3L', {'x': 603, 'y': 463}),
    ('A4L', {'x': 617, 'y': 404}),
    ('A5L', {'x': 633, 'y': 340}),
    ('A6L', {'x': 645, 'y': 284}),
    ('A7L', {'x': 660, 'y': 236}),
    ('A8L', {'x': 670, 'y': 192}),
    ('A8U', {'x': 735, 'y': 149}),
    ('B8U', {'x': 798, 'y': 145}),
    ('C8U', {'x': 866, 'y': 144}),
    ('D8U', {'x': 928, 'y': 141}),
    ('E8U', {'x': 994, 'y': 142}),
    ('F8U', {'x': 1059, 'y': 143}),
    ('G8U', {'x': 1131, 'y': 137}),
    ('H8U', {'x': 1190, 'y': 151}),
    ('H8R', {'x': 1255, 'y': 191}),
    ('H7R', {'x': 1269, 'y': 238}),
    ('H6R', {'x': 1283, 'y': 293}),
    ('H5R', {'x': 1293, 'y': 345}),
    ('H4R', {'x': 1310, 'y': 403}),
    ('H3R', {'x': 1320, 'y': 474}),
    ('H2R', {'x': 1338, 'y': 542}),
    ('H1R', {'x': 1355, 'y': 616}),
    ('H1D', {'x': 1287, 'y': 698}),
    ('G1D', {'x': 1194, 'y': 692}),
    ('F1D', {'x': 1093, 'y': 695}),
    ('E1D', {'x': 1001, 'y': 691}),
    ('D1D', {'x': 913, 'y': 693}),
    ('C1D', {'x': 820, 'y': 689}),
    ('B1D', {'x': 728, 'y': 689}),
    ('A1D', {'x': 630, 'y': 689})
])

itemoffsetFirstRowX = 54
itemoffsetFirstRowy = 31
itemoffsetSecondRowX = 75
itemoffsetSecondRowy = 0 #6 old

def toggleLockItem(slot):
    slotID = 'chickSlot'+slot
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[slotID]['x']),
                    str(COORDMAP[slotID]['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '3'])
    time.sleep(0.5)
    lockLabelPosX = str(COORDMAP[slotID]['x']+itemoffsetFirstRowX)
    lockLabelPosY = str(COORDMAP[slotID]['y']+itemoffsetFirstRowy)
    if(int(slot) > 3):
        lockLabelPosX = str(COORDMAP[slotID]['x']+itemoffsetSecondRowX)
        lockLabelPosY = str(COORDMAP[slotID]['y']+itemoffsetSecondRowy)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    lockLabelPosX,
                    lockLabelPosY,
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])

def grabItemChickenloop():
    # pos chicken at A1 first
    rightClickAtCoord(COORDMAP['a1'])
    time.sleep(3)
    for coord in CHICKENLOOP:
        rightClickAtCoord(CHICKENLOOP[coord])
        time.sleep(0.3)
    resetChickenPos()

def rightClickAtCoord(coord):
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(coord['x']),
                    str(coord['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '3'])
    time.sleep(delayBetweenActions)

def resetChickenPos():
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['resetChicken']['x']),
                    str(COORDMAP['resetChicken']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '3'])
    time.sleep(delayBetweenActions)


def moveItem(slot, target):
    '''
    move item from chicken slot to target hero
    '''
    print('trying to move item: %s' % slot)
    print('to %s' % target)
    slotID = 'chickSlot'+slot
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[slotID]['x']),
                    str(COORDMAP[slotID]['y'])])
    time.sleep(1)
    subprocess.run(['xdotool', 'mousedown', '--window', dota2WindowID, '1'])
    time.sleep(0.5)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[target]['x']),
                    str(COORDMAP[target]['y'])])
    time.sleep(1)
    subprocess.run(['xdotool', 'mouseup', '--window', dota2WindowID, '1'])
    # give chicken time to run to the destination
    time.sleep(5)
    resetChickenPos()


def grabItem(target):
    print('trying to grab item: %s' % target)
    rightClickAtCoord(COORDMAP[target])

def tabTour():
    print('tabtour...')
    clickNothing()
    time.sleep(delayBetweenActions)
    for i in range(8):
        subprocess.run(['xdotool', 'key', '--window', dota2WindowID, 'Tab'])
        time.sleep(0.625)


def camCalibration():
    print('calibrating cam...')
    tabTour()
    # global gameState
    # gameState = GameStates.gaming
    time.sleep(delayBetweenActions)


def searchNextGame():
    pass


def acceptGame():
    print('accepting game...')
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['dotaAcceptBtn']['x']),
                    str(COORDMAP['dotaAcceptBtn']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    #global gameState
    #gameState = GameStates.calibration


def searchGame():
    print('searching game...')
    # subprocess.run(['xdotool', 'search', "Dota 2", 'windowactivate'])
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['dotaSearchBtn']['x']),
                    str(COORDMAP['dotaSearchBtn']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(5)
    acceptGame()


def leaveGame():
    print('trying to leave game...')
    # global gameState
    if(adminMode == False):
        # gameState = GameStates.searching
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        dota2WindowID,
                        str(COORDMAP['dotaMenu']['x']),
                        str(COORDMAP['dotaMenu']['y']),
                        'click',
                        '--window',
                        dota2WindowID,
                        '1'])

        time.sleep(0.5)

        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        dota2WindowID,
                        str(COORDMAP['dotaDisconnectBtn']['x']),
                        str(COORDMAP['dotaDisconnectBtn']['y']),
                        'click',
                        '--window',
                        dota2WindowID,
                        '1'])

        time.sleep(0.5)

        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        dota2WindowID,
                        str(COORDMAP['dotaLeaveBtn']['x']),
                        str(COORDMAP['dotaLeaveBtn']['y']),
                        'click',
                        '--window',
                        dota2WindowID,
                        '1'])

        time.sleep(0.5)

        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        dota2WindowID,
                        str(COORDMAP['dotaLeaveAcceptBtn']['x']),
                        str(COORDMAP['dotaLeaveAcceptBtn']['y']),
                        'click',
                        '--window',
                        dota2WindowID,
                        '1'])

    else:
        pass
        # continueGame = input('reconnect? y/n')
        # if(continueGame.lower() == 'n'):
        #     gameState = GameStates.searching


def randomAction():
    randomNumber = random.randint(0, 4)
    if(randomNumber == 0):
        # pick random piece
        pickPiece(random.randint(1, 5))
    elif(randomNumber == 1):
        # sell random unit on bench
        charNr = random.randint(0, 7)
        sellChar = chr(charNr+ord('a'))
        sellChar += sellChar
        sellPiece(sellChar)
    elif(randomNumber == 2):
        # move random unit to random pos
        rand1X = random.randint(0, 7)  # A-H
        rand1Y = random.randint(1, 8)  # 1-8
        rand2X = random.randint(0, 7)
        rand2Y = random.randint(1, 8)
        source = chr(rand1X + ord('a')) + rand1Y
        target = chr(rand2X + ord('a')) + rand2Y
        movePiece(source, target)
        # bench reroll
    elif(randomNumber == 3):
        # bench random unit
        rand1X = random.randint(0, 7)  # A-H
        rand1Y = random.randint(1, 8)  # 1-8
        target = chr(rand1X + ord('a')) + rand1Y
        benchPiece(target)

    elif(randomNumber == 4):
        # reroll
        rerollPieces()


def pickPiece(target):
    print('trying to pick: %s' % target)
    pickString = 'pick'+str(target)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[pickString]['x']),
                    str(COORDMAP[pickString]['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)
    clickNothing()


def clickNothing():
    '''
    can be used to click empty space as well for resetting commandchain (autochess bug)
    '''
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['nothing']['x']),
                    str(COORDMAP['nothing']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)


# !shophowSelection

def closeSelection():
    '''
    closes Selection via X button
    '''
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['close']['x']),
                    str(COORDMAP['close']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)


def showSelection(isOn):
    print('trying to show selection: %s' % isOn)
    closeSelection()
    if(isOn == 'on'):
        subprocess.run(['xdotool', 'key', '--window', dota2WindowID, 'space'])

# !l


def lockSelection():
    print('trying to lock')
    # first open selection
    showSelection('on')
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP['lock']['x']),
                    str(COORDMAP['lock']['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    # optionally close selection afterwards
    # xdotool key space

# !m AA F4


def movePiece(source, target):
    print('trying to move: %s' % source)
    print('to %s' % target)
    # make sure selection is closed
    showSelection('off')
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[source]['x']),
                    str(COORDMAP[source]['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool', 'key', '--window', dota2WindowID, 'm'])
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[target]['x']),
                    str(COORDMAP[target]['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)
    clickNothing()
# !b F5


def benchPiece(target):
    print('trying to bench: %s' % target)
    subprocess.run(['xdotool',
                    'mousemove',
                    '--window',
                    dota2WindowID,
                    str(COORDMAP[target]['x']),
                    str(COORDMAP[target]['y']),
                    'click',
                    '--window',
                    dota2WindowID,
                    '1'])
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool', 'key', '--window', dota2WindowID, 'b'])
    time.sleep(delayBetweenActions)
    clickNothing()
# !s F6


def sellPiece(target):
    print('trying to sell piece: %s' % target)
    subprocess.run(['xdotool',
                    'mousemove',
                    str(COORDMAP[target]['x']),
                    str(COORDMAP[target]['y']),
                    'click', '1'])
    time.sleep(delayBetweenActions)
    subprocess.run(['xdotool', 'key', 's'])
    time.sleep(delayBetweenActions)
    clickNothing()

# !r null


def rerollPieces():
    print('trying to reroll')
    subprocess.run(['xdotool', 'key', 'r'])
    time.sleep(delayBetweenActions)
    clickNothing()
# !x null


def buyXP(amount):
    print('trying to buy xp: %s' % amount)
    for i in range(int(amount)):
        subprocess.run(['xdotool', 'key', 'x'])
        time.sleep(0.8)
    clickNothing()


def findAndExecute(splitted):
    # if(gameState == GameStates.gaming):
    if splitted[0] == '!m':
        time.sleep(.02)
        # execute command
        movePiece(splitted[1], splitted[2])
    if splitted[0] == '!b':
        time.sleep(.02)
        # execute command
        benchPiece(splitted[1])
    if splitted[0] == '!s':
        time.sleep(.02)
        # execute command
        sellPiece(splitted[1])
    if splitted[0] == '!r':
        time.sleep(.02)
        # execute command
        rerollPieces()
    if splitted[0] == '!x':
        time.sleep(.02)
        # execute command
        buyXP(splitted[1])
    if splitted[0] == '!shop':
        time.sleep(.02)
        # execute command
        showSelection(splitted[1])
    if splitted[0] == '!p':
        time.sleep(.02)
        # execute command
        pickPiece(splitted[1])
    if splitted[0] == '!l':
        time.sleep(.02)
        # execute command
        lockSelection()
    if splitted[0] == '!g':
        time.sleep(.02)
        # execute command
        grabItem(splitted[1])
    if splitted[0] == '!i':
        time.sleep(.02)
        # execute command
        moveItem(splitted[1], splitted[2])
    if splitted[0] == '!tab':
        time.sleep(.02)
        # execute command
        tabTour()
    if splitted[0] == '!random':
        time.sleep(.02)
        # execute command
        randomAction()
    if splitted[0] == '!rq':
        time.sleep(.02)
        leaveGame()
    # elif(gameState == GameStates.searching):
    if(splitted[0] == '!search'):
        time.sleep(.02)
        searchGame()
    if(splitted[0] == '!accept'):
        print('about to enter acceptGame()')
        time.sleep(.02)
        acceptGame()
    # elif(gameState == GameStates.calibration):
    if(splitted[0] == '!calib'):
        time.sleep(.02)
        camCalibration()


def addtofile():
    if len(commands) >= command_length:
        del commands[0]
        commands.extend([user[1:] + out.lower()])
        if mode.lower() == "democracy":
            list_commands.extend([out.lower()])
    else:
        commands.extend([user[1:] + out.lower()])
        if mode.lower() == "democracy":
            list_commands.extend([out.lower()])


def most_common(lst):
    # Write to file for stream view
    tempList = lst
    maxList = []
    if(len(lst) > 5):
        for i in range(5):
            if(len(tempList) > 0):
                tempMax = max(tempList, key=tempList.count)
                maxList.append(tempMax)
                tempList = list(filter(lambda a: a != tempMax, tempList))
            else:
                break

    else:
        for i in range(len(lst)):
            if(len(tempList) > 0):
                tempMax = max(tempList, key=tempList.count)
                maxList.append(tempMax)
                tempList = list(filter(lambda a: a != tempMax, tempList))
            else:
                break

    with open("most_common_commands.txt", "w") as f:
        f.write('Top commands:\n')
        for item in maxList:
            f.write(item + '\n')
    return maxList[0]

# TODO: sort/reorder same solution for move (!m A3 F2 == !m F2 A3)


def commandValidator(incomingString):
    '''
    Validate incoming commands
    '''
    # not a command
    if(incomingString[:1] != '!'):
        return None

    # starts with keywords?
    if(incomingString.startswith('!m ')):
        print('!m command to check: %s' % incomingString)
        # check for valid move; ref example !m AA F4
        movePattern = r'^!m ([a-hA-H][a-hA-H1-4]{1}) (?!\1)([a-hA-H][a-hA-H1-4]{1})$'
        if(re.match(movePattern, incomingString)):
            return True
        else:
            return None

    elif(incomingString.startswith('!g ')):
        print('!g command to check: %s' % incomingString)
        # check for valid grab; ref example !g AA
        grabPattern = r'^!g ([a-hA-H][a-hA-H1-8])$'
        if(re.match(grabPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!b '):
        print('!b command to check: %s' % incomingString)
        # check for valid bench; ref example !b A3
        benchPattern = r'^!b ([a-hA-H][1-4])$'
        if(re.match(benchPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!s '):
        print('!s command to check: %s' % incomingString)
        # check for valid delete; ref example !s A3
        benchPattern = r'^!s ([a-hA-H][a-hA-H1-4])$'
        if(re.match(benchPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!rq'):
        print('!rq command to check: %s' % incomingString)
        # check for valid rq; ref example !rq
        pattern = r'^!rq$'
        if(re.match(pattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!r'):
        print('!r command to check: %s' % incomingString)
        # check for valid reroll; ref example !r
        rerollPattern = r'^!r$'
        if(re.match(rerollPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!x '):
        print('!x command to check: %s' % incomingString)
        # check for valid xp; ref example !x
        buyXPPattern = r'^!x [1-4]$'
        if(re.match(buyXPPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!shop '):
        print('!shop command to check: %s' % incomingString)
        # check for valid space; ref example !shop
        showSelectionPattern = r'^!shop (on|off)$'
        if(re.match(showSelectionPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!l'):
        print('!l command to check: %s' % incomingString)
        # check for valid lock; ref example !l
        lockPattern = r'^!l$'
        if(re.match(lockPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!p '):
        print('!p command to check: %s' % incomingString)
        # check for valid pick; ref example !p 1
        pickPattern = r'^!p [1-5]$'
        if(re.match(pickPattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!i'):
        print('!i command to check: %s' % incomingString)
        # check for valid item to hero command; ref example !i 2 A5
        pattern = r'^!i ([1-9]) ([a-hA-H][a-hA-H1-8]{1})$'
        if(re.match(pattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!tab'):
        print('!tab command to check: %s' % incomingString)
        # check for valid tab; ref example !tab
        pattern = r'^!tab$'
        if(re.match(pattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!random'):
        print('!random command to check: %s' % incomingString)
        # check for valid random; ref example !random
        pattern = r'^!random$'
        if(re.match(pattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!search'):
        print('!search command to check: %s' % incomingString)
        # check for valid search; ref example !search
        pattern = r'^!search$'
        if(re.match(pattern, incomingString)):
            print('!search accepted')
            return True
        else:
            return None

    elif incomingString.startswith('!calib'):
        print('!calib command to check: %s' % incomingString)
        # check for valid calib; ref example !calib
        pattern = r'^!calib$'
        if(re.match(pattern, incomingString)):
            return True
        else:
            return None

    elif incomingString.startswith('!accept'):
        print('!accept command to check: %s' % incomingString)
        # check for valid accept; ref example !accept
        pattern = r'^!accept$'
        if(re.match(pattern, incomingString)):
            print('accept is valid!')
            return True
        else:
            return None

    else:
        return None


def democracy():
    global list_commands
    list_commands = []
    last_command = time.time()
    selected_c = "None"

    while True:
        if time.time() > last_command + democracy_time:
            last_command = time.time()
            if(len(list_commands) > 0):
                selected_c = most_common(list_commands)
                print('selected_c: %s' % selected_c)
            else:
                selected_c = 'None'
            with open("lastsaid.txt", "w") as f:
                f.write("Selected %s\n" % selected_c)
                f.write("Time left: %s" % str(democracy_time)[0:1])
            list_commands = []
            if(selected_c != 'None'):
                splitted = selected_c.lower().split(' ')
                findAndExecute(splitted)
        else:
            with open("lastsaid.txt", "w") as f:
                f.write("Selected %s\n" % selected_c)
                f.write("Time left: %s" % str(
                    1.0 + last_command + democracy_time - time.time())[0:1])
        time.sleep(1)


# Generate a config file if one doesn't exist
while True:
    if os.path.isfile("settings.txt"):
        config = configparser.ConfigParser()
        config.read("settings.txt")
        HOST = config.get('Settings', 'HOST')
        PORT = config.getint('Settings', 'PORT')
        AUTH = config.get('Settings', 'AUTH')
        NICK = config.get('Settings', 'USERNAME').lower()
        APP = config.get('Settings', 'APP')
        CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()
        command_length = config.getint('Settings', 'LENGTH')
        break
    else:
        print("Let's make you a config file")
        settings.append("; Settings for Twitch Plays AutoChess bot")
        settings.append("; Thanks to sunshinekitty, RDJ, MZ, AP, & Oriax\n")

        settings.append("[Settings]\n")

        settings.append(
            "; Where you're connecting to, if it's Twitch leave it as is")
        print("Where you're connecting to, if it's Twitch use irc.twitch.tv")
        settings_host = input("Hostname: ")
        settings.append("HOST = " + settings_host + "\n")

        settings.append("; Port number, probably should use 6667")
        print("Port number, probably should use 6667")
        settings_port = input("Port: ")
        settings.append("PORT = " + settings_port + "\n")

        settings.append(
            "; Auth token, grab this from http://www.twitchapps.com/tmi")
        print("Auth token, grab this from http://www.twitchapps.com/tmi")
        settings_auth = input("Auth Token: ")
        settings.append("AUTH = " + settings_auth + "\n")

        settings.append("; Your Twitch Bot's Username")
        print("Your Twitch Bot's Username")
        settings_bot = input("Bot's Username: ")
        settings.append("USERNAME = " + settings_bot + "\n")

        settings.append(
            "; Name of the application")
        print("Name of the application")
        settings_app = input("Application name: ")
        settings.append("APP = " + settings_app + "\n")

        settings.append("; Username of who's channel you're connecting to")
        print("Username of who's channel you're connecting to")
        settings_chat = input("Username: ")
        settings.append("CHAT_CHANNEL = " + settings_chat + "\n")

        settings.append(
            "; The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        print("The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        settings_length = input("Length: ")
        settings.append("LENGTH = " + settings_length + "\n")

        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')

# Select game type
while True:
    while dota2WindowID == '':
        waitForDota = input("Dota already running? Then press enter")
        completedProcess = subprocess.run(['xdotool', 'search', '--name',
                                           'Dota 2'], capture_output=True)
        dota2WindowID = completedProcess.stdout.decode('UTF-8')
    aMode = input('Adminmode? y/n: ')
    if(aMode.lower() == 'y'):
        adminMode = True
    else:
        adminMode = False
    print("Currently available: Democracy, Anarchy")
    mode = input("Game type: ")
    #mode = 'anarchy'
    if mode.lower() == "anarchy":
        break
    if mode.lower() == "democracy":
        print("Takes most said command every X second(s): ")
        democracy_time = float(input("(must be integer) X="))
        break

# Democracy Game Mode
if mode.lower() == "democracy":
    with open("lastsaid.txt", "w") as f:
        f.write("")
    with open("most_common_commands.txt", "w") as f:
        f.write("")
    count_job = Thread(target=democracy, args=())
    count_job.start()
    # count_job.join()

    time.sleep(1)

    # TODO: start dota game here

    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"))
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1

            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)

            # Take in output
            # sanitize output
            if(commandValidator(out.lower())):
                addtofile()

            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')

# Anarchy Game Mode
if mode.lower() == "anarchy":
    with open("lastsaid.txt", "w") as f:
        f.write("")
    with open("most_common_commands.txt", "w") as f:
        f.write("")
    time.sleep(1)

    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"))
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1

            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)

            # Take in output
            # sanitize output
            if(commandValidator(out.lower())):
                addtofile()
                splitted = out.lower().split(' ')
                findAndExecute(splitted)

            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')
