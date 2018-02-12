import json
import re

def parse_baxter(reading):
    """
    Parse a Baxter string and render it with all its contents, namely
    initial, medial, final, and tone.
    """

    initial = ''
    medial = ''
    final = ''
    tone = ''
    
    # determine environments
    inienv = True
    medienv = False
    finenv = False
    tonenv = False

    inichars = "pbmrtdnkgnsyhzl'x"
    

    chars = list(reading)
    for char in chars:
        
        # switch environments
        if char in 'jw' and not finenv:
            inienv,medienv,finenv,tonenv = False,True,False,False
        elif char not in inichars or finenv:
            if char in 'XH':
                inienv,medienv,finenv,tonenv = False,False,False,True
            else:
                inienv,medienv,finenv,tonenv = False,False,True,False
        
        # fill in slots
        if inienv:
            initial += char
            
        if medienv:
            medial += char

        if finenv:
            final += char

        if tonenv:
            tone += char

    # post-parse tone
    if not tone and final[-1] in 'ptk':
        tone = 'R'
    elif not tone:
        tone = 'P'

    # post-parse medial
    if 'j' not in medial and 'y' in initial:
        medial += 'j'

    # post-parse labial
    if final[0] in 'u' and 'w' not in medial:
        medial = 'w' + medial

    return initial,medial,final,tone

