"""Contains the private `_Mod` enum class"""

from enum import IntEnum

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

    @staticmethod
    def parse(s) -> '_Mod':
        s = str(s)
        if s in ('', '1'):
            return _Mod.CW
        elif s == '2':
            return _Mod.HALF
        elif s in ("'", '-1', '3'): # NOTE: this allows things like Rw3 to be parsed correctly.
            return _Mod.CCW
        else:
            raise ValueError(f"Invalid modifier string: {s}")
