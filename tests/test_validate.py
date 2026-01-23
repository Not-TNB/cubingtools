import pytest
from cubingtools.cube import *
from cubingtools.valid import *

def test_solved_is_valid():
    for n in range(2,100):
        c = CubeN(n)
        assert isValid(c.state, n)

def test_scrambles_are_valid():
    for n in [2,3,4,5,6,7,10,20]:
        c = CubeN(n)
        for _ in range(5):
            c.scramble()
            assert isValid(c.state, n)

def test_scrambles_are_valid_big():
    for n in [50,70]:
        c = CubeN(n)
        c.scramble()
        assert isValid(c.state, n)