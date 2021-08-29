from asemmbly import *
from tokenizer import *
from RDP import *
import sys

args=sys.argv

if len(args)!=2:
    print("引数にファイル名を1つ指定してください",file=sys.stderr)
    sys.exit(1)

with open(args[1],"r") as f:
    code=f.read()

code.replace("\n","")

tokens=tokenize(code)
trees=program()

with open("output.txt","w") as f:
    f.write(".intel_syntax noprefix\n")
    f.write(".global main\n")
    f.write("main:\n")

for i in trees:    
    GenerateAsemmbly(i)
    write("  pop rax\n")

with open("output.txt","a") as f:
    f.write("  ret\n")

