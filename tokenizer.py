from enum import Enum
import sys

#トークンの種類
class TokenKind(Enum):
    RESERVED=1
    NUM=2
    EOF=3
    IDENT=4
    RETURN=5

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

    if token.kind !=TokenKind.RESERVED or token.str!=symbol:
        return False

    token=token.next
    return True

#渡された記号がローカル変数かどうか判別し、トークンを1つ進める
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

#エラーを出力し、プロセスを終了する関数
def error(x):
    print(x)
    print("式が間違ってるのん！",file=sys.stderr)
    sys.exit(1)

#渡された記号が期待しているものかどうか判別し、偽のときはエラーを報告する
def expect(symbol):
    global token
    if token.kind !=TokenKind.RESERVED or token.str[0]!=symbol:
        error(0)
    token=token.next
    return True

#トークンが数字の場合、トークンを1つ進めて値を返す。偽の場合はエラー出力
def expectNum():
    global token
    if token.kind !=TokenKind.NUM:
        error(1)
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

        if p>="a" and p<="z":
            val+=p
            continue
        
        if len(val)!=0:
            if val=="return" and p!="=":
                cur=NewToken(TokenKind.RETURN,cur,val)
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

        if p==";":
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
