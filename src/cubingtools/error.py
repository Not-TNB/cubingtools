'''
Custom errors raise-able in the module
'''

class InvalidMoveError(ValueError):
    def __init__(self, move: str):
        self.move = move
        super().__init__(f"Invalid move: {move}")

class InvalidAlgorithmError(ValueError):
    def __init__(self, algo: str, reason: str):
        self.algo = algo
        self.reason = reason
        super().__init__(f"Invalid algorithm: {algo} \nwith reason: {reason}")