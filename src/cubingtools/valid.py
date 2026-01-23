'''
Methods related to the validation of a cube state, ensuring the internal representation
of the cube state is reachable from a solved state with valid moves.
'''

from cubingtools.constants import *
from cubingtools.cube import *
from collections import Counter

def validateShape(state: dict, n: int) -> bool:
    if set(state.keys()) != set("UFRBLD"): return False
    for face in state.values():
        if len(face) != n: return False
        if any(len(row) != n for row in face): return False
    return True
def validateColorCounts(state: dict, n: int) -> bool | str:
    a = n*n
    counts = Counter([
        sticker for face in state.values()
                for row in face
                for sticker in row
    ])
    if all(v==a for v in counts.values()) and len(counts) == 6: 
        return counts.keys()
    return False
def validateCenters(state: dict, n: int, colors: str) -> bool:
    return set(face[1][1] for face in state.values()) == set(c for c in colors)

def isValid(state: dict, n: int) -> bool:
    def guard(f, *args): # early exists False if condition not met
        result = f(state, n, *args)
        if result: return result
        return False
    
    guard(validateShape)
    colors = guard(validateColorCounts) 
    guard(validateCenters, colors)
    return True
    # TODO complete