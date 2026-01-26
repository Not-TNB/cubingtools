'''
Methods related to the validation of a cube state, ensuring the internal representation
of the cube state is reachable from a solved state with valid moves.
'''

from cubingtools.constants import *
from cubingtools.cube import *
from collections import Counter

def __validateShape(state: dict, n: int) -> bool:
    if set(state.keys()) != set(FACES): return False
    for face in state.values():
        if len(face) != n: return False
        if any(len(row) != n for row in face): return False
    return True

def __validateColorCounts(state: dict, n: int) -> bool:
    a = n*n
    counts = Counter([
        sticker for face in state.values()
                for row in face
                for sticker in row
    ])
    print(counts.values())
    if all(v==a for v in counts.values()) and len(counts) == 6:
        return [state[face][0][0] for face in FACES] # ordered colors
    return False

def __validateCenters(state: dict, n: int, colors: str) -> bool:
    return set(face[1][1] for face in state.values()) == set(colors)

###################################################################################################

def __validateCorners(state: dict, n: int, colors: str) -> bool:
    pass

###################################################################################################

# allows early fail
class _GuardFail(Exception): pass

def isValid(state: dict, n: int) -> bool:
    def guard(f, *args): # early exits if result is falsy
        result = f(state, n, *args)
        return result if result else _GuardFail()
    
    try:
        guard(__validateShape)
        colors = guard(__validateColorCounts)
        guard(__validateCenters, colors)
    except: return False
    else: return True

def isValidCube(cube: CubeN) -> bool:
    return isValid(cube.state, cube.size)