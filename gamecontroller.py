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
import time
import random
import math
from collections import OrderedDict
from threading import Thread

import validator
import iocontroller
import coordmaps
import peripherals


class GameController:
    """Controls the game input. Emulates mouse and keyboard input via pynput.
    Each Dota AutoChess action is mapped as function"""

    myIO = iocontroller.IOController()
    myPeripheral = peripherals.Peripherals()
    commandStack = []
    # default delay after interacting with the dota menu
    sleepBetweenMenu = 1
    dota2WindowID = ''
    allowRagequit = False
    TWITCHEMOTES = ['monkaS', '4Head', 'FailFish', 'DansGame', 'LUL', 'Kappa',
                    'NotLikeThis', 'OSFrog', 'PJSalt', 'WutFace', 'cmonBruh',
                    'TriHard', 'PogChamp', 'ResidentSleeper']

    COORDMAP = {}

    itemoffsetFirstRowX = 54
    itemoffsetFirstRowy = 31
    itemoffsetSecondRowX = 75
    itemoffsetSecondRowy = 0  # 6 old

    def __init__(self, channelName, hotkeys, resolution):
        self.channelName = channelName
        self.hotkeys = hotkeys
        self.resolution = resolution

        aR4To3 = (int(self.resolution[0])/int(self.resolution[1]) * 3/4)
        aR16To9 = (int(self.resolution[0])/int(self.resolution[1]) * 9/16)
        aR16To10 = (int(self.resolution[0])/int(self.resolution[1]) * 10/16)
        if(math.isclose(aR4To3, 1.0, rel_tol=0.05)):
            print('4:3!')
            diffResoX = int(self.resolution[0])/1024
            diffResoY = int(self.resolution[1])/768
            self.COORDMAP = coordmaps.COORDMAP_RESOLUTION_4TO3

        elif(math.isclose(aR16To9, 1.0, rel_tol=0.05)):
            print('16:9!')
            diffResoX = int(self.resolution[0])/1920
            diffResoY = int(self.resolution[1])/1080
            self.COORDMAP = coordmaps.COORDMAP_RESOLUTION_16TO9

        elif(math.isclose(aR16To10, 1.0, rel_tol=0.05)):
            print('16:10!')
            diffResoX = int(self.resolution[0])/1280
            diffResoY = int(self.resolution[1])/800
            self.COORDMAP = coordmaps.COORDMAP_RESOLUTION_16TO10

        for coord in self.COORDMAP:
            relativeXValue = float(self.COORDMAP[coord]['x']) * diffResoX
            relativeYValue = float(self.COORDMAP[coord]['y']) * diffResoY
            self.COORDMAP[coord]['x'] = str(int(relativeXValue))
            self.COORDMAP[coord]['y'] = str(int(relativeYValue))

    def searchGame(self):
        """Initiates the search for a Dota AutoChess game inside Dota."""
        # press esc to close any info windows
        # (for example due to not accepting b4)
        self.clickNothing()
        # self.pressKeyWithPynput(KeyboardKey.esc)

        # go to main menu first
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaMainMenuBtn']['x'],
            self.COORDMAP['dotaMainMenuBtn']['y'], '1')
        time.sleep(self.sleepBetweenMenu)
        # navigate to autochess
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaAutoChessBtn']['x'],
            self.COORDMAP['dotaAutoChessBtn']['y'], '1')
        time.sleep(self.sleepBetweenMenu)
        # start autochess search
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaPlayAutoChessBtn']['x'],
            self.COORDMAP['dotaPlayAutoChessBtn']['y'], '1')
        # automatically accept the first lobby to reduce user burden.
        # Estimated time after a lobby is ready
        waitForFirstLobby = 5
        time.sleep(waitForFirstLobby)
        self.acceptGame()

    def acceptGame(self):
        """Press the accept button in Dota"""
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaAcceptBtn']['x'],
            self.COORDMAP['dotaAcceptBtn']['y'], '1')

    def declineGame(self):
        """Decline a lobby (useful if lobbies keep failing)"""
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaDeclineBtn']['x'],
            self.COORDMAP['dotaDeclineBtn']['y'], '1')

    def leaveGame(self):
        """Initiates a process of leaving the current AutoChess game
        with the option to abort that process."""
        # Make sure the process is only started once
        if(self.allowRagequit):
            print('ragequit already in process')
            return
        self.allowRagequit = True
        # start counter in seperate thread
        rageQuitJob = Thread(target=self.rageQuitProcess, args=())
        rageQuitJob.start()

    def abortRagequit(self):
        """Stop quitting the current AutoChess game"""
        self.allowRagequit = False
        # clear text file for stream view
        self.myIO.resetFile("ragequit.txt")

    def rageQuitProcess(self):
        """Starts a timer of 20s to display a warning.
        After 20s the current AutoChess game will be abandoned.
        Can be stopped by writing !stay in chat"""
        # how long should the message be displayed and the quitting delayed?
        targetTime = 20
        starttime = time.time()
        while True:
            if(time.time() - starttime < targetTime):
                if(self.allowRagequit):
                    # write remaining time for chat
                    # (adding +1s because of lazy cutting of decimals)
                    self.myIO.writeFile(
                        "ragequit.txt",
                        "Time left till ragequit!: {0} \nTo abort write !stay"
                        .format(
                            str(1.0 + targetTime - (time.time() - starttime))
                            .split('.')[0]
                        ))
                    # let one second pass to prevent spam
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
            self.myPeripheral.moveMouse(
                self.COORDMAP['dotaArrowBtn']['x'],
                self.COORDMAP['dotaArrowBtn']['y'], '1')
            time.sleep(self.sleepBetweenMenu)
            # Press the dota disconnect button on the bottom right corner
            self.myPeripheral.moveMouse(
                self.COORDMAP['dotaDisconnectBtn']['x'],
                self.COORDMAP['dotaDisconnectBtn']['y'], '1')
            time.sleep(self.sleepBetweenMenu)
            # circumvent dac rating popup
            self.clickNothing()
            time.sleep(self.sleepBetweenMenu)
            # Press the dota leave button above the re/disconnect button
            # TODO: Test if this works without the workaround now
            # since we use pynput
            self.myPeripheral.moveMouse(
                self.COORDMAP['dotaLeaveBtn']['x'],
                self.COORDMAP['dotaLeaveBtn']['y'], '1')
            time.sleep(self.sleepBetweenMenu)
            # Press the dota acccept button for leaving
            # in the middle of the screen
            self.myPeripheral.moveMouse(
                self.COORDMAP['dotaLeaveAcceptBtn']['x'],
                self.COORDMAP['dotaLeaveAcceptBtn']['y'], '1')
            # clean file for stream view
            self.myIO.resetFile("ragequit.txt")

        self.allowRagequit = False

    def reconnectGame(self):
        """Reconnect game after disconnected from server"""
        self.myPeripheral.moveMouse(
            self.COORDMAP['dotaDisconnectBtn']['x'],
            self.COORDMAP['dotaDisconnectBtn']['y'], '1')

    def camCalibration(self, promote=False):
        """Needs to be done once at the start of each game!
        Sets cam to playerposition.
        This is the referenceposition for all other commands
        and therefore important!
        Without calibration every chess piece interaction will fail.

        Keyword arguments:
            promote -- Promotes the twitch channel in allchat (bool)
        """
        pass
        # self.pressKeyWithPynput('1')
        # # shoutout in allchat to promote the bot
        # if(promote):
        #     self.writeAllChat(
        #         'Chat is playing right now on https://www.twitch.tv/' +
        # self.channelName)
        # time.sleep(self.delayBetweenActions)

    def tabTour(self, playerPlacementID=-1):
        '''Show chessboard of player x or
        if no player is given show every chessboard in 5s

        Keyword arguments:
            playerPlacementID -- PlayerID defined by current placement (1-8)
        '''
        self.closeSelection()
        if(playerPlacementID != -1):
            # timeToStayOnPlayer = 3
            x, y = self.getLocationOfIntermediatePoint(
                self.COORDMAP['playerPosFirst'],
                self.COORDMAP['playerPosLast'], 7, (int(playerPlacementID)-1))
            # cheeky message to be displayed to make it feel more interactive
            # with the other players
            # allChatMessage = 'Chat wants to inspect the current position: '+
            # playerPlacementID
            # self.writeAllChat(allChatMessage)
            # clicking on the avatar of the specific player leads us to their
            # camposition
            self.myPeripheral.moveMouse(x, y, '1')
            # move mouse away from avatars so the popovertext is not blocking
            # the view
            self.clickNothing()
            # time.sleep(timeToStayOnPlayer)
            # cheeky message to be displayed to make it feel more interactive
            # with the other players
            # allChatMessage = 'Chat judgement: ' + \
            #     self.TWITCHEMOTES[random.randint(0, len(self.TWITCHEMOTES))]
            # self.writeAllChat(allChatMessage)
            # self.camCalibration()
        else:
            self.clickNothing()
            tabTourDuration = 5
            timeToLingerOnPlayer = tabTourDuration/8
            for i in range(8):
                x, y = self.getLocationOfIntermediatePoint(
                    self.COORDMAP['playerPosFirst'],
                    self.COORDMAP['playerPosLast'], 7, i)
                self.myPeripheral.moveMouse(x, y, '1')
                # move mouse away from avatars so the popovertext is not
                # blocking the view
                self.clickNothing()

                time.sleep(timeToLingerOnPlayer)

    def pickPiece(self, target):
        """Buy a chess piece from the shop.

        Keyword arguments:
            target -- Number between 1-5
        """
        self.showSelection('on')
        x, y = self.getLocationOfIntermediatePoint(
            self.COORDMAP['chickenAbility1'],
            self.COORDMAP['chickenAbility5'], 4, (int(target)-1))
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()

    def movePiece(self, source, target):
        """Moves piece from source to target location.
        Source and target locations are fields on the chessboard or on the
        bench

        Keyword arguments:
            source -- Field on the chessboard (aa,a1..h8)
            target -- Field on the chessboard (aa,a1..h8)
        """
        # make sure shop is closed while moving pieces
        self.showSelection('off')
        self.resetChickenPos()
        self.myPeripheral.moveMouse(
            self.COORDMAP['chickenAbility1']['x'],
            self.COORDMAP['chickenAbility1']['y'], '1')
        x, y = self.convertToLocation(source)
        self.myPeripheral.moveMouse(x, y, '1')

        # self.pressKeyWithPynput(self.hotkeys[0])
        x, y = self.convertToLocation(target)
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()
        # show shop after movement for comfort
        self.showSelection('on')

    def movePieceFromSlot(self, slot, direction=''):
        """Shortcut command: Moves a piece from a slot/bench
        towards a general direction.
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

    def moveBot(self):
        """Shortcut command: Moves the first piece to the backline"""
        self.resetChickenPos()
        self.myPeripheral.moveMouse(
            self.COORDMAP['chickenAbility1']['x'],
            self.COORDMAP['chickenAbility1']['y'], '1')
        x, y = self.convertToLocation('aa')
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[0])

        x, y = self.convertToLocation('e1')
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()
        self.showSelection('on')

    def moveTop(self):
        """Shortcut command: Moves the first piece to the frontline"""
        self.resetChickenPos()
        self.myPeripheral.moveMouse(
            self.COORDMAP['chickenAbility1']['x'],
            self.COORDMAP['chickenAbility1']['y'], '1')

        x, y = self.convertToLocation('aa')
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[0])
        x, y = self.convertToLocation('d4')
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()
        self.showSelection('on')

    def moveRight(self):
        """Shortcut command: Moves the first piece to the right side"""
        self.resetChickenPos()
        self.myPeripheral.moveMouse(
            self.COORDMAP['chickenAbility1']['x'],
            self.COORDMAP['chickenAbility1']['y'], '1')
        x, y = self.convertToLocation('aa')
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[0])
        x, y = self.convertToLocation('g3')
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()
        self.showSelection('on')

    def moveLeft(self):
        """Shortcut command: Moves the first piece to the left side"""
        self.resetChickenPos()
        self.myPeripheral.moveMouse(
            self.COORDMAP['chickenAbility1']['x'],
            self.COORDMAP['chickenAbility1']['y'], '1')
        x, y = self.convertToLocation('aa')
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[0])
        x, y = self.convertToLocation('b3')
        self.myPeripheral.moveMouse(x, y, '1')
        self.clickNothing()
        self.showSelection('on')

    def closeSelection(self):
        '''Closes the shop via X button in the right upper corner'''
        self.myPeripheral.moveMouse(
            self.COORDMAP['close']['x'], self.COORDMAP['close']['y'], '1')

    def showSelection(self, isOn):
        """Shows/hides the shop.

        Keyword arguments:
            isOn -- Show/hide (bool)
        """
        # Make sure to close the shop via X button before since we do not have
        # game feedback and therefore need to prevent toggling wrongly
        self.closeSelection()
        if(isOn == 'on'):
            # reopen shop in this case, otherwise keep it closed
            self.myPeripheral.moveMouse(
                self.COORDMAP['shopButton']['x'],
                self.COORDMAP['shopButton']['y'], '1')

    def lockSelection(self):
        """Locks the shop to prevent automatic rerolling"""
        # first open selection
        self.showSelection('on')
        # click on the lock icon
        self.myPeripheral.moveMouse(
            self.COORDMAP['lock']['x'], self.COORDMAP['lock']['y'], '1')

    def benchPiece(self, target):
        """Removes an active chess piece from the chessboard and puts it on the bench.

        Keyword arguments:
            target -- target chessboard position
        """
        self.showSelection('off')
        self.resetChickenPos()
        x, y = self.getLocationOfIntermediatePoint(
            self.COORDMAP['chickenAbility1'],
            self.COORDMAP['chickenAbility5'], 4, 1)
        self.myPeripheral.moveMouse(x, y, '1')
        x, y = self.convertToLocation(target)
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[1])
        self.clickNothing()
        self.showSelection('on')

    def sellPiece(self, target):
        """Sells a piece.
        Target is a field on the chessboard and on the bench

        Keyword arguments:
            target -- target chessboard position
        """
        self.showSelection('off')
        self.resetChickenPos()
        x, y = self.getLocationOfIntermediatePoint(
            self.COORDMAP['chickenAbility1'],
            self.COORDMAP['chickenAbility5'], 4, 2)
        self.myPeripheral.moveMouse(x, y, '1')
        x, y = self.convertToLocation(target)
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[2])
        self.clickNothing()
        self.showSelection('on')

    def rerollPieces(self):
        """Rerolls the shop selection."""
        self.showSelection('off')
        self.resetChickenPos()
        x, y = self.getLocationOfIntermediatePoint(
            self.COORDMAP['chickenAbility1'],
            self.COORDMAP['chickenAbility5'], 4, 3)
        self.myPeripheral.moveMouse(x, y, '1')
        # self.pressKeyWithPynput(self.hotkeys[3])
        self.clickNothing()
        self.showSelection('on')

    def buyXP(self, amount):
        """Buys experience x times depending on the amount

        Keyword arguments:
            amount -- How many times xp should be bought (1-4)
        """
        waitBetweenClicks = 0.8
        for dummy in range(int(amount)):
            self.myPeripheral.moveMouse(
                self.COORDMAP['chickenAbility5']['x'],
                self.COORDMAP['chickenAbility5']['y'], '1')
            # self.pressKeyWithPynput(self.hotkeys[4])
            time.sleep(waitBetweenClicks)
        self.clickNothing()

    def toggleLockItem(self, slot):
        """Locks item in specified itemslot (1-9)

        Keyword arguments:
            slot -- number between 1-9
        """
        # TODO: check if special delay is still needed since pynput
        waitForRightClickMenu = 0.5
        # We have 3x3 item matrix
        # after 3 and 6 the next row starts
        countingXSteps = (int(slot)-1) % 3
        # reduce slot number slightly so 1,2,3 / 3.0 casted to int becomes 0;
        # 4,5,6 become 1; and 7,8,9 become 2
        countingYSteps = int((int(slot)-1)/3)
        x, y = self.getLocationOfIntermediatePoint(
            self.COORDMAP['chickSlot1'],
            self.COORDMAP['chickSlot9'], 3, [countingXSteps, countingYSteps])
        self.myPeripheral.moveMouse(x, y, '3')
        time.sleep(waitForRightClickMenu)
        # the rightclick menu changes position depending on row
        lockLabelPosX = str(int(x)+int(self.itemoffsetFirstRowX))
        lockLabelPosY = str(int(y)+int(self.itemoffsetFirstRowy))
        if(int(slot) > 3):
            # slot is below first row
            lockLabelPosX = str(int(x)+int(self.itemoffsetSecondRowX))
            lockLabelPosY = str(int(y)+int(self.itemoffsetSecondRowy))
        self.myPeripheral.moveMouse(lockLabelPosX, lockLabelPosY, '1')

    def moveItem(self, slot, target):
        '''Move item from chicken slot to target hero coordinates.

        Keyword arguments:
            slot -- Itemslot of the chicken (1-9)
            target -- target chessboard/bench position
        '''
        # close shop before
        self.showSelection('off')
        distanceX = int(self.COORDMAP['chickSlot9']['x']) - \
            int(self.COORDMAP['chickSlot1']['x'])
        distanceY = int(self.COORDMAP['chickSlot9']['y']) - \
            int(self.COORDMAP['chickSlot1']['y'])
        # We have 3x3 item matrix
        distanceToEachCenterX = distanceX / 3
        distanceToEachCenterY = distanceY / 3
        # after 3 and 6 the next row starts
        newXCoord = int(self.COORDMAP['chickSlot1']['x']) + \
            ((int(slot)-1) % 3) * distanceToEachCenterX
        # reduce slot number slightly so 1,2,3 / 3.0 casted to int becomes 0;
        # 4,5,6 become 1; and 7,8,9 become 2
        newYCoord = int(self.COORDMAP['chickSlot1']['y']) + \
            int((int(slot)-1)/3.0) * distanceToEachCenterY
        self.dragAndDrop({'x': newXCoord, 'y': newYCoord}, target)
        # give chicken time to run to the destination
        # TODO: dynamic time depending on target location
        waitForChickenDelivery = 5
        time.sleep(waitForChickenDelivery)
        self.resetChickenPos()

    def grabItem(self, target):
        """Let's the chicken pick up dropped items

        Keyword arguments:
            target -- target chessboard position
        """
        # close shop first
        self.showSelection('off')
        x, y = self.convertToLocation(target)
        self.myPeripheral.moveMouse(x, y, '3')
        # TODO: dynamic time depending on target location
        waitForChickenDelivery = 5
        time.sleep(waitForChickenDelivery)
        self.resetChickenPos()

    def executeStack(self):
        """Executes a stack/queue of commands sequentially."""
        for command in self.commandStack:
            self.findAndExecute(command)
        # clear command stack afterwards
        self.commandStack = []

    def addToStack(self, commandForStack):
        """Add a command to stack/queue for later execution

        Keyword arguments:
            commandForStack -- Command as string
        """
        # TODO: set a limit on stack?
        self.commandStack.append(commandForStack)

    def stackCommand(self, commandForStack):
        """Add a command to stack/queue for later execution

        Keyword arguments:
            commandForStack -- Command as string
        """
        # remove '!stack ' beforehand
        idxSpace = commandForStack.find(' ')
        patchedCommand = commandForStack[idxSpace+1:]
        # check the nested command
        if validator.validateCommand(patchedCommand):
            # valid, add to stack
            self.addToStack(patchedCommand)

    # TODO: optimize, reduce redundancy
    def grabItemChickenloop(self, side):
        """Let's the chicken/courier walk alongside a side of the chessboard
        to pick up items.

        Keyword arguments:
            side -- Which side should be checked for items.
            Can be left, top, bot or right.
        """
        # make sure the shop is hidden to not interfere with our clicks
        self.showSelection('off')
        # give chicken time to reach starting pos
        timeToReachStartPos = 3
        if(side == 'left'):
            # pos chicken at A1 first
            x, y = self.convertToLocation('a1')
            self.myPeripheral.moveMouse(x, y, '3')
            time.sleep(timeToReachStartPos)
            for coord in coordmaps.CHICKENLEFT:
                self.myPeripheral.moveMouse(
                    coordmaps.CHICKENLEFT[coord]['x'],
                    coordmaps.CHICKENLEFT[coord]['y'], '3')
        elif(side == 'top'):
            # pos chicken at A8 first
            x, y = self.convertToLocation('a8')
            self.myPeripheral.moveMouse(x, y)
            time.sleep(timeToReachStartPos)
            for coord in coordmaps.CHICKENTOP:
                self.myPeripheral.moveMouse(
                    coordmaps.CHICKENTOP[coord]['x'],
                    coordmaps.CHICKENTOP[coord]['y'])
        elif(side == 'right'):
            # pos chicken at H8 first
            x, y = self.convertToLocation('h8')
            self.myPeripheral.moveMouse(x, y)
            time.sleep(timeToReachStartPos)
            for coord in coordmaps.CHICKENRIGHT:
                self.myPeripheral.moveMouse(
                    coordmaps.CHICKENRIGHT[coord]['x'],
                    coordmaps.CHICKENRIGHT[coord]['y'])
        elif(side == 'bot'):
            # pos chicken at H1 first
            x, y = self.convertToLocation('h1')
            self.myPeripheral.moveMouse(x, y)
            time.sleep(timeToReachStartPos)
            for coord in coordmaps.CHICKENBOT:
                self.myPeripheral.moveMouse(
                    coordmaps.CHICKENBOT[coord]['x'],
                    coordmaps.CHICKENBOT[coord]['y'])

        # send chicken back to default position
        self.resetChickenPos()

    def resetChickenPos(self):
        """Sends chicken back to default position"""
        self.myPeripheral.moveMouse(
            self.COORDMAP['resetChicken']['x'],
            self.COORDMAP['resetChicken']['y'], '3')

    def testAllFields(self):
        """Testfunction that will move the mouse to every field"""
        # give time to switch to dota/focus dota window
        waitForAltTab = 5
        durationLingerOnOneField = 0.1
        time.sleep(waitForAltTab)
        startOffset = ord('a')
        for i in range(1, 9):
            for j in range(8):
                tempChar = str(chr(startOffset + j))
                x, y = self.convertToLocation(tempChar+str(i))
                self.myPeripheral.moveMouse(x, y)
                time.sleep(durationLingerOnOneField)

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
            x, y = self.getLocationOfIntermediatePoint(
                self.COORDMAP['hh'], self.COORDMAP['aa'], 7, diffNr)
        else:
            x, y = self.getLocationOfIntermediatePoint(
                self.COORDMAP['h'+secondChar],
                self.COORDMAP['a'+secondChar], 7, diffNr)
        return x, y

    def dragAndDrop(self, source, target):
        """Drags & drops from source to target location.
        This is used for items.

        Keyword arguments:
            source -- coordinates of source item location [x,y]
            target -- Field name ('aa','a1'..'h8')
        """
        # TODO: check if dragExtraWaitTime is even needed anymore since we
        # switched to pynput
        dragExtraWaitTime = 1
        self.myPeripheral.moveMouse(source['x'], source['y'])
        time.sleep(dragExtraWaitTime)
        # hold mouse button
        self.myPeripheral.holdMouse('1')
        time.sleep(dragExtraWaitTime)
        x, y = self.convertToLocation(target)
        self.myPeripheral.moveMouse(x, y)
        time.sleep(dragExtraWaitTime)
        # release mouse button
        self.myPeripheral.releaseMouse('1')

    # def pressKeyWithPynput(self, key):
    #     """Presses specified key on keyboard with pykeyboard module

    #     Keyword arguments:
    #         key -- keyboard key (keycodes)
    #     """
    #     print('trying to press key: ',key)
    #     self.keyboard.press(key)
    #     self.keyboard.release(key)

    # TODO: add profanity filter to prevent possible repercussions through
    # twitch/ possible violation of TOS?
    # def writeAllChat(self, message):
    #     """Writes a message to everyone

    #     Keyword arguments:
    #         message -- Textmessage to be send
    #     """
    #     print('trying to hold shift...')
    #     with self.keyboard.pressed(KeyboardKey.shift):
    #          print('shift held')
    #          self.pressKeyWithPynput(KeyboardKey.enter)

    #     time.sleep(self.delayBetweenActions)
    #     print('typing message')
    #     self.keyboard.type(message)
    #     time.sleep(0.5)
    #     self.pressKeyWithPynput(KeyboardKey.enter)
    #     time.sleep(self.delayBetweenActions)

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

    def clickNothing(self):
        '''Click on the right side of the chessboard where nothing is to interact with.
        Can be used to click empty space as well for resetting commandchain
        (autochess bug)'''
        self.myPeripheral.moveMouse(
            self.COORDMAP['nothing']['x'], self.COORDMAP['nothing']['y'], '1')

    def getLocationOfIntermediatePoint(self, pointA, pointB, intervals, idx):
        aX = int(pointA.x)
        aY = int(pointA.Y)
        bX = int(pointB.x)
        bY = int(pointB.Y)
        diffDistanceX = aX - bX
        diffDistanceY = aY - bY
        distanceBetweenEachPointX = diffDistanceX/intervals
        distanceBetweenEachPointY = diffDistanceY/intervals

        if(len(idx) == 1):
            newCoordX = aX - idx[0] * distanceBetweenEachPointX
            newCoordY = aY - idx[0] * distanceBetweenEachPointY
        else:
            newCoordX = aX - idx[0] * distanceBetweenEachPointX
            newCoordY = aY - idx[1] * distanceBetweenEachPointY

        return newCoordX, newCoordY

    def findAndExecute(self, command):
        """Checks which command is invoked and executes the command accordingly

        Keyword arguments:
            command -- commandstring to execute
        """
        splitted = command.split(' ')
        if validator.validateCommand(command) == "move":
            if(len(splitted) > 2):
                self.movePiece(splitted[1], splitted[2])
            else:
                self.movePieceDirection(splitted[1])
        elif validator.validateCommand(command) == 'bench':
            self.benchPiece(splitted[1])
        elif validator.validateCommand(command) == 'sell':
            self.sellPiece(splitted[1])
        elif validator.validateCommand(command) == 'reroll':
            self.rerollPieces()
        elif validator.validateCommand(command) == 'buyxp':
            self.buyXP(splitted[1])
        elif validator.validateCommand(command) == 'shop':
            self.showSelection(splitted[1])
        elif validator.validateCommand(command) == 'pick':
            self.pickPiece(splitted[1])
        elif validator.validateCommand(command) == 'lock':
            self.lockSelection()
        elif validator.validateCommand(command) == 'grab':
            self.grabItem(splitted[1])
        elif validator.validateCommand(command) == 'itemtohero':
            self.moveItem(splitted[1], splitted[2])
        elif validator.validateCommand(command) == 'tab':
            if(len(splitted) > 1):
                self.tabTour(splitted[1])
            else:
                self.tabTour()
        elif validator.validateCommand(command) == 'random':
            self.randomAction()
        elif validator.validateCommand(command) == 'rq':
            self.leaveGame()
        elif validator.validateCommand(command) == 'lockitem':
            self.toggleLockItem(splitted[1])
        elif validator.validateCommand(command) == 'run':
            self.grabItemChickenloop(splitted[1])
        elif validator.validateCommand(command) == 'stay':
            self.abortRagequit()
        elif validator.validateCommand(command) == 'write':
            tempword = ''
            for i in range(1, len(splitted)):
                tempword += splitted[i] + ' '
            # self.writeAllChat(tempword)
        elif validator.validateCommand(command) == 'stack':
            self.stackCommand(command)
        elif validator.validateCommand(command) == 'exec':
            self.executeStack()
        elif validator.validateCommand(command) == 'movefromslots':
            if len(splitted) > 1:
                self.movePieceFromSlot(splitted[0][1:], splitted[1])
            else:
                self.movePieceFromSlot(splitted[0][1:], 'd3')
        elif validator.validateCommand(command) == 'search':
            self.searchGame()
        elif validator.validateCommand(command) == 'accept':
            self.acceptGame()
        elif validator.validateCommand(command) == 'calib':
            self.camCalibration(True)
        elif validator.validateCommand(command) == 'reconnect':
            self.reconnectGame()
        elif validator.validateCommand(command) == 'decline':
            self.declineGame()
