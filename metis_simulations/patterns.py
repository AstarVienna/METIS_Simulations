"""
A repository to hold patterns for chop-dither/nod.  The user defines
patterns with a name and a sequence of offsets. 

throw/posang (pixels, degrees) specificy offsets via the internal chopper

offset1/offset2 (pixels) specify offset by the telescope. 

TODO: check orientations. 

Code snippets to create patterns can also be included in this file. 


"""

PATTERNDICT = {}

# default for no offset
PATTERNDICT['none'] = {}
PATTERNDICT['none']['throw'] = [0]
PATTERNDICT['none']['posang'] = [0]
PATTERNDICT['none']['offset1'] = [0]
PATTERNDICT['none']['offset2'] = [0]


# a simple jitter pattern
PATTERNDICT['simpleJitter1'] = {}
PATTERNDICT['simpleJitter1']['throw'] = [0, 0.2, -0.5, 0.2, 0.5]
PATTERNDICT['simpleJitter1']['posang'] = [0, 30, 20, -20, 0]
PATTERNDICT['simpleJitter1']['offset1'] = [0, 0, 0, 0, 0]
PATTERNDICT['simpleJitter1']['offset2'] = [0, 0, 0, 0, 0]


