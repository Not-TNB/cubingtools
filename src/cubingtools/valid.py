'''
Methods related to the validation of a cube state, ensuring the internal representation
of the cube state is reachable from a solved state with valid moves.
'''

from cubingtools.constants import *

def validateShape(state: dict) -> bool:
    # Check face names
    if set(state.keys()) != set("UFRBLD"): return False

    # Check all faces have same square shape
    shapes = set()
    for face in state.values():
        if any(len(row) != len(face) for row in face): return False 
        shapes.add((len(face), len(face[0])))

    if len(shapes) != 1: return False

    n = next(iter(shapes))[0]

    # Check centers distinct (only odd cubes)
    if n % 2 == 1:
        centers = [state[f][n//2][n//2] for f in state]
        if len(centers) != len(set(centers)): return False

    # Check color counts are equal
    from collections import Counter
    counts = Counter()
    for face in state.values():
        for row in face: counts.update(row)

    # 6 colors each must appear n*n times
    vals = list(counts.values())
    if len(set(vals)) != 1: return False
    if vals[0] != n*n:      return False

    return True

# WIP