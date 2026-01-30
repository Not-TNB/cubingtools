import pytest
from cubingtools.algorithm import Move, Algorithm

def test_algorithm_str():
    alg = Algorithm([Move(1, 'U', '1'), Move(1, 'R', "'")])
    assert str(alg) == "U R'"

def test_algorithm_len():
    alg = Algorithm([Move(), Move(), Move()])
    assert len(alg) == 3

def test_algorithm_add_move():
    a = Algorithm([Move(1, "U", "1")])
    r = a + Move(1, "R", "1")
    assert str(r) == "U R"

def test_algorithm_add_string():
    a = Algorithm([Move(1, "U", "1")])
    r = a + "R2 F'"
    assert str(r) == "U R2 F'"

def test_algorithm_add_algorithm():
    a1 = Algorithm.parse("U R")
    a2 = Algorithm.parse("F2 U'")
    a3 = a1 + a2
    assert str(a3) == "U R F2 U'"

def test_algorithm_repeat():
    a = Algorithm.parse("R U")
    r = a * 3
    assert str(r) == "R U R U R U"

def test_algorithm_inverse_basic():
    a = Algorithm.parse("U R' F2")
    assert str(a.inverse()) == "F2 R U'"

def test_algorithm_double_inverse():
    a = Algorithm.parse("U R")
    assert str(-(-a)) == "U R"
