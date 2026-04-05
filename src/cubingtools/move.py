"""
Classes and methods working with the internal representation of cube moves.
"""

from .error import InvalidMoveError
from ._enumHelpers import _Mod, _BaseMove, FACES
import re

########################################################################################################################

_MOVE_LEXER_REGEX = re.compile(r"\d*|[A-Za-z]|w?|[2']?")

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
        modStr = str(self.mod) if self.mod != _Mod.CW else ''
        return lay + self.mov + w + modStr

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

        guardFace = lambda x: throw() if x not in FACES else None

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

    def mirror(self):
        """Returns the mirror of the move."""

        def mir(new): return -Move(self.width, new, self.mod)

        match self.mov:
            case 'x' : return self
            case 'y' : return -self
            case 'z' : return -self
            case 'u' : return -self
            case 'f' : return -self
            case 'r' : return mir(_BaseMove.LBig)
            case 'b' : return -self
            case 'l' : return mir(_BaseMove.RBig)
            case 'd' : return -self
            case 'U' : return -self
            case 'F' : return -self
            case 'R' : return mir(_BaseMove.LTurn)
            case 'B' : return -self
            case 'L' : return mir(_BaseMove.RTurn)
            case 'D' : return -self
            case 'M' : return self
            case 'E' : return -self
            case 'S' : return -self
            case _   : raise InvalidMoveError(f"Invalid move to mirror: {self.mov}")