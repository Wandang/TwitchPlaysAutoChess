#!/usr/bin/env python3

# tpacLaunchv2.py
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


class GameController:
    def __init__(self):
        self.validator = Validator()
        self.commandStack = []
        self.delayBetweenActions = 0.3
        self.dota2WindowID = ''
        self.allowRagequit = False

        self.TWITCHEMOTES = ['monkaS', '4Head', 'FailFish', 'DansGame', 'LUL', 'Kappa', 'NotLikeThis',
                        'OSFrog', 'PJSalt', 'WutFace', 'cmonBruh', 'TriHard', 'PogChamp', 'ResidentSleeper']

        self.COORDMAP = {
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

            'dotaArrowBtn': {'x': 32, 'y': 27},
            'dotaDisconnectBtn': {'x': 1627, 'y': 1035},
            'dotaLeaveBtn': {'x': 1648, 'y': 985},
            'dotaLeaveAcceptBtn': {'x': 874, 'y': 603},
            'dotaPlayAutoChessBtn': {'x': 1530, 'y': 866},
            'dotaAcceptBtn': {'x': 901, 'y': 529},
            'dotaMainMenuBtn': {'x': 286, 'y': 32},
            'dotaAutoChessBtn': {'x': 780, 'y': 478},

            'playerPos1': {'x': 1737, 'y': 155},
            'playerPos2': {'x': 1737, 'y': 255},
            'playerPos3': {'x': 1737, 'y': 355},
            'playerPos4': {'x': 1737, 'y': 455},
            'playerPos5': {'x': 1737, 'y': 555},
            'playerPos6': {'x': 1737, 'y': 655},
            'playerPos7': {'x': 1737, 'y': 755},
            'playerPos8': {'x': 1737, 'y': 855}
        }
        self.CHICKENLEFT = OrderedDict([
            ('A1L', {'x': 565, 'y': 612}),
            ('A2L', {'x': 583, 'y': 541}),
            ('A3L', {'x': 603, 'y': 463}),
            ('A4L', {'x': 617, 'y': 404}),
            ('A5L', {'x': 633, 'y': 340}),
            ('A6L', {'x': 645, 'y': 284}),
            ('A7L', {'x': 660, 'y': 236}),
            ('A8L', {'x': 670, 'y': 192})
        ])

        self.CHICKENTOP = OrderedDict([
            ('A8T', {'x': 735, 'y': 149}),
            ('B8T', {'x': 798, 'y': 145}),
            ('C8T', {'x': 866, 'y': 144}),
            ('D8T', {'x': 928, 'y': 141}),
            ('E8T', {'x': 994, 'y': 142}),
            ('F8T', {'x': 1059, 'y': 143}),
            ('G8T', {'x': 1131, 'y': 137}),
            ('H8T', {'x': 1190, 'y': 151})])

        self.CHICKENRIGHT = OrderedDict([
            ('H8R', {'x': 1255, 'y': 191}),
            ('H7R', {'x': 1269, 'y': 238}),
            ('H6R', {'x': 1283, 'y': 293}),
            ('H5R', {'x': 1293, 'y': 345}),
            ('H4R', {'x': 1310, 'y': 403}),
            ('H3R', {'x': 1320, 'y': 474}),
            ('H2R', {'x': 1338, 'y': 542}),
            ('H1R', {'x': 1355, 'y': 616})])

        self.CHICKENBOT = OrderedDict([
            ('H1B', {'x': 1287, 'y': 698}),
            ('G1B', {'x': 1194, 'y': 692}),
            ('F1B', {'x': 1093, 'y': 695}),
            ('E1B', {'x': 1001, 'y': 691}),
            ('D1B', {'x': 913, 'y': 693}),
            ('C1B', {'x': 820, 'y': 689}),
            ('B1B', {'x': 728, 'y': 689}),
            ('A1B', {'x': 630, 'y': 689})])

        self.itemoffsetFirstRowX = 54
        self.itemoffsetFirstRowy = 31
        self.itemoffsetSecondRowX = 75
        self.itemoffsetSecondRowy = 0  # 6 old


    def toggleLockItem(self, slot):
        slotID = 'chickSlot'+slot
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[slotID]['x']),
                        str(self.COORDMAP[slotID]['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '3'])
        time.sleep(0.5)
        lockLabelPosX = str(self.COORDMAP[slotID]['x']+self.itemoffsetFirstRowX)
        lockLabelPosY = str(self.COORDMAP[slotID]['y']+self.itemoffsetFirstRowy)
        if(int(slot) > 3):
            lockLabelPosX = str(self.COORDMAP[slotID]['x']+self.itemoffsetSecondRowX)
            lockLabelPosY = str(self.COORDMAP[slotID]['y']+self.itemoffsetSecondRowy)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        lockLabelPosX,
                        lockLabelPosY,
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])


    def grabItemChickenloop(self, side):
        self.showSelection('off')
        if(side == 'left'):
            # pos chicken at A1 first
            self.rightClickAtCoord(self.COORDMAP['a1'])
            time.sleep(3)
            for coord in self.CHICKENLEFT:
                self.rightClickAtCoord(self.CHICKENLEFT[coord])
                time.sleep(0.3)
            self.resetChickenPos()
        elif(side == 'top'):
            # pos chicken at A1 first
            self.rightClickAtCoord(self.COORDMAP['a8'])
            time.sleep(3)
            for coord in self.CHICKENTOP:
                self.rightClickAtCoord(self.CHICKENTOP[coord])
                time.sleep(0.3)
            self.resetChickenPos()
        elif(side == 'right'):
            # pos chicken at A1 first
            self.rightClickAtCoord(self.COORDMAP['h8'])
            time.sleep(3)
            for coord in self.CHICKENRIGHT:
                self.rightClickAtCoord(self.CHICKENRIGHT[coord])
                time.sleep(0.3)
            self.resetChickenPos()
        elif(side == 'bot'):
            # pos chicken at A1 first
            self.rightClickAtCoord(self.COORDMAP['h1'])
            time.sleep(3)
            for coord in self.CHICKENBOT:
                self.rightClickAtCoord(self.CHICKENBOT[coord])
                time.sleep(0.3)
            self.resetChickenPos()


    def rightClickAtCoord(self, coord):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(coord['x']),
                        str(coord['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '3'])
        time.sleep(self.delayBetweenActions)


    def resetChickenPos(self):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['resetChicken']['x']),
                        str(self.COORDMAP['resetChicken']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '3'])
        time.sleep(self.delayBetweenActions)


    def moveItem(self, slot, target):
        '''
        move item from chicken slot to target hero
        '''
        print('trying to move item: %s' % slot)
        print('to %s' % target)
        # close shop b4
        self.showSelection('off')
        slotID = 'chickSlot'+slot
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[slotID]['x']),
                        str(self.COORDMAP[slotID]['y'])])
        time.sleep(1)
        subprocess.run(['xdotool', 'mousedown', '--window', self.dota2WindowID, '1'])
        time.sleep(0.5)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[target]['x']),
                        str(self.COORDMAP[target]['y'])])
        time.sleep(1)
        subprocess.run(['xdotool', 'mouseup', '--window', self.dota2WindowID, '1'])
        # give chicken time to run to the destination
        # TODO: dynamic time depending on target location
        time.sleep(5)
        self.resetChickenPos()


    def grabItem(self, target):
        # close shop first
        self.showSelection('off')
        print('trying to grab item: %s' % target)
        self.rightClickAtCoord(self.COORDMAP[target])
        # TODO: dynamic time depending on target location
        time.sleep(5)
        self.resetChickenPos()


    def tabTour(self, playerPlacementID=-1):
        '''
        Show chessboard of player x or if no player is given show every chessboard in 5s
        '''
        if(playerPlacementID != -1):
            timeToStayOnPlayer = 3
            placementKey = 'playerPos'+playerPlacementID
            allChatMessage = 'Chat wants to inspect the current position: '+playerPlacementID
            self.writeAllChat(allChatMessage)
            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            str(self.COORDMAP[placementKey]['x']),
                            str(self.COORDMAP[placementKey]['y']),
                            'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])
            time.sleep(self.delayBetweenActions)
            # move mouse away from avatars so the popovertext is not blocking the view
            self.clickNothing()
            time.sleep(timeToStayOnPlayer)
            allChatMessage2 = 'Chat judgement: ' + \
                self.TWITCHEMOTES[random.randint(0, len(self.TWITCHEMOTES))]
            self.writeAllChat(allChatMessage2)
            self.camCalibration()
        else:
            print('tabtour...')
            self.clickNothing()
            time.sleep(self.delayBetweenActions)
            for dummy in range(8):
                subprocess.run(
                    ['xdotool', 'key', '--window', self.dota2WindowID, 'Tab'])
                time.sleep(0.625)


    def writeAllChat(self, message):
        subprocess.run(['xdotool', 'key', '--window',
                        self.dota2WindowID, 'shift+Return'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'type', '--window', self.dota2WindowID, message])
        time.sleep(0.5)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'Return'])
        time.sleep(self.delayBetweenActions)


    def camCalibration(self, promote=False):
        print('calibrating cam...')
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, '1'])
        # shoutout in allchat to promote the bot
        if(promote):
            self.writeAllChat(
                'Chat is playing right now on https://www.twitch.tv/twitchplaysautochess')
        # gameState = GameStates.gaming
        time.sleep(self.delayBetweenActions)


    def acceptGame(self):
        print('accepting game...')
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['dotaAcceptBtn']['x']),
                        str(self.COORDMAP['dotaAcceptBtn']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        #gameState = GameStates.calibration


    def searchGame(self):
        print('searching game...')
        # subprocess.run(['xdotool', 'search', "Dota 2", 'windowactivate'])
        # press esc to close any info windows (for example due to not accepting b4)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'Escape'])
        # go to main menu first
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['dotaMainMenuBtn']['x']),
                        str(self.COORDMAP['dotaMainMenuBtn']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)

        # navigate to autochess
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['dotaAutoChessBtn']['x']),
                        str(self.COORDMAP['dotaAutoChessBtn']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)

        # start autochess search
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['dotaPlayAutoChessBtn']['x']),
                        str(self.COORDMAP['dotaPlayAutoChessBtn']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(5)
        self.acceptGame()


    def abortRagequit(self):
        # print('aborting ragequit by setting flag to false')
        # 
        self.allowRagequit = False
        # print('writing empty file')
        with open("ragequit.txt", "w") as f:
            f.write("")


    def rageQuitProcess(self):
        # print('in rq process')
        targetTime = 20
        # 
        starttime = time.time()
        # do nothing till 20s passed
        # time.sleep(20)
        while True:
            if(time.time() - starttime < targetTime):
                if(self.allowRagequit):
                    # print('self.allowRagequit: %s ' % self.allowRagequit)
                    # write for chat
                    with open("ragequit.txt", "w") as f:
                        f.write("Time left till ragequit!: %s \n" % str(
                                1.0 + targetTime - (time.time() - starttime)).split('.')[0])
                        f.write("To abort write !stay")
                    time.sleep(1)
                else:
                    # print('in rq process: self.allowRagequit = False, therefore aborting rq, cleaning file')
                    with open("ragequit.txt", "w") as f:
                        f.write('')
                    break
            else:
                # times up
                break

        if(self.allowRagequit):
            # print('trying to leave game...')
            # gameState = GameStates.searching
            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            str(self.COORDMAP['dotaArrowBtn']['x']),
                            str(self.COORDMAP['dotaArrowBtn']['y']),
                            'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])

            time.sleep(0.5)

            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            str(self.COORDMAP['dotaDisconnectBtn']['x']),
                            str(self.COORDMAP['dotaDisconnectBtn']['y']),
                            'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])

            time.sleep(1)
            self.clickNothing()

            time.sleep(1)

            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            str(self.COORDMAP['dotaLeaveBtn']['x']),
                            str(self.COORDMAP['dotaLeaveBtn']['y'])])
            time.sleep(2)
            subprocess.run(['xdotool', 'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])

            time.sleep(1)
            subprocess.run(['xdotool', 'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])

            time.sleep(1)

            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            str(self.COORDMAP['dotaLeaveAcceptBtn']['x']),
                            str(self.COORDMAP['dotaLeaveAcceptBtn']['y'])])
            time.sleep(1)

            subprocess.run(['xdotool', 'click',
                            '--window',
                            self.dota2WindowID,
                            '1'])

            with open("ragequit.txt", "w") as f:
                f.write("")

        self.allowRagequit = False


    def leaveGame(self):
        # 
        if(self.allowRagequit):
            print('ragequit already in process, aborting another thread')
            return
        self.allowRagequit = True
        # start counter in seperate thread
        print('starting rq thread')
        rageQuitJob = Thread(target=self.rageQuitProcess, args=())
        rageQuitJob.start()


    def randomAction(self):
        randomNumber = random.randint(0, 4)
        if(randomNumber == 0):
            # pick random piece
            self.pickPiece(random.randint(1, 5))
        elif(randomNumber == 1):
            # sell random unit on bench
            charNr = random.randint(0, 7)
            sellChar = chr(charNr+ord('a'))
            sellChar += sellChar
            self.sellPiece(sellChar)
        elif(randomNumber == 2):
            # move random unit to random pos
            rand1X = random.randint(0, 7)  # A-H
            rand1Y = random.randint(1, 8)  # 1-8
            rand2X = random.randint(0, 7)
            rand2Y = random.randint(1, 8)
            source = chr(rand1X + ord('a')) + rand1Y
            target = chr(rand2X + ord('a')) + rand2Y
            self.movePiece(source, target)
            # bench reroll
        elif(randomNumber == 3):
            # bench random unit
            rand1X = random.randint(0, 7)  # A-H
            rand1Y = random.randint(1, 8)  # 1-8
            target = chr(rand1X + ord('a')) + rand1Y
            self.benchPiece(target)

        elif(randomNumber == 4):
            # reroll
            self.rerollPieces()


    def pickPiece(self, target):
        self.showSelection('on')
        print('trying to pick: %s' % target)
        pickString = 'pick'+str(target)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[pickString]['x']),
                        str(self.COORDMAP[pickString]['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()


    def clickNothing(self):
        '''
        can be used to click empty space as well for resetting commandchain (autochess bug)
        '''
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['nothing']['x']),
                        str(self.COORDMAP['nothing']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)


    # !shophowSelection

    def closeSelection(self):
        '''
        closes Selection via X button
        '''
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['close']['x']),
                        str(self.COORDMAP['close']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)


    def showSelection(self, isOn):
        print('trying to show selection: %s' % isOn)
        self.closeSelection()
        if(isOn == 'on'):
            subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'space'])
        time.sleep(self.delayBetweenActions)
    # !l


    def lockSelection(self):
        print('trying to lock')
        # first open selection
        self.showSelection('on')
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['lock']['x']),
                        str(self.COORDMAP['lock']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        # optionally close selection afterwards
        # xdotool key space


    def moveBot(self):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['aa']['x']),
                        str(self.COORDMAP['aa']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'm'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['e1']['x']),
                        str(self.COORDMAP['e1']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveTop(self):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['aa']['x']),
                        str(self.COORDMAP['aa']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'm'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['d4']['x']),
                        str(self.COORDMAP['d4']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveRight(self):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['aa']['x']),
                        str(self.COORDMAP['aa']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'm'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['g3']['x']),
                        str(self.COORDMAP['g3']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveLeft(self):
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['aa']['x']),
                        str(self.COORDMAP['aa']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'm'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP['b3']['x']),
                        str(self.COORDMAP['b3']['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def movePieceFromSlot(self, slot, direction=''):
        if direction == 'left':
            self.movePiece(slot, 'b3')
        elif direction == 'right':
            self.movePiece(slot, 'g3')
        elif direction == 'top':
            self.movePiece(slot, 'd4')
        elif direction == 'bot':
            self.movePiece(slot, 'e1')
        else:
            self.movePiece(slot, 'd3')


    # probably obsolete
    def movePieceDirection(self, direction):
        if direction == 'left':
            self.moveLeft()
        elif direction == 'right':
            self.moveRight()
        elif direction == 'top':
            self.moveTop()
        elif direction == 'bot':
            self.moveBot()


    def movePiece(self, source, target):
        print('trying to move: %s' % source)
        print('to %s' % target)
        # make sure selection is closed
        self.showSelection('off')
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[source]['x']),
                        str(self.COORDMAP[source]['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'm'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[target]['x']),
                        str(self.COORDMAP[target]['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')
    # !b F5


    def benchPiece(self, target):
        self.showSelection('off')
        print('trying to bench: %s' % target)
        subprocess.run(['xdotool',
                        'mousemove',
                        '--window',
                        self.dota2WindowID,
                        str(self.COORDMAP[target]['x']),
                        str(self.COORDMAP[target]['y']),
                        'click',
                        '--window',
                        self.dota2WindowID,
                        '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, 'b'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')
    # !s F6


    def sellPiece(self, target):
        self.showSelection('off')
        print('trying to sell piece: %s' % target)
        subprocess.run(['xdotool',
                        'mousemove',
                        str(self.COORDMAP[target]['x']),
                        str(self.COORDMAP[target]['y']),
                        'click', '1'])
        time.sleep(self.delayBetweenActions)
        subprocess.run(['xdotool', 'key', 's'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')
    # !r null


    def rerollPieces(self):
        self.showSelection('off')
        print('trying to reroll')
        subprocess.run(['xdotool', 'key', 'r'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')
    # !x null


    def buyXP(self, amount):
        print('trying to buy xp: %s' % amount)
        for dummy in range(int(amount)):
            subprocess.run(['xdotool', 'key', 'x'])
            time.sleep(0.8)
        self.clickNothing()
    
    def executeStack(self):
        for command in self.commandStack:
            self.findAndExecute(command.split(' '))
        self.commandStack = []


    def addToStack(self, commandForStack):
        # TODO: set a limit on stack
        self.commandStack.append(commandForStack)


    def stackCommand(self, commandArray):
        patchedCommand = ''
        for i in range(1, len(commandArray)):
            patchedCommand += commandArray[i] + ' '
        patchedCommand = patchedCommand[:-1]
        if self.validator.validateCommand(patchedCommand):
            # valid, add to stack
            self.addToStack(patchedCommand)

    
    def findAndExecute(self, splitted):
        # todo reuse patterns on unsplitted string to reduce redundance
        # if(gameState == GameStates.gaming):
        if splitted[0] == '!m' or splitted[0] == '!move':
            time.sleep(.02)
            # execute command
            print(splitted)
            if(len(splitted) > 2):
                self.movePiece(splitted[1], splitted[2])
            else:
                self.movePieceDirection(splitted[1])
        if splitted[0] == '!b' or splitted[0] == '!bench':
            time.sleep(.02)
            # execute command
            self.benchPiece(splitted[1])
        if splitted[0] == '!s' or splitted[0] == '!sell':
            time.sleep(.02)
            # execute command
            self.sellPiece(splitted[1])
        if splitted[0] == '!r' or splitted[0] == '!reroll':
            time.sleep(.02)
            # execute command
            self.rerollPieces()
        if splitted[0] == '!x' or splitted[0] == '!xp':
            time.sleep(.02)
            # execute command
            self.buyXP(splitted[1])
        if splitted[0] == '!shop':
            time.sleep(.02)
            # execute command
            self.showSelection(splitted[1])
        if splitted[0] == '!p' or splitted[0] == '!pick':
            time.sleep(.02)
            # execute command
            self.pickPiece(splitted[1])
        if splitted[0] == '!l' or splitted[0] == '!lock':
            time.sleep(.02)
            # execute command
            self.lockSelection()
        if splitted[0] == '!g' or splitted[0] == '!grab':
            time.sleep(.02)
            # execute command
            self.grabItem(splitted[1])
        if splitted[0] == '!i' or splitted[0] == '!item':
            time.sleep(.02)
            # execute command
            self.moveItem(splitted[1], splitted[2])
        if splitted[0] == '!tab':
            time.sleep(.02)
            # execute command
            if(len(splitted) > 1):
                self.tabTour(splitted[1])
            else:
                self.tabTour()
        if splitted[0] == '!random':
            time.sleep(.02)
            # execute command
            self.randomAction()
        if splitted[0] == '!rq':
            time.sleep(.02)
            self.leaveGame()
        if splitted[0] == '!li' or splitted[0] == '!uli' or splitted[0] == '!itemlock':
            time.sleep(.02)
            self.toggleLockItem(splitted[1])
        if splitted[0] == '!run':
            time.sleep(.02)
            self.grabItemChickenloop(splitted[1])
        if splitted[0] == '!stay':
            time.sleep(.02)
            self.abortRagequit()
        if splitted[0] == '!write':
            time.sleep(.02)
            tempword = ''
            for i in range(1, len(splitted)):
                tempword += splitted[i] + ' '
            self.writeAllChat(tempword)
        if splitted[0] == '!stack':
            time.sleep(.02)
            self.stackCommand(splitted)
        if splitted[0] == '!exec':
            time.sleep(.02)
            self.executeStack()
        if (splitted[0] == '!aa'
            or splitted[0] == '!bb'
            or splitted[0] == '!cc'
            or splitted[0] == '!dd'
            or splitted[0] == '!ee'
            or splitted[0] == '!ff'
            or splitted[0] == '!gg'
                or splitted[0] == '!hh'):
            time.sleep(.02)
            if len(splitted) > 1:
                self.movePieceFromSlot(splitted[0][1:], splitted[1])
            else:
                self.movePieceFromSlot(splitted[0][1:], 'd3')
        # elif(gameState == GameStates.searching):
        if(splitted[0] == '!search'):
            time.sleep(.02)
            self.searchGame()
        if(splitted[0] == '!accept'):
            print('about to enter acceptGame()')
            time.sleep(.02)
            self.acceptGame()
        # elif(gameState == GameStates.calibration):
        if(splitted[0] == '!calib'):
            time.sleep(.02)
            self.camCalibration(True)

class IO:
    def __init__(self):
        pass
    def writeFile(self, ):
        pass

    def readFile(self):
        pass

# class Controller

class Setup:
    def __init__(self):
        self.commands = []
        self.list_commands = []
        self.gc = GameController()
        # TODO: 2 instanzen von validator -> singleton
        self.validator = Validator()
        # self.dota2WindowID = ''
        self.config()
        
    def config(self):
        # Generate a config file if one doesn't exist
        # TODO: exclude settings and configs outside of controlling programflow -> move programflow to controller class
        while True:
            if os.path.isfile("settings.txt"):
                config = configparser.ConfigParser()
                config.read("settings.txt")
                self.HOST = config.get('Settings', 'HOST')
                self.PORT = config.getint('Settings', 'PORT')
                self.AUTH = config.get('Settings', 'AUTH')
                self.NICK = config.get('Settings', 'USERNAME').lower()
                self.APP = config.get('Settings', 'APP')
                self.CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()
                self.command_length = config.getint('Settings', 'LENGTH')
                break
            else:
                print("Let's make you a config file")
                settings = []
                settings.append("; Settings for Twitch Plays AutoChess bot")
                settings.append("; Thanks to TwitchPlaysPokemon developers: sunshinekitty, RDJ, MZ, AP, & Oriax\n")

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

    def start(self):
        # Select game type
        while True:
            while self.gc.dota2WindowID == '':
                input("Dota already running? Then press enter")
                completedProcess = subprocess.run(['xdotool', 'search', '--name',
                                                'Dota 2'], capture_output=True)
                self.gc.dota2WindowID = completedProcess.stdout.decode('UTF-8')
            print("Currently available: Democracy, Anarchy")
            self.mode = input("Game type (default Anarchy): ")
            #mode = 'anarchy'
            # if mode.lower() == "anarchy":
            #     break
            if self.mode.lower() == "democracy":
                print("Takes most said command every X second(s): ")
                self.democracy_time = float(input("(must be integer) X="))
                break
            else:
                break

        self.startMode()

    def startMode(self):
        self.resetFiles()
        # Democracy Game Mode?
        if self.mode.lower() == "democracy":
            
            count_job = Thread(target=self.democracy, args=())
            count_job.start()

        time.sleep(1)
        twitchSocket = self.connectToTwitch()
        self.handleTwitchResponse(twitchSocket)

    def democracy(self):
        list_commands = []
        last_command = time.time()
        selected_c = "None"

        while True:
            if time.time() > last_command + self.democracy_time:
                last_command = time.time()
                if(len(list_commands) > 0):
                    selected_c = self.most_common(list_commands)
                    print('selected_c: %s' % selected_c)
                else:
                    selected_c = 'None'
                with open("lastsaid.txt", "w") as f:
                    f.write("Selected %s\n" % selected_c)
                    f.write("Time left: %s" % str(self.democracy_time)[0:1])
                list_commands = []
                if(selected_c != 'None'):
                    splitted = selected_c.lower().split(' ')
                    self.gc.findAndExecute(splitted)
            else:
                with open("lastsaid.txt", "w") as f:
                    f.write("Selected %s\n" % selected_c)
                    f.write("Time left: %s" % str(
                        1.0 + last_command + self.democracy_time - time.time())[0:1])
            time.sleep(1)

    def resetFiles(self):
        with open("lastsaid.txt", "w") as f:
            f.write("")
        with open("most_common_commands.txt", "w") as f:
            f.write("")
        with open("ragequit.txt", "w") as f:
            f.write("")
        with open("commands.txt", "w") as f:
            f.write("")

    def connectToTwitch(self):
        s = socket.socket()
        s.connect((self.HOST, self.PORT))

        s.send(bytes("PASS %s\r\n" % self.AUTH, "UTF-8"))
        s.send(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
        s.send(bytes("USER %s %s bla :%s\r\n" % (self.NICK, self.HOST, self.NICK), "UTF-8"))
        s.send(bytes("JOIN #%s\r\n" % self.CHAT_CHANNEL, "UTF-8"))
        s.send(bytes("PRIVMSG #%s :Connected\r\n" % self.CHAT_CHANNEL, "UTF-8"))
        print("Sent connected message to channel %s" % self.CHAT_CHANNEL)
        return s
    
    def handleTwitchResponse(self, s):
        readbuffer = ''
        while 1:
            readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()

            for line in temp:
                x = 0
                out = ""
                line = str.rstrip(line)
                line = str.split(line)

                for index, dummy in enumerate(line):
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
                elif user == ":%s.tmi.twitch.tv: " % self.NICK:
                    pass
                else:
                    try:
                        print(user + out)
                    except UnicodeEncodeError:
                        print(user)
                
                # Take in output
                # sanitize output
                # TODO: transfer command logic outside setup logic/ use another class
                if(self.validator.validateCommand(out.lower())):
                    self.addToCommandList(user, out)
                    # Write to file for stream view
                    with open("commands.txt", "w") as f:
                        for item in self.commands:
                            f.write(item + '\n')
                    if(self.mode == "anarchy"):
                        splitted = out.lower().split(' ')
                        self.gc.findAndExecute(splitted)

    def addToCommandList(self, user, out):
        if len(self.commands) >= self.command_length:
            del self.commands[0]
            self.commands.extend([user[1:] + out.lower()])
            if self.mode.lower() == "democracy":
                self.list_commands.extend([out.lower()])
        else:
            self.commands.extend([user[1:] + out.lower()])
            if self.mode.lower() == "democracy":
                self.list_commands.extend([out.lower()])

    def most_common(self, lst):
        # Write to file for stream view
        tempList = lst
        maxList = []
        if(len(lst) > 5):
            for dummy in range(5):
                if(len(tempList) > 0):
                    tempMax = max(tempList, key=tempList.count)
                    maxList.append(tempMax)
                    tempList = list(filter(lambda a: a != tempMax, tempList))
                else:
                    break

        else:
            for dummy in range(len(lst)):
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

class Validator:
    def __init__(self):
        self.PATTERNS = {
            # ! + m or move + (a-H + a-H(same a-H as b4) or number 1-4) +
            # (must be different then b4 =>)(a-H + a-H(same a-H as b4) or number 1-4) + ending or + ' trash'
            'move': r'^!(m|move) (([a-hA-H])((?=\3)[a-hA-H]|[1-4])) (?!\2)(([a-hA-H])((?=\3)[a-hA-H]|[1-4]))($| +)',
            'movedirection': r'^!(m|move) (left|right|top|bot)($| +)',
            'movefromslots': r'^!(aa|bb|cc|dd|ee|ff|gg|hh)( (left|right|top|bot))?($| +)',
            'grab': r'^!(g|grab) (([a-hA-H])((?=\3)[a-hA-H]|[1-8]))($| +)',
            'bench': r'^!(b|bench) ([a-hA-H][1-4])($| +)',
            'sell': r'^!(s|sell) (([a-hA-H])((?=\3)[a-hA-H]|[1-8]))($| +)',
            'rq': r'^!rq($| +)',
            'reroll': r'^!(r|reroll)($| +)',
            'buyxp': r'^!(x|xp) [1-4]($| +)',
            'shop': r'^!shop (on|off)($| +)',
            'lock': r'^!(l|lock)($| +)',
            'pick': r'^!(p|pick) [1-5]($| +)',
            'itemtohero': r'^!(i|item) ([1-9]) (([a-hA-H])((?=\4)[a-hA-H]|[1-8]))($| +)',
            'tab': r'^!tab( [1-8])?($| +)',
            'random': r'^!random($| +)',
            'search': r'^!search($| +)',
            'accept': r'^!accept($| +)',
            'calib': r'^!calib($| +)',
            'run': r'^!run (left|right|top|bot)($| +)',
            'lockitem': r'^!(iu?l|itemlock) ([1-9])($| +)',
            'stay': r'^!stay($| +)',
            'write': r'^!write($| +)',
            'exec': r'^!exec($| +)',
            'stack': r'^!stack (!m|!g|!b|!s|!rq|!r|!x|!shop|!l|!p|!i|!tab|!random|!search|!accept|!calib|!run|!iu?l|!stay)'
        }

    # TODO: validator als eigene klasse mit PATTERNs attribut
    def validateCommand(self, incomingString):
        '''
        Validate incoming commands
        '''
        # not a command
        if(incomingString[:1] != '!'):
            return None

        # does it match any pattern?
        for pattern in self.PATTERNS:
            if(re.match(self.PATTERNS[pattern], incomingString, re.IGNORECASE)):
                print('found pattern for: %s' % pattern)
                return True

        return False

if __name__ == "__main__":
    setup = Setup()
    gc = GameController()
