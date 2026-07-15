"""Location for chop-nod-dither patterns

The patterns are defined in the dictionary ditherPatterns. 

Each pattern is defined by a sub-dictionary with a unique name.

A pattern consists of a set of lists, wiht one element for each position 
in the entire sequence. 

dx, dy: dither offsets from the base position.. Dither offsets are small,
        slow mirror offets used to reject sources for sky 
        background corrects and reject bad pixels. Dither size must by < 5".

cx, cy: chop offsets from the base bosition. Chop offsets are fast (20 Hz)
        mirror offsets used for background subtraction. 

nx, ny: nod offsets from the base position. not offsets are produced by moving
        the telescope. 

If a sky parameter is set in the YAML, the whole sequence is repeated
at the new position. 


For LM band, the expected sequence is 

    dither sequence

or 

    dither sequence -> sky offset -> dither sequence

for N band the expected sequence is 

    chop sequence -> nod -> chop sequence

or

    (chop sequence  -> dither) x N -> nod -> (chop sequence  -> dither) x N 


However, many things are still very TBD, so specifying the sequence
gives us enough flexibility so that we don't have to rewrite the simulations 
code when Ops decides on the observation strategy. 

The mirror offset is the sum of (dx,dy) and (cx,cy). 

The total image offset is the sum of (dx,dy), (cx,cy) and (nx,ny).

The following keywords will be set:
  SEQ


"""


ditherPatterns = {}

# a simple LM band dither sequence

simpleDither = {}


# type of offset
# d = dither
# c = chop
# n = nod
# dither and chop use the mirror, nod uses the telescope

# dither offsets in x and y relative to initial position
simpleDither['dx'] = [0,1,-3,5,-1,2]
simpleDither['dy'] = [0,-3,1,-1,2,5]

simpleDither['cx'] = [0,0,0,0,0,0]
simpleDither['cy'] = [0,0,0,0,0,0]

simpleDither['nx'] = [0,0,0,0,0,0]
simpleDither['ny'] = [0,0,0,0,0,0]

# convert to angle and throw
simpleDither['ang'] = np.atan2(simpleDither['dy']/simpleDither['dx'])
simpleDither['throw'] = np.sqrt(simpleDither['dy']**2+simpleDither['dy']**2)


ditherPatterns['simpleDither'] = simpleDither




