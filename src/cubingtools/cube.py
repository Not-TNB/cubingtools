"""
Contains the `CubeN` class working with NxN Rubik's cubes for N>=2
"""

from .algorithm import Algorithm
from .move import Move, MODS
from .error import InvalidMoveError
from enum import StrEnum
import random
from copy import deepcopy

########################################################################################################################

class _Face(StrEnum):
    U = 'U'
    F = 'F'
    R = 'R'
    B = 'B'
    L = 'L'
    D = 'D'

FACES = list(_Face)

def _generateScrambleMoveList(n: int):
    match n:
        case 2: return deepcopy(FACES[:3])
        case 3: return deepcopy(FACES)
        case _:
            result = deepcopy(FACES)
            for i in range(2, 1 + n // 2):
                result += [str(i) + m + 'w' for m in FACES]
            return result

########################################################################################################################

class CubeN:
    def __init__(self, n: int = 3, cols: str = 'wgrboy'):
        """
        Initializes a solved NxNxN Rubik's Cube, defaulting to the classic 3x3
        and standard color scheme (white, green, red, blue, orange, yellow).

        :param n: Size of the cube (NxNxN)
        :param cols: Symbol (color) on each face of the cube (In the order UFRBLD)

        >>> myCube  = CubeN()                   # 3x3 cube with standard color scheme (wgrboy)
        >>> revenge = CubeN(n=4, cols='abcdef') # 4x4 cube with custom color scheme
        """
        if n <= 1: raise ValueError("Cube size must be at least 2")
        if len(cols) != 6: raise ValueError("There must be exactly 6 colors for the cube faces")
        if len(set(cols)) != 6: raise ValueError("Colors for the cube faces must be unique")

        self.size = n
        self.cols = cols

        self._ms = _generateScrambleMoveList(n)

        # Generate solved and initial state
        def genFaceMat(col: str) -> list[list[str]]:
            """Generate a face matrix filled with the given color."""
            return [[col for _ in range(self.size)] for _ in range(self.size)]

        stateKs = FACES
        stateVs = list(map(genFaceMat, self.cols))

        self.state = dict(zip(stateKs, deepcopy(stateVs)))
        self.solved = deepcopy(self.state)

    def showFace(self, face: str) -> str:
        """
        Print a single face of the cube.

        :param face: The face to display.

        :rtype: str
        :returns: A string representation of the specified face.
        """
        self._validateFace(face)
        bordr = "──" * (self.size - 1)
        out = f'┌{bordr}───┐\n'
        out += '\n'.join([f'│ {" ".join(row)} │' for row in self.state[face]])
        out += f'\n└{bordr}───┘'
        return out

    def __repr__(self) -> str:
        """Print's a net of the cube's current state."""
        space = ' ' * (2 * self.size + 2)
        bordr = '─' * (2 * self.size + 1)
        uTop = f'{space}┌{bordr}┐\n'
        dBot = f'{space}└{bordr}┘\n'
        lurdTop = f'┌{bordr}┼{bordr}┼{bordr}┬{bordr}┐\n'
        lurdBot = f'└{bordr}┼{bordr}┼{bordr}┴{bordr}┘\n'
        zipLURDFaces = zip(self.state['L'], self.state['F'], self.state['R'], self.state['B'])
        showRow = lambda r: f'{space}│ {" ".join(r)} │\n'

        # print U face
        out = uTop
        for row in self.state['U']: out += showRow(row)
        # print LFRD faces
        out += lurdTop
        for l, u, r, d in zipLURDFaces:
            out += f'│ {" ".join(l)} │ {" ".join(u)} │ {" ".join(r)} │ {" ".join(d)} │\n'
        out += lurdBot
        # print D face
        for row in self.state['D']: out += showRow(row)
        out += dBot

        return out

    def __str__(self) -> str:
        """Print's a net of the cube's current state."""
        return self.__repr__()

    @staticmethod
    def _validateFace(face: str):
        if not isinstance(face, str) or (face not in FACES) or (len(face) != 1):
            raise ValueError(f"Face must be one of {FACES}")

    def _rtFC(self, face: str) -> list[list[str]]:
        """Rotates a face (NOT A LAYER) clockwise."""
        self._validateFace(face)
        return [list(row) for row in zip(*self.state[face][::-1])]

    def _rtFA(self, face: str) -> list[list[str]]:
        """Rotates a face (NOT A LAYER) anticlockwise."""
        self._validateFace(face)
        return list(list(x) for x in zip(*self.state[face]))[::-1]

    def _rtF2(self, face: str) -> list[list[str]]:
        """Rotates a face (NOT A LAYER) by 180 degrees."""
        self._validateFace(face)
        return [row[::-1] for row in self.state[face][::-1]]

    def _uTurn(self, n: int = 1) -> None:
        """
        Rotates the top `n` layers of the cube clockwise.

        :param n: The number of layers to turn along the U face

        :raises ValueError: If ``n>=self.size`` or ``n<=0``.

        .. Notes::
        ``_uTurn(1)`` is equivalent to the move ``U``,
        and ``_uTurn(n>=2)`` is equivalent to ``nUw``.
        """
        if n <= 0 or n >= self.size:
            raise ValueError(f"n must be strictly 1 or more, and strictly less than self.size (your n={n})")
        self.state['U'] = self._rtFC('U')
        for i in range(n):
            (self.state['F'][i][:], self.state['R'][i][:], self.state['B'][i][:], self.state['L'][i][:]) = (
             self.state['R'][i][:], self.state['B'][i][:], self.state['L'][i][:], self.state['F'][i][:])

    def _xRot(self) -> None:
        """Rotates the entire cube along the x-axis clockwise."""
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self.state['F'], self._rtFC('R'), self._rtFA('L'), self._rtF2('B'), self.state['D'], self._rtF2('U'))

    def _yRot(self) -> None:
        """Rotates the entire cube along the y-axis clockwise."""
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self._rtFC('U'), self.state['B'], self.state['F'], self._rtFA('D'), self.state['R'], self.state['L'])

    def _zRot(self) -> None:
        """Rotates the entire cube along the z-axis clockwise."""
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self._rtFC('L'), self._rtFC('U'), self._rtFC('D'), self._rtFC('R'), self._rtFC('F'), self._rtFA('B'))

    def _turn(self, move: Move) -> None:
        """Executes a given `Move` to the cube's state."""
        width, mov, mod = move.width, move.mov, move.mod

        if mod != 1:
            for _ in range(mod): self._turn(Move(width, mov, 1))
            return

        uMov = 'U' if width == 1 else f'{width}Uw'

        match mov:
            case 'x': self._xRot()
            case 'y': self._yRot()
            case 'z': self._zRot()
            case 'U': self._uTurn(width)

            case 'D': self.algo(f"x2 {uMov} x2")
            case 'L': self.algo(f"z {uMov} z'")
            case 'R': self.algo(f"z' {uMov} z")
            case 'F': self.algo(f"x {uMov} x'")
            case 'B': self.algo(f"x' {uMov} x")
            case 'M': self.algo("L' R x'")
            case 'E': self.algo("U D' y'")
            case 'S': self.algo("F' B z")

            case 'u': self.algo("y D'")
            case 'd': self.algo("y' U'")
            case 'l': self.algo("x' R'")
            case 'r': self.algo("x L'")
            case 'f': self.algo("z B'")
            case 'b': self.algo("z' F'")

            case _: raise InvalidMoveError(f"Invalid turn attempted on a cube: {move}")

    def algo(self, alg: Move | str | Algorithm) -> None:
        """
        Executes a given `Move` or `Algorithm` to the cube in-place.

        :param alg: The `Move` or `Algorithm` to execute on the cube.

        >>> myCube = CubeN(3) ; alg1 = "R U R' U'"
        >>> myCube.algo(alg1)

        .. Notes::
        If a `str` is given, it will be parsed as an `Algorithm` first.
        """
        match alg:
            case Move(): self._turn(alg)
            case str() : self.algo(Algorithm.parse(alg))
            case Algorithm():
                for m in alg: self._turn(m)
            case _:
                raise TypeError(f"Cannot execute the type {type(alg)} on a cube.")

    def __rshift__(self, alg: Move | str | Algorithm) -> 'CubeN':
        """
        Executes an algorithm to the cube and returns it (good for chaining algorithms).

        :param alg: The `Move` or `Algorithm` to execute on the cube.

        >>> myCube = CubeN(3) ; alg1 = "R U R' U'" ; alg2 = "F2 B2"
        >>> myCube >> alg1 >> alg2 -> CubeN(...)

        .. Notes::
        For algorithms/moves ``x`` and ``y`` and a cube ``c`` which ``x`` and ``y`` can be executed on,
        ``c>>x+y`` should have the same effect as ``c>>x>>y``.
        """
        self.algo(alg)
        return self

    def isSolved(self) -> bool:
        def faceSolved(mat):
            v = mat[0][0]
            for row in mat:
                for col in row:
                    if col != v: return False
            return True
        for face in self.state.values():
            if not faceSolved(face): return False
        return True

    def reset(self) -> None:
        """Resets the cube to its initial state."""
        self.state = deepcopy(self.solved)

    def _randMove(self) -> Move:
        """Returns a random scramble move"""
        mov = random.choice(self._ms)
        mod = random.choice(MODS)
        return Move.parse(mov + str(mod))

    def __hash__(self) -> int:
        return hash(''.join([''.join(''.join(r) for r in self.state[f]) for f in FACES]))

    def scramble(self, m: int | None = None) -> Algorithm:
        """
        Scrambles the cube with randomized moves and returns the generated scramble algorithm.

        :param m: The number of moves to scramble the cube by.
        """
        moves = m or 8*self.size
        states = set()
        algo = Algorithm()
        lastBaseMov = None
        while len(algo) < moves:
            mv = self._randMove()

            if lastBaseMov == mv.mov: continue
            lastBaseMov = mv.mov

            self.algo(mv)
            if self in states:
                self.algo(-mv)
                continue

            states.add(self)
            algo += mv
        return algo
