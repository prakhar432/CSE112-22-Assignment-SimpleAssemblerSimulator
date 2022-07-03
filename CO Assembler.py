#Dictionary containing operations and respective codes
import sys
opcodes={
    "add":'10000',
    "sub":'10001',
    "mov":'1001010011',
    "ld":'10100',
    "st":'10101',
    "mul":'10110',
    "div":'10111',
    "rs":'11000',
    "ls":'11001',
    "xor":'11010',
    "or":'11011',
    "and":'11100',
    "not":'11101',
    "cmp":'11110',
    "jmp":'11111',
    "jlt":'01100',
    "jgt":'01101',
    "je":'01111',
    "hlt":'01010'
}
#List containing sublists with the sublist of the form- [register name,register code,register value]
registers=[
    ["R0",'000',0],
    ["R1",'001',0],
    ["R2",'010',0],
    ["R3",'011',0],
    ["R4",'100',0],
    ["R5",'101',0],
    ["R6",'110',0],
    ["FLAGS",'111',0],
]
register_list=['R0','R1','R2','R3','R4','R5','R6','FLAGS']
Type_A=['add','sub','mul','or','and','xor']
Type_B=['mov','rs','ls']
Type_C=['mov','div','not','cmp']
Type_D=['ld','st']
Type_E=['jmp','jlt','jgt','je']
Type_F=['hlt']  
reserved=Type_A+Type_B+Type_C+Type_D+Type_E+Type_F
#Assembly to machine code for type A instructions
def typeA(instruction):
    line=''
    line+=opcodes[instruction[0]]
    line+='00'
    line+=registers[int(instruction[1][1])][1]
    line+=registers[int(instruction[2][1])][1]
    line+=registers[int(instruction[3][1])][1]
    return line
#Assembly to machine code for type B instructions
def typeB(instruction):
    line=''
    line+=opcodes[instruction[0]][:5]
    line+=registers[int(instruction[1][1])][1]
    line+=bin8(instruction[2][1:])
    return line
#Assembly to machine lone for type C instructions
def typeC(instruction,variables_dict):
    line=''
    if instruction[0]=='mov':
        line+=opcodes[instruction[0]][5:]
    else:
        line+=opcodes[instruction[0]]
    line+='00000'
    line+=registers[int(instruction[1][1])][1]
    line+=registers[int(instruction[2][1])][1] 
    return line
#Assembly to machine code for type D instructions
def typeD(instruction,variables_dict):
    line=''
    line+=opcodes[instruction[0]]
    line+=registers[int(instruction[1][1])][1]
    x=instruction[2]
    line+=variables_dict[x]
    return line
#Assembly to machine code for type E instructions
def typeE(instruction,variables_dict):
    line=''
    line+=opcodes[instruction[0]]
    line+='000'
    x=instruction[1]
    line+=variables_dict[x]
    return line
#Assembly to machine code for type F instructions
def typeF(instruction):
    line=''
    line+=opcodes[instruction[0]]
    line+='00000000000'
    return line 
#integer to 16 bit binary number
def bin16(num):
    num=int(num)
    bin_num=bin(num).replace('0b','')
    bin_num1=bin_num[::-1]
    while len(bin_num1)<16:
        bin_num1+='0'
    bin_num=bin_num1[::-1]
    return bin_num
#integer to 8 bit binary number
def bin8(num):
    num=int(num)
    bin_num=bin(num).replace('0b','')
    bin_num1=bin_num[::-1]
    while len(bin_num1)<8:
        bin_num1+='0'
    bin_num=bin_num1[::-1]
    return bin_num
with open("assembly code.txt",'r') as file:
    instructions=file.read()
#List which stores all the information which have to be run in the correct order required
instruct_list=[]
#Count of first & last instruction, as well as the first & last variable
first_exe=0
last_exe=0
var_first=0
var_last=0
#Instruction list stores each line of the assembly code as different elements of the list
instructions_list=instructions.split('\n')
for i in range(instructions_list.count('')):
    instructions_list.remove('')
for i in range(len(instructions_list)):
    if instructions_list[i][:3]!='var':
        first_exe=i+1
        break
last_exe=len(instructions_list)
var_first=0
var_last=i
no_var=var_last-var_first+1
no_instruct=last_exe-first_exe+1
#Adding elements in the instruct element list using list slicing
instruct_list=instructions_list[i:]
instruct_list+=instructions_list[0:i]
#Creating a dictionary with only variables and their respective memory addresses
variables_dict={}
for i in range(no_instruct,len(instruct_list)):
    if instruct_list[i][:3]=='var':
        variables_dict[instruct_list[i][4]]=bin8(i)
#Dictionary which stores all the instructions which can be run
instruct_dict={}
labels={}
for i in range(len(instruct_list)):
    labels[i]=[instruct_list[i],bin8(i)]
print(variables_dict)
print(instruct_dict)
print(instruct_list)
print(labels)
print(instructions_list)
#Error Handling
def error_identification(instructions,labels,reserved,registers,register_list,type_A,type_B,type_C,type_D,type_E,type_F):
    error=0
    instruction_list=[]
    instruction_list=labels.values()
    for i in range(len(labels)):
        instruction_list[i]=labels[i][0]
    #(h) Hlt error handling
    hlt_count=instructions.count('hlt')
    if hlt_count==0:
        error=1
        print("Error: Missing hlt instruction!\nAdd a hlt instruction at the end of the program")
        sys.exit()
    if hlt_count>1:
        error=1
        print("Error: There should be only one hlt instruction in the program")
        sys.exit()
    if instruction_list[-1]!="hlt":
        error=1
        print("Error! The last instruction is not hlt instruction")
        sys.exit()
    #(a) Typos in instruction name
    for i in range(len(instruction_list)):
        instruction=instruction_list[i].split()
        if instruction[0] not in reserved:
            error=1
            print('In line',i,', there is a typo in the instruction name')
            print(instruction[0]+'is not a reserved keyword in the ISA')
            sys.exit()
    #(b) Typos in register name
    for i in range(len(instruction_list)):
        instruction=instruction_list[i].split()
        if instruction[0] in type_A:
            if instruction[1] not in register_list or instruction[2] not in register_list or instruction[3] not in register_list :
                error=1
                print('In line',i,',there is a typo in the register name')
                print(instruction[1]+'is not a reserved keyword in the ISA')
                sys.exit()
        if instruction[0] in type_B and instruction[2][0]=='$':
            if instruction[1] not in register_list:
                error=1
                print('In line',i,',there is a typo in the register name')
                print(instruction[1]+'is not a reserved keyword in the ISA')
                sys.exit()
        if instruction[0] in type_C:
            if instruction[1] not in register_list or instruction[2] not in register_list:
                error=1
                print('In line',i,',there is a typo in the register name')
                print(instruction[1]+'is not a reserved keyword in the ISA')
                sys.exit()
        if instruction[0] in type_D:
            if instruction[1] not in register_list:
                error=1
                print('In line',i,',there is a typo in the register name')
                print(instruction[1]+'is not a reserved keyword in the ISA')
                sys.exit()
    #(d) Mention of FLAGS as register name
    for i in range(len(instruction_list)):
        instruction=instruction_list[i].split()
        if instruction[0] in type_A:
            if instruction[2]=='FLAGS' or instruction[2]=='FLAGS' or instruction[3]=='FLAGS':
                error=1
                print("Illegal use of FLAGS as register")
                sys.exit()
        if instruction[0] in type_B and instruction[2][0]=='$':
            if instruction[1]=='FLAGS':
                error=1
                print("Illegal use of FLAGS as register")
                sys.exit()
        if instruction[0] in type_C:
            if instruction[1]=='FLAGS' or instruction[2]=='FLAGS':
                error=1
                print("Illegal use of FLAGS as register")
                sys.exit()
        if instruction[0] in type_D:
            if instruction[1]=='FLAGS':
                error=1
                print("Illegal use of FLAGS as register")
                sys.exit()
    #(e) Illegal use of immediate values 
    for i in range(len(instruction_list)):
        instruction=instruction_list[i].split()
        if instruction[0] in type_B and instruction[2][0]=='$':
            number=bin8(instruction[2][1:])
            if number>=256:
                error=1
                print("Error in line",i)
                print("Immediate value passed in line"+i+"is beyond the range of possible values")
                print("Provide a value which is between 0-255")
                sys.exit()
    #(g) Variables not declared in the beginning
    for i in range(len(instruction_list)):
        instruction=instruction_list[i].split()
        if instruction[0]=='hlt':
            break
        if instruction[0]=='var':
            error=1
            print("Error in line",i)
            print("Variables are declared in the middle of the instructoins!")
            print("Variables should be declared at the beginning of the program")
            sys.exit()
error = 0
error = error_identification(instructions,labels,reserved,registers,register_list,Type_A,Type_B,Type_C,Type_D,Type_E,Type_F)
if error==0:
    #Creating an empty file which stores the machine code 
    file=open("machine_code.txt",'w')
    file.close()
    #Writing the machine code into the file
    with open("machine_code.txt",'a') as file:
        for i in range(len(labels)):
            labels[i][0].strip()
            instruction=labels[i][0].split()
            if instruction==[]:
                continue
            line=''
            if instruction[0] in Type_A:
                line=typeA(instruction)
            elif instruction[0] in Type_B and instruction[2][0]=='$':
                line=typeB(instruction)
            elif instruction[0] in Type_C:
                line=typeC(instruction)
            elif instruction[0] in Type_D:
                line=typeD(instruction,variables_dict)
            elif instruction[0] in Type_E:
                line=typeE(instruction,variables_dict)
            elif instruction[0] in Type_F:
                line=typeF(instruction)
            elif instruction[0]=='var':
                break
            file.write(line)
            file.write("\n")