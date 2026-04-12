import pytest
from cubingtools.algorithm import *

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
    a = Algorithm("U")
    r = a + "R2 F'"
    assert str(r) == "U R2 F'"
    r = "R2 F'" + a
    assert str(r) == "R2 F' U"

def test_algorithm_add_algorithm():
    a1 = Algorithm("U R")
    a2 = Algorithm("F2 U'")
    a3 = a1 + a2
    assert str(a3) == "U R F2 U'"

def test_algorithm_repeat():
    a = Algorithm("R U")
    r = a * 3
    assert str(r) == "R U R U R U"

def test_algorithm_inverse_basic():
    a = Algorithm("U R' F2")
    assert str(a.inverse()) == "F2 R U'"

def test_algorithm_double_inverse():
    a = Algorithm("U R")
    assert str(-(-a)) == "U R"

def test_identity_and_inverse():
    """
    > a + (-a) = id
    > (-a) + a = id
    """
    idn = Algorithm()

    a = Algorithm("R U F2 D' L B")
    assert idn == Algorithm()
    assert a + (-a) == idn
    assert (-a) + a == idn

def test_equivalent_representations():
    tests = [
        ("R R", "R2"),
        ("(R U)2", "R U R U"),
        ("Rw Rw'", ""),
        ("(R U R' U')6", ""),
        ("3Rw 3Rw'", ""),
    ]
    for a,b in tests:
        assert Algorithm(a) == Algorithm(b)

def test_equality_different_degrees():
    a = Algorithm("L")
    b = Algorithm("100Rw L 100Rw'")
    assert a == b
    assert b == a

def test_inequality_and_non_commutativity():
    tests = [
        ("R U", "U R"),
        ("R U R'", "R U2 R'"),
        ("R2 U", "R U2"),
        ("F R U", "F U R"),
    ]
    for a,b in tests:
        assert Algorithm(a) != Algorithm(b)

def test_invalid_addition():
    with pytest.raises(TypeError):
        a = Algorithm("U R'") + 6

def test_invalid_algorithm_constructor():
    with pytest.raises(TypeError):
        a = Algorithm([Move.parse("U"), 7])
    with pytest.raises(TypeError):
        a = Algorithm(8936384)

def test_mirror_involution():
    alg = Algorithm("R U r u M E S x y z")
    assert alg.mirror().mirror() == alg

def test_mirror_unchanged_moves():
    alg = Algorithm("x M")
    assert alg.mirror() == alg

def test_mirror_expected():
    alg = Algorithm("R L U D F B r l u d f b M E S x y z")
    assert alg.mirror() == Algorithm("L' R' U' D' F' B' l' r' u' d' f' b' M E' S' x y' z'")