import pytest
from copy import deepcopy

from cubingtools.cube import CubeN
from cubingtools.algorithm import Move, Algorithm, toAlgo

# Construction Tests

def test_construct_default_cube():
    c = CubeN()
    assert c.size == 3
    assert c.cols == "wgrboy"
    assert set(c.state.keys()) == set("UFRBLD")


def test_invalid_size():
    with pytest.raises(ValueError):
        CubeN(1)

def test_invalid_colors():
    with pytest.raises(ValueError):
        CubeN(3, "abc")      # too short
    with pytest.raises(ValueError):
        CubeN(3, "abcdea")   # not unique

# Face Rotation Tests

def test_rotations_are_inverse():
    c = CubeN()
    face = "F"

    orig = deepcopy(c.state[face])

    # rotate clockwise then anticlockwise
    cw = c.rotFC(face)
    c.state[face] = cw
    acw = c.rotFA(face)
    assert acw == orig

    # 180 twice = original
    c.state[face] = deepcopy(orig)
    r2 = c.rotF2(face)
    c.state[face] = r2
    assert c.rotF2(face) == orig


def test_show_face_returns_string():
    c = CubeN()
    out = c.showFace("U")
    assert isinstance(out, str)
    assert c.cols[0] in out  # "w" normally

# Whole Cube Rotations

def test_x_rotation_preserves_colors():
    c = CubeN()
    before = deepcopy(c.state)
    c.xRot()
    # Should still be 6 uniform faces
    for f in "UFRBLD":
        vals = {x for row in c.state[f] for x in row}
        assert len(vals) == 1


def test_y_rotation_moves_faces():
    c = CubeN()
    c >> "R"
    top_before = deepcopy(c.state["U"])
    c.yRot()
    assert c.state["U"] != top_before  # U rotated


def test_z_rotation_moves_faces():
    c = CubeN()
    up_before = deepcopy(c.state["U"])
    c.zRot()
    assert c.state["U"] != up_before

# Turns (U, R, F, etc.)

def test_u_turn_works():
    c = CubeN(3)
    before = deepcopy(c.state["F"][0])
    c.uTurn(1)
    after = c.state["F"][0]
    assert after != before  # U should rotate F top row


def test_invalid_u_turn():
    c = CubeN(3)
    with pytest.raises(ValueError):
        c.uTurn(3)


def test_turn_basic_move():
    c = CubeN()
    before = deepcopy(c.state)
    c.turn(Move(1, "U", "1"))
    assert c.state != before


def test_turn_prime_and_double():
    c = CubeN()
    before = deepcopy(c.state)

    c.turn(Move(1, "R", "'"))
    assert c.state != before

    c.reset()
    c.turn(Move(1, "R", "2"))
    assert c.state != before

# algo() execution

def test_algo_string():
    c = CubeN()
    before = deepcopy(c.state)
    c.algo("R U R' U'")
    assert c.state != before


def test_algo_move():
    c = CubeN()
    before = deepcopy(c.state)
    c.algo(Move(1, "F", "1"))
    assert c.state != before


def test_algo_algorithm():
    c = CubeN()
    alg = toAlgo("R2 U2")
    before = deepcopy(c.state)
    c.algo(alg)
    assert c.state != before


# __rshift__ (>>) operator

def test_rshift_operator():
    c = CubeN()
    before = deepcopy(c.state)
    c >> "R U"
    assert c.state != before

# Solved state & reset

def test_is_solved_on_start():
    c = CubeN()
    assert c.isSolved() is True

def test_reset():
    c = CubeN()
    c.algo("R U")
    assert not c.isSolved()
    c.reset()
    assert c.isSolved()

# Random Moves & Scrambling

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