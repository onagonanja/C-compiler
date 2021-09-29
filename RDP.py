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
    BLOCK=14 #ブロック型
    IF=15
    ELSE=16
    IFEL=17
    WHILE=18
    FOR=19
    NULL=20
    FUNCDEF=21
    FUNCCALL=22
    ARG=23

#ノードクラス
class Node():
    def __init__(self,kind=None,left=None,right=None,val=None,offset=0):
        self.kind=kind
        self.left=left
        self.right=right
        self.val=val
        self.offset=offset
        #print(self.kind)

#ブロック型ノードクラス
class Node_Block():
    def __init__(self,kind=None):
        self.kind=kind
        self.stmt=[]

    def add(self,stmt):
        self.stmt.append(stmt)

#IF文ノードクラス
class Node_IF():
    def __init__(self,kind=None):
        self.kind=kind
    
    def setExpr(self,expr):
        self.expr=expr
    
    def setStmt(self,stmt):
        self.stmt=stmt

    def setElseStmt(self,stmt):
        self.elstmt=stmt

#WHILE型ノードクラス
class Node_While():
    def __init__(self,kind=None):
        self.kind=kind
    
    def setExpr(self,expr):
        self.expr=expr
    
    def setStmt(self,stmt):
        self.stmt=stmt

#FOR型ノードクラス
class Node_For():
    def __init__(self,kind=None):
        self.kind=kind

    def setInit(self,expr):
        self.Init=expr
    
    def setCmp(self,expr):
        self.Cmp=expr
    
    def setReset(self,expr):
        self.Reset=expr
    
    def setStmt(self,stmt):
        self.Stmt=stmt

#ローカル変数クラス
class Lval():
    def __init__(self,next=None,name="",offset=0):
        self.next=next
        self.name=name
        self.offset=offset

#関数定義クラス
class Node_Func():
    def __init__(self,kind=None,name=None):
        global local,arguments,lvalCnt
        local=Lval()
        arguments={}
        lvalCnt=0

        self.kind=kind
        self.name=name
        self.offset=8
        self.args={}
    
    def addArg(self,name):
        global local
        self.args[name]=self.offset
        arguments[name]=self.offset
        self.offset+=8

    def setStmt(self,stmt):
        self.stmt=stmt
    
    def setLvalCnt(self,cnt):
        self.lvalCnt=cnt

#引数クラス
class Node_Arg():
    def __init__(self,kind,name,offset):
        self.kind=kind
        self.name=name
        self.offset=offset

#関数呼出しクラス
class Node_Func_Call():
    def __init__(self,kind,name):
        self.kind=kind
        self.name=name
        self.args=[]
    
    def addArg(self,arg):
        self.args.append(arg)
    
#program=func*
def program():
    code=[]
    while not at_eof():
        code.append(func())
    return code

#func=funcname "(" ((arg ",")* arg)? ")" stmt
def func():
    funcName=consume_val()
    if not funcName:
        error(8)

    node=Node_Func(NodeKind.FUNCDEF,funcName)
    expect("(")
    #引数
    while not at_eof():
        if consume(")"):
            break
        if consume(","):
            continue
        argName=consume_val()
        if not argName:
            print(argName)
            error("引数が正しくありません")
        node.addArg(argName)

    #処理内容
    node.setStmt(stmt())
    global lvalCnt
    print(lvalCnt)
    node.setLvalCnt(lvalCnt)
    return node

#stmt=";"
#    |expr ";" 
#    |"{" stmt* "}"
#    |"return" expr ";"
#    |"if" "(" expr ")" stmt ("else" stmt)? 
#    |"while" "(" expr ")" stmt
#    |"for" "(" expr? ";" expr? ";" expr? ")" stmt

def stmt():
    if consume_ret():
        node =Node(NodeKind.RET,left=expr())
        expect(";")

    elif consume("{"):
        node=Node_Block(NodeKind.BLOCK)
        while not consume("}") and not at_eof():
            node.add(stmt())

    elif consume("if"):
        expect("(")
        if serch_else():
            node=Node_IF(NodeKind.IFEL)
            node.setExpr(expr())
            expect(")")
            node.setStmt(stmt())
            expect("else")
            node.setElseStmt(stmt())
        else:
            node=Node_IF(NodeKind.IF)
            node.setExpr(expr())
            expect(")")
            node.setStmt(stmt())

    elif consume("while"):
        expect("(")
        node=Node_While(NodeKind.WHILE)
        node.setExpr(expr())
        expect(")")
        node.setStmt(stmt())
    
    elif consume("for"):
        expect("(")
        node=Node_For(NodeKind.FOR)
        if not consume(";"):
            node.setInit(expr())
            expect(";")
        if not consume(";"):
            node.setCmp(expr())
            expect(";")
        if not consume(")"):
            node.setReset(expr())
            expect(")")
        node.setStmt(stmt())

    elif consume(";"):
        node=Node(NodeKind.NULL)

    else:
        node =expr()
        expect(";")
    return node

#expr=assign
def expr():
    trace("expr")
    node=assign()
    return node

#assign=equal ("=" assign)?
def assign():
    trace("assign")
    node=equal()
    if consume("="):
        #trace("assign")
        node=Node(NodeKind.ASSIGN,node,assign())
    return node

#equal = (relate "=="|relate "!=")
def equal():
    trace("equal")
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
    trace("relate")
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
    trace("add")
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
    trace("mul")
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
    trace("unary")
    if consume('+'):
        return primary()
    if consume("-"):
        return Node(NodeKind.SUB,Node(kind=NodeKind.NUM,val=0),primary())
    return primary()

#primary = num | lval | "(" expr ")" |func "(" ((expr ",")* expr)? ")"
def primary():
    trace("prymary")
    if consume('('):
        node=expr()
        expect(')')
        return node

    str=consume_val()
    if str:
        if consume("("): #関数の場合
            node=Node_Func_Call(NodeKind.FUNCCALL,str)
            while not at_eof():
                if consume(")"):
                    break

                node.addArg(primary())

                if consume(","):
                    continue

        else:   #変数または引数の場合
            if str in arguments: #引数の場合
                node=Node_Arg(NodeKind.ARG,str,arguments[str])
            else:                #ローカル変数の場合
                LVAL=FindLval(str)
                if LVAL==None:
                    global local,lvalCnt
                    lval=Lval(next=local,name=str,offset=local.offset+8)
                    node=Node(NodeKind.LVAL,offset=lval.offset)
                    local=lval
                    lvalCnt+=1
                else:
                    node=Node(NodeKind.LVAL,offset=LVAL.offset)
        return node

    node=Node(kind=NodeKind.NUM,val=expectNum())
    return node

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

#関数名のリスト
funclist=[]

#引数のリスト
arguments={}

#ローカル変数の数
lvalCnt=0

