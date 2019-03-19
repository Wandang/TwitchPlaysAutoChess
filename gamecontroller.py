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

    COORDMAP = {
        'a1': {'x': '633', 'y': '620'},
        'a2': {'x': '651', 'y': '548'},
        'a3': {'x': '669', 'y': '471'},
        'a4': {'x': '683', 'y': '402'},
        'a5': {'x': '695', 'y': '346'},
        'a6': {'x': '708', 'y': '293'},
        'a7': {'x': '715', 'y': '240'},
        'a8': {'x': '727', 'y': '194'},
        'b1': {'x': '734', 'y': '624'},
        'b2': {'x': '744', 'y': '545'},
        'b3': {'x': '750', 'y': '472'},
        'b4': {'x': '761', 'y': '408'},
        'b5': {'x': '769', 'y': '347'},
        'b6': {'x': '778', 'y': '292'},
        'b7': {'x': '783', 'y': '241'},
        'b8': {'x': '793', 'y': '195'},
        'c1': {'x': '824', 'y': '625'},
        'c2': {'x': '831', 'y': '542'},
        'c3': {'x': '835', 'y': '475'},
        'c4': {'x': '842', 'y': '409'},
        'c5': {'x': '846', 'y': '348'},
        'c6': {'x': '853', 'y': '290'},
        'c7': {'x': '856', 'y': '240'},
        'c8': {'x': '862', 'y': '192'},
        'd1': {'x': '913', 'y': '621'},
        'd2': {'x': '917', 'y': '542'},
        'd3': {'x': '919', 'y': '473'},
        'd4': {'x': '920', 'y': '405'},
        'd5': {'x': '923', 'y': '346'},
        'd6': {'x': '926', 'y': '289'},
        'd7': {'x': '928', 'y': '238'},
        'd8': {'x': '927', 'y': '189'},
        'e1': {'x': '1006', 'y': '621'},
        'e2': {'x': '1004', 'y': '546'},
        'e3': {'x': '1000', 'y': '476'},
        'e4': {'x': '999', 'y': '409'},
        'e5': {'x': '998', 'y': '346'},
        'e6': {'x': '996', 'y': '288'},
        'e7': {'x': '994', 'y': '240'},
        'e8': {'x': '994', 'y': '188'},
        'f1': {'x': '1098', 'y': '621'},
        'f2': {'x': '1091', 'y': '541'},
        'f3': {'x': '1084', 'y': '471'},
        'f4': {'x': '1081', 'y': '404'},
        'f5': {'x': '1072', 'y': '342'},
        'f6': {'x': '1069', 'y': '288'},
        'f7': {'x': '1066', 'y': '238'},
        'f8': {'x': '1061', 'y': '192'},
        'g1': {'x': '1193', 'y': '620'},
        'g2': {'x': '1180', 'y': '543'},
        'g3': {'x': '1167', 'y': '469'},
        'g4': {'x': '1159', 'y': '405'},
        'g5': {'x': '1149', 'y': '344'},
        'g6': {'x': '1142', 'y': '293'},
        'g7': {'x': '1137', 'y': '241'},
        'g8': {'x': '1134', 'y': '191'},
        'h1': {'x': '1278', 'y': '619'},
        'h2': {'x': '1265', 'y': '539'},
        'h3': {'x': '1248', 'y': '468'},
        'h4': {'x': '1235', 'y': '405'},
        'h5': {'x': '1227', 'y': '346'},
        'h6': {'x': '1213', 'y': '290'},
        'h7': {'x': '1204', 'y': '241'},
        'h8': {'x': '1195', 'y': '194'},

        'aa': {'x': '592', 'y': '807'},
        'bb': {'x': '699', 'y': '809'},
        'cc': {'x': '804', 'y': '809'},
        'dd': {'x': '908', 'y': '808'},
        'ee': {'x': '1014', 'y': '807'},
        'ff': {'x': '1115', 'y': '809'},
        'gg': {'x': '1224', 'y': '805'},
        'hh': {'x': '1329', 'y': '806'},

        'pick1': {'x': '464', 'y': '276'},
        'pick2': {'x': '712', 'y': '257'},
        'pick3': {'x': '973', 'y': '265'},
        'pick4': {'x': '1220', 'y': '271'},
        'pick5': {'x': '1458', 'y': '256'},
        'lock': {'x': '313', 'y': '445'},
        'close': {'x': '1610', 'y': '344'},
        'nothing': {'x': '1547', 'y': '77'},

        'chickSlot1': {'x': '1158', 'y': '964'},
        'chickSlot2': {'x': '1224', 'y': '964'},
        'chickSlot3': {'x': '1288', 'y': '965'},
        'chickSlot4': {'x': '1158', 'y': '1012'},
        'chickSlot5': {'x': '1223', 'y': '1010'},
        'chickSlot6': {'x': '1286', 'y': '1010'},
        'chickSlot7': {'x': '1159', 'y': '1057'},
        'chickSlot8': {'x': '1223', 'y': '1057'},
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

        'playerPos1': {'x': '1737', 'y': '155'},
        'playerPos2': {'x': '1737', 'y': '255'},
        'playerPos3': {'x': '1737', 'y': '355'},
        'playerPos4': {'x': '1737', 'y': '455'},
        'playerPos5': {'x': '1737', 'y': '555'},
        'playerPos6': {'x': '1737', 'y': '655'},
        'playerPos7': {'x': '1737', 'y': '755'},
        'playerPos8': {'x': '1737', 'y': '855'}
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
        for coord in self.COORDMAP:
            relativeXValue = float(self.COORDMAP[coord]['x'])/1920 * int(self.resolution[0])
            relativeYValue = float(self.COORDMAP[coord]['y'])/1080 * int(self.resolution[1])
            self.COORDMAP[coord]['x'] = str(int(relativeXValue))
            self.COORDMAP[coord]['y'] = str(int(relativeYValue))

    def moveMouse(self,x,y,clickType = None):
        """Move the mouse to the desired coordinates and optionally click at that location.
        
        Keyword arguments:
            x -- x coordinate inside screen resolution
            y -- y coordinate inside screen resolution
            clickType -- 1: leftclick, 2: middleclick, 3: rightclick
        """
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
            source -- coordinates of source location [x,y]
            target -- coordinates of target location [x,y]
        """
        self.moveMouse(source['x'],source['y'])
        time.sleep(1)
        # hold mouse button
        if(self.isXDOTOOL):
            subprocess.run(['xdotool', 'mousedown', '--window', self.dota2WindowID, '1'])
        else:
            self.mouse.press(MouseButton.left)
        time.sleep(0.5)
        self.moveMouse(target['x'],target['y'])
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

    def pressKeyWithPynput(self, key):
        """Presses specified key on keyboard with pykeyboard module
        
        Keyword arguments:
            key -- keyboard key (keycodes)
        """        
        self.keyboard.press(key)
        self.keyboard.release(key)

    def toggleLockItem(self, slot):
        """Locks item in specified itemslot (1-9)
        
        Keyword arguments:
            slot -- number between 1-9
        """
        slotID = 'chickSlot'+slot
        self.moveMouse(self.COORDMAP[slotID]['x'],self.COORDMAP[slotID]['y'],'3')
        time.sleep(0.5)
        # the rightclick menu changes position depending on row
        lockLabelPosX = str(int(self.COORDMAP[slotID]['x'])+int(self.itemoffsetFirstRowX))
        lockLabelPosY = str(int(self.COORDMAP[slotID]['y'])+int(self.itemoffsetFirstRowy))
        if(int(slot) > 3):
            # slot is below first row
            lockLabelPosX = str(int(self.COORDMAP[slotID]['x'])+int(self.itemoffsetSecondRowX))
            lockLabelPosY = str(int(self.COORDMAP[slotID]['y'])+int(self.itemoffsetSecondRowy))
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
            self.rightClickAtCoord(self.COORDMAP['a1'])
            time.sleep(3)
            for coord in self.CHICKENLEFT:
                self.rightClickAtCoord(self.CHICKENLEFT[coord])
                time.sleep(0.3)
        elif(side == 'top'):
            # pos chicken at A8 first
            self.rightClickAtCoord(self.COORDMAP['a8'])
            time.sleep(3)
            for coord in self.CHICKENTOP:
                self.rightClickAtCoord(self.CHICKENTOP[coord])
                time.sleep(0.3)
        elif(side == 'right'):
            # pos chicken at H8 first
            self.rightClickAtCoord(self.COORDMAP['h8'])
            time.sleep(3)
            for coord in self.CHICKENRIGHT:
                self.rightClickAtCoord(self.CHICKENRIGHT[coord])
                time.sleep(0.3)
        elif(side == 'bot'):
            # pos chicken at H1 first
            self.rightClickAtCoord(self.COORDMAP['h1'])
            time.sleep(3)
            for coord in self.CHICKENBOT:
                self.rightClickAtCoord(self.CHICKENBOT[coord])
                time.sleep(0.3)
        
        # send chicken back to default position
        self.resetChickenPos()


    def rightClickAtCoord(self, coord):
        """Rightclick at target coordinates
        
        Keyword arguments:
            coord -- target coordinates (in pixel) for rightclicking 
        """
        self.moveMouse(coord['x'],coord['y'],'3')
        time.sleep(self.delayBetweenActions)


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
        slotID = 'chickSlot'+slot
        self.dragAndDrop(self.COORDMAP[slotID],self.COORDMAP[target])
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
        self.rightClickAtCoord(self.COORDMAP[target])
        # TODO: dynamic time depending on target location
        time.sleep(5)
        self.resetChickenPos()


    def tabTour(self, playerPlacementID=-1):
        '''Show chessboard of player x or if no player is given show every chessboard in 5s
        
        Keyword arguments:
            playerPlacementID -- PlayerID defined by current placement (1-8)
        '''
        if(playerPlacementID != -1):
            timeToStayOnPlayer = 3
            placementKey = 'playerPos'+playerPlacementID
            # cheeky message to be displayed to make it feel more interactive with the other players
            allChatMessage = 'Chat wants to inspect the current position: '+playerPlacementID
            self.writeAllChat(allChatMessage)
            # clicking on the avatar of the specific player leads us to their camposition
            self.moveMouse(self.COORDMAP[placementKey]['x'],self.COORDMAP[placementKey]['y'], '1')
            time.sleep(self.delayBetweenActions)
            # move mouse away from avatars so the popovertext is not blocking the view
            self.clickNothing()
            time.sleep(timeToStayOnPlayer)
            # cheeky message to be displayed to make it feel more interactive with the other players
            allChatMessage = 'Chat judgement: ' + \
                self.TWITCHEMOTES[random.randint(0, len(self.TWITCHEMOTES))]
            self.writeAllChat(allChatMessage)
            self.camCalibration()
        else:
            self.clickNothing()
            time.sleep(self.delayBetweenActions)
            for dummy in range(8):
                if(self.isXDOTOOL):
                    self.pressKey('Tab')
                else:
                    self.pressKeyWithPynput(KeyboardKey.tab)

                time.sleep(0.625)


    # TODO: add profanity filter to prevent possible repercussions through twitch/ possible violation of TOS?
    def writeAllChat(self, message):
        """Writes a message to everyone
        
        Keyword arguments:
            message -- Textmessage to be send
        """
        if(self.isXDOTOOL):
            self.pressKey('shift+Return')
        else:
            with self.keyboard.pressed(KeyboardKey.shift):
                self.pressKeyWithPynput(KeyboardKey.enter)

        time.sleep(self.delayBetweenActions)
        if(self.isXDOTOOL):
            subprocess.run(['xdotool', 'type', '--window', self.dota2WindowID, message])
        else:
            self.keyboard.type(message)
        time.sleep(0.5)
        if (self.isXDOTOOL):
            self.pressKey('Return')
        else:
            self.pressKeyWithPynput(KeyboardKey.enter)
        time.sleep(self.delayBetweenActions)

    # TODO: promotelink should be read from settings file
    def camCalibration(self, promote=False):
        """Needs to be done once at the start of each game!
        Sets cam to playerposition.
        This is the referenceposition for all other commands and therefore important!
        Without calibration every chess piece interaction will fail.
        
        Keyword arguments:
            promote -- Promotes the twitch channel in allchat (bool)
        """
        if (self.isXDOTOOL):
            self.pressKey('1')
        else:
            self.pressKeyWithPynput('1')
        # shoutout in allchat to promote the bot
        if(promote):
            self.writeAllChat(
                'Chat is playing right now on https://www.twitch.tv/' + self.channelName)
        time.sleep(self.delayBetweenActions)


    def acceptGame(self):
        """Press the accept button in Dota"""
        self.moveMouse(self.COORDMAP['dotaAcceptBtn']['x'],self.COORDMAP['dotaAcceptBtn']['y'], '1')

    def searchGame(self):
        """Initiates the search for a Dota AutoChess game inside Dota."""
        # press esc to close any info windows (for example due to not accepting b4)
        if (self.isXDOTOOL):
            self.pressKey('Escape')
        else:
            self.pressKeyWithPynput(KeyboardKey.esc)
        
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
        pickString = 'pick'+str(target)
        self.moveMouse(self.COORDMAP[pickString]['x'],self.COORDMAP[pickString]['y'], '1')
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
                self.pressKeyWithPynput(KeyboardKey.space)
        time.sleep(self.delayBetweenActions)

    def lockSelection(self):
        """Locks the shop to prevent automatic rerolling"""
        # first open selection
        self.showSelection('on')
        # click on the lock icon
        self.moveMouse(self.COORDMAP['lock']['x'],self.COORDMAP['lock']['y'],'1')

    def moveBot(self):
        """Shortcut command: Moves the first piece to the backline"""
        self.moveMouse(self.COORDMAP['aa']['x'],self.COORDMAP['aa']['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[0])
        else:
            self.pressKeyWithPynput(self.hotkeys[0])

        time.sleep(self.delayBetweenActions)
        self.moveMouse(self.COORDMAP['e1']['x'],self.COORDMAP['e1']['y'])
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveTop(self):
        """Shortcut command: Moves the first piece to the frontline"""
        self.moveMouse(self.COORDMAP['aa']['x'],self.COORDMAP['aa']['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[0])
        else:
            self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        self.moveMouse(self.COORDMAP['d4']['x'],self.COORDMAP['d4']['y'])
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveRight(self):
        """Shortcut command: Moves the first piece to the right side"""
        self.moveMouse(self.COORDMAP['aa']['x'],self.COORDMAP['aa']['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[0])
        else:
            self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        self.moveMouse(self.COORDMAP['g3']['x'],self.COORDMAP['g3']['y'])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')


    def moveLeft(self):
        """Shortcut command: Moves the first piece to the left side"""
        self.moveMouse(self.COORDMAP['aa']['x'],self.COORDMAP['aa']['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[0])
        else:
            self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        self.moveMouse(self.COORDMAP['b3']['x'],self.COORDMAP['b3']['y'])
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
            direction -- Direction can be left, right, top or bot
        """
        # make sure shop is closed while moving pieces
        self.showSelection('off')
        self.moveMouse(self.COORDMAP[source]['x'],self.COORDMAP[source]['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[0])
        else:
            self.pressKeyWithPynput(self.hotkeys[0])
        time.sleep(self.delayBetweenActions)
        self.moveMouse(self.COORDMAP[target]['x'],self.COORDMAP[target]['y'],'1')
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
        # TODO: Check if click should not be done because of quickcast
        self.moveMouse(self.COORDMAP[target]['x'],self.COORDMAP[target]['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[1])
        else:
            self.pressKeyWithPynput(self.hotkeys[1])
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
        self.moveMouse(self.COORDMAP[target]['x'],self.COORDMAP[target]['y'])
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[2])
        else:
            self.pressKeyWithPynput(self.hotkeys[2])
        time.sleep(self.delayBetweenActions)
        self.clickNothing()
        time.sleep(self.delayBetweenActions)
        self.showSelection('on')

    def rerollPieces(self):
        """Rerolls the shop selection."""
        self.showSelection('off')
        if (self.isXDOTOOL):
            self.pressKey(self.hotkeys[3])
        else:
            self.pressKeyWithPynput(self.hotkeys[3])
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
            if (self.isXDOTOOL):
                self.pressKey(self.hotkeys[4])
            else:
                self.pressKeyWithPynput(self.hotkeys[4])
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
            self.writeAllChat(tempword)
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

