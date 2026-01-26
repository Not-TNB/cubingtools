'''
Methods related to the validation of a cube state, ensuring the internal representation
of the cube state is reachable from a solved state with valid moves.
'''

from cubingtools.constants import *
from cubingtools.cube import *
from collections import Counter

def _validateShape(state: dict, n: int) -> bool:
    if set(state.keys()) != set(MOVS): return False
    for face in state.values():
        if len(face) != n: return False
        if any(len(row) != n for row in face): return False
    return True

def _validateColorCounts(state: dict, n: int) -> bool | str:
    a = n*n
    counts = Counter([
        sticker for face in state.values()
                for row in face
                for sticker in row
    ])
    if all(v==a for v in counts.values()) and len(counts) == 6:
        return ''.join(state[face][0][0] for face in MOVS) # ordered colors

def _validateCenters(state: dict, n: int, colors: str) -> bool:
    if n % 2 == 0: return True
    c = n//2 + 1
    return set(face[c][c] for face in state.values()) == set(colors)

###################################################################################################
# CORNER STUFF

# VALIDATION STUFF
def corners(n: int, colors: str):
    m = n-1
    u,f,r,b,l,d = colors
    return {
        ('U','R','F', u,r,f , ((m,m),(0,0),(0,m))),
        ('U','F','L', u,f,l , ((m,0),(0,0),(0,m))),
        ('U','L','B', u,l,b , ((0,0),(0,0),(0,m))),
        ('U','B','R', u,b,r , ((0,m),(0,0),(0,m))),
        ('D','F','R', d,f,r , ((0,m),(m,m),(m,0))), 
        ('D','L','F', d,l,f , ((0,0),(m,m),(m,0))), 
        ('D','B','L', d,b,l , ((m,0),(m,m),(m,0))), 
        ('D','R','B', d,r,b , ((m,m),(m,m),(m,0))),
    }

def _validateCornerExistence(state: dict, n: int, colors: str) -> bool:
    crnrs = corners(n, colors)
    expected = set()
    actual = set()
    for f1,f2,f3, c1,c2,c3, ((i1,j1),(i2,j2),(i3,j3)) in crnrs:
        actual.add(frozenset((
            state[f1][i1][j1],
            state[f2][i2][j2],
            state[f3][i3][j3],
        )))
        expected.add(frozenset([c1,c2,c3]))

    return actual == expected

def _validateCornerPermutation(state: dict, n: int, colors: str) -> bool:
    # inversions method
    pass

###################################################################################################

# allows early fail from inner function
class _GuardFail(Exception): pass

def isValid(state: dict, n: int) -> bool:
    def guard(f, *args): # early exits if result is falsy
        result = f(state, n, *args)
        return result if result else _GuardFail()
    
    try:
        guard(_validateShape)
        colors = guard(_validateColorCounts)
        guard(_validateCenters, colors)
        guard(_validateCornerExistence, colors)
    except: return False
    else: return True

def isValidCube(cube: CubeN) -> bool:
    return isValid(cube.state, cube.size)