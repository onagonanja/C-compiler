from enum import Enum
import sys
import copy

#トークンの種類
class TokenKind(Enum):
    RESERVED=1
    NUM=2
    EOF=3
    IDENT=4
    RETURN=5
    IF=6
    WHILE=7
    FOR=8
    ELSE=9
    IFEL=10
    FUNC=11
    TYPE=12

#トークンクラス
class Token():
    def __init__(self,kind=None,next=None,val=None,str=None):
        self.kind=kind
        self.next=next
        self.val=val
        self.str=str
        #print(self.str)

#現在注目しているトークン
token=Token()

#渡された記号が期待しているものかどうか判別し、トークンを1つ進める
def consume(symbol):
    global token
    if token.str!=symbol:
        return False
    token=token.next
    return True

def trace(symbol):
    global token
    if token.str=="=":
        print(symbol)
    return True

#現在注目しているトークンが変数名または関数名かどうか判別し、真ならトークンを1つ進める
def consume_val():
    global token

    if token.kind !=TokenKind.IDENT:
        return False
    res=token.str
    token=token.next
    return res


#returnかどうか判別し、トークンを1つ進める
def consume_ret():
    global token

    if token.kind !=TokenKind.RETURN:
        return False

    token=token.next
    return True

def consume_type():
    global token

    if token.kind!=TokenKind.TYPE:
        return False
    
    token=token.next
    return token.str

#エラーを出力し、プロセスを終了する関数
def error(x):
    print(x)
    print("式が間違ってるのん！",file=sys.stderr)
    sys.exit(1)

#渡された記号が期待しているものかどうか判別し、偽のときはエラーを報告する
def expect(symbol):
    global token
    if token.str!=symbol:
        print(token.str)
        error(0)
    token=token.next
    return True

#トークンが数字の場合、トークンを1つ進めて値を返す。偽の場合はエラー出力
def expectNum():
    global token
    if token.kind !=TokenKind.NUM:
        print(token.kind)
        print(token.str)
        error(1000000)
    res=token.val
    token=token.next
    return res

#トークンが型名の場合、トークンを1つ進めて型名を返す。偽の場合はエラー出力
def expectType():
    global token
    if token.kind !=TokenKind.TYPE:
        print(token.kind)
        print(token.str)
        error("型が不明です")
    res=token.val
    token=token.next
    return res

#プログラムの終わりかどうか判別する関数
def at_eof():
    global token
    #print(token.str)
    return token.kind==TokenKind.EOF

#新たなトークンを作成する関数
def NewToken(kind,cur,str):
    token=Token(kind=kind,str=str)
    cur.next=token
    return token

#渡された文字列をトークン化する関数
def tokenize(str):
    global token
    head=Token()
    cur=head #現在注目しているトークン
    flag=False
    val="" #変数名

    for i, p in enumerate(str):
        if flag==True:
            flag=False
            continue

        if (p>="a" and p<="z") or p.isdigit():
            val+=p
            continue
        
        if len(val)!=0:
            if val=="return" and p!="=":
                cur=NewToken(TokenKind.RETURN,cur,val)
            elif val.isdigit():
                cur=NewToken(TokenKind.NUM,cur,val)
                cur.val=int(val)
            elif val=="if":
                cur=NewToken(TokenKind.IF,cur,val)
            elif val=="while":
                cur=NewToken(TokenKind.WHILE,cur,val)
            elif val=="for":
                cur=NewToken(TokenKind.FOR,cur,val)
            elif val=="else":
                cur=NewToken(TokenKind.ELSE,cur,val)
            elif val=="int":
                cur=NewToken(TokenKind.TYPE,cur,val)
            else:
                cur=NewToken(TokenKind.IDENT,cur,val)
            val=""    
        
        if(p==" "):
            continue

        if i<=len(str)-2:
            if (p=="=" and str[i+1]=="=") or (p=="!" and str[i+1]=="="):
                cur=NewToken(TokenKind.RESERVED,cur,p+str[i+1])
                flag=True
                continue
            if (p=="<" and str[i+1]=="=") or (p==">" and str[i+1]=="="):
                cur=NewToken(TokenKind.RESERVED,cur,p+str[i+1])
                flag=True
                continue

        if p=="=":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue
        
        if p=="<" or p==">":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p=="+" or p=="-" or p=="*" or p=="/":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p=="(" or p==")":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p=="{" or p=="}":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p==";" or p==",":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p=="&":
            cur=NewToken(TokenKind.RESERVED,cur,p)
            continue

        if p.isdigit():
            cur=NewToken(TokenKind.NUM,cur,p)
            cur.val=int(p)
            continue
        error(3)
    eof=NewToken(TokenKind.EOF,cur,"EOF")
    token=head.next
    return head.next

def serch_else():
    global token
    Token=copy.deepcopy(token)
    cnt=0
    while not at_eof():
        if Token.str=="{":
            cnt+=1
        elif Token.str=="}":
            cnt-=1
            if cnt<=0:
                Token=Token.next
                if Token.kind==TokenKind.ELSE:
                    return True
                else:
                    return False
        elif Token.kind==TokenKind.ELSE and cnt==0:
            return True
        
        Token=Token.next
    return False

def show_tokens():
    global token
    Token=copy.deepcopy(token)
    while Token.kind!=TokenKind.EOF:
        print(Token.str)
        print(Token.kind)
        Token=Token.next

def show_token():
    global token
    print(token.str)