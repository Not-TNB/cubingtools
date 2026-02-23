import pytest

from cubingtools import CubeN, Move, Algorithm

def test_rand_move_returns_move():
    c = CubeN()
    mv = c.randMove()
    assert isinstance(mv, Move)

def test_scramble_length_and_not_solved():
    c = CubeN(67)
    alg = c.scramble(100)
    assert isinstance(alg, Algorithm)
    assert len(alg.movs) == 100
    assert not c.isSolved()