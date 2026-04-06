from cubingtools.algorithmExtensions import order
from cubingtools.algorithm import *

def test_algo_order_3x3_small():
    cases = [
        ("R2",         3, 2),
        ("R",          3, 4),
        ("R U R' U",  3, 5),
        ("R2 U2",      3, 6),
        ("R' U' F2",   3, 9),
        ("R2 r U' S",  3, 15),
        ("R U R' D2",  3, 20),
    ]
    for alg_str, n, expected in cases:
        alg = Algorithm(alg_str)
        result = order(alg, n)
        assert result == expected, f"{alg_str!r} on {n}×{n}: expected {expected}, got {result}"


def test_algo_order_3x3_medium():
    cases = [
        ("R U'",    3, 63),
        ("R U",     3, 105),
        ("R L' U",  3, 180),
        ("R B L F", 3, 315),
        ("F U R'",  3, 360),
    ]
    for alg_str, n, expected in cases:
        alg = Algorithm(alg_str)
        result = order(alg, n)
        assert result == expected, f"{alg_str!r} on {n}×{n}: expected {expected}, got {result}"


def test_algo_order_3x3_large():
    cases = [
        ("R U z2",     3, 630),
        ("R2 r U' y2", 3, 720),
        ("R y",        3, 1260),
    ]
    for alg_str, n, expected in cases:
        alg = Algorithm(alg_str)
        result = order(alg, n)
        assert result == expected, f"{alg_str!r} on {n}×{n}: expected {expected}, got {result}"


def test_algo_order_2x2():
    cases = [
        ("R2",            2, 2),
        ("R",             2, 4),
        ("R U2",          2, 6),
        ("R U",           2, 15),
        ("R y",           2, 36),
    ]
    for alg_str, n, expected in cases:
        alg = Algorithm(alg_str)
        result = order(alg, n)
        assert result == expected, f"{alg_str!r} on {n}×{n}: expected {expected}, got {result}"


def test_algo_order_4x4():
    cases = [
        ("R2",   4, 2),
        ("R",    4, 4),
        ("R U2", 4, 30),
        ("R U",  4, 105),
        ("R y",  4, 1260),
    ]
    for alg_str, n, expected in cases:
        alg = Algorithm(alg_str)
        result = order(alg, n)
        assert result == expected, f"{alg_str!r} on {n}×{n}: expected {expected}, got {result}"