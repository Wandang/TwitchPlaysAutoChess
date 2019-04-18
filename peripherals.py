#!/usr/bin/env python3
# peripherals.py
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

import time
from enum import Enum

from pynput.mouse import Button as MouseButton
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key as KeyboardKey
from pynput.keyboard import Controller as KeyboardController


class Peripherals:

    mouse = MouseController()
    mouseButtons = [MouseButton.left, MouseButton.middle, MouseButton.right]
    keyboard = KeyboardController()
    # default delay after each peripheral action. Needs to be > 0 to make sure
    # that the actions are finished properly
    sleepAfterMouseMove = 0.3

    def moveMouse(self, x, y, clickType=None):
        """Move the mouse to the desired coordinates and optionally click at
        that location.

        Keyword arguments:
            x -- x coordinate inside screen resolution
            y -- y coordinate inside screen resolution
            clickType -- 1: leftclick, 2: middleclick, 3: rightclick
        """
        # print('trying to click: ' + clickType)
        self.mouse.position = (int(x), int(y))
        if(clickType):
            self.clickMouse(clickType)
        time.sleep(self.sleepAfterMouseMove)

    def clickMouse(self, clickType):
        """Clicks the specified mousebutton

        Keyword arguments:
            clickType -- 1: leftclick, 2: middleclick, 3: rightclick
        """
        self.mouse.click(self.mouseButtons[int(clickType)-1])

    def holdMouse(self, clickType):
        self.mouse.press(self.mouseButtons[int(clickType)-1])

    def releaseMouse(self, clickType):
        self.mouse.release(self.mouseButtons[int(clickType)-1])
