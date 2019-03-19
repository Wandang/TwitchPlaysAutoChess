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
import time
import socket
from threading import Thread

import validator
import iocontroller
import gamecontroller

# TODO: split setup/configuration from controller flow
class Setup:
    """
    Configures program and controls flow
    """
    mode = ''
    commands = []
    list_commands = []
    myIO = iocontroller.IOController()

    def __init__(self):
        self.config()
        
    def config(self):
        """Generates a config file if it does not exist"""
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

                allSettings = ''
                for each_setting in settings:
                    allSettings += each_setting + '\n'
                self.myIO.writeFile("settings.txt",allSettings)

        self.gc = gamecontroller.GameController(self.CHAT_CHANNEL)
        self.configDynamicSettings()

    def configDynamicSettings(self):
        """Checks if Dota is running to get dota window ID.
        Select game type (Democracy/Anarchy)"""
        while True:
            # TODO: get window ID cross platform style (maybe with pynput)
            # while self.gc.dota2WindowID == '':
            #     input("Dota already running? Then press enter")
            #     completedProcess = subprocess.run(['xdotool', 'search', '--name',
            #                                     'Dota 2'], capture_output=True)
            #     self.gc.dota2WindowID = completedProcess.stdout.decode('UTF-8')
            print("Currently available: Democracy, Anarchy\n"+
                "Democracy: Takes most said command every X second(s)\nAnarchy: Executes every incoming command")
            self.mode = input("Game type (default Anarchy): ")
            if self.mode.lower() == "democracy":
                print("Takes most said command every X second(s): ")
                try:
                    self.democracy_time = float(input("(must be integer) X="))
                    if(self.democracy_time > 0):
                        break
                except ValueError as identifier:
                    print(identifier)
            else:
                break

    def start(self):
        """Starts the main program flow
        Empties the text files for streaming (OBS)
        Creates parallel threads for democracy if needed
        Initiates connection to twitch"""
        self.myIO.resetFile()
        # Democracy Game Mode?
        if self.mode.lower() == "democracy":
            
            count_job = Thread(target=self.democracy, args=())
            count_job.start()

        time.sleep(1)
        twitchSocket = self.connectToTwitch()
        self.handleTwitchResponse(twitchSocket)

    def democracy(self):
        """Runs in parallel thread and counts the most popular commands for a few seconds.
        After that the most popular command is executed"""
        list_commands = []
        last_command = time.time()
        selected_c = "None"

        while True:
            if time.time() > last_command + self.democracy_time:
                # Time has run out since last command
                last_command = time.time()
                if(len(list_commands) > 0):
                    # Select the most popular command
                    selected_c = self.most_common(list_commands)
                else:
                    selected_c = 'None'
                self.myIO.writeFile("lastsaid.txt","Selected {0}\nTime left: {1}".format(selected_c,str(self.democracy_time)[0:1]))
                list_commands = []
                if(selected_c != 'None'):
                    # Do nothing if chat didn't write any commands
                    splitted = selected_c.lower().split(' ')
                    self.gc.findAndExecute(splitted)
            else:
                self.myIO.writeFile("lastsaid.txt","Selected {0}\nTime left: {1}".format(selected_c ,str(
                        1.0 + last_command + self.democracy_time - time.time())[0:1]))
            time.sleep(1)

    def connectToTwitch(self):
        """Connects to twitch by using a socket, host, port and user credentials"""
        s = socket.socket()
        s.connect((self.HOST, self.PORT))

        s.send(bytes("PASS {0}\r\n".format(self.AUTH), "UTF-8"))
        s.send(bytes("NICK {0}\r\n".format(self.NICK), "UTF-8"))
        s.send(bytes("USER {0} {1} bla :{2}\r\n".format(self.NICK, self.HOST, self.NICK), "UTF-8"))
        s.send(bytes("JOIN #{0}\r\n".format(self.CHAT_CHANNEL), "UTF-8"))
        s.send(bytes("PRIVMSG #{0} :Connected\r\n".format(self.CHAT_CHANNEL), "UTF-8"))
        print("Sent connected message to channel {0}".format(self.CHAT_CHANNEL))
        return s
    
    def handleTwitchResponse(self, s):
        """Extracts the relevant info/command from each chat line

        Keyword arguments:
            s -- socket containing live data
        """
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

                # remove username and : in front of each line 
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
                elif user == ":{0}.tmi.twitch.tv: ".format(self.NICK):
                    pass
                else:
                    try:
                        print(user + out)
                    except UnicodeEncodeError:
                        print(user)
                
                # Take in output
                # sanitize output
                if(validator.validateCommand(out.lower())):
                    self.addToCommandList(user, out)
                    # Write to file for stream view
                    items = ''
                    for item in self.commands:
                            items += item + '\n'
                    self.myIO.writeFile('commands.txt',items)
                    if(self.mode != "democracy"):
                        splitted = out.lower().split(' ')
                        self.gc.findAndExecute(splitted)

    def addToCommandList(self, user, out):
        """Adds all valid commands to a list and removes/pops the first entry if the list gets too long.
        Additionally adds commands to a democracy list which is used to determine the top 5 commands

        Keyword arguments:
            user -- twitch username as send by twitch api
            out -- chatline from user
        """
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
        """Return the most common/popular command of a given list.
        At the same time determine the Top 5 commands to show stream view by writing it to a file
        
        Keyword arguments:
            lst -- list of commands to be examined
        """
        # Write to file for stream view
        tempList = lst
        maxList = []
        if(len(lst) > 5):
            # if more than 5 commands are found, only get the top5
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

        topCommands = 'Top commands:\n'
        for item in maxList:
            topCommands += item + '\n'
        self.myIO.writeFile("most_common_commands.txt", topCommands)
        return maxList[0]

print('starting v2...')
if __name__ == "__main__":
    setup = Setup()
    setup.start()