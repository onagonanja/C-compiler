from tokenizer import *
from RDP import *

def write(asemmbly):
    with open("output.txt","a") as f:
        f.write(asemmbly)

def GenerateAsemmbly(node):
    if node.kind==NodeKind.NUM:
        write("  push %d\n" %node.val)
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
    
    write("  push rax\n")