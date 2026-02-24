"""Contains the private `_Mod` enum class"""

from enum import IntEnum

class _Mod(IntEnum):
    CW = 1
    HALF = 2
    CCW = 3

    def __str__(self):
        match self:
            case _Mod.CW: return ''
            case _Mod.HALF: return '2'
            case _Mod.CCW: return "'"

    def __repr__(self):
        match self:
            case _Mod.CW: return '1'
            case _Mod.HALF: return '2'
            case _Mod.CCW: return '-1'

    @staticmethod
    def parse(s) -> '_Mod':
        s = str(s)
        if s in ('','1')     : return _Mod.CW
        elif s == '2'        : return _Mod.HALF
        elif s in ("'",'-1','3') : return _Mod.CCW
        else:
            raise ValueError(f"Invalid modifier string: {s}")

    def __neg__(self) -> '_Mod':
        match self:
            case _Mod.CW: return _Mod.CCW
            case _Mod.HALF: return _Mod.HALF
            case _Mod.CCW: return _Mod.CW