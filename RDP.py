from enum import Enum
from tokenizer import*

#ノードの種類を判別する型
class NodeKind(Enum):
    ADD=1
    SUB=2
    MUL=3
    DIV=4
    NUM=5

#ノードクラス
class Node():
    def __init__(self,kind=None,left=None,right=None,val=None):
        self.kind=kind
        self.left=left
        self.right=right
        self.val=val

#expr = mul ("+" mul | "-" mul)*
def expr():
    node=mul()
    while True:
        if consume("+"):
            node=Node(NodeKind.ADD,node,mul())
        elif consume("-"):
            node=Node(NodeKind.SUB,node,mul())
        else:
            return node

#mul = primary ("*" primary | "/" primary)*
def mul():
    node=primary()
    while True:
        if consume("*"):
           node=Node(NodeKind.MUL,node,mul())
        elif consume("/"):
            node=Node(NodeKind.DIV,node,mul())
        else:
            return node

#primary = num | "(" expr ")"
def primary():
    if consume('('):
        node=expr()
        expect(')')
        return node

    node=Node(kind=NodeKind.NUM,val=expectNum())
    return node
    
