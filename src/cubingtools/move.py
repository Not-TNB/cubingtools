"""
Classes and methods working with the internal representation of cube moves.
"""

from .error import InvalidMoveError
from enum import IntEnum, StrEnum
import re

########################################################################################################################

_MOVE_LEXER_REGEX = re.compile(r"\d*|[A-Za-z]|w?|[2']?")

########################################################################################################################

class _Mod(IntEnum):
    CW = 1
    HALF = 2
    CCW = 3

    def _matchup(self, cw, half, ccw):
        match self:
            case _Mod.CW   : return cw
            case _Mod.HALF : return half
            case _Mod.CCW  : return ccw

    def __str__(self) -> str:
        return self._matchup('', '2', "'")

    def __repr__(self) -> str:
        return self._matchup('1',  '2', '-1')

    def __neg__(self) -> '_Mod':
        return self._matchup(_Mod.CCW, _Mod.HALF, _Mod.CW)

    @classmethod
    def parse(cls, s) -> '_Mod':
        s = str(s)
        if s in ('', '1'):
            return cls.CW
        elif s == '2':
            return cls.HALF
        elif s in ("'", '-1'):
            return cls.CCW
        else:
            raise ValueError(f"Invalid modifier string: {s}")

MODS = list(_Mod)

########################################################################################################################

class _BaseMove(StrEnum):
    XRot = 'x'
    YRot = 'y'
    ZRot = 'z'
    UBig = 'u'
    FBig = 'f'
    RBig = 'r'
    BBig = 'b'
    LBig = 'l'
    DBig = 'd'
    UTurn = 'U'
    FTurn = 'F'
    RTurn = 'R'
    BTurn = 'B'
    LTurn = 'L'
    DTurn = 'D'
    MSlice = 'M'
    ESlice = 'E'
    SSlice = 'S'

ALL_MOVS = list(_BaseMove)

_MOVE_FACES = tuple(
    m.value
    for m in _BaseMove
    if m.name.endswith("Turn")
)

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
        if width <= 0: raise InvalidMoveError(self)

        self.width = width

        match mov:
            case _BaseMove() : self.mov = mov
            case str()       : self.mov = _BaseMove(mov)
            case _: raise InvalidMoveError(self)

        match mod:
            case _Mod() : self.mod = mod
            case int()  : self.mod = _Mod(mod)
            case str()  : self.mod = _Mod.parse(mod)
            case _: raise InvalidMoveError(self)

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

        guardFace = lambda x: throw() if x not in _MOVE_FACES else None

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
                return Move(2, mov, mod)  # ex. Rw === 2Rw
            case [width, mov, 'w']:
                width = parseWidth(width)
                guardFace(mov)
                return Move(width, mov, 1)
            case [width, mov, 'w', mod]:
                width = parseWidth(width)
                mod = parseMod(mod)
                guardFace(mov)
                return Move(width, mov, mod)
            case _:
                throw()
                return None
