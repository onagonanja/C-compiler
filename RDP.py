from enum import Enum
from tokenizer import*

#ノードの種類を判別する型
class NodeKind(Enum):
    ADD=1
    SUB=2
    MUL=3
    DIV=4
    NUM=5
    LT=6 #<
    RT=7 #>
    LET=8 #<=
    RET=9 #>=
    EQ=10 #==
    NEQ=11 #!=

#ノードクラス
class Node():
    def __init__(self,kind=None,left=None,right=None,val=None):
        self.kind=kind
        self.left=left
        self.right=right
        self.val=val

#start=equal
def start():
    node=equal()
    return node

#equal = (relate "=="|relate "!=")
def equal():
    node=relate()
    while True:
        if consume("=="):
            node=Node(NodeKind.EQ,node,relate())
        elif consume("!="):
            node=Node(NodeKind.NEQ,node,relate())
        else:
            return node

#relate = add ("<" add | ">" add | "<=" add | ">=" add)
def relate():
    node=add()
    while True:
        if consume("<"):
            node=Node(NodeKind.LT,node,add())
        elif consume(">"):
            node=Node(NodeKind.RT,node,add())
        elif consume("<="):
            node=Node(NodeKind.LET,node,add())
        elif consume(">="):
            node=Node(NodeKind.RET,node,add())
        else:
            return node

#add = mul ("+" mul | "-" mul)*
def add():
    node=mul()
    while True:
        if consume("+"):
            node=Node(NodeKind.ADD,node,mul())
        elif consume("-"):
            node=Node(NodeKind.SUB,node,mul())
        else:
            return node

#mul = unary ("*" unary | "/" unary)*
def mul():
    node=unary()
    while True:
        if consume("*"):
            node=Node(NodeKind.MUL,node,unary())
        elif consume("/"):
            node=Node(NodeKind.DIV,node,unary())
        else:
            return node

#unary = ("+" | "-")? primary
def unary():
    if consume('+'):
        return primary()
    if consume("-"):
        return Node(NodeKind.SUB,Node(kind=NodeKind.NUM,val=0),primary())
    return primary()

#primary = num | "(" start ")"
def primary():
    if consume('('):
        node=start()
        expect(')')
        return node

    node=Node(kind=NodeKind.NUM,val=expectNum())
    return node