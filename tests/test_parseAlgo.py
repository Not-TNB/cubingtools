import pytest
from cubingtools.algorithm import Move, toMove, toAlgo, Algorithm

def test_toAlgo_basic():
    alg = toAlgo("U R2 F'")
    assert str(alg) == "U R2 F'"

def test_toAlgo_parens_repeat():
    alg = toAlgo("(R U)3")
    assert str(alg) == "R U R U R U"

def test_toAlgo_nested_parens():
    alg = toAlgo("B (R (U F2)3 R')2 F (R U R' U')")
    assert isinstance(alg, Algorithm)
    assert str(alg) == "B R U F2 U F2 U F2 R' R U F2 U F2 U F2 R' F R U R' U'" 

def test_toAlgo_wide_moves():
    alg = toAlgo("Rw U Rw'")
    assert str(alg) == "Rw U Rw'"

def test_toAlgo_mismatched_paren():
    with pytest.raises(ValueError):
        toAlgo("(R U")