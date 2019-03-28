#!/usr/bin/env python3

# coordmaps.py
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


from collections import OrderedDict


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

    'chickenAbility1': {'x': '438', 'y': '690'},
    'chickenAbility5': {'x': '601', 'y': '690'},
    'shopButton': {'x': '249', 'y': '30'},

    'chickSlot1': {'x': '651', 'y': '686'},
    'chickSlot9': {'x': '739', 'y': '747'},

    'resetChicken': {'x': '514', 'y': '500'},

    'dotaArrowBtn': {'x': '22', 'y': '20'},
    'dotaDisconnectBtn': {'x': '841', 'y': '735'},
    'dotaLeaveBtn': {'x': '850', 'y': '700'},
    'dotaLeaveAcceptBtn': {'x': '456', 'y': '423'},
    'dotaPlayAutoChessBtn': {'x': '892', 'y': '351'},
    'dotaAcceptBtn': {'x': '504', 'y': '371'},
    'dotaDeclineBtn': {'x': '724', 'y': '419'},
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

    'chickenAbility1': {'x': '855', 'y': '970'},
    'chickenAbility5': {'x': '1087', 'y': '970'},
    'shopButton': {'x': '591', 'y': '37'},

    'chickSlot1': {'x': '1158', 'y': '964'},
    'chickSlot9': {'x': '1286', 'y': '1057'},

    'resetChicken': {'x': '914', 'y': '712'},

    'dotaArrowBtn': {'x': '32', 'y': '27'},
    'dotaDisconnectBtn': {'x': '1627', 'y': '1035'},
    'dotaLeaveBtn': {'x': '1648', 'y': '985'},
    'dotaLeaveAcceptBtn': {'x': '874', 'y': '603'},
    'dotaPlayAutoChessBtn': {'x': '1473', 'y': '485'},
    'dotaAcceptBtn': {'x': '901', 'y': '529'},
    'dotaDeclineBtn': {'x': '1255', 'y': '589'},
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

    'chickenAbility1': {'x': '562', 'y': '717'},
    'chickenAbility5': {'x': '734', 'y': '717'},
    'shopButton': {'x': '365', 'y': '30'},

    'chickSlot1': {'x': '785', 'y': '715'},
    'chickSlot9': {'x': '880', 'y': '780'},

    'resetChicken': {'x': '642', 'y': '508'},

    'dotaArrowBtn': {'x': '22', 'y': '20'},
    'dotaDisconnectBtn': {'x': '1103', 'y': '764'},
    'dotaLeaveBtn': {'x': '1100', 'y': '730'},
    'dotaLeaveAcceptBtn': {'x': '553', 'y': '444'},
    'dotaPlayAutoChessBtn': {'x': '1029', 'y': '362'},
    'dotaAcceptBtn': {'x': '627', 'y': '390'},
    'dotaDeclineBtn': {'x': '865', 'y': '438'},
    'dotaMainMenuBtn': {'x': '214', 'y': '24'},
    'dotaAutoChessBtn': {'x': '504', 'y': '357'},

    'playerPosFirst': {'x': '1144', 'y': '112'},
    'playerPosLast': {'x': '1144', 'y': '630'}
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
