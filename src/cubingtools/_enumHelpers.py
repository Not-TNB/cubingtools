"""Contains some enums used in the move.py, algorithm.py and cube.py methods/classes."""

from enum import StrEnum, IntEnum

class _CubeFace(StrEnum):
    U = 'U'
    F = 'F'
    R = 'R'
    B = 'B'
    L = 'L'
    D = 'D'

FACES = list(_CubeFace)

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