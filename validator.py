import re

PATTERNS = {
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

def validateCommand(command):
    '''
    Validate incoming commands
    '''
    # not a command
    if(command[:1] != '!'):
        return None

    # does it match any pattern?
    for pattern in PATTERNS:
        if(re.match(PATTERNS[pattern], command, re.IGNORECASE)):
            print('found pattern for: %s' % pattern)
            return True

    return False