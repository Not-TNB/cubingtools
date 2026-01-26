'''
Classes and methods working with the internal representation of moves and algorithms,
which can be performed on cubes.
'''

import operator
import re
from cubingtools.constants import *
from cubingtools.error import *

class Move:
    def __init__(self, width: int=1, mov: str='U', mod: str='1'):
        '''
        Represents a single move on the cube.

        :param width: The number of layers to turn (default is 1).
        :param mov: The move notation (e.g., 'U', 'R', 'F', 'D', 'L', 'B', 'x', 'y', 'z', etc.).
        :param mod: The modifier for the move ('1' for clockwise, "'" for counter-clockwise, '2' for 180 degrees).
        '''
        def raiseInvalid(): raise ValueError(f'Invalid move: {mov}.')

        if mov in ALL_MOVS: self.mov = mov
        else: raiseInvalid()

        self.width = 1
        if mov in W_MOVS:
            if width > 1: self.width = width
            else: raiseInvalid()

        if mod in MODS or mod == '1': self.mod = mod
        else: raiseInvalid()
    
    def __repr__(self):
        return f"Move(width={self.width}, mov=\"{self.mov}\", mod=\"{self.mod}\")"
    
    def __neg__(self) -> 'Move':
        '''Returns the inverse of the move.'''
        match self.mod:
            case '2': return self
            case '1': return Move(self.width, self.mov, "'")
            case "'": return Move(self.width, self.mov, '1')
    
    def __str__(self) -> str:
        '''Returns the string representation of the move.'''
        return ((str(self.width) if self.width>2 else '') +
                 self.mov +
                (self.mod if self.mod!='1' else ''))

class Algorithm:
    def __init__(self, moves: list[Move] | None | str = None):
        '''
        Represents a sequence of moves (an algorithm) on the cube.

        :param movs: A list of `Move` objects representing the sequence of moves.
        '''
        if isinstance(moves, str): self.movs = toAlgo(moves).movs
        else: self.movs = moves or []
    
    def inverse(self) -> 'Algorithm':
        '''Returns the inverse of the algorithm.'''
        return Algorithm([-move for move in self.movs[::-1]])
    def __neg__(self) -> 'Algorithm':
        '''Returns the inverse of the algorithm.'''
        return self.inverse()
    
    def __repr__(self):
        padLen = len(str(len(self) - 1))
        out = list(map(
                operator.add,
                [f"{i:>{padLen}}: " for i in range(len(self))],
                [repr(move) for move in self.movs]))
        return '\n'.join(out)
    
    def __str__(self) -> str:
        '''Returns the string representation of the algorithm.'''
        return ' '.join([str(move) for move in self.movs])

    def __add__(self, other) -> 'Algorithm':
        '''Concatenates two algorithms. 
        Accepts addition of an algorithm with one of the following types: 
        Move, Algorithm, String, List[Move]'''
        if isinstance(other, Move)      : return Algorithm(self.movs + [other])
        if isinstance(other, str)       : return Algorithm(self.movs + toAlgo(other).movs)
        if isinstance(other, Algorithm) : return Algorithm(self.movs + other.movs)
        if isinstance(other, list)      : return Algorithm(self.movs + other)
        raise TypeError(f'Cannot add Algorithm with type {type(other)}.')
    
    def __mul__(self, times:int) -> 'Algorithm':
        '''Repeats the algorithm a specified number of times.'''
        if times < 1: raise ValueError("Times must be a positive integer.")
        return Algorithm(self.movs * times)
    
    def __len__(self) -> int: 
        '''Returns the number of moves making up the algorithm.'''
        return len(self.movs)

###################################################################################################

def toMove(tok: str) -> Move:
    '''
    Parses a string token into a Move.

    :param tok: The string representation of the move (e.g., U, R2, 3Fw', etc.) to be consumed.

    :rtype: Move
    :returns: A `Move` object corresponding to the token.
    '''

    # helper parsing/guarding functions; raises invalid moves if applicable.
    def parseWidth(dig): 
        if not dig.isdigit()   : raise InvalidMoveError(tok)
        if (d := int(dig)) < 2 : raise InvalidMoveError(tok)
        return d
    def guardList(x, xs): 
        if x not in xs: raise InvalidMoveError(tok)
    guardMov = lambda mov: guardList(mov, ALL_MOVS)
    guardMod = lambda mod: guardList(mod, MODS)

    tokens = [t for t in re.findall(MOVE_LEXER_REGEX, tok) if t != '']

    match tokens:
        case [t]:
            guardMov(t)
            return Move(1, t, '1')
        case [mov,'w']:
            guardMov(mov)
            return Move(2, mov+'w', '1')
        case [mov,mod]:
            guardMov(mov)
            guardMod(mod)
            return Move(1, mov, mod)
        case [mov,'w',mod]:
            guardMov(mov)
            guardMod(mod)
            return Move(2, mov+'w', mod)
        case [width,mov,'w']:
            width = parseWidth(width)
            guardMov(mov)
            return Move(width, mov+'w', '1')   
        case [width,mov,'w',mod]:
            width = parseWidth(width)
            guardMov(mov)
            guardMod(mod)
            return Move(width, mov+'w', mod)
        case _: raise InvalidMoveError(tok)

def toAlgo(algStr: str) -> Algorithm:
    '''
    Parses a string representation of an algorithm into an Algorithm object. 
    
    :param algStr: The string representation of the algorithm to be consumed.

    :rtype: Algorithm
    :returns: An `Algorithm` object corresponding to the input string.

    >>> toAlgo("U R2 F' 3Rw2 (R U')3 D") -> Algorithm(...)
    '''
    tokens = re.findall(ALGORITHM_LEXER_REGEX, algStr)
    stk = []
    for t in tokens:
        if t.startswith(')'):
            # how many times to repeat inner alg?
            if t == ')': mul = 1
            else: 
                if (dig := t[1:]).isdigit(): mul = int(dig)
                else: raise InvalidAlgorithmError(algStr, f"Invalid multiplier in token: {t}")
            # pop til '(' and remove it
            inner = []
            while stk[-1] != '(':
                inner.append(stk.pop())
                if not stk: 
                    raise InvalidAlgorithmError(algStr, "Mismatched parentheses in algorithm string.")
            stk.pop()
            # repeat inner alg and push stk
            innerAlg = Algorithm(inner[::-1])
            stk.extend((innerAlg * mul).movs)
        elif t == '(': stk.append(t)
        else: stk.append(toMove(t))

    if '(' in stk:
        raise InvalidAlgorithmError(algStr, "Unmatched '(' in algorithm string.")
    
    return Algorithm(stk)