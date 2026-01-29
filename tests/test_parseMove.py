import pytest
from cubingtools.algorithm import Move, toMove, toAlgo, Algorithm
from cubingtools.error import *

def test_toMove_simple():
    m = toMove("U")
    assert isinstance(m, Move)
    assert str(m) == "U"

def test_toMove_with_mod():
    assert str(toMove("R'")) == "R'"
    assert str(toMove("F2")) == "F2"

def test_toMove_wide_no_mod():
    assert str(toMove("Rw")) == "Rw"

def test_toMove_wide_with_mod():
    assert str(toMove("Rw'")) == "Rw'"

def test_toMove_explicit_width():
    assert str(toMove("3Fw")) == "3Fw"

def test_toMove_width_and_mod():
    assert str(toMove("13Fw2")) == "13Fw2"

def test_toMove_invalid_token():
    with pytest.raises(InvalidMoveError):
        toMove("Q")
    with pytest.raises(InvalidMoveError):
        toMove("2F")
    with pytest.raises(InvalidMoveError):
        toMove("Rw3")
    with pytest.raises(InvalidMoveError):
        toMove("D'2")
    with pytest.raises(InvalidMoveError):
        toMove("Sw")