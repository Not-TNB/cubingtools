'''
Classes and methods working with the internal representation of moves and algorithms,
which can be performed on cubes.
'''

import re
from cubingtools.constants import *

class Move:
    def __init__(self, width:int=1, mov:str='U', mod:str='1'):
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

        if mod in ['1']+MODS: self.mod = mod
        else: raiseInvalid()
    
    def __repr__(self):
        return f"Move(width={self.width}, mov='{self.mov}', mod='{self.mod}')"
    
    def __neg__(self) -> 'Move':
        '''Returns the inverse of the move.'''
        if self.mod == '2': return self
        if self.mod == '1': return Move(self.width, self.mov, "'")
        if self.mod == "'": return Move(self.width, self.mov, '1')
    
    def __str__(self) -> str:
        '''Returns the string representation of the move.'''
        return (str(self.width) if self.width>2 else '') + self.mov + (self.mod if self.mod!='1' else '')

class Algorithm:
    def __init__(self, movs: list[Move] | None = None):
        '''
        Represents a sequence of moves (an algorithm) on the cube.

        :param movs: A list of `Move` objects representing the sequence of moves.
        '''
        self.movs = movs or None
    
    def inverse(self) -> 'Algorithm':
        '''Returns the inverse of the algorithm.'''
        return Algorithm([-move for move in self.movs[::-1]])
    def __neg__(self) -> 'Algorithm':
        '''Returns the inverse of the algorithm.'''
        return self.inverse()
    
    def __str__(self) -> str:
        '''Returns the string representation of the algorithm.'''
        return ' '.join([str(move) for move in self.movs])

    def __add__(self, other) -> 'Algorithm':
        '''Concatenates two algorithms. Accepts addition of an algorithm with one of the following types: Move, Algorithm, String, List[Move]'''
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

################################################################################################

def toMove(tok: str) -> Move:
    '''
    Converts a string token into a Move.

    :param tok: The string representation of the move (e.g., U, R2, 3Fw', etc.).

    :rtype: Move
    :returns: A `Move` object corresponding to the token.
    '''
    def raiseInvalid(): raise ValueError(f'Invalid move token: {tok}')

    token = [t for t in re.findall(r'\d*|[A-Za-z]|w?|[2\']?', tok) if t != '']
    
    match len(token):
        case 1:
            # Only case: it is exactly one of the base moves
            if (t:=token[0]) in ALL_MOVS: return Move(1, t, '1')
            # Invalid!
            else: raiseInvalid()

        case 2:
            # Case 1: 1-base move with modifier
            if (mov:=token[0]) in ALL_MOVS and (mod:=token[1]) in MODS:
                return Move(1, mov, mod)
            # Case 2: wide move without modifier
            elif (token1:=''.join(token)) in W_MOVS:
                return Move(2, token1, '1')
            # Invalid!
            else: raiseInvalid()
        
        case 3:
            # Case 1: wide move with modifier
            if (wMov:=''.join(token[:2])) in W_MOVS and (mod:=token[2]) in MODS:
                return Move(2, wMov, mod)
            # Case 2: wide move with width
            elif (w:=token[0]).isdigit() and (wMov:=''.join(token[1:])) in W_MOVS:
                if (width:=int(w)) >= 2: return Move(width, wMov, '1')
                else: raiseInvalid()
            # Invalid!
            else: raiseInvalid()
        
        case 4:
            # Only case: wide move with width and modifier
            w = token[0]
            wMov = ''.join(token[1:3])
            mod = token[3]
            if not w.isdigit(): raiseInvalid()
            if (width:=int(w)) < 2: raiseInvalid()
            if wMov not in W_MOVS: raiseInvalid()
            if mod not in MODS: raiseInvalid()
            return Move(width, wMov, mod)


def toAlgo(algStr: str) -> Algorithm:
    '''
    Converts a string representation of an algorithm into an Algorithm object. 
    
    :param algStr: The string representation of the algorithm.

    :rtype: Algorithm
    :returns: An `Algorithm` object corresponding to the input string.

    >>> toAlgo("U R2 F' 3Rw2 (R U')3 D") -> Algorithm(...)
    '''
    # split on (optional digits)(one A-Za-z)(optional w)(optional 2 or ')
    #       or (left bracket "(")
    #       or (right bracket ")")(optional digits)
    tokens = re.findall(r'\d*[A-Za-z]w?[2\']?|\(|\)\d*', algStr)
    stk = []
    for t in tokens:
        if t.startswith(')'):
            # how many times to repeat inner alg?
            if t == ')': mul = 1
            else: 
                if (dig:=t[1:]).isdigit(): mul = int(dig)
                else: raise ValueError(f"Invalid multiplier in token: {t}")
            # pop til '(' and remove it
            inner = []
            while stk[-1] != '(':
                inner.append(stk.pop())
                if not stk: raise ValueError("Mismatched parentheses in algorithm string.")
            stk.pop()
            # repeat inner alg and push stk
            innerAlg = Algorithm(inner[::-1])
            stk.extend((innerAlg * mul).movs)
        elif t == '(':
            stk.append(t)
        else:
            stk.append(toMove(t))

    if '(' in stk:
        raise ValueError("Unmatched '(' in algorithm string.")
    return Algorithm(stk)