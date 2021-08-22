from enum import Enum

class TokenKind(Enum):
    RESERVED=1
    NUM=2
    TK_EOF=3

class Test():
    def __init__(self,a=None):
        self.a=a
        pass

test=Test(1)

a=1

print("いんせおｒｎ%d" %a)
