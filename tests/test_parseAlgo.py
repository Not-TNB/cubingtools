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

def test_toAlgo_condensed():
    s = "L2 B' Fw' D2 B' 3Rw2 3Lw Fw 3Bw2 F2 3Rw F' Dw2 Rw U' D2 B2 3Lw' 3Fw' 3Lw' 3Fw Uw2 U' Bw2 Rw' Fw' Uw2 D Bw' 3Uw Lw R' 3Lw 3Rw' Fw2 3Lw2 Dw2 3Rw' 3Fw2 3Uw' 3Lw' Bw Dw2 Lw Dw R2 F' Bw R 3Uw2 Dw 3Rw2 Rw2 Lw2 3Fw L2 F 3Uw2 L 3Uw' L2 3Bw2 U2 3Rw 3Bw Fw R' 3Rw2 Dw 3Uw 3Dw 3Bw Lw L Dw2 L' Rw 3Lw2 D 3Rw' 3Fw' 3Dw2 U' Lw Rw 3Fw Fw' 3Bw2 U' 3Uw 3Dw2 Lw2 Dw' Bw' 3Rw 3Lw2 3Uw' D2 R2 3Rw'"
    condensed = s.replace(' ','')
    assert str(toAlgo(condensed)) == s

def test_toAlgo_wide_moves():
    alg = toAlgo("Rw U Rw'")
    assert str(alg) == "Rw U Rw'"

def test_toAlgo_mismatched_paren():
    with pytest.raises(ValueError):
        toAlgo("(R U")
    with pytest.raises(ValueError):
        toAlgo("R U2 (D ) R ) B ( F )")