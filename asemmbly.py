from tokenizer import *
from RDP import *

def write(asemmbly):
    with open("output.txt","a") as f:
        f.write(asemmbly)

def GenerateAsemmbly(node):
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
        write("  push rdi\n")
        return
    elif node.kind==NodeKind.LVAL:
        GenerateLval(node)
        write("  pop rax\n")
        write("  mov rax, [rax]\n")
        write("  push rax\n")
        return
    elif node.kind==NodeKind.RET:
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
        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .LendXXX\n")
        GenerateAsemmbly(node.stmt)
        write(".LendXXX:\n")
        return
    elif node.kind==NodeKind.IFEL:
        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .LelseXXX\n")
        GenerateAsemmbly(node.stmt)
        write("  jmp .LendXXX\n")
        write(".LelseXXX:\n")
        GenerateAsemmbly(node.elstmt)
        write(".LendXXX:\n")
        return 
    elif node.kind==NodeKind.WHILE:
        write(".LbeginXXX:\n")
        GenerateAsemmbly(node.expr)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .LendXXX\n")
        GenerateAsemmbly(node.stmt)
        write("  jmp .LbeginXXX\n")
        write(".LendXXX:\n")
        return
    elif node.kind==NodeKind.FOR:
        GenerateAsemmbly(node.Init)
        write(".LbeginXXX:\n")
        GenerateAsemmbly(node.Cmp)
        write("  pop rax\n")
        write("  cmp rax, 0\n")
        write("  je  .LendXXX\n")
        GenerateAsemmbly(node.Stmt)
        GenerateAsemmbly(node.Reset)
        write(".LendXXX:\n")
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

def GenerateLval(node):
    if node.kind!=NodeKind.LVAL:
        error("左辺値が変数ではないのん")
    write("  mov rax, rbp\n")
    write("  sub rax, %d\n" %node.offset)
    write("  push rax\n")