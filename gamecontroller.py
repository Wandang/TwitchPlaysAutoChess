#!/usr/bin/env python3

# gamecontroller.py
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


import subprocess
from pynput.mouse import Button as MouseButton
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key as KeyboardKey
from pynput.keyboard import Controller as KeyboardController
import time
import random
import math
from collections import OrderedDict
from threading import Thread

import validator
import iocontroller

class GameController:
    """Controls the game input. Emulates mouse and keyboard input via xdotools.
    Each Dota AutoChess action is mapped as function"""

    myIO = iocontroller.IOController()
    isXDOTOOL = False
    mouse = MouseController()
    keyboard = KeyboardController()
    commandStack = []
    # default delay after each peripheral action. Needs to be > 0 to make sure that the actions are finished properly
    delayBetweenActions = 0.3
    dota2WindowID = ''
    allowRagequit = False
    TWITCHEMOTES = ['monkaS', '4Head', 'FailFish', 'DansGame', 'LUL', 'Kappa', 'NotLikeThis',
                    'OSFrog', 'PJSalt', 'WutFace', 'cmonBruh', 'TriHard', 'PogChamp', 'ResidentSleeper']


    # taken with reference resolution of 1024x768
    COORDMAP_RESOLUTION_4TO3 = {
        'a1': {'x': '285', 'y': '449'},
        'a2': {'x': '295', 'y': '391'},
        'a3': {'x': '303', 'y': '339'},
        'a4': {'x': '314', 'y': '293'},
        'a5': {'x': '323', 'y': '250'},
        'a6': {'x': '331', 'y': '212'},
        'a7': {'x': '338', 'y': '176'},
        'a8': {'x': '343', 'y': '142'},
        'h1': {'x': '736', 'y': '445'},
        'h2': {'x': '726', 'y': '390'},
        'h3': {'x': '715', 'y': '337'},
        'h4': {'x': '706', 'y': '294'},
        'h5': {'x': '698', 'y': '252'},
        'h6': {'x': '690', 'y': '211'},
        'h7': {'x': '683', 'y': '173'},
        'h8': {'x': '677', 'y': '141'},

        'aa': {'x': '253', 'y': '578'},
        'hh': {'x': '770', 'y': '578'},

        'pickFirst': {'x': '152', 'y': '196'},
        'pickLast': {'x': '861', 'y': '194'},
        'lock': {'x': '53', 'y': '312'},
        'close': {'x': '971', 'y': '245'},
        'nothing': {'x': '848', 'y': '39'},

        'chickenAbility1':{'x': '438', 'y': '690'},
        'chickenAbility5':{'x': '601', 'y': '690'},
        'shopButton': {'x': '249', 'y': '30'},

        'chickSlot1': {'x': '651', 'y': '686'},
        'chickSlot9': {'x': '739', 'y': '747'},

        'resetChicken': {'x': '514', 'y': '500'},

        'dotaArrowBtn': {'x': '22', 'y': '20'},
        'dotaDisconnectBtn': {'x': '841', 'y': '735'},
        'dotaLeaveBtn': {'x': '850', 'y': '700'},
        'dotaLeaveAcceptBtn': {'x': '456', 'y': '423'},
        'dotaPlayAutoChessBtn': {'x': '900', 'y': '616'},
        'dotaAcceptBtn': {'x': '504', 'y': '371'},
        'dotaMainMenuBtn': {'x': '207', 'y': '27'},
        'dotaAutoChessBtn': {'x': '394', 'y': '345'},

        'playerPosFirst': {'x': '895', 'y': '108'},
        'playerPosLast': {'x': '895', 'y': '605'}
    }

    # taken with reference resolution of 1920x1080
    COORDMAP_RESOLUTION_16TO9 = {
        'a1': {'x': '633', 'y': '620'},
        'a2': {'x': '651', 'y': '548'},
        'a3': {'x': '669', 'y': '471'},
        'a4': {'x': '683', 'y': '402'},
        'a5': {'x': '695', 'y': '346'},
        'a6': {'x': '708', 'y': '293'},
        'a7': {'x': '715', 'y': '240'},
        'a8': {'x': '727', 'y': '194'},
        'h1': {'x': '1278', 'y': '619'},
        'h2': {'x': '1265', 'y': '539'},
        'h3': {'x': '1248', 'y': '468'},
        'h4': {'x': '1235', 'y': '405'},
        'h5': {'x': '1227', 'y': '346'},
        'h6': {'x': '1213', 'y': '290'},
        'h7': {'x': '1204', 'y': '241'},
        'h8': {'x': '1195', 'y': '194'},

        'aa': {'x': '592', 'y': '807'},
        'hh': {'x': '1329', 'y': '806'},

        'pickFirst': {'x': '464', 'y': '276'},
        'pickLast': {'x': '1458', 'y': '256'},
        'lock': {'x': '313', 'y': '445'},
        'close': {'x': '1610', 'y': '344'},
        'nothing': {'x': '1547', 'y': '77'},

        'chickenAbility1':{'x': '855', 'y': '970'},
        'chickenAbility5':{'x': '1087', 'y': '970'},
        'shopButton': {'x': '591', 'y': '37'},

        'chickSlot1': {'x': '1158', 'y': '964'},
        'chickSlot9': {'x': '1286', 'y': '1057'},

        'resetChicken': {'x': '914', 'y': '712'},

        'dotaArrowBtn': {'x': '32', 'y': '27'},
        'dotaDisconnectBtn': {'x': '1627', 'y': '1035'},
        'dotaLeaveBtn': {'x': '1648', 'y': '985'},
        'dotaLeaveAcceptBtn': {'x': '874', 'y': '603'},
        'dotaPlayAutoChessBtn': {'x': '1530', 'y': '866'},
        'dotaAcceptBtn': {'x': '901', 'y': '529'},
        'dotaMainMenuBtn': {'x': '286', 'y': '32'},
        'dotaAutoChessBtn': {'x': '780', 'y': '478'},

        'playerPosFirst': {'x': '1737', 'y': '155'},
        'playerPosLast': {'x': '1737', 'y': '855'}
    }

    # taken with reference resolution of 1280x800
    COORDMAP_RESOLUTION_16TO10 = {
        'a1': {'x': '399', 'y': '464'},
        'a2': {'x': '412', 'y': '401'},
        'a3': {'x': '422', 'y': '349'},
        'a4': {'x': '434', 'y': '300'},
        'a5': {'x': '440', 'y': '258'},
        'a6': {'x': '449', 'y': '215'},
        'a7': {'x': '457', 'y': '176'},
        'a8': {'x': '463', 'y': '143'},
        'h1': {'x': '877', 'y': '460'},
        'h2': {'x': '867', 'y': '402'},
        'h3': {'x': '855', 'y': '348'},
        'h4': {'x': '846', 'y': '299'},
        'h5': {'x': '836', 'y': '253'},
        'h6': {'x': '828', 'y': '215'},
        'h7': {'x': '821', 'y': '176'},
        'h8': {'x': '815', 'y': '142'},

        'aa': {'x': '366', 'y': '600'},
        'hh': {'x': '910', 'y': '600'},

        # old 16:9 values below!
        'pickFirst': {'x': '271', 'y': '207'},
        'pickLast': {'x': '1014', 'y': '207'},
        'lock': {'x': '161', 'y': '325'},
        'close': {'x': '1121', 'y': '255'},
        'nothing': {'x': '1027', 'y': '39'},

        'chickenAbility1':{'x': '562', 'y': '717'},
        'chickenAbility5':{'x': '734', 'y': '717'},
        'shopButton': {'x': '365', 'y': '30'},

        'chickSlot1': {'x': '785', 'y': '715'},
        'chickSlot9': {'x': '880', 'y': '780'},

        'resetChicken': {'x': '642', 'y': '508'},

        'dotaArrowBtn': {'x': '22', 'y': '20'},
        'dotaDisconnectBtn': {'x': '1103', 'y': '764'},
        'dotaLeaveBtn': {'x': '1100', 'y': '730'},
        'dotaLeaveAcceptBtn': {'x': '553', 'y': '444'},
        'dotaPlayAutoChessBtn': {'x': '1017', 'y': '644'},
        'dotaAcceptBtn': {'x': '627', 'y': '390'},
        'dotaMainMenuBtn': {'x': '214', 'y': '24'},
        'dotaAutoChessBtn': {'x': '504', 'y': '357'},

        'playerPosFirst': {'x': '1144', 'y': '112'},
        'playerPosLast': {'x': '1144', 'y': '630'}
    }

    COORDMAP = {
        'a1': {'x': '633', 'y': '620'},
        'a2': {'x': '651', 'y': '548'},
        'a3': {'x': '669', 'y': '471'},
        'a4': {'x': '683', 'y': '402'},
        'a5': {'x': '695', 'y': '346'},
        'a6': {'x': '708', 'y': '293'},
        'a7': {'x': '715', 'y': '240'},
        'a8': {'x': '727', 'y': '194'},
        'h1': {'x': '1278', 'y': '619'},
        'h2': {'x': '1265', 'y': '539'},
        'h3': {'x': '1248', 'y': '468'},
        'h4': {'x': '1235', 'y': '405'},
        'h5': {'x': '1227', 'y': '346'},
        'h6': {'x': '1213', 'y': '290'},
        'h7': {'x': '1204', 'y': '241'},
        'h8': {'x': '1195', 'y': '194'},

        'aa': {'x': '592', 'y': '807'},
        'hh': {'x': '1329', 'y': '806'},

        'pickFirst': {'x': '464', 'y': '276'},
        'pickLast': {'x': '1458', 'y': '256'},
        'lock': {'x': '313', 'y': '445'},
        'close': {'x': '1610', 'y': '344'},
        'nothing': {'x': '1547', 'y': '77'},

        'chickenAbility1':{'x': '855', 'y': '970'},
        'chickenAbility5':{'x': '1087', 'y': '970'},
        'shopButton': {'x': '591', 'y': '37'},

        'chickSlot1': {'x': '1158', 'y': '964'},
        'chickSlot9': {'x': '1286', 'y': '1057'},

        'resetChicken': {'x': '914', 'y': '712'},

        'dotaArrowBtn': {'x': '32', 'y': '27'},
        'dotaDisconnectBtn': {'x': '1627', 'y': '1035'},
        'dotaLeaveBtn': {'x': '1648', 'y': '985'},
        'dotaLeaveAcceptBtn': {'x': '874', 'y': '603'},
        'dotaPlayAutoChessBtn': {'x': '1530', 'y': '866'},
        'dotaAcceptBtn': {'x': '901', 'y': '529'},
        'dotaMainMenuBtn': {'x': '286', 'y': '32'},
        'dotaAutoChessBtn': {'x': '780', 'y': '478'},

        'playerPosFirst': {'x': '1737', 'y': '155'},
        'playerPosLast': {'x': '1737', 'y': '855'}
    }

    CHICKENLEFT = OrderedDict([
        ('A1L', {'x': '565', 'y': '612'}),
        ('A2L', {'x': '583', 'y': '541'}),
        ('A3L', {'x': '603', 'y': '463'}),
        ('A4L', {'x': '617', 'y': '404'}),
        ('A5L', {'x': '633', 'y': '340'}),
        ('A6L', {'x': '645', 'y': '284'}),
        ('A7L', {'x': '660', 'y': '236'}),
        ('A8L', {'x': '670', 'y': '192'})
    ])

    CHICKENTOP = OrderedDict([
        ('A8T', {'x': '735', 'y': '149'}),
        ('B8T', {'x': '798', 'y': '145'}),
        ('C8T', {'x': '866', 'y': '144'}),
        ('D8T', {'x': '928', 'y': '141'}),
        ('E8T', {'x': '994', 'y': '142'}),
        ('F8T', {'x': '1059', 'y': '143'}),
        ('G8T', {'x': '1131', 'y': '137'}),
        ('H8T', {'x': '1190', 'y': '151'})])

    CHICKENRIGHT = OrderedDict([
        ('H8R', {'x': '1255', 'y': '191'}),
        ('H7R', {'x': '1269', 'y': '238'}),
        ('H6R', {'x': '1283', 'y': '293'}),
        ('H5R', {'x': '1293', 'y': '345'}),
        ('H4R', {'x': '1310', 'y': '403'}),
        ('H3R', {'x': '1320', 'y': '474'}),
        ('H2R', {'x': '1338', 'y': '542'}),
        ('H1R', {'x': '1355', 'y': '616'})])

    CHICKENBOT = OrderedDict([
        ('H1B', {'x': '1287', 'y': '698'}),
        ('G1B', {'x': '1194', 'y': '692'}),
        ('F1B', {'x': '1093', 'y': '695'}),
        ('E1B', {'x': '1001', 'y': '691'}),
        ('D1B', {'x': '913', 'y': '693'}),
        ('C1B', {'x': '820', 'y': '689'}),
        ('B1B', {'x': '728', 'y': '689'}),
        ('A1B', {'x': '630', 'y': '689'})])

    itemoffsetFirstRowX = 54
    itemoffsetFirstRowy = 31
    itemoffsetSecondRowX = 75
    itemoffsetSecondRowy = 0  # 6 old

    def __init__(self, channelName, hotkeys, resolution):
        self.channelName = channelName
        self.hotkeys = hotkeys
        self.resolution = resolution

        aspectRatio4To3 = (int(self.resolution[0])/int(self.resolution[1]) * 3/4)
        aspectRatio16To9 = (int(self.resolution[0])/int(self.resolution[1]) * 9/16)
        aspectRatio16To10 = (int(self.resolution[0])/int(self.resolution[1]) * 10/16)
        if( math.isclose(aspectRatio4To3,1.0,rel_tol=0.05)):
            print('4:3!')
            diffResoX = int(self.resolution[0])/1024
            diffResoY = int(self.resolution[1])/768
            self.COORDMAP = self.COORDMAP_RESOLUTION_4TO3

        elif(math.isclose(aspectRatio16To9,1.0,rel_tol=0.05)):
            print('16:9!')
            diffResoX = int(self.resolution[0])/1920
            diffResoY = int(self.resolution[1])/1080
            self.COORDMAP = self.COORDMAP_RESOLUTION_16TO9

        elif(math.isclose(aspectRatio16To10,1.0,rel_tol=0.05)):
            print('16:10!')
            diffResoX = int(self.resolution[0])/1280
            diffResoY = int(self.resolution[1])/800
            self.COORDMAP = self.COORDMAP_RESOLUTION_16TO10

        for coord in self.COORDMAP:
            relativeXValue = float(self.COORDMAP[coord]['x']) * diffResoX
            relativeYValue = float(self.COORDMAP[coord]['y']) * diffResoY
            self.COORDMAP[coord]['x'] = str(int(relativeXValue))
            self.COORDMAP[coord]['y'] = str(int(relativeYValue))
            


    def testAllFields(self):
        """Testfunction that will move the mouse to every field"""
        time.sleep(5)
        startOffset = ord('a')
        for i in range(1,9):
            for j in range(8):
                tempChar = str(chr(startOffset + j))
                x, y = self.convertToLocation(tempChar+str(i))
                self.moveMouse(x,y)
                time.sleep(0.1)

    def convertToLocation(self, field):
        """Returns pixel coordinates of a given field (AA,A1..H8)
        
        Keyword arguments:
            field -- Field (AA,A1..H8)
        """
        aAsNr = ord('a')
        firstChar = field[:1]
        secondChar = field[1:]
        firstCharNr = ord(firstChar)
        diffNr = firstCharNr - aAsNr 
        if(firstChar == secondChar):
            diffRow = float(self.COORDMAP['hh']['x']) - float(self.COORDMAP['aa']['x'])
            intervalRow = diffRow / 7
            newXPos = int(float(self.COORDMAP['aa']['x'])+diffNr*intervalRow)
            newYPos = int(self.COORDMAP['aa']['y'])
        else:
            diffRow = float(self.COORDMAP['h'+secondChar]['x']) - float(self.COORDMAP['a'+secondChar]['x'])
            intervalRow = diffRow / 7
            newXPos = int(float(self.COORDMAP['a'+secondChar]['x'])+diffNr*intervalRow)
            newYPos = int(self.COORDMAP['a'+secondChar]['y'])
        return newXPos, newYPos


    def moveMouse(self,x,y,clickType = None):
        """Move the mouse to the desired coordinates and optionally click at that location.
        
        Keyword arguments:
            x -- x coordinate inside screen resolution
            y -- y coordinate inside screen resolution
            clickType -- 1: leftclick, 2: middleclick, 3: rightclick
        """
        print('trying to move to x: ',x)
        print('trying to move to y: ',y)
        # print('trying to click: ' + clickType)
        if(self.isXDOTOOL):
            # -- window param makes sure that the input gets send to a specific window, even if it is in the background
            subprocess.run(['xdotool',
                            'mousemove',
                            '--window',
                            self.dota2WindowID,
                            x,
                            y])
            if(clickType):
                self.clickMouse(clickType)
        else:
            self.mouse.position = (int(x),int(y))
            if(clickType):
                self.clickMouse(clickType)
        time.sleep(self.delayBetweenActions)

    def clickMouse(self, clickType):
        """Clicks the specified mousebutton    
                
        Keyword arguments:
            clickType -- 1: leftclick, 2: middleclick, 3: rightclick
        """
        if(self.isXDOTOOL):
            subprocess.run(['xdotool','click','--window',self.dota2WindowID, clickType])
        else:
            if(clickType == '1'):
                self.mouse.click(MouseButton.left)
            elif(clickType == '2'):
                self.mouse.click(MouseButton.middle)
            elif(clickType == '3'):
                self.mouse.click(MouseButton.right)


    def dragAndDrop(self,source,target):
        """Drags & drops from source to target location.
        This is used for items.
        
        Keyword arguments:
            source -- coordinates of source item location [x,y]
            target -- Field name ('aa','a1'..'h8')
        """
        self.moveMouse(source['x'],source['y'])
        time.sleep(1)
        # hold mouse button
        if(self.isXDOTOOL):
            subprocess.run(['xdotool', 'mousedown', '--window', self.dota2WindowID, '1'])
        else:
            self.mouse.press(MouseButton.left)
        time.sleep(0.5)
        x, y = self.convertToLocation(target)
        self.moveMouse(x,y)
        time.sleep(1)
        # release mouse button
        if(self.isXDOTOOL):
            subprocess.run(['xdotool', 'mouseup', '--window', self.dota2WindowID, '1'])
        else:
            self.mouse.release(MouseButton.left)

    def pressKey(self, key):
        """Presses specified key on keyboard
        
        Keyword arguments:
            key -- keyboard key (keycodes)
        """
        subprocess.run(['xdotool', 'key', '--window', self.dota2WindowID, key])

    # def pressKeyWithPynput(self, key):
    #     """Presses specified key on keyboard with pykeyboard module
        
    #     Keyword arguments:
    #         key -- keyboard key (keycodes)
    #     """
    #     print('trying to press key: ',key)
    #     self.keyboard.press(key)
    #     self.keyboard.release(key)

    def toggleLockItem(self, slot):
        """Locks item in specified itemslot (1-9)
        
        Keyword arguments:
            slot -- number between 1-9
        """
        distanceX = int(self.COORDMAP['chickSlot9']['x']) - int(self.COORDMAP['chickSlot1']['x'])
        distanceY = int(self.COORDMAP['chickSlot9']['y']) - int(self.COORDMAP['chickSlot1']['y'])
        # We have 3x3 item matrix
        distanceToEachCenterX = distanceX / 3
        distanceToEachCenterY = distanceY / 3
        # after 3 and 6 the next row starts
        newXCoord = int(self.COORDMAP['chickSlot1']['x']) + ((int(slot)-1) % 3) * distanceToEachCenterX
        # reduce slot number slightly so 1,2,3 / 3.0 casted to int becomes 0; 4,5,6 become 1; and 7,8,9 become 2
        newYCoord = int(self.COORDMAP['chickSlot1']['y']) + int((int(slot)-1)/3.0) * distanceToEachCenterY
        self.moveMouse(newXCoord,newYCoord, '3')
        time.sleep(0.5)
        # the rightclick menu changes position depending on row
        lockLabelPosX = str(int(newXCoord)+int(self.itemoffsetFirstRowX))
        lockLabelPosY = str(int(newYCoord)+int(self.itemoffsetFirstRowy))
        if(int(slot) > 3):
            # slot is below first row
            lockLabelPosX = str(int(newXCoord)+int(self.itemoffsetSecondRowX))
            lockLabelPosY = str(int(newYCoord)+int(self.itemoffsetSecondRowy))
        self.moveMouse(lockLabelPosX,lockLabelPosY,'1')

    # TODO: optimize, reduce redundancy
    def grabItemChickenloop(self, side):
        """Let's the chicken/courier walk alongside a side of the chessboard to pick up items.
        
        Keyword arguments:
            side -- Which side should be checked for items. Can be left, top, bot or right.
        """
        # make sure the shop is hidden to not interfere with our clicks
        self.showSelection('off')
        if(side == 'left'):
            # pos chicken at A1 first
            x, y = self.convertToLocation('a1')
            self.moveMouse(x,y ,'3')
            time.sleep(3)
            for coord in self.CHICKENLEFT:
                self.moveMouse(self.CHICKENLEFT[coord]['x'],self.CHICKENLEFT[coord]['y'],'3')
                time.sleep(0.3)
        elif(side == 'top'):
            # pos chicken at A8 first
            x,y = self.convertToLocation('a8')
            self.moveMouse(x,y)
            time.sleep(3)
            for coord in self.CHICKENTOP:
                self.moveMouse(self.CHICKENTOP[coord]['x'],self.CHICKENTOP[coord]['y'])
                time.sleep(0.3)
        elif(side == 'right'):
            # pos chicken at H8 first
            x,y = self.convertToLocation('h8')
            self.moveMouse(x,y)
            time.sleep(3)
            for coord in self.CHICKENRIGHT:
                self.moveMouse(self.CHICKENRIGHT[coord]['x'],self.CHICKENRIGHT[coord]['y'])
                time.sleep(0.3)
        elif(side == 'bot'):
            # pos chicken at H1 first
            x,y = self.convertToLocation('h1')
            self.moveMouse(x,y)
            time.sleep(3)
            for coord in self.CHICKENBOT:
                self.moveMouse(self.CHICKENBOT[coord]['x'],self.CHICKENBOT[coord]['y'])
                time.sleep(0.3)
        
        # send chicken back to default position
        self.resetChickenPos()


    def resetChickenPos(self):
        """Sends chicken back to default position"""
        self.moveMouse(self.COORDMAP['resetChicken']['x'],self.COORDMAP['resetChicken']['y'],'3')
        time.sleep(self.delayBetweenActions)


    def moveItem(self, slot, target):
        '''Move item from chicken slot to target hero coordinates.
        
        Keyword arguments:
            slot -- Itemslot of the chicken (1-9)
            target -- target chessboard/bench position
        '''
        # close shop before
        self.showSelection('off')
        distanceX = int(self.COORDMAP['chickSlot9']['x']) - int(self.COORDMAP['chickSlot1']['x'])
        distanceY = int(self.COORDMAP['chickSlot9']['y']) - int(self.COORDMAP['chickSlot1']['y'])
        # We have 3x3 item matrix
        distanceToEachCenterX = distanceX / 3
        distanceToEachCenterY = distanceY / 3
        # after 3 and 6 the next row starts
        newXCoord = int(self.COORDMAP['chickSlot1']['x']) + ((int(slot)-1) % 3) * distanceToEachCenterX
        # reduce slot number slightly so 1,2,3 / 3.0 casted to int becomes 0; 4,5,6 become 1; and 7,8,9 become 2
        newYCoord = int(self.COORDMAP['chickSlot1']['y']) + int((int(slot)-1)/3.0) * distanceToEachCenterY
        self.dragAndDrop({'x': newXCoord, 'y': newYCoord},target)
        # give chicken time to run to the destination
        # TODO: dynamic time depending on target location
        time.sleep(5)
        self.resetChickenPos()


    def grabItem(self, target):
        """Let's the chicken pick up dropped items
        
        Keyword arguments:
            target -- target chessboard position
        """
        # close shop first
        self.showSelection('off')
        x, y = self.convertToLocation(target)
        self.moveMouse(x,y,'3')
        # TODO: dynamic time depending on target location
        time.sleep(5)
        self.resetChickenPos()


    def tabTour(self, playerPlacementID=-1):
        '''Show chessboard of player x or if no player is given show every chessboard in 5s
        
        Keyword arguments:
            playerPlacementID -- PlayerID defined by current placement (1-8)
        '''
        distancePlayersY = int(self.COORDMAP['playerPosFirst']['y']) - int(self.COORDMAP['playerPosLast']['y'])
        diffCenter = distancePlayersY / 8
        if(playerPlacementID != -1):
            #timeToStayOnPlayer = 3

            newYCoord = int(self.COORDMAP['playerPosFirst']['y']) + (playerPlacementID-1) * diffCenter
            # cheeky message to be displayed to make it feel more interactive with the other players
            # allChatMessage = 'Chat wants to inspect the current position: '+playerPlacementID
            # self.writeAllChat(allChatMessage)
            # clicking on the avatar of the specific player leads us to their camposition
            self.moveMouse(self.COORDMAP['playerPosFirst']['x'],newYCoord, '1')
            time.sleep(self.delayBetweenActions)
            # move mouse away from avatars so the popovertext is not blocking the view
            self.clickNothing()
            #time.sleep(timeToStayOnPlayer)
            # cheeky message to be displayed to make it feel more interactive with the other players
            # allChatMessage = 'Chat judgement: ' + \
            #     self.TWITCHEMOTES[random.randint(0, len(self.TWITCHEMOTES))]
            # self.writeAllChat(allChatMessage)
            #self.camCalibration()
        else:
            self.clickNothing()
            time.sleep(self.delayBetweenActions)
            for i in range(8):
                if(self.isXDOTOOL):
                    self.pressKey('Tab')
                else:
                    newYCoord = int(self.COORDMAP['playerPosFirst']['y']) + i * diffCenter
                    self.moveMouse(self.COORDMAP['playerPosFirst']['x'],newYCoord, '1')
                    time.sleep(self.delayBetweenActions)
                    # move mouse away from avatars so the popovertext is not blocking the view
                    self.clickNothing()

                time.sleep(0.625)


    # TODO: add profanity filter to prevent possible repercussions through twitch/ possible violation of TOS?
    # def writeAllChat(self, message):
    #     """Writes a message to everyone
        
    #     Keyword arguments:
    #         message -- Textmessage to be send
    #     """
    #     if(self.isXDOTOOL):
    #         self.pressKey('shift+Return')
    #     else:
    #         print('trying to hold shift...')
    #         with self.keyboard.pressed(KeyboardKey.shift):
    #             print('shift held')
    #             self.pressKeyWithPynput(KeyboardKey.enter)

    #     time.sleep(self.delayBetweenActions)
    #     if(self.isXDOTOOL):
    #         subprocess.run(['xdotool', 'type', '--window', self.dota2WindowID, message])
    #     else:
    #         print('typing message')
    #         self.keyboard.type(message)
    #     time.sleep(0.5)
    #     if (self.isXDOTOOL):
    #         self.pressKey('Return')
    #     else:
    #         self.pressKeyWithPynput(KeyboardKey.enter)
    #     time.sleep(self.delayBetweenActions)

    # TODO: promotelink should be read from settings file
    def camCalibration(self, promote=False):
        """Needs to be done once at the start of each game!
        Sets cam to playerposition.
        This is the referenceposition for all other commands and therefore important!
        Without calibration every chess piece interaction will fail.
        
        Keyword arguments:
            promote -- Promotes the twitch channel in allchat (bool)
        """
        pass
        # if (self.isXDOTOOL):
        #     self.pressKey('1')
        # else:
        #     self.pressKeyWithPynput('1')
        # # shoutout in allchat to promote the bot
        # if(promote):
        #     self.writeAllChat(
        #         'Chat is playing right now on https://www.twitch.tv/' + self.channelName)
        # time.sleep(self.delayBetweenActions)


    def acceptGame(self):
        """Press the accept button in Dota"""
        self.moveMouse(self.COORDMAP['dotaAcceptBtn']['x'],self.COORDMAP['dotaAcceptBtn']['y'], '1')

    def searchGame(self):
        """Initiates the search for a Dota AutoChess game inside Dota."""
        # press esc to close any info windows (for example due to not accepting b4)
        # if (self.isXDOTOOL):
        #     self.pressKey('Escape')
        # else:
        #     self.pressKeyWithPynput(KeyboardKey.esc)
        
        # go to main menu first
        self.moveMouse(self.COORDMAP['dotaMainMenuBtn']['x'],self.COORDMAP['dotaMainMenuBtn']['y'], '1')
        # navigate to autochess
        self.moveMouse(self.COORDMAP['dotaAutoChessBtn']['x'],self.COORDMAP['dotaAutoChessBtn']['y'], '1')
        # start autochess search
        self.moveMouse(self.COORDMAP['dotaPlayAutoChessBtn']['x'],self.COORDMAP['dotaPlayAutoChessBtn']['y'], '1')
        time.sleep(5)
        self.acceptGame()


    def abortRagequit(self):
        """Stop quitting the current AutoChess game"""
        self.allowRagequit = False
        # clear text file for stream view
        self.myIO.resetFile("ragequit.txt")


    def rageQuitProcess(self):
        """Starts a timer of 20s to display a warning. After 20s the current AutoChess game will be abandoned.
        Can be stopped by writing !stay in chat"""
        # how long should the message be displayed and the quitting delayed?
        targetTime = 20
        starttime = time.time()
        while True:
            if(time.time() - starttime < targetTime):
                if(self.allowRagequit):
                    # write remaining time for chat (adding +1s because of lazy cutting of decimals)
                    self.myIO.writeFile("ragequit.txt","Time left till ragequit!: {0} \nTo abort write !stay".format(str(
                                1.0 + targetTime - (time.time() - starttime)).split('.')[0]))
                    time.sleep(1)
                else:
                    # quitting aborted, clean the file
                    self.myIO.resetFile("ragequit.txt")
                    break
            else:
                # time's up
                break

        # Ragequit still allowed?
        if(self.allowRagequit):
            # Press the dota arrow button on the upper left corner
            self.moveMouse(self.COORDMAP['dotaArrowBtn']['x'],self.COORDMAP['dotaArrowBtn']['y'], '1')
            time.sleep(0.5)
            # Press the dota disconnect button on the bottom right corner
            self.moveMouse(self.COORDMAP['dotaDisconnectBtn']['x'],self.COORDMAP['dotaDisconnectBtn']['y'], '1')
            time.sleep(1)
            # circumvent dac rating popup
            self.clickNothing()
            time.sleep(1)
            # Press the dota leave button above the disconnect (now reconnect) button
            self.moveMouse(self.COORDMAP['dotaLeaveBtn']['x'],self.COORDMAP['dotaLeaveBtn']['y'])
            time.sleep(2)
            self.clickMouse('1')
            time.sleep(1)
            # since this part is glitching, we need to click twice
            self.clickMouse('1')
            time.sleep(1)
            # Press the dota acccept button for leaving in the middle of the screen
            self.moveMouse(self.COORDMAP['dotaLeaveAcceptBtn']['x'],self.COORDMAP['dotaLeaveAcceptBtn']['y'])
            time.sleep(1)
            self.clickMouse('1')
            # clean file for stream view
            self.myIO.resetFile("ragequit.txt")

        self.allowRagequit = False


    def leaveGame(self):
        """Initiates a process of leaving the current AutoChess game with the option to abort that process."""
        # Make sure the process is only started once
        if(self.allowRagequit):
            print('ragequit already in process')
            return
        self.allowRagequit = True
        # start counter in seperate thread
        rageQuitJob = Thread(target=self.rageQuitProcess, args=())
        rageQuitJob.start()


    # TODO: recheck entire function
    def randomAction(self):
        """Execute a random action to confuse everyone and yourself."""
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
        """Buy a chess piece from the shop.
             
        Keyword arguments:
            target -- Number between 1-5
        """
        self.showSelection('on')
        distancePixels = int(self.COORDMAP['pickLast']['x']) - int(self.COORDMAP['pickFirst']['x'])
        distanceToEachCenter = distancePixels / 4
        newXCoord = int(self.COORDMAP['pickFirst']['x']) + (int(target)-1) * distanceToEachCenter
        self.moveMouse(newXCoord,self.COORDMAP['pickFirst']['y'], '1')
        time.sleep(self.delayBetweenActions)
        self.clickNothing()

    def clickNothing(self):
        '''Click on the right side of the chessboard where nothing is to interact with.
        Can be used to click empty space as well for resetting commandchain (autochess bug)'''
        self.moveMouse(self.COORDMAP['nothing']['x'],self.COORDMAP['nothing']['y'], '1')

    def closeSelection(self):
        '''Closes the shop via X button in the right upper corner'''
        self.moveMouse(self.COORDMAP['close']['x'],self.COORDMAP['close']['y'], '1')

    def showSelection(self, isOn):
        """Shows/hides the shop.
        
        Keyword arguments:
            isOn -- Show/hide (bool)
        """
        # Make sure to close the shop via X button before since we do not have game feedback and therefore need to prevent toggling wrongly
        self.closeSelection()
        if(isOn == 'on'):
            # reopen shop in this case, otherwise keep it closed
            if (self.isXDOTOOL):
                self.pressKey('space')
            else:
                self.moveMouse(self.COORDMAP['shopButton']['x'],self.COORDMAP['shopButton']['y'],'1')
        time.sleep(self.delayBetweenActions)

    def lockSelection(self):
        """Locks the shop to prevent automatic rerolling"""
        # first open selection
        self.showSelection('on')
        # click on the lock icon
        self.moveMouse(self.COORDMAP['lock']['x'],self.COORDMAP['lock']['y'],'1')

    def moveBot(self):
        """Shortcut command: Moves the first piece to the backline"""
        self.moveMouse(self.COORDMAP['chickenAbility1']['x'],self.COORDMAP['chickenAbility1']['y'],'1')
        x,y = self.convertToLocation('aa')
        self.moveMouse(x,y,'1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[0])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[0])

        time.sleep(self.delayBetweenActions)
        x,y = self.convertToLocation('e1')
        self.moveMouse(x,y,'1')
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveTop(self):
        """Shortcut command: Moves the first piece to the frontline"""
        self.moveMouse(self.COORDMAP['chickenAbility1']['x'],self.COORDMAP['chickenAbility1']['y'],'1')

        x,y = self.convertToLocation('aa')
        self.moveMouse(x,y, '1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[0])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        x,y = self.convertToLocation('d4')
        self.moveMouse(x,y, '1')
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveRight(self):
        """Shortcut command: Moves the first piece to the right side"""
        self.moveMouse(self.COORDMAP['chickenAbility1']['x'],self.COORDMAP['chickenAbility1']['y'],'1')
        x,y = self.convertToLocation('aa')
        self.moveMouse(x,y, '1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[0])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        x,y = self.convertToLocation('g3')
        self.moveMouse(x,y, '1')
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveLeft(self):
        """Shortcut command: Moves the first piece to the left side"""
        self.moveMouse(self.COORDMAP['chickenAbility1']['x'],self.COORDMAP['chickenAbility1']['y'],'1')
        x,y = self.convertToLocation('aa')
        self.moveMouse(x,y, '1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[0])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        x,y = self.convertToLocation('b3')
        self.moveMouse(x,y, '1')
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def movePieceFromSlot(self, slot, direction=''):
        """Shortcut command: Moves a piece from a slot/bench towards a general direction.
        If no direction is specified the piece will be put in the middle
        
        Keyword arguments:
            slot -- Bench/slot position of chess piece
            direction -- Direction can be left, right, top or bot
        """
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


    # TODO: check if this is needed anymore (probably obsolete)
    def movePieceDirection(self, direction):
        """Shortcut command: Moves first piece towards a general direction
        
        Keyword arguments:
            direction -- Direction can be left, right, top or bot
        """
        if direction == 'left':
            self.moveLeft()
        elif direction == 'right':
            self.moveRight()
        elif direction == 'top':
            self.moveTop()
        elif direction == 'bot':
            self.moveBot()


    def movePiece(self, source, target):
        """Moves piece from source to target location.
        Source and target locations are fields on the chessboard or on the bench
        
        Keyword arguments:
            source -- Field on the chessboard (aa,a1..h8)
            target -- Field on the chessboard (aa,a1..h8)
        """
        # make sure shop is closed while moving pieces
        self.showSelection('off')
        self.moveMouse(self.COORDMAP['chickenAbility1']['x'],self.COORDMAP['chickenAbility1']['y'],'1')
        x, y = self.convertToLocation(source)
        self.moveMouse(x,y, '1')

        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[0])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        x, y = self.convertToLocation(target)
        self.moveMouse(x,y,'1')
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        # show shop after movement for comfort
        self.showSelection('on')

    def benchPiece(self, target):
        """Removes an active chess piece from the chessboard and puts it on the bench.
        
        Keyword arguments:
            target -- target chessboard position
        """
        self.showSelection('off')
        diffDistance = self.COORDMAP['chickenAbility5']['x'] - self.COORDMAP['chickenAbility1']['x']
        interval = diffDistance / 4
        newXCoord = self.COORDMAP['chickenAbility1']['x'] + interval
        self.moveMouse(newXCoord,self.COORDMAP['chickenAbility1']['y'],'1')
        x, y = self.convertToLocation(target)
        self.moveMouse(x,y, '1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[1])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[1])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')

    def sellPiece(self, target):
        """Sells a piece.
        Target is a field on the chessboard and on the bench
        
        Keyword arguments:
            target -- target chessboard position
        """
        self.showSelection('off')
        diffDistance = self.COORDMAP['chickenAbility5']['x'] - self.COORDMAP['chickenAbility1']['x']
        interval = diffDistance / 4
        newXCoord = self.COORDMAP['chickenAbility1']['x'] + 2 * interval
        self.moveMouse(newXCoord,self.COORDMAP['chickenAbility1']['y'],'1')
        x, y = self.convertToLocation(target)
        self.moveMouse(x,y, '1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[2])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[2])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')

    def rerollPieces(self):
        """Rerolls the shop selection."""
        self.showSelection('off')
        diffDistance = self.COORDMAP['chickenAbility5']['x'] - self.COORDMAP['chickenAbility1']['x']
        interval = diffDistance / 4
        newXCoord = self.COORDMAP['chickenAbility1']['x'] + 3 * interval
        self.moveMouse(newXCoord,self.COORDMAP['chickenAbility1']['y'],'1')
        # if (self.isXDOTOOL):
        #     self.pressKey(self.hotkeys[3])
        # else:
        #     self.pressKeyWithPynput(self.hotkeys[3])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')

    def buyXP(self, amount):
        """Buys experience x times depending on the amount
        
        Keyword arguments:
            amount -- How many times xp should be bought (1-4)
        """
        for dummy in range(int(amount)):
            self.moveMouse(self.COORDMAP['chickenAbility5']['x'],self.COORDMAP['chickenAbility5']['y'],'1')
            # if (self.isXDOTOOL):
            #     self.pressKey(self.hotkeys[4])
            # else:
            #     self.pressKeyWithPynput(self.hotkeys[4])
            time.sleep(0.8)
        self.clickNothing()
    
    def executeStack(self):
        """Executes a stack/queue of commands sequentially."""
        for command in self.commandStack:
            self.findAndExecute(command.split(' '))
        # clear command stack afterwards
        self.commandStack = []


    def addToStack(self, commandForStack):
        """Add a command to stack/queue for later execution
        
        Keyword arguments:
            commandForStack -- Command as string
        """
        # TODO: set a limit on stack?
        self.commandStack.append(commandForStack)


    def stackCommand(self, commandArray):
        """Add a command to stack/queue for later execution
        
        Keyword arguments:
            commandForStack -- Command as string
        """
        # since it was a splitted array before we need to recreate the original nested command string first
        patchedCommand = ''
        for i in range(1, len(commandArray)):
            patchedCommand += commandArray[i] + ' '
        patchedCommand = patchedCommand[:-1]
        # check the nested command
        if validator.validateCommand(patchedCommand):
            # valid, add to stack
            self.addToStack(patchedCommand)

    
    def findAndExecute(self, splitted):
        """Checks which command is invoked and executes the command accordingly
        
        Keyword arguments:
            splitted -- Array of commando parts that was splitted by space 
        """
        # TODO: reuse patterns on unsplitted string to reduce redundance
        if splitted[0] == '!m' or splitted[0] == '!move':
            time.sleep(.02)
            # execute command
            if(len(splitted) > 2):
                self.movePiece(splitted[1], splitted[2])
            else:
                self.movePieceDirection(splitted[1])
        elif splitted[0] == '!b' or splitted[0] == '!bench':
            time.sleep(.02)
            # execute command
            self.benchPiece(splitted[1])
        elif splitted[0] == '!s' or splitted[0] == '!sell':
            time.sleep(.02)
            # execute command
            self.sellPiece(splitted[1])
        elif splitted[0] == '!r' or splitted[0] == '!reroll':
            time.sleep(.02)
            # execute command
            self.rerollPieces()
        elif splitted[0] == '!x' or splitted[0] == '!xp':
            time.sleep(.02)
            # execute command
            self.buyXP(splitted[1])
        elif splitted[0] == '!shop':
            time.sleep(.02)
            # execute command
            self.showSelection(splitted[1])
        elif splitted[0] == '!p' or splitted[0] == '!pick':
            time.sleep(.02)
            # execute command
            self.pickPiece(splitted[1])
        elif splitted[0] == '!l' or splitted[0] == '!lock':
            time.sleep(.02)
            # execute command
            self.lockSelection()
        elif splitted[0] == '!g' or splitted[0] == '!grab':
            time.sleep(.02)
            # execute command
            self.grabItem(splitted[1])
        elif splitted[0] == '!i' or splitted[0] == '!item':
            time.sleep(.02)
            # execute command
            self.moveItem(splitted[1], splitted[2])
        elif splitted[0] == '!tab':
            time.sleep(.02)
            # execute command
            if(len(splitted) > 1):
                self.tabTour(splitted[1])
            else:
                self.tabTour()
        elif splitted[0] == '!random':
            time.sleep(.02)
            # execute command
            self.randomAction()
        elif splitted[0] == '!rq':
            time.sleep(.02)
            self.leaveGame()
        elif splitted[0] == '!il' or splitted[0] == '!iul' or splitted[0] == '!itemlock':
            time.sleep(.02)
            self.toggleLockItem(splitted[1])
        elif splitted[0] == '!run':
            time.sleep(.02)
            self.grabItemChickenloop(splitted[1])
        elif splitted[0] == '!stay':
            time.sleep(.02)
            self.abortRagequit()
        elif splitted[0] == '!write':
            time.sleep(.02)
            tempword = ''
            for i in range(1, len(splitted)):
                tempword += splitted[i] + ' '
            # self.writeAllChat(tempword)
        elif splitted[0] == '!stack':
            time.sleep(.02)
            self.stackCommand(splitted)
        elif splitted[0] == '!exec':
            time.sleep(.02)
            self.executeStack()
        elif (splitted[0] == '!aa'
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
        elif splitted[0] == '!search':
            time.sleep(.02)
            self.searchGame()
        elif splitted[0] == '!accept':
            time.sleep(.02)
            self.acceptGame()
        elif splitted[0] == '!calib':
            time.sleep(.02)
            self.camCalibration(True)

