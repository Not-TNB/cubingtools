import pytest
from cubingtools.algorithm import *
from cubingtools.error import *

def test_move_simple():
    m = parseMove("U")
    assert isinstance(m, Move)
    assert str(m) == "U"

def test_move_with_mod():
    assert str(parseMove("R'")) == "R'"
    assert str(parseMove("F2")) == "F2"

def test_move_wide_no_mod():
    assert str(parseMove("Rw")) == "Rw"

def test_move_wide_with_mod():
    assert str(parseMove("Rw'")) == "Rw'"

def test_move_explicit_width():
    assert str(parseMove("3Fw")) == "3Fw"

def test_move_width_and_mod():
    assert str(parseMove("13Fw2")) == "13Fw2"

def test_move_invalid_token():
    with pytest.raises(InvalidMoveError):
        parseMove("Q")
    with pytest.raises(InvalidMoveError):
        parseMove("2F")
    with pytest.raises(InvalidMoveError):
        parseMove("Rw3")
    with pytest.raises(InvalidMoveError):
        parseMove("D'2")
    with pytest.raises(InvalidMoveError):
        parseMove("Sw")
    with pytest.raises(InvalidMoveError):
        parseMove("Sw")