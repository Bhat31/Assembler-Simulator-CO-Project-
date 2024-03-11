import re
import sys
registers = {
    "zero": "00000", #hardwired 0
    "ra": "00001", #ra Return address
    "sp": "00010", #sp Stack Pointer
    "gp": "00011", #gp Global Pointer
    "tp": "00100", #tp Thread Pointer
    "t0": "00101", #t0 Temporary/alternate link register
    "t1": "00110", #t1-2 Temporaries
    "t2": "00111", #t1-2 Temporaries
    "s0": "01000", #s0/fp Saved register/frame pointer
    "s1": "01001", #s1 Saved Register
    "a0": "01010",#a0-1 Function arguments/ return values
    "a1": "01011",# a0-1 Function arguments/ return values
    "a2": "01100",#Function arguments
    "a3": "01101",#Function arguments
    "a4": "01110",#Function arguments
    "a5": "01111",#Function arguments
    "a6": "10000",#Function arguments
    "a7": "10001",#Function arguments
    "s2": "10010", #s2 Saved registers
    "s3": "10011", #s3 save registers;
    "s4": "10100", #s4 saved register;
    "s5": "10101", #s5 saved register
    "s6": "10110", #s6 saved register
    "s7": "10111", #s7 saved register
    "s8": "11000", #s8 saved register
    "s9": "11001", # s9 saved register
    "s10": "11010", # s10 saved register
    "s11": "11011", # s11 saved register
    "t3": "11100", # t3 Temporaries
    "t4": "11101", # t4 Temporaries
    "t5": "11110", # t5 Temporaries
    "t6": "11111", # t6 Temporaries
}
oppcodes = { 'add': '0110011', 'sub': '0110011', 'sll': '0110011', 'slt': '0110011',
    'sltu': '0110011', 'xor': '0110011', 'srl': '0110011', 'or': '0110011',
    'and': '0110011', 'lw': '0000011', 'addi': '0010011', 'sltiu': '0010011',
    'jalr': '1100111', 'sw': '0100011', 'beq': '1100011', 'bne': '1100011',
    'bge': '1100011', 'bgeu': '1100011', 'blt': '1100011', 'bltu': '1100011',
    'auipc': '0010111', 'lui': '0110111', 'jal': '1101111'}
oppcodesforR= {"add":"000", "sub":"000", "sll":"001","slt":"010",
              "sltu":"011","xor":"100","srl":"101","or":"110","and":"111"}
oppcodesfori={"lw":"010","addi":"000","sltiu":"011","jalr":"000"}
oppcodesforB={"beq":"000","bne":"001","blt":"100","bge":"101"}
def checkInstructionType(instruction):
    if instruction[0] == 'sw':
        return 'S-type'
    elif instruction[0] == 'jal':
        return 'J-type'
    elif instruction[0] in ['add', 'sub', 'slt', 'sltu', 'xor', 'sll', 'srl', 'or', 'and']:
        return 'R-type'
    elif instruction[0] in ['lw', 'addi', 'sltiu', 'jalr']:
        return 'I-type'
    elif instruction[0] in ['beq', 'bne', 'bge', 'bgeu', 'blt', 'bltu']:
        return 'B-type'
    elif instruction[0] in ['lui', 'auipc']:
        return 'U-type'
    else:
        return 'Unknown-type'


def missing_halt(instruction):
# Get the last instruction from the list
   last_instruction = instruction[-1]
# Check if the last instruction is "beq zero,zero,0"
   if last_instruction == "beq zero,zero,0":
       return True
   else:
       return False

def convert_to_binary(number):
    decimal_number=int(number)
    binary_representation=bin(decimal_number)
    decimal_number_string=str(binary_representation)
    decimal_number_string=decimal_number_string[2:len(decimal_number_string)]
    if(len(decimal_number_string)!=11):
         for i in range(len(decimal_number_string),11):
              decimal_number_string=decimal_number_string+"0"
    return decimal_number_string
def convert_to_binary_19(num):
    dec_number=int(num)
    bin_rep=bin(dec_number)
    dec_number_str=str(bin_rep)
    dec_number_str=dec_number_str[2:len(dec_number_str)]
    if(len(dec_number_str)!=19):
        for j in range(len(dec_number_str),19):
            dec_number_str=dec_number_str+"0"
    return dec_number_str
def convert_to_binary_12(num):
    dec_numb=int(num)
    bin_represent=bin(dec_numb)
    dec_number_string=str(bin_represent)
    dec_number_string=dec_number_string[2:len(dec_number_string)]
    if(len(dec_number_string)!=19):
        for j in range(len(dec_number_string),19):
            dec_number_string=dec_number_string+"0"
    return dec_number_string
def assemble_instruction(instruction):
    tokens = instruction.strip().split()
    print(instruction)
    print(tokens)
    final1=[]
    for i in tokens:
        if i[len(i)-1]==",":
                i=i[0:len(i)-1]
                final1.append(i)
        else:
             final1.append(i)
    print(final1)
    return final1
#c = assemble_instruction("add r23, r1, r2")
def identificationforR(tokens):
    function7="0000000"
    if(tokens[0]=="sub"):
         function7="0100000"
    final_output=""
    final_output=final_output+oppcodes[tokens[0]]
    final_output=final_output+registers[tokens[1]]
    final_output=final_output+oppcodesforR[tokens[0]]
    final_output=final_output+registers[tokens[2]]
    final_output=final_output+registers[tokens[3]]
    final_output=final_output+function7
    return(final_output)
    print(len(final_output))
#identificationforR(c)
def identificationfori(tokens):
    final_output=""
    if(tokens[0]=="lw"):
        binary_number=convert_to_binary[tokens[2]]
        final_output=final_output+oppcodes[tokens[0]]
        final_output=final_output+registers[tokens[1]]
        final_output=final_output+oppcodesforI[tokens[0]]
        final_output=final_output+registers[tokens[3]]
        final_output=final_output+binary_number
    else:
        binary_number=convert_to_binary[tokens[2]]
        final_output=final_output+oppcodes[tokens[0]]
        final_output=final_output+registers[tokens[1]]
        final_output=final_output+oppcodesforI[tokens[0]]
        final_output=final_output+registers[tokens[3]]
        final_output=final_output+binary_number
    return(final_output)
def identificationforS(tokens):
     final_output=""
     final_output=final_output+oppcodes["sw"]
     final_output=final_output+registers[tokens[1]]
     binary_number_S=convert_to_binary[tokens[2]]
     final_output=final_output+registers[tokens[3]]
     final_output=final_output+binary_number_S
     return(final_output)
def identificationforU(tokens):
     final_output=""
     final_output=final_output+oppcodes[tokens[0]]
     final_output=final_output+registers[tokens[1]]
     binary_number_U=convert_to_binary[tokens[2]]
     final_output=final_output+binary_number_U
     return(final_output)
def identificationforJ(tokens):
     final_output=""
     final_output=final_output+oppcodes[tokens[0]]
     final_output=final_output+registers[tokens[1]]
     binary_number_J=convert_to_binary[tokens[2]]
     final_output=final_output+binary_number_J
     return(final_output)
def identificationforB(tokens):
     final_output=""
     final_output=final_output+oppcodes["blt"]
     final_output=final_output+registers[tokens[1]]
     binary_number_B=convert_to_binary[tokens[2]]
     final_output=final_output+registers[tokens[3]]
     final_output=final_output+binary_number_B
     return(final_output)


    

