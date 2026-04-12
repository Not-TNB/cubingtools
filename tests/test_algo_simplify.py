import pytest
from cubingtools.algorithm import *
from cubingtools.algorithmExtensions import *
import random

# -----------------------
# Basic cancellations
# -----------------------

def test_cancel():
    alg = Algorithm("R R'")
    assert simplified(alg) == Algorithm()
    alg = Algorithm("R2 R2")
    assert simplified(alg) == Algorithm()
    alg = Algorithm("R R R")
    assert simplified(alg) == Algorithm("R'")
    alg = Algorithm("R R R R")
    assert simplified(alg) == Algorithm()

def test_mixed_mod():
    alg = Algorithm("R R2")
    assert simplified(alg) == Algorithm("R'")
    alg = Algorithm("R2 R")
    assert simplified(alg) == Algorithm("R'")
    alg = Algorithm("R' R'")
    assert simplified(alg) == Algorithm("R2")

# -----------------------
# Width-sensitive merging
# -----------------------

def test_wide_moves_merge():
    alg = Algorithm("2Rw 2Rw 2Rw")
    assert simplified(alg) == Algorithm("2Rw'")

def test_wide_moves_different_width_do_not_merge():
    alg = Algorithm("Rw 2Rw")
    assert simplified(alg) == Algorithm("Rw 2Rw")

# -----------------------
# Non-adjacent should not merge
# -----------------------

def test_non_adjacent_no_merge():
    alg = Algorithm("R U R")
    assert equiv(simplified(alg), Algorithm("R U R"))

# -----------------------
# Basic example
# -----------------------

def test_basic():
    alg = Algorithm("F U R' U' U R2")
    assert equiv(simplified(alg), Algorithm("F U R"))

# -----------------------
# Idempotency
# -----------------------

def test_idempotent():
    alg = Algorithm("R R R")
    first = simplified(alg)
    second = simplified(first)
    assert equiv(first, second)

# -----------------------
# In-place simplify()
# -----------------------

def test_simplify_in_place():
    alg = Algorithm("R R'")
    alg.simplify()
    assert equiv(alg, Algorithm())
