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

# TODO: use IO for every file write
class IOController:
    def __init__(self):
        pass
        
    def writeFile(self, filename, message):
        with open(filename, "w") as f:
            f.write(message)
        pass

    def readFile(self):
        pass


    def resetFile(self, filename = None):
        """Cleans specific file or all files"""
        if(filename):
            with open(filename, "w") as f:
                f.write("")
        else:
            with open("lastsaid.txt", "w") as f:
                f.write("")
            with open("most_common_commands.txt", "w") as f:
                f.write("")
            with open("ragequit.txt", "w") as f:
                f.write("")
            with open("commands.txt", "w") as f:
                f.write("")
