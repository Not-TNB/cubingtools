"""
Classes and methods working with the internal representation of algorithms,
which can be performed on cubes.
"""

from __future__ import annotations
import operator
import re
from .move import Move
from .error import InvalidAlgorithmError

########################################################################################################################

_VALID_MOVE_STRING     = r"\d*[A-Za-z]w?[2']?|\(|\)\d*"
_VALID_MOVE_REGEX      = re.compile(_VALID_MOVE_STRING)
_ALGORITHM_LEXER_REGEX = re.compile(rf"^(\s*({_VALID_MOVE_STRING})\s*)*$")

########################################################################################################################

class Algorithm:
    def __init__(self, moves: Move | list[Move] | str | None = None):
        """
        Represents a sequence of moves (an algorithm) on the cube.

        :param moves: ``None`` (cast to empty algorithms), ``Move`` (cast to a single-move algorithm), \
        ``list[Move]`` or ``str`` (parsed using ``Algorithm.parse()``)
        """
        self._movs = None

        match moves:
            case None:
                self._movs = []
            case list():
                if any((not isinstance(m, Move)) for m in moves):
                    raise TypeError('List must contain only Move objects')
                self._movs = moves
            case str():
                parsed = Algorithm.parse(moves)
                self._movs = parsed._movs.copy()
            case Move():
                self._movs = [moves]
            case _:
                raise TypeError(f'Cannot construct an Algorithm with type {type(moves)}')

        # for what N can this be executed on an NxN cube?
        self.degree = 2
        if self._movs:
            self.degree = max([m.width for m in self._movs]) + 1

    def __eq__(self, other: 'Algorithm') -> bool:
        """
        Checks if two algorithms are equivalent by applying one then the
        inverse of the other to a solved cube and checking if it is still solved.
        """
        from cubingtools.cube import CubeN
        d = max(self.degree, other.degree)
        return (CubeN(d) >> self >> -other).isSolved()

    def inverse(self) -> 'Algorithm':
        """Returns the inverse of the algorithm."""
        return Algorithm([-move for move in self._movs[::-1]])

    def __neg__(self) -> 'Algorithm':
        return self.inverse()

    def __repr__(self) -> str:
        padLen = len(str(len(self) - 1))
        out = list(map(
            operator.add,
            [f"{i:>{padLen}}: " for i in range(1, len(self) + 1)],
            [repr(move) for move in self._movs]
        ))
        return '\n'.join(out)

    def __str__(self) -> str:
        """Returns the string representation of the algorithm."""
        return ' '.join([str(move) for move in self._movs])

    @staticmethod
    def _coerceToAlgo(other: 'Move | str | Algorithm') -> Algorithm:
        """Helper function for Algorithm binary operators."""
        match other:
            case Move()      : return Algorithm([other])
            case str()       : return Algorithm(other)
            case Algorithm() : return other
            case _:
                raise TypeError(f'Cannot combine Algorithm with type {type(other)}.')

    def __add__(self, other: 'Move | str | Algorithm') -> 'Algorithm':
        """
        Concatenates two algorithms and simplifies the output.

        :param other: The other algorithm to concatenate.
        """
        otherAlgo = Algorithm._coerceToAlgo(other)
        return simplified(Algorithm(self._movs + otherAlgo._movs))

    def __sub__(self, other: 'Move | str | Algorithm') -> 'Algorithm':
        """
        Concatenates the inverse of the second algorithm to the first algorithm, and simplifies the output.

        :param other: The other algorithm to "subtract".

        .. Notes::
        For algorithms ``A`` and ``B`` we have ``A-B==A+(-B)``
        """
        otherAlgo = Algorithm._coerceToAlgo(other)
        return simplified(Algorithm(self._movs + (-otherAlgo)._movs))

    def __radd__(self, other: 'Move | str | Algorithm') -> 'Algorithm':
        otherAlgo = Algorithm._coerceToAlgo(other)
        return simplified(Algorithm(otherAlgo._movs + self._movs))

    def __rsub__(self, other: 'Move | str | Algorithm') -> 'Algorithm':
        otherAlgo = Algorithm._coerceToAlgo(other)
        return simplified(Algorithm(otherAlgo._movs + (-self)._movs))

    def __mul__(self, times: int) -> 'Algorithm':
        """Repeats the algorithm a specified number of times and simplifies the output."""
        if times < 1: raise ValueError("Times must be a positive integer.")
        return simplified(Algorithm(self._movs * times))

    def __len__(self) -> int:
        """Returns the number of moves making up the algorithm."""
        return len(self._movs)

    @staticmethod
    def _tokenize(algStr: str) -> list[str]:
        if not _ALGORITHM_LEXER_REGEX.match(algStr):
            raise InvalidAlgorithmError("Invalid token in algorithm string.")
        return _VALID_MOVE_REGEX.findall(algStr)

    @staticmethod
    def parse(algStr: str) -> Algorithm:
        """
        Parses a string representation of an algorithm into an Algorithm object.

        :param algStr: The string representation of the algorithm to be consumed.

        :rtype: Algorithm
        :returns: An `Algorithm` object corresponding to the input string.

        >>> Algorithm.parse("U R2 F' 3Rw2 (R U')3 D") -> Algorithm(...)
        """
        tokens = Algorithm._tokenize(algStr)
        stk = []
        for t in tokens:
            if t.startswith(')'):
                # how many times to repeat inner alg?
                if t == ')': mul = 1
                else:
                    tail = t[1:]
                    if (mul := int(tail)) <= 0:
                        raise InvalidAlgorithmError(f"Invalid multiplier in token: {tail}")
                # pop til '(' and remove it
                inner = []
                while stk[-1] != '(':
                    inner.append(stk.pop())
                    if not stk:
                        raise InvalidAlgorithmError("Unmatched ')' in algorithm string.")
                stk.pop()
                # repeat inner alg and push stk
                innerAlg = Algorithm(inner[::-1])
                stk.extend((innerAlg * mul)._movs)
            elif t == '(':
                stk.append(t)
            else:
                stk.append(Move.parse(t))

        if '(' in stk:
            raise InvalidAlgorithmError("Unmatched '(' in algorithm string.")

        return Algorithm(stk)

    def simplify(self):
        """Simplifies the algorithm in place."""
        self._movs = simplified(self)._movs.copy()

    def commutator(self, other: 'Algorithm') -> 'Algorithm':
        """
        Given algorithms ``A`` and ``B``, will return their commutator.

        :param other: The other algorithm ``B`` to commute with.

        :rtype: Algorithm
        :returns: The commutator algorithm, ``[A,B]=A+B+(-A)+(-B)``
        """
        return self + other - self - other

    def conjugate(self, other: 'Algorithm') -> 'Algorithm':
        """
        Given algorithms ``A`` and ``B``, will return the conjugation of ``A`` by ``B``.

        :param other: The setup algorithm ``B``

        :rtype: Algorithm
        :returns: The conjugation, ``[A:B]=A+B+(-A)``
        """
        return self + other - self

    def __iter__(self):
        return iter(self._movs)

    def mirror(self):
        """Returns the mirror of the algorithm, making right-handed algorithms left-handed and vice versa."""
        return Algorithm([m.mirror() for m in self._movs])


def simplified(alg: Algorithm) -> Algorithm:
    """
    Returns the naive simplification of a given algorithm.

    :param alg: The ``Algorithm`` to simplify.

    :rtype: Algorithm
    :returns: The simplified algorithm.

    >>> simplified(Algorithm("F U R' U' U R2")) -> Algorithm("F U R")

    .. Notes::
    Note that for all ``a:Algorithm`` we have ``len(a) >= len(simplified(a))`` and ``a == simplified(a)``.
    """
    stk: list[Move] = []

    for move in alg:
        if stk:
            top = stk[-1]
            if (top.mov == move.mov) and (top.width == move.width):
                stk.pop()
                if (total := (top.mod + move.mod) % 4) != 0:
                    stk.append(Move(move.width, move.mov, total))
                continue
        stk.append(move)
    return Algorithm(stk)
