"""Some external/extension functions related to algorithms."""

from .cube import *
from .algorithm import *

def order(alg: Algorithm, n: int | None = None) -> int:
    """
    Returns the order of an algorithm on an NxN cube.
    """
    n = n or alg.degree

    if n <= 1:
        raise ValueError('n must be greater than 1')
    if alg.degree > n:
        raise ValueError('n must be greater than algorithm degree')

    i = 1
    c = CubeN(n)
    c >> alg
    while not c.isSolved():
        i += 1
        c >> alg
    return i

def equiv(alg1: Algorithm, alg2: Algorithm) -> bool:
    degree = max(alg1.degree, alg2.degree)
    cube = CubeN(degree)
    cube >> alg1 >> -alg2
    return cube.isSolved()