import pytest
from cubingtools.algorithm import *
from cubingtools.error import *

def test_move_simple():
    m = Move.parse("U")
    assert isinstance(m, Move)
    assert str(m) == "U"

def test_move_with_mod():
    assert str(Move.parse("R'")) == "R'"
    assert str(Move.parse("F2")) == "F2"

def test_move_wide_no_mod():
    assert str(Move.parse("Rw")) == "Rw"

def test_move_wide_with_mod():
    assert str(Move.parse("Rw'")) == "Rw'"

def test_move_explicit_width():
    assert str(Move.parse("3Fw")) == "3Fw"

def test_move_width_and_mod():
    assert str(Move.parse("13Fw2")) == "13Fw2"

def test_move_invalid_token():
    with pytest.raises(InvalidMoveError):
        Move.parse("Q")
    with pytest.raises(InvalidMoveError):
        Move.parse("2F")
    with pytest.raises(InvalidMoveError):
        Move.parse("Rw3")
    with pytest.raises(InvalidMoveError):
        Move.parse("D'2")
    with pytest.raises(InvalidMoveError):
        Move.parse("Sw")
    with pytest.raises(InvalidMoveError):
        Move.parse("Sw")