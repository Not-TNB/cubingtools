'''
Contains moves, algorithms and other utility constants
'''

# MOVESET
MOVS     = ['U', 'F', 'R', 'B', 'L', 'D']
W_MOVS   = [x+'w' for x in MOVS]
T_MOVS   = [x.lower() for x in MOVS]
ROTS     = ['x', 'y', 'z']
MIDS     = ['M', 'E', 'S']
MODS     = ["'", '2']
ALL_MOVS = MOVS + W_MOVS + T_MOVS + ROTS + MIDS

# REGEXES
MOVE_LEXER_REGEX = r"\d*|[A-Za-z]|w?|[2\']?"
ALGORITHM_LEXER_REGEX = r"\d*[A-Za-z]w?[2\']?|\(|\)\d*"