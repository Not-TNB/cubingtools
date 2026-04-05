import pytest
from cubingtools import *

# [A,B] = AB(A^-1)(B^-1)
def test_commutator_basic():
    A = Algorithm("R")
    B = Algorithm("U")
    comm = A.commutator(B)
    assert str(comm) == "R U R' U'"

# [A,A] = I
def test_commutator_identity_with_self():
    A = Algorithm("R U F")
    comm = A.commutator(A)
    # [A,A] = identity
    assert comm == Algorithm("")

# [A:I] = A
def test_conjugate_identity():
    A = Algorithm("R U")
    I = Algorithm("")
    assert I.conjugate(A) == A

# [A:B] = BA(B^-1)
def test_conjugate_basic():
    A = Algorithm("R U")
    B = Algorithm("F")
    conj = B.conjugate(A)
    expected = B + A - B
    assert conj == expected

# [A,B]^-1 = [B,A]
def test_commutator_inverse_relation():
    A = Algorithm("R")
    B = Algorithm("U")
    comm = A.commutator(B)
    assert -comm == B.commutator(A)