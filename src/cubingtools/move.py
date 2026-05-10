"""
Classes and methods working with the internal representation of cube moves.
"""

from .error import InvalidMoveError
from ._enumHelpers import _Mod, _BaseMove, _FACES
import re

########################################################################################################################

_MOVE_LEXER_REGEX = re.compile(r"\d*|[A-Za-z]|w?|[2']?")

########################################################################################################################

_MIRROR_MAP = {
    _BaseMove.RBig: _BaseMove.LBig,
    _BaseMove.LBig: _BaseMove.RBig,

    _BaseMove.RTurn: _BaseMove.LTurn,
    _BaseMove.LTurn: _BaseMove.RTurn,

    _BaseMove.FBig: _BaseMove.FBig,
    _BaseMove.BBig: _BaseMove.BBig,
    _BaseMove.UBig: _BaseMove.UBig,
    _BaseMove.DBig: _BaseMove.DBig,

    _BaseMove.FTurn: _BaseMove.FTurn,
    _BaseMove.BTurn: _BaseMove.BTurn,
    _BaseMove.UTurn: _BaseMove.UTurn,
    _BaseMove.DTurn: _BaseMove.DTurn,

    _BaseMove.MSlice: _BaseMove.MSlice,
    _BaseMove.ESlice: _BaseMove.ESlice,
    _BaseMove.SSlice: _BaseMove.SSlice,

    _BaseMove.XRot: _BaseMove.XRot,
    _BaseMove.YRot: _BaseMove.YRot,
    _BaseMove.ZRot: _BaseMove.ZRot,
}

_MIRROR_FLIP = frozenset({
    _BaseMove.RBig,
    _BaseMove.LBig,
    _BaseMove.FBig,
    _BaseMove.BBig,
    _BaseMove.UBig,
    _BaseMove.DBig,

    _BaseMove.RTurn,
    _BaseMove.LTurn,
    _BaseMove.FTurn,
    _BaseMove.BTurn,
    _BaseMove.UTurn,
    _BaseMove.DTurn,

    _BaseMove.YRot,
    _BaseMove.ZRot,

    _BaseMove.ESlice,
    _BaseMove.SSlice,
})

########################################################################################################################

_DEG_3_MOVES = frozenset({
    _BaseMove.MSlice, _BaseMove.ESlice, _BaseMove.SSlice,
    _BaseMove.UBig, _BaseMove.DBig, _BaseMove.LBig, _BaseMove.RBig, _BaseMove.FBig, _BaseMove.BBig,
})

########################################################################################################################

class Move:
    def __init__(self,
                 width: int = 1,
                 mov: str | _BaseMove = _BaseMove.UTurn,
                 mod: int | str | _Mod = _Mod.CW):
        """
        Initializes a ``Move`` object a representing single move on a cube.

        :param width: The number of layers to turn (default is 1).
        :param mov: The base move notation (e.g., 'U', 'R', 'F', 'D', 'L', 'B', 'x', 'y', 'z', etc.).
        :param mod: The modifier for the move ('1' for clockwise, "'" for counter-clockwise, '2' for 180 degrees).
        """
        if width <= 0:
            raise InvalidMoveError(f"Invalid width: {width}")

        self.width = width

        match mov:
            case _BaseMove():
                self.mov = mov
            case str():
                self.mov = _BaseMove(mov)
            case _:
                raise InvalidMoveError(f"Invalid move: {mov}")

        match mod:
            case _Mod():
                self.mod = mod
            case int():
                self.mod = _Mod(mod)
            case str():
                self.mod = _Mod.parse(mod)
            case _:
                raise InvalidMoveError(f"Invalid mod: {mod}")

        self.degree = self.width+1
        if mov in _DEG_3_MOVES: self.degree = max(self.degree, 3)

    def __repr__(self):
        return f'Move({self.width}, {self.mov}, {self.mod})'

    def __neg__(self) -> 'Move':
        """Returns the inverse of the move."""
        return Move(self.width, self.mov, -self.mod)

    def __str__(self) -> str:
        """Returns the string representation of the move."""
        lay = str(self.width) if self.width > 2 else ''
        w = 'w' if self.width >= 2 else ''
        modStr = str(self.mod) if self.mod != _Mod.CW else ''
        return lay + str(self.mov) + w + modStr

    @staticmethod
    def parse(tok: str) -> 'Move | None':
        """
        Parses a string token into a Move.

        :param tok: The string representation of the move (e.g., U, R2, 3Fw', etc.) to be consumed.

        :rtype: Move
        :returns: A `Move` object corresponding to the token.
        """
        def throw(): raise InvalidMoveError(f"Invalid move: {tok}")

        def parseWidth(dig):
            if not dig.isdigit(): throw()
            if (d := int(dig)) < 2: throw()
            return d

        def parseMov(m):
            try: return _BaseMove(m)
            except ValueError: throw()

        def parseMod(m):
            try: return _Mod.parse(m)
            except ValueError: throw()

        def guardFace(x):
            try:
                if _BaseMove(x) not in _FACES: throw()
            except ValueError:
                throw()

        tokens = [t for t in re.findall(_MOVE_LEXER_REGEX, tok) if t != '']

        match tokens:
            case [t]:
                mov = parseMov(t)
                return Move(1, mov, 1)

            case [mov, 'w']:
                guardFace(mov)
                return Move(2, mov, 1)

            case [mov, mod]:
                mov = parseMov(mov)
                mod = parseMod(mod)
                return Move(1, mov, mod)

            case [mov, 'w', mod]:
                guardFace(mov)
                mod = parseMod(mod)
                return Move(2, mov, mod)

            case [width, mov, 'w']:
                width = parseWidth(width)
                guardFace(mov)
                return Move(width, mov, 1)

            case [width, mov, 'w', mod]:
                width = parseWidth(width)
                guardFace(mov)
                mod = parseMod(mod)
                return Move(width, mov, mod)

            case _:
                throw()
                return None

    def mirror(self):
        """Returns the mirror of the move."""

        new_mov = _MIRROR_MAP.get(self.mov)
        if new_mov is None:
            raise InvalidMoveError(f"Invalid move to mirror: {self.mov}")

        new_mod = -self.mod if self.mov in _MIRROR_FLIP else self.mod

        return Move(self.width, new_mov, new_mod)