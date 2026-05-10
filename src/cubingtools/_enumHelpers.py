"""DO NOT IMPORT. Contains some enums used in the move.py, algorithm.py and cube.py methods/classes."""

from enum import StrEnum, IntEnum

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
    def parse(_BaseMove, s) -> '_Mod':
        s = str(s)
        if s in ('', '1'):
            return _BaseMove.CW
        elif s == '2':
            return _BaseMove.HALF
        elif s in ("'", '-1'):
            return _BaseMove.CCW
        else:
            raise ValueError(f"Invalid modifier string: {s}")

_MODS = list(_Mod)

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

_SLICES = frozenset({_BaseMove.MSlice, _BaseMove.ESlice, _BaseMove.SSlice})
_ROTS = frozenset({_BaseMove.XRot, _BaseMove.YRot, _BaseMove.ZRot})
_FACES = frozenset({_BaseMove.UTurn, _BaseMove.FTurn, _BaseMove.RTurn, _BaseMove.BTurn, _BaseMove.LTurn, _BaseMove.DTurn})
_FACES_LIST = [_BaseMove.UTurn, _BaseMove.FTurn, _BaseMove.RTurn, _BaseMove.BTurn, _BaseMove.LTurn, _BaseMove.DTurn] # UFRBLD
_WIDES = frozenset({_BaseMove.UBig, _BaseMove.FBig, _BaseMove.RBig, _BaseMove.BBig, _BaseMove.LBig, _BaseMove.DBig})