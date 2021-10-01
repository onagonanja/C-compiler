from tokenizer import *
from RDP import *

def write(asemmbly):
    with open("../output.s","a") as f:
        f.write(asemmbly)

def GenerateAsemmbly(node):
    global ID
    if node.kind==NodeKind.NUM:
        write("  push %d\n" %node.val)
        return
    elif node.kind==NodeKind.NULL:
        return
    elif node.kind==NodeKind.ASSIGN:
        GenerateLval(node.left)
        GenerateAsemmbly(node.right)
        write("  pop rdi\n")
        write("  pop rax\n")
        write("  mov [rax], rdi\n")
        #write("  push rdi\n")
        return
    elif node.kind==NodeKind.LVAL:
        GenerateLval(node)
        write("  pop rax\n")
        write("  mov rax, [rax]\n")
        write("  push rax\n")
        return
    elif node.kind==NodeKind.RETURN:
        GenerateAsemmbly(node.left)
        write("  pop rax\n")
        write("  mov rsp, rbp\n")
        write("  pop rbp\n")
        write("  ret\n")
        return
    elif node.kind==NodeKind.BLOCK:
        for stmt in node.stmt:
            GenerateAsemmbly(stmt)
        return
    elif node.kind==NodeKind.IF:
        id=ID
        ID+=1

        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .Lend"+str(id)+"\n")
        GenerateAsemmbly(node.stmt)
        write(".Lend"+str(id)+":\n")
        return
    elif node.kind==NodeKind.IFEL:
        id=ID
        ID+=1

        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .Lelse"+str(id)+"\n")
        GenerateAsemmbly(node.stmt)
        write("  jmp .Lend"+str(id)+"\n")
        write(".Lelse"+str(id)+":\n")
        GenerateAsemmbly(node.elstmt)
        write(".Lend"+str(id)+":\n")
        return 
    elif node.kind==NodeKind.WHILE:
        id=ID
        ID+=1

        write(".Lbegin"+str(id)+":\n")
        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .Lend"+str(id)+"\n")
        GenerateAsemmbly(node.stmt)
        write("  jmp .Lbegin"+str(id)+"\n")
        write(".Lend"+str(id)+":\n")
        return
    elif node.kind==NodeKind.FOR:
        id=ID
        ID+=1

        GenerateAsemmbly(node.Init)
        write(".Lbegin"+str(id)+":\n")
        GenerateAsemmbly(node.Cmp)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .Lend"+str(id)+"\n")
        GenerateAsemmbly(node.Stmt)
        GenerateAsemmbly(node.Reset)
        write("  jmp .Lbegin"+str(id)+"\n")
        write(".Lend"+str(id)+":\n")
        return
    elif node.kind==NodeKind.FUNCDEF:
        write(node.name+":\n")
        write("  push rbp\n")
        write("  mov rbp, rsp\n")
        write("  sub rsp, %d\n" %(node.lvalCnt*8))
        GenerateAsemmbly(node.stmt)
        write("\n")
        return
    elif node.kind==NodeKind.FUNCCALL:
        for arg in node.args[::-1]:
            GenerateAsemmbly(arg)
        write("  call %s\n" %node.name)
        write("  push rax\n")
        return
    elif node.kind==NodeKind.ARG:
         write("  mov rax, rbp\n")
         write("  add rax, %d\n" %(node.offset+8))
         write("  mov rax, [rax]\n")
         write("  push rax\n")
         return
    elif node.kind==NodeKind.PONTER:
        GenerateAsemmbly(node.left)
        write("  pop rax\n")
        write("  mov rax, [rax]\n")
        write("  push rax\n")
        return
    elif node.kind==NodeKind.ADDRESS:
        GenerateLval(node.left)
        return

    GenerateAsemmbly(node.left)
    GenerateAsemmbly(node.right)

    write("  pop rdi\n")
    write("  pop rax\n")

    if node.kind==NodeKind.ADD:
        write("  add rax, rdi\n")
    elif node.kind==NodeKind.SUB:
        write("  sub rax, rdi\n")
    elif node.kind==NodeKind.MUL:
        write("  imul rax, rdi\n")
    elif node.kind==NodeKind.DIV:
        write("  idiv rax, rdi\n")
    elif node.kind==NodeKind.LT:
        write("  cmp rax, rdi\n")
        write("  setl al\n")
        write("  movzb rax, al\n")
    elif node.kind==NodeKind.RT:
        write("  cmp rdi, rax\n")
        write("  setl al\n")
        write("  movzb rax, al\n")
    elif node.kind==NodeKind.LET:
        write("  cmp rax, rdi\n")
        write("  setle al\n")
        write("  movzb rax, al\n")
    elif node.kind==NodeKind.RET:
        write("  cmp rdi, rax\n")
        write("  setle al\n")
        write("  movzb rax, al\n")
    elif node.kind==NodeKind.EQ:
        write("  cmp rdi, rax\n")
        write("  sete al\n")
        write("  movzb rax, al\n")
    elif node.kind==NodeKind.NEQ:
        write("  cmp rdi, rax\n")
        write("  setne al\n")
        write("  movzb rax, al\n")
    write("  push rax\n")

#ローカル変数のアドレスをスタックに積む 
def GenerateLval(node):
    if node.kind!=NodeKind.LVAL and  node.kind!=NodeKind.ARG:
        print(node.kind)
        error("左辺値が変数ではないのん")
    if node.kind==NodeKind.LVAL:
        write("  mov rax, rbp\n")
        write("  sub rax, %d\n" %node.offset)
        write("  push rax\n")
    
    elif node.kind==NodeKind.ARG:
        write("  mov rax, rbp\n")
        write("  add rax, %d\n" %(node.offset+8))
        write("  push rax\n")

#条件分岐文を区別するid
ID=0
