import pytest
from cubingtools.algorithm import Algorithm
from cubingtools.metric import Metric, size

# ── ETM ──────────────────────────────────────────────────────────────────────

def test_etm_equals_len():
    cases = [
        "R",
        "R2",
        "M",
        "M2",
        "x2",
        "Fw'",
        "Rw",
        "R U R' U'",
        "",
    ]
    for s in cases:
        alg = Algorithm(s)
        assert len(alg) == size(alg, Metric.ETM)

# ── HTM ──────────────────────────────────────────────────────────────────────

def test_htm_basic():
    assert size(Algorithm("R"),   Metric.HTM) == 1
    assert size(Algorithm("R2"),  Metric.HTM) == 1
    assert size(Algorithm("M"),   Metric.HTM) == 2
    assert size(Algorithm("M2"),  Metric.HTM) == 2
    assert size(Algorithm("Fw'"), Metric.HTM) == 1
    assert size(Algorithm("Rw"),  Metric.HTM) == 1
    assert size(Algorithm("x2"),  Metric.HTM) == 0

def test_htm_rotations_are_free():
    assert size(Algorithm("x y z"), Metric.HTM) == 0

def test_htm_combined():
    # R U R' U' — all face moves, each = 1
    assert size(Algorithm("R U R' U'"), Metric.HTM) == 4
    # M E S — each slice = 2
    assert size(Algorithm("M E S"),     Metric.HTM) == 6

# ── QTM ──────────────────────────────────────────────────────────────────────

def test_qtm_basic():
    assert size(Algorithm("R"),   Metric.QTM) == 1
    assert size(Algorithm("R2"),  Metric.QTM) == 2
    assert size(Algorithm("M"),   Metric.QTM) == 2
    assert size(Algorithm("M2"),  Metric.QTM) == 4
    assert size(Algorithm("Fw'"), Metric.QTM) == 1
    assert size(Algorithm("Rw"),  Metric.QTM) == 1
    assert size(Algorithm("x2"),  Metric.QTM) == 0

def test_qtm_rotations_are_free():
    assert size(Algorithm("x2 y z'"), Metric.QTM) == 0

def test_qtm_half_turns():
    # all half turns
    assert size(Algorithm("R2 U2 F2"), Metric.QTM) == 6

# ── STM ──────────────────────────────────────────────────────────────────────

def test_stm_basic():
    assert size(Algorithm("R"),   Metric.STM) == 1
    assert size(Algorithm("R2"),  Metric.STM) == 1
    assert size(Algorithm("M"),   Metric.STM) == 1
    assert size(Algorithm("M2"),  Metric.STM) == 1
    assert size(Algorithm("Fw'"), Metric.STM) == 1
    assert size(Algorithm("Rw"),  Metric.STM) == 1
    assert size(Algorithm("x2"),  Metric.STM) == 0

def test_stm_rotations_are_free():
    assert size(Algorithm("x y2 z'"), Metric.STM) == 0

def test_stm_everything_else_costs_one():
    # 4 distinct move types, all = 1 each
    assert size(Algorithm("R M Fw' Rw"), Metric.STM) == 4

# ── OBTM ─────────────────────────────────────────────────────────────────────

def test_obtm_basic():
    assert size(Algorithm("R"),   Metric.OBTM) == 1
    assert size(Algorithm("R2"),  Metric.OBTM) == 1
    assert size(Algorithm("M"),   Metric.OBTM) == 2
    assert size(Algorithm("M2"),  Metric.OBTM) == 2
    assert size(Algorithm("Fw'"), Metric.OBTM) == 1
    assert size(Algorithm("Rw"),  Metric.OBTM) == 1
    assert size(Algorithm("x2"),  Metric.OBTM) == 0

def test_obtm_rotations_are_free():
    assert size(Algorithm("x2 y z'"), Metric.OBTM) == 0

def test_obtm_slice_half_turn_same_as_quarter():
    # M and M2 both = 2 in OBTM
    assert size(Algorithm("M"),  Metric.OBTM) == size(Algorithm("M2"), Metric.OBTM)

# ── Cross-metric consistency ──────────────────────────────────────────────────

def test_rotation_free_except_etm():
    alg = Algorithm("x2")
    assert size(alg, Metric.ETM)  == 1
    assert size(alg, Metric.HTM)  == 0
    assert size(alg, Metric.QTM)  == 0
    assert size(alg, Metric.STM)  == 0
    assert size(alg, Metric.OBTM) == 0

def test_empty_algorithm_all_zero():
    alg = Algorithm("")
    for metric in Metric:
        assert size(alg, metric) == 0, f"empty alg should be 0 in {metric}"

# ── String metric input ───────────────────────────────────────────────────────

def test_string_metric_input():
    alg = Algorithm("R U R' U'")
    assert size(alg, "HTM")  == size(alg, Metric.HTM)
    assert size(alg, "QTM")  == size(alg, Metric.QTM)
    assert size(alg, "OBTM") == size(alg, Metric.OBTM)

def test_invalid_metric_raises():
    with pytest.raises(ValueError):
        size(Algorithm("R"), "XTM")