import pytest
from cubingtools.cube import *
from cubingtools.valid import *

from cubingtools.valid import _validateCornerExistence

def test_solved_is_valid():
    for n in range(2,50):
        c = CubeN(n)
        assert isValid(c.state, n)

def test_scrambles_are_valid():
    for n in [2,3,4,5,6,7,10,20]:
        c = CubeN(n)
        for _ in range(3):
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

def test_validate_corner_existence():
    colors = 'ejimda'

    for n in range(2,11):
        bad = CubeN(n, colors)
        bad.state['U'][n-1][n-1] = bad.state['U'][n-1][0]
        bad.state['R'][0][0]     = bad.state['F'][0][0]
        bad.state['F'][0][n-1]   = bad.state['L'][0][0]
        assert not _validateCornerExistence(bad.state, n, colors)

        bad.scramble()
        assert not _validateCornerExistence(bad.state, n, colors)

        bad2 = CubeN(n, colors)
        bad2.state['D'][0][0]     = bad2.state['U'][n-1][n-1]
        bad2.state['L'][n-1][n-1] = bad2.state['R'][0][0]
        bad2.state['F'][n-1][0]   = bad2.state['B'][0][n-1]
        assert not _validateCornerExistence(bad2.state, n, colors)

        bad2.scramble()
        assert not _validateCornerExistence(bad2.state, n, colors)