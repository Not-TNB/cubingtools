"""Some functions related to algorithms which require an auxiliary cube in their implementation."""

from .cube import *
from .algorithm import *

def order(alg: Algorithm, n: int) -> int:
    """
    Returns the order of an algorithm on an NxN cube — the number of times it must
    be applied to return the cube to its original state.

    :param alg: The algorithm whose order to compute.
    :param n: The size of the cube to evaluate on.

    :rtype: int
    :returns: The smallest positive integer ``k`` such that ``alg^k == id``

    :raises ValueError: If ``n <= 1`` or ``n < alg.degree``.
    """
    if n <= 1: raise ValueError('n must be greater than 1')
    if alg.degree > n: raise ValueError('n must be greater than algorithm degree')
    i = 1
    c = CubeN(n)
    c >> alg
    while not c.isSolved():
        i += 1
        c.algo(alg)
    return i


def equiv(alg1: Algorithm, alg2: Algorithm) -> bool:
    degree = max(alg1.degree, alg2.degree)
    cube = CubeN(degree)
    cube >> alg1 >> -alg2
    return cube.isSolved()
