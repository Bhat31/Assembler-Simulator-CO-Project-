import sys
input = sys.argv[-2]
output = sys.argv[-1]
inputfile = open(input) 
outputfile = open(output,"w+")

# creating a list of all lines in input txt file, each element in lines is a line
lines_unrefined = inputfile.readlines() 
lines = [line.strip() for line in lines_unrefined]
lines_noblank = [line for line in lines if line != '']
# lines excludes all new line characters and empty lines

line_no = 0
line_no_label = 0
global instrCounter
global stackCounter
global dataMemoryCounter

PrgC = 0 # Program Counter
PrgC_label = 0
PrgCMax = 4*(len(lines_noblank) -1)
if PrgCMax > 255:
    print('Error: Program memory exceeded:no of instr > 64')
    sys.exit()
# we may use PrgCMax instead of instrCounter
instrCounter = 0 #for tracking the numbers of instructions assembled don't exceed program memory
stackCounter = 32 #for tracking variables don't exceed stack memory, we have only 32 registers
dataMemoryCounter = 0 # don't know for now
virtual_halt_flag = False



# register type instructions
R_type_instr = ['add','sub','slt','sltu','xor','sll','srl','or','and'] 
# immediate type instructions
I_type_instr = ['lw','addi','sltiu','jalr']
# s type instructions
S_type_instr = ['sw']
# branch type instructions
B_type_instr = ['beq','bne','blt','bge','bltu','bgeu']
# unsigned type instructions
U_type_instr = ['lui','auipc']
# j type instructions
J_type_instr = ['jal']
# bonus instructions
Bonus_instr = ['mul','rst','halt','rvrs']

# register encodings in dict (ABI:Address)
# Registers Assignment

registers_dict = {
    'zero': '00000',
    'ra':   '00001',
    'sp':   '00010',
    'gp':   '00011',
    'tp':   '00100',
    't0':   '00101',
    't1':   '00110',
    't2':   '00111',
    's0':   '01000',
    's1':   '01001',
    'a0':   '01010',
    'a1':   '01011',
    'a2':   '01100',
    'a3':   '01101',
    'a4':   '01110',
    'a5':   '01111',
    'a6':   '10000',
    'a7':   '10001',
    's2':   '10010',
    's3':   '10011',
    's4':   '10100',
    's5':   '10101',
    's6':   '10110',
    's7':   '10111',
    's8':   '11000',
    's9':   '11001',
    's10':   '11010',
    's11':   '11011',
    't3':   '11100',
    't4':   '11101',
    't5':   '11110',
    't6':   '11111',
}


labels_dict = {} 
#empty dict for storing label:PC values here (Note PC has hex range from 00 to ff i.e 0 to 255 bytes each instruction consuming 4 bytes)
# Opcodes

func3_dict = {
    'add': '000',
    'sub': '000',
    'sll': '001',
    'slt': '010',
    'sltu': '011',
    'xor': '100',
    'srl': '101',
    'or': '110',
    'and': '111',
    'lw': '010',
    'addi': '000',
    'sltiu': '011',
    'jalr': '000',
    'sw': '010',
    'beq': '000',
    'bne': '001',
    'blt': '100',
    'bge': '101',
    'bltu': '110',
    'bgeu': '111'
}

def valid_imm(n):
    numlist = ['0','1','2','3','4','5','6','7','8','9','-','.']
    for i in n:
        if i not in numlist:
            print("Syntax Error: imm value is not a number on line",line_no,'\n',"Note: if you were giving in a label, it might be undefined in code!")
            sys.exit()


# decimal to binary with sign ext converter
def bin_ext_converter(n,bits):
    n_1 = str(bin(n))
    if n >= 0:
        n_2 = '0' + n_1[2:]
        if len(n_2) > bits:
            print('Error: illegal Imm out of bounds on line',line_no)
            sys.exit()
        else:
            n_2 = '0'*(bits-len(n_2)) + n_2
    else:
        if abs(n) == 2 ** (bits-1):
            n_2 = str(bin(n))
            n_2 = n_2[3:]
            return n_2
        
        n_2 = '0'+ n_1[3:]
        n_2 = ''.join('1' if b == '0' else '0' for b in n_2)
        n_2 = str(bin(int(n_2,2)+1))
        n_2 = n_2[2:]
        if len(n_2)> bits:
            print('Error: illegal Imm out of bounds on line',line_no)
            sys.exit()
        else:
            n_2 = '1'*(bits-len(n_2)) + n_2
    return n_2

# no label
def R_type_encoder(token_1):
    global PrgC
    op_code = '0110011'
    
    op_name = token_1[0]
    func3 = func3_dict[op_name]
    token_2 = token_1[1].split(",")
    if len(token_2) != 3:
        print("Syntax Error on line ",line_no,"Note: Check for missing comma/regname/imm value or extra comma/regnames/imm values!")
        sys.exit()
    if (len(token_2) == 3) and ('' in token_2):
        print('Syntax Error: missing regname or imm value on line',line_no)
        sys.exit()
    for i in token_2:
        if i not in registers_dict:
            print("Error: illegal register name used on line",line_no)
            sys.exit()
    rd = registers_dict[token_2[0]]
    rs1 = registers_dict[token_2[1]]
    rs2 = registers_dict[token_2[2]]
    if op_name == 'sub':
        func7 = '0100000'
    else:
        func7 = '0000000'

    binstr = func7 + rs2 + rs1 + func3 + rd + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4


#note some confusion in jalr right now
def I_type_encoder(token_1):
    global PrgC

    op_name = token_1[0]
    if op_name == 'lw':
        op_code = '0000011'
    elif op_name == 'addi':
        op_code = '0010011'
    elif op_name == 'sltiu':
        op_code = '0010011'
    else:
        op_code = '1100111'
    func3 = func3_dict[op_name]

    token_2 = token_1[1].split(",") #token_2[0] has rd
    rd = token_2[0]
    if (len(token_2) > 3) or (len(token_2) < 2):
        print("Syntax error: missing regname/imm value or extra regnames/imm values on line",line_no)
        sys.exit()
    if (len(token_2) == 3) and ('' in token_2):
        print('Syntax Error: missing regname or imm value on line',line_no)
        sys.exit()
    if len(token_2) == 2:
        if '(' not in token_2[1]:
            print('Syntax Error: on line',line_no,'\n','Note: Check for missing commas!')
            sys.exit()
        if '' in token_2:
            print('Syntax Error: missing regname or imm value on line',line_no)
            sys.exit()
        token_3 = token_2[1].split("(") #token_3[0] has imm[11:0] in decimal
        if token_3[0] == '':
            print('Syntax Error: missing imm value on line',line_no)
            sys.exit()
        valid_imm(token_3[0])
        token_4 = token_3[1]          #token_4 has rs1
        token_4 = token_4[:-1]        #token_4 has rs1
        rs1 = token_4
        imm = bin_ext_converter(int(token_3[0]),12)

    else:
        rs1 = token_2[1]
        valid_imm(token_2[2])
        imm = bin_ext_converter(int(token_2[2]),12)

    if (rd not in registers_dict) or (rs1 not in registers_dict):
        print("Error: illegal register name used on line",line_no)
        sys.exit()
    rd = registers_dict[rd]
    rs1 = registers_dict[rs1]

    binstr = imm + rs1 + func3 + rd + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4

    

# no label
def S_type_encoder(token_1):
    global PrgC
    op_code = '0100011'

    op_name = token_1[0]
    func3 = func3_dict[op_name]

    token_2 = token_1[1].split(",") #token_2[0] has rs2
    if len(token_2) != 2:
        print("Error: Syntax error on line",line_no,'\n',"Note: Check for missing comma or extra comma/regname/imm values!")
        sys.exit()
    if (len(token_2) == 2) and ('' in token_2):
        print('Syntax Error: missing regname or imm value on line',line_no)
        sys.exit()
    token_3 = token_2[1].split("(") #token_3[0] has imm[11:0] in decimal
    if token_3[0] == '':
        print("Syntax Error: missing imm value on line",line_no)
        sys.exit()
    valid_imm(token_3[0])
    token_4 = token_3[1]          #token_4 has rs1)
    token_4 = token_4[:-1]        #token_4 has rs1
    rs1 = token_4
    rs2 = token_2[0]
    if (rs2 not in registers_dict) or (rs1 not in registers_dict):
        print("Error: illegal register name used on line",line_no)
        sys.exit()
    rs2 = registers_dict[rs2]
    rs1 = registers_dict[rs1]
    imm = bin_ext_converter(int(token_3[0]),12)
    imm1 = imm[:-5]
    imm0 = imm[-5:]

    binstr = imm1 + rs2 + rs1+ func3 + imm0 + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4

# label
def B_type_encoder(token_1):
    global PrgC
    op_code = '1100011'

    op_name = token_1[0]
    func3 = func3_dict[op_name]

    token_2 = token_1[1].split(",") 
    if len(token_2) != 3:
        print("Syntax Error: missing comma /regname /imm values on line or extra comma/regnames/imm values!",line_no)
        sys.exit()
    if (len(token_2) == 3) and ('' in token_2):
        print('Syntax Error: missing regname or imm value on line',line_no)
        sys.exit()
    rs1 = token_2[0]
    rs2 = token_2[1]
    if (rs2 not in registers_dict) or (rs1 not in registers_dict):
        print("Error: illegal register name used on line",line_no)
        sys.exit()
    label = token_2[2]
    # if label is given
    if label in labels_dict:
        
        imm = labels_dict[label] - PrgC #doing absolute addr - current addr
        imm = bin_ext_converter(imm,13)
        imm1 = imm[0] + imm[2:8]
        imm0 = imm[-5:-1] + imm[1]
    #if direct imm given in decimal
    else:
        valid_imm(label)
        imm = int(label)
        imm = bin_ext_converter(imm,13)
        imm1 = imm[0] + imm[2:8]
        imm0 = imm[-5:-1] + imm[1]
    
    
    rs1 = registers_dict[rs1]
    rs2 = registers_dict[rs2]

    binstr = imm1 + rs2 + rs1+ func3 + imm0 + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4


#no label
def U_type_encoder(token_1):
    global PrgC
    op_name = token_1[0]
    token_2 = token_1[1].split(",")
    if (len(token_2) != 2) or ('' in token_2):
        print("Error: Syntax error on line",line_no,'\n',"Note: Check for missing comma/ imm value/ regname or extra regnames/imm values!")
        sys.exit()
    rd = token_2[0]
    if rd not in registers_dict:
        print("Error: illegal register name used on line",line_no)
        sys.exit()

    rd = registers_dict[rd]
    valid_imm(token_2[1])
    imm = int(token_2[1])
    imm = bin_ext_converter(imm,32)
    imm = imm[0:20]
    if op_name == 'lui':
        op_code = '0110111'
    else:
        op_code = '0010111'
    
    binstr = imm + rd + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4
    

#label
def J_type_encoder(token_1):
    global PrgC
    op_code = '1101111'
    op_name = token_1[0]
    token_2 = token_1[1].split(",")
    if (len(token_2) != 2) or ('' in token_2):
        print("Error: Syntax error on line",line_no,'\n',"Note: Check for missing comma/ imm value/ missing regname or extra commas/regnames/imm values!")
        sys.exit()
    rd = token_2[0]
    if rd not in registers_dict:
        print("Error: illegal register name used on line",line_no)
        sys.exit()
    rd = registers_dict[rd]
    label = token_2[1]
    # if label is given
    if label in labels_dict:
        
        imm = labels_dict[label] - PrgC #doing absolute addr - current addr
        imm = bin_ext_converter(imm,21)
        imm = imm[0] + imm[-11:-1] + imm[9] + imm[1:9]
    #if direct imm given in decimal
    else:
        valid_imm(label)
        imm = int(label)
        imm = bin_ext_converter(imm,21)
        imm = imm[0] + imm[-11:-1] + imm[9] + imm[1:9]

    binstr = imm + rd + op_code + '\n'
    outputfile.write(binstr)

    
    PrgC = PrgC + 4

#no label
def Bonus_type_encoder(token_1):
    global PrgC
    opname = token_1[0]
    if opname == 'rst':
        binstr = '00000000000000000000000000000000' + '\n'
        outputfile.write(binstr)
        PrgC = PrgC + 4

    elif opname == 'halt':
        binstr = '11111111111111111111111111111111' + '\n'
        outputfile.write(binstr)
        PrgC = PrgC + 4

    elif opname == 'mul':
        op_code = '1000000'
        func3 = '001'
        func7 = '0000000'
        token_2 = token_1[1].split(",")
        if len(token_2) != 3:
            print("Syntax Error on line ",line_no,"Note: Check for missing comma/regname/imm value or extra comma/regnames/imm values!")
            sys.exit()
        if (len(token_2) == 3) and ('' in token_2):
            print('Syntax Error: missing regname or imm value on line',line_no)
            sys.exit()
        for i in token_2:
            if i not in registers_dict:
                print("Error: illegal register name used on line",line_no)
                sys.exit()
        rd = registers_dict[token_2[0]]
        rs1 = registers_dict[token_2[1]]
        rs2 = registers_dict[token_2[2]]
        binstr = func7 + rs2 + rs1 + func3 + rd + op_code + '\n'
        outputfile.write(binstr)
        PrgC = PrgC + 4

    else:
        op_code = '1000001' #rvrs
        func3 = '010'
        func12 = '000000000000'
        token_2 = token_1[1].split(",")
        if len(token_2) != 2:
            print("Syntax Error on line ",line_no,"Note: Check for missing comma/regname/imm value or extra comma/regnames/imm values!")
            sys.exit()
        if (len(token_2) == 2) and ('' in token_2):
            print('Syntax Error: missing regname or imm value on line',line_no)
            sys.exit()
        for i in token_2:
            if i not in registers_dict:
                print("Error: illegal register name used on line",line_no)
                sys.exit()
        rd = registers_dict[token_2[0]]
        rs1 = registers_dict[token_2[1]]
        
        binstr = func12 + rs1 + func3 + rd + op_code + '\n'
        outputfile.write(binstr)
        PrgC = PrgC + 4
        

def Label_type_encoder(opname,token_1):
    
    
    token_1.remove(opname)
    new_line = " ".join(token_1)
    instr_identifier(new_line)


def instr_identifier(line):
    global virtual_halt_flag
    if line == 'beq zero,zero,0':
        virtual_halt_flag = True
    
    token_1 = line.split() #token_1 contains tokens split about white spaces
    opname = token_1[0]
    
    if opname[-1] == ":":
        Label_type_encoder(opname,token_1)
    elif opname in R_type_instr:
        R_type_encoder(token_1)
    elif opname in I_type_instr:
        I_type_encoder(token_1)
    elif opname in S_type_instr:
        S_type_encoder(token_1)
    elif opname in B_type_instr:
        B_type_encoder(token_1)
    elif opname in U_type_instr:
        U_type_encoder(token_1)
    elif opname in J_type_instr:
        J_type_encoder(token_1)
    elif opname in Bonus_instr:
        Bonus_type_encoder(token_1)
    else:
        print("Error: invalid operation name on line",line_no,"\n","Note: Check for missed space between opname and reg!")
        sys.exit()

#Collecting labels first
for i in range(len(lines)):
    line_no_label += 1
    line = lines[i]
    if(line == ''):
        continue
    token_1 = list(map(str,line.split()))
    opname = token_1[0]
    label = opname[0:-1]

    if len(token_1) > 3:
        print("Error: Syntax error on line",line_no_label,"\n","Note: Check for redundant spaces in names of label/opname/reg name!")
        sys.exit()
    if (len(token_1) == 3) and (':' not in opname): #we expect a label here but don't get it
        print("Error: Syntax error on line",line_no_label,"\n","Note: Check for redundant spaces before or after comma in regname or before colon if using label or in names of label/opname/reg name!")
        sys.exit()
    if (len(token_1) == 2) and ( ':' in opname) and (token_1[1] != 'rst') and (token_1[1] != 'halt'): #we don't expect label here but get it
        print("Error: Syntax error on line",line_no_label,"\n","Note: Check for missing space after colon/opname or missing opname!")
        sys.exit()
    if len(token_1) == 1 and (token_1[0] != 'rst') and (token_1[0] != 'halt'):
        print("Error: Syntax error on line",line_no_label,"\n","Note: Check for missed spaces in names of label/opname/reg name!")
        sys.exit()
    if opname[-1] == ":":
        if label in labels_dict:
            # line no considering blank lines
            print("Error: redefining already used label on instruction ",line_no_label)
            sys.exit()
        else:
            labels_dict.update({label:PrgC_label})
            
    PrgC_label = PrgC_label + 4


#iterating through lines of input assembly code


while(PrgC <= PrgCMax):
    line_no = line_no + 1
    line = lines[int(line_no-1)]
    if(line == ''):
        continue
    instr_identifier(line)


if virtual_halt_flag != True:
    print("Error: virtual halt missing!")


