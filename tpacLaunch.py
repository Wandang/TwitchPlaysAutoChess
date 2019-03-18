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

import validator
import io
import gamecontroller

class Setup:
    mode = ''
    commands = []
    list_commands = []
    gc = gamecontroller.GameController()
    myIO = io.IO()

    def __init__(self):
        self.config()
        
    def config(self):
        print('in config')
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
            if self.mode.lower() == "democracy":
                print("Takes most said command every X second(s): ")
                self.democracy_time = float(input("(must be integer) X="))
                break
            else:
                break

        self.startMode()

    def startMode(self):
        self.myIO.resetFiles()
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
        while True:
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
                if(validator.validateCommand(out.lower())):
                    self.addToCommandList(user, out)
                    # Write to file for stream view
                    with open("commands.txt", "w") as f:
                        for item in self.commands:
                            f.write(item + '\n')
                    if(self.mode != "democracy"):
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

print('starting v2...')
setup = Setup()
setup.start()