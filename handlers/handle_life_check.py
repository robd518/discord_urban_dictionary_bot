#!/usr/bin/python3
import re

def handle_life_check(message):
    ''' Read the discord message that would represent your character
        returning from battle, and determine if their life is below
        a certain threshold

        Returns:
            True: is below threshold
            False: isn't
    '''
    
    try:
        if int(re.search('\d{1,3}\/\d{3}', message).group(0).split('/')[0]) <= 160:
            return True
        else:
            return False
    
    except AttributeError:
        return