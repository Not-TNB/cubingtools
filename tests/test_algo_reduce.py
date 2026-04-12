import pytest
import random
from cubingtools.algorithm import *
from cubingtools.algorithmExtensions import reduced, equiv, simplified

# Adjacent cancels still work
def test_adjacent_cancel():
    assert reduced(Algorithm("R R'")) == Algorithm()
    assert reduced(Algorithm("R2 R2")) == Algorithm()
    assert reduced(Algorithm("R R R")) == Algorithm("R'")

# Same-axis non-adjacent cancel
def test_RL_cancel():
    assert reduced(Algorithm("R L R'")) == Algorithm("L")
    assert reduced(Algorithm("R L2 R'")) == Algorithm("L2")
    assert reduced(Algorithm("L R L'")) == Algorithm("R")
def test_UD_cancel():
    assert reduced(Algorithm("U D U'")) == Algorithm("D")
    assert reduced(Algorithm("U D' U'")) == Algorithm("D'")
def test_FB_cancel():
    assert reduced(Algorithm("F B F'")) == Algorithm("B")
    assert reduced(Algorithm("B F2 B'")) == Algorithm("F2")

# Partial merge
def test_partial_merge():
    assert reduced(Algorithm("R L R")) == Algorithm("L R2") or \
           reduced(Algorithm("R L R")) == Algorithm("R2 L")
    assert reduced(Algorithm("R L R")) == Algorithm("R L R") or \
           equiv(reduced(Algorithm("R L R")), Algorithm("R L R"))


def test_mod_merge():
    assert reduced(Algorithm("R2 L R2")) == Algorithm("L") 
    assert reduced(Algorithm("R' L R")) == Algorithm("L R2") or \
           equiv(reduced(Algorithm("R' L R")), Algorithm("R' L R"))

# No reduction when axes differ
def test_no_reduction_different_axis():
    assert reduced(Algorithm("R U R'")) == Algorithm("R U R'")
    assert reduced(Algorithm("U R U'")) == Algorithm("U R U'")
    assert reduced(Algorithm("F R F'")) == Algorithm("F R F'")

# Rotations block commutation
def test_rotation_blocks():
    assert reduced(Algorithm("U x U'")) == Algorithm("U x U'")
    assert reduced(Algorithm("R y R'")) == Algorithm("R y R'")

# Slice moves commute on their axis
def test_slice_commutes():
    # M on RL
    assert reduced(Algorithm("R M R'")) == Algorithm("M")
    assert reduced(Algorithm("L M L'")) == Algorithm("M")
    # E on UD
    assert reduced(Algorithm("U E U'")) == Algorithm("E")
    # S on FB
    assert reduced(Algorithm("F S F'")) == Algorithm("S")
    
# Wide moves commute on their axis
def test_wide_moves_commute():
    assert reduced(Algorithm("Rw L Rw'")) == Algorithm("L")
    assert reduced(Algorithm("R Lw R'")) == Algorithm("Lw")
def test_wide_moves_different_width_no_merge():
    alg = Algorithm("Rw 2Rw Rw'")
    result = reduced(alg)
    assert equiv(result, alg)
    assert len(result) >= 1 

# Chained reductions
def test_chained():
    assert reduced(Algorithm("R L R' L'")) == Algorithm()
def test_cascading():
    assert reduced(Algorithm("U R U' R'")) == Algorithm("U R U' R'") 
    assert reduced(Algorithm("U D U' D'")) == Algorithm()
        
# Invariants
MODS = ["", "2", "'"]
WIDTHS = ["", "2", "3", "4"]
def _random_move():
    face = random.choice("UFLBRD")
    mod = random.choice(MODS)
    width = random.choice(WIDTHS)
    if width == "":
        return face + mod
    if width == "2":
        return face + "w" + mod
    return width + face + "w" + mod

def _random_algorithm(length=25):
    return Algorithm(" ".join(_random_move() for _ in range(length)))