"""
Classes and methods working with the internal representation of moves and algorithms,
which can be performed on cubes.
"""

from __future__ import annotations
import operator
import re
from .modifier import _Mod
from .constants import *
from .error import *


class Move:
    def __init__(self, width: int = 1, mov: str = 'U', mod: str | _Mod = '1'):
        """
        Initializes a ``Move`` object a representing single move on a cube.

        :param width: The number of layers to turn (default is 1).
        :param mov: The base move notation (e.g., 'U', 'R', 'F', 'D', 'L', 'B', 'x', 'y', 'z', etc.).
        :param mod: The modifier for the move ('1' for clockwise, "'" for counter-clockwise, '2' for 180 degrees).
        """
        if mov not in ALL_MOVS: raise InvalidMoveError(self)
        if width <= 0: raise InvalidMoveError(self)

        self.mov = mov
        self.width = width
        self.mod = mod if isinstance(mod, _Mod) else _Mod.parse(mod)

    def __repr__(self):
        return f'Move({self.width}, {self.mov}, {self.mod})'

    def __neg__(self) -> 'Move':
        """Returns the inverse of the move."""
        return Move(self.width, self.mov, -self.mod)

    def __str__(self) -> str:
        """Returns the string representation of the move."""
        lay = str(self.width) if self.width > 2 else ''
        w = 'w' if self.width >= 2 else ''
        return (lay +
                self.mov + w +
                (str(self.mod) if self.mod != _Mod.CW else ''))

    @staticmethod
    def parse(tok: str) -> Move:
        """
        Parses a string token into a Move.

        :param tok: The string representation of the move (e.g., U, R2, 3Fw', etc.) to be consumed.

        :rtype: Move
        :returns: A `Move` object corresponding to the token.
        """
        def throw(): raise InvalidMoveError(f"Invalid move: {tok}")

        def guardList(x, xs):
            if x not in xs: throw()

        def parseWidth(dig):
            if not dig.isdigit(): throw()
            if (d := int(dig)) < 2: throw()
            return d

        guardAllMov = lambda m: guardList(m, ALL_MOVS)
        guardWideMov = lambda m: guardList(m, MOVS)

        tokens = [t for t in re.findall(MOVE_LEXER_REGEX, tok) if t != '']

        match tokens:
            case [t]:
                guardAllMov(t)
                return Move(1, t, '1')
            case [mov, 'w']:
                guardWideMov(mov)
                return Move(2, mov, '1')
            case [mov, mod]:
                guardAllMov(mov)
                return Move(1, mov, mod)
            case [mov, 'w', mod]:
                guardWideMov(mov)
                return Move(2, mov, mod)  # ex. Rw === 2Rw
            case [width, mov, 'w']:
                width = parseWidth(width)
                guardWideMov(mov)
                return Move(width, mov, '1')
            case [width, mov, 'w', mod]:
                width = parseWidth(width)
                guardWideMov(mov)
                return Move(width, mov, mod)
            case _:
                raise InvalidMoveError(tok)


class Algorithm:
    def __init__(self, moves: Move | list[Move] | str | None = None):
        """
        Represents a sequence of moves (an algorithm) on the cube.

        :param moves: ``None`` (cast to empty algorithms), ``Move`` (cast to a single-move algorithm), ``list[Move]`` or ``str`` (parsed using ``Algorithm.parse()``)
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
    def parse(algStr: str) -> Algorithm:
        """
        Parses a string representation of an algorithm into an Algorithm object.

        :param algStr: The string representation of the algorithm to be consumed.

        :rtype: Algorithm
        :returns: An `Algorithm` object corresponding to the input string.

        >>> Algorithm.parse("U R2 F' 3Rw2 (R U')3 D") -> Algorithm(...)
        """
        tokens = re.findall(ALGORITHM_LEXER_REGEX, algStr)
        stk = []
        for t in tokens:
            if t.startswith(')'):
                # how many times to repeat inner alg?
                if t == ')': mul = 1
                else:
                    if (mul := int(t[1:])) <= 0:
                        raise InvalidAlgorithmError("Invalid multiplier in token:", t)
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
        :returns: The conjugation, ``[A:B]=B+A+(-B)``
        """
        return other + self - other

    def __iter__(self):
        return iter(self._movs)


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
