from algorithm import *
from functools import wraps

class CubeN:
    def __init__(self, n:int=3, cols:str='wgrboy'):
        '''
        Initialize a solved NxNxN Rubik's Cube, defaulting to the classic 3x3 
        and standard color scheme (white, green, red, blue, orange, yellow).

        ### Parameters:
        - `n`: Size of the cube (n x n x n)
        - `cols`: Symbol (color) on each face of the cube (In the order UFRBLD)

        >>> myCube  = CubeN()                   # 3x3 cube with standard color scheme
        >>> revenge = CubeN(n=4, cols='abcdef') # 4x4 cube with custom color scheme
        '''
        if n <= 1             : raise ValueError("Cube size must be at least 2")
        if len(cols) != 6     : raise ValueError("There must be exactly 6 colors for the cube faces")
        if len(set(cols)) != 6: raise ValueError("Colors for the cube faces must be unique")

        self.size = n
        self.area = n * n
        self.cols = cols

        # Generate solved and initial state
        def genFaceMat(col:str) -> list[list[str]]:
            '''Generate a face matrix filled with the given color.'''
            return [[col for _ in range(self.size)] for _ in range(self.size)]
        stateKs = 'UFRBLD'
        stateVs = list(map(genFaceMat, self.cols))
        self.state = self.solved = dict(zip(stateKs, stateVs))

    def validateFace(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Prefer an instance attribute 'face' if present, otherwise fall back to the
            # first positional argument or a 'face' keyword argument.
            face = getattr(self, 'face', None)
            if face is None:
                if args: face = args[0]
                else: face = kwargs.get('face', None)
            if not isinstance(face, str) or face not in 'UFRBLD' or len(face) != 1:
                raise ValueError("Face must be one of 'U', 'F', 'R', 'B', 'L', 'D'")
            return func(self, *args, **kwargs)
        return wrapper

    @validateFace
    def rotFC(self, face:str) -> list[list[str]]:
        '''
        Returns the clockwise roation of a single face.

        ### Parameters:
        - `face`: One of 'U', 'F', 'R', 'B', 'L', 'D' representing the face to rotate.
        '''
        return [list(row) for row in zip(*self.state[face][::-1])]
    @validateFace
    def rotFA(self, face:str) -> list[list[str]]:
        '''
        Returns the anti-clockwise roation of a single face.

        ### Parameters:
        - `face`: One of 'U', 'F', 'R', 'B', 'L', 'D' representing the face to rotate.

        ### Returns:
        - The rotated face as a 2D list.
        ''' 
        return list(list(x) for x in zip(*self.state[face]))[::-1]
    @validateFace
    def rotF2(self, face:str) -> list[list[str]]:
        '''
        Returns the 180 degree roation of a single face.

        ### Parameters:
        - `face`: One of 'U', 'F', 'R', 'B', 'L', 'D' representing the face to rotate.

        ### Returns:
        - The rotated face as a 2D list.
        '''
        return [row[::-1] for row in self.state[face][::-1]]
    
    @validateFace
    def showFace(self, face:str) -> str:
        '''
        Print a single face of the cube.

        ### Parameters:
        - `face`: One of 'U', 'F', 'R', 'B', 'L', 'D' representing the face to print.

        ### Returns:
        - A string representation of the specified face.
        '''
        out  = '┌' + '──'*(self.size-1) + '───┐\n'
        out += '\n'.join(['│ ' + ' '.join(row) + ' │' for row in self.state[face]])
        out += '\n└' + '──'*(self.size-1) + '───┘'

        return out
        
    def __repr__(self) -> str:
        '''Print's a net of the cube's current state.'''
        space = ' '*(2*self.size+2)
        bordr = '─'*(2*self.size+1)

        # print B face
        out = space + '┌' + bordr + '┐\n'
        for row in self.rotF2('B'):
            out += space + '│ ' + ' '.join(row) + ' │\n'

        # print L, U, R, D faces
        zipFaces = zip(self.rotFC('L'), self.state['U'], self.rotFA('R'), self.rotF2('D'))
        out += '┌' + bordr + '┼' + bordr + '┼' + bordr + '┬' + bordr + '┐\n'
        for l,u,r,d in zipFaces:
            out += '│ ' + ' '.join(l) + ' │ ' + ' '.join(u) + ' │ ' + ' '.join(r) + ' │ ' + ' '.join(d) + ' │\n'
        out += '└' + bordr + '┼' + bordr + '┼' + bordr + '┴' + bordr + '┘\n'

        # print F face
        space = ' '*(2*self.size+2)
        bordr = '─'*(2*self.size+1)
        for row in self.state['F']:
            out += space + '│ ' + ' '.join(row) + ' │\n'
        out += space + '└' + bordr + '┘'

        return out
    
    def __str__(self) -> str:
        '''Print's a net of the cube's current state.'''
        return self.__repr__()
    
    def uTurn(self, n:int=1) -> 'CubeN':
        '''
        Rotates the top `n` layers of the cube clockwise.

        ### Parameters:
        - `n`: The number of layers to turn along the U face

        Note that `uTurn(1) === "U"` and `uTurn(n>=2) === "nUw"`.
        Will error if `n>=self.size`
        '''
        if n<1 or n>=self.size:
            raise ValueError(f"n must be stricly 1 or more, and strictly less than self.size (your n={n})")

        # Rotate U
        self.state['U'] = self.rotFC('U')

        # Apply effects to other layers
        for i in range(n):
            (self.state['F'][i][:], self.state['R'][i][:], self.state['B'][i][:], self.state['L'][i][:]) = (
            self.state['R'][i][:], self.state['B'][i][:], self.state['L'][i][:], self.state['F'][i][:])
        
        return self
    
    def xRot(self) -> None:
        '''Rotates the entire cube along the x-axis clockwise.'''
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self.state['F'], self.rotFC('R'), self.rotFA('L'), self.rotF2('B'), self.state['D'], self.rotF2('U'))
    def yRot(self) -> None:
        '''Rotates the entire cube along the y-axis clockwise.'''
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self.rotFC('U'), self.state['B'], self.state['F'], self.rotFA('D'), self.state['R'], self.state['L'])
    def zRot(self) -> None:
        '''Rotates the entire cube along the z-axis clockwise.'''
        (self.state['U'], self.state['R'], self.state['L'], self.state['D'], self.state['F'], self.state['B']) = (
         self.rotFC('L'), self.rotFC('U'), self.rotFC('D'), self.rotFC('R'), self.rotFC('F'), self.rotFA('B'))

    def turn(self, move: Move) -> None:
        '''
        Executes a given `Move` to the cube's state.

        ### Parameters:
        - `move`: The `Move` to execute on the cube.
        '''        
        width, mov, mod = move.width, move.mov, move.mod

        if mod == '\'': 
            for _ in range(3): self.turn(Move(width, mov, '1'))
            return
        if mod == '2': 
            for _ in range(2): self.turn(Move(width, mov, '1'))
            return
        
        uMov = 'U' if width==1 else f'{width}Uw'

        match mov[0]:
            case 'x': self.xRot()
            case 'y': self.yRot()
            case 'z': self.zRot()      
            case 'U': self.uTurn(width)

            case 'D': self.algo(f'x2 {uMov} x2')
            case 'L': self.algo(f'z {uMov} z\'')      
            case 'R': self.algo(f'z\' {uMov} z')
            case 'F': self.algo(f'x {uMov} x\'')
            case 'B': self.algo(f'x\' {uMov} x')
            case 'M': self.algo('L\' R x\'')
            case 'E': self.algo('U D\' y\'')
            case 'S': self.algo('F\' B z')

            case 'u': self.algo('y D')
            case 'd': self.algo('y\' U')
            case 'l': self.algo('x\' R')
            case 'r': self.algo('x L')
            case 'f': self.algo('z B')
            case 'b': self.algo('z\' F')

    def algo(self, alg) -> None:
        '''
        Executes a given `Move` or `Algorithm` to the cube's state.

        ### Parameters:
        - `alg`: The `Move` or `Algorithm` to execute on the cube.

        >>> myCube = CubeN(3) ; alg1 = "R U R' U'"
        >>> myCube.algo(alg1)
        '''
        if   isinstance(alg, Move): self.turn(alg)
        elif isinstance(alg, str): self.algo(toAlgo(alg))
        elif isinstance(alg, Algorithm): 
            for m in alg.movs: self.turn(m)
        else:
            raise TypeError(f"Cannot execute the type {type(alg)} on a cube.")
    def __rshift__(self, alg) -> 'CubeN': 
        '''
        Same as `algo`, but also returns the cube (good for chaining algorithms).

        >>> myCube = CubeN(3) ; alg1 = "R U R' U'" ; alg2 = "F2 B2"
        >>> myCube >> alg1 >> alg2
        '''
        self.algo(alg)
        return self