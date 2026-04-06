"""Contains the Metric class and the size method to compute the size of an algorithm wrt various metrics."""

from enum import StrEnum
from .algorithm import *

class Metric(StrEnum):
    HTM  = "HTM"   # Half Turn Metric
    QTM  = "QTM"   # Quarter Turn Metric
    ETM  = "ETM"   # Execution Turn Metric
    STM  = "STM"   # Slice Turn Metric
    OBTM = "OBTM"  # Outer Block Turn Metric

_ROTATIONS = frozenset('xyz')
_SLICES = frozenset('MES')
_FACES = frozenset('UDFBLR')
_WIDES = frozenset('udfblr')

def size(alg: Algorithm, metric: Metric | str = Metric.OBTM) -> int:
    """
    Returns the size of an algorithm under the given move-counting metric.

    :param alg: The algorithm to measure.
    :param metric: The metric to use. Defaults to ``Metric.OBTM``.

    :rtype: int
    :returns: The move count of the algorithm under the given metric.

    :raises ValueError: If ``metric`` is not a recognized metric string.

    .. Notes::
    The size of the simplified algorithm will be computed. Also, note that for
    all algorithms ``A`` we have ``len(A)==size(A,"ETM")``. HTM is most meaningful on 3x3x3 cubes.
    """
    metric = Metric(metric)
    total = 0

    for move in alg:
        b        = str(move.mov)
        is_half  = move.mod == 2
        is_rot   = b in _ROTATIONS
        is_slice = b in _SLICES
        is_wide  = b in _WIDES or (b in _FACES and move.width >= 2)

        match metric:
            case Metric.ETM:
                total += 1

            case Metric.STM:
                if not is_rot:
                    total += 1

            case Metric.HTM:
                if   is_rot  : pass
                elif is_slice: total += 2
                elif is_wide : total += 1
                else         : total += 1

            case Metric.QTM:
                if   is_rot  : pass
                elif is_slice: total += 4 if is_half else 2
                elif is_wide : total += 2 if is_half else 1
                else         : total += 2 if is_half else 1

            case Metric.OBTM:
                if   is_rot  : pass
                elif is_slice: total += 2
                else         : total += 1

    return total