import pytest
from cubingtools.algorithm import Move, toMove, toAlgo, Algorithm

def test_move_simple():
    m = Move(1, 'U', '1')
    assert m.mov == 'U'
    assert m.mod == '1'
    assert m.width == 1

def test_move_prime():
    m = Move(1, 'R', "'")
    assert str(m) == "R'"

def test_move_180():
    m = Move(1, 'F', '2')
    assert str(m) == "F2"

def test_move_wide_move_default_width():
    m = Move(2, 'Rw', '1')
    assert m.width == 2
    assert str(m) == "Rw"

def test_wider_move():
    m = Move(2025, 'Fw', '2')
    assert m.width == 2025
    assert str(m) == "2025Fw2"