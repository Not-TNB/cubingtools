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
    for n in [51,61]:
        c = CubeN(n)
        c.scramble()
        assert isValidCube(c)

def test_invalid_color_num():
    d = {'L': [['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']], 
         'U': [['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']], 
         'B': [['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'y']], # extra y here!
         'R': [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']], 
         'F': [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], 
         'D': [['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']]}
    assert not isValid(d, 3)