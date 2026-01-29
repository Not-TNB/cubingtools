import pytest
from cubingtools.algorithm import toAlgo
from cubingtools.cube import CubeN

def test_algoBB_2():
    c2 = CubeN(2)
    c2 >> "D2 F' U R' U2 R D' L U B2 U L2 B2 U' L2 U B2 L' U R D2 R F' D2 U L D' B F U2 L B L D' R' D F' D2 U R2 B F2 R2 L D' U2 B2 U B' U2 D B R2 U L' F R U R' D2 F' B' U2 L' D2 F2 R' D F D' R2 D' U R' B2 R B' F' U D' L F U' L' B2 U2 B U2 R' U L B R2 B2 L' F B2 D2 R' U'"
    c2 >> "U2 F2 L2 F' U2 F' U F' L'"
    assert c2.isSolved()

def test_algoBB_3():
    c3 = CubeN(3)
    c3 >> "D2 L2 D' F2 U2 L2 F2 U L2 B U2 F' B L' U' B R2 L2 U2 F2 R' F' R2 D U F U R D' F2 L2 B U' B R2 B U D' F' U' D2 R2 F2 D2 F' U' D' F2 B D B2 L' B' L' B' L2 F' U' R2 U F D R' B2 D R B U2 F R2 L U' D B2 L2 U' L' F' R F D2 L2 F U2 D' B' U2 F D' U2 F2 B' D' B D B2 D2 F' U' L"
    c3 >> "B' U B' U' F D' R' F L2 F2 L2 U' R2 U' F2 D' B2 D2 B2 F R"
    assert c3.isSolved()

def test_algoBB_4():
    c4 = CubeN(4)
    algo = toAlgo("L2 B2 D2 L2 B2 D2 R L D2 L F2 D' L U B R L2 B2 D' F2 Fw2 L U' F2 Rw2 D R2 U' Fw2 Uw2 Fw2 D2 Fw' L F' R Fw2 D2 Uw' Rw2 F' Uw2 Fw R' Uw")
    c4 >> algo
    c4 >> -algo
    assert c4.isSolved()

def test_algoBB_7():
    c7 = CubeN(7)
    algo = toAlgo("L2 B' Fw' D2 B' 3Rw2 3Lw Fw 3Bw2 F2 3Rw F' Dw2 Rw U' D2 B2 3Lw' 3Fw' 3Lw' 3Fw Uw2 U' Bw2 Rw' Fw' Uw2 D Bw' 3Uw Lw R' 3Lw 3Rw' Fw2 3Lw2 Dw2 3Rw' 3Fw2 3Uw' 3Lw' Bw Dw2 Lw Dw R2 F' Bw R 3Uw2 Dw 3Rw2 Rw2 Lw2 3Fw L2 F 3Uw2 L 3Uw' L2 3Bw2 U2 3Rw 3Bw Fw R' 3Rw2 Dw 3Uw 3Dw 3Bw Lw L Dw2 L' Rw 3Lw2 D 3Rw' 3Fw' 3Dw2 U' Lw Rw 3Fw Fw' 3Bw2 U' 3Uw 3Dw2 Lw2 Dw' Bw' 3Rw 3Lw2 3Uw' D2 R2 3Rw'")
    c7 >> algo
    c7 >> -algo
    assert c7.isSolved()

def test_algoBB_50():
    c50 = CubeN(50)
    alg = c50.scramble()
    c50 >> -alg
    assert c50.isSolved()