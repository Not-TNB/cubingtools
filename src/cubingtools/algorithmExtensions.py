from .cube import *
from .algorithm import *

def order(alg: Algorithm, size: int) -> int:
    i = 1
    c = CubeN(alg.degree)
    c >> alg
    while not c.isSolved():
        i += 1
        c.algo(alg)
    return i