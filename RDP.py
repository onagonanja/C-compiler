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
    LVAL=12 #ローカル変数
    ASSIGN=13 #=

#ノードクラス
class Node():
    def __init__(self,kind=None,left=None,right=None,val=None,offset=0):
        self.kind=kind
        self.left=left
        self.right=right
        self.val=val
        self.offset=offset
        #print(self.kind)

#program=stmt*
def program():
    code=[]
    while not at_eof():
        code.append(stmt())
    return code

#stmt=expr ";" |"return" expr ";"
def stmt():
    if consume_ret():
        node =Node(NodeKind.RET,left=expr())
    else:
        node =expr()
    expect(";")
    return node

#expr=assign
def expr():
    node=assign()
    return node

#assign=equal ("="assign)?
def assign():
    node=equal()
    if consume("="):
        node=Node(NodeKind.ASSIGN,node,assign())
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
        node=expr()
        expect(')')
        return node

    str=consume_val()
    if str:
        LVAL=FindLval(str)
        if LVAL==None:
            global local
            lval=Lval(next=local,name=str,offset=local.offset+8)
            node=Node(NodeKind.LVAL,offset=lval.offset)
            local=lval
        else:
            node=Node(NodeKind.LVAL,offset=LVAL.offset)
        return node

    node=Node(kind=NodeKind.NUM,val=expectNum())
    return node

#ローカル変数クラス
class Lval():
    def __init__(self,next=None,name="",offset=0):
        self.next=next
        self.name=name
        self.offset=offset

#ローカル変数
local=Lval()

#ローカル変数を探す関数
def FindLval(str):
    global local 
    lval=local

    while True:
        if lval.name==str:
            return lval
        elif lval.next==None:
            return None
        lval=lval.next