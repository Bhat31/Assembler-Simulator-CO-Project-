import re
registers = {
    "r0": "00000", #hardwired 0
    "r1": "00001", #ra Return address
    "r2": "00010", #sp Stack Pointer
    "r3": "00011", #gp Global Pointer
    "r4": "00100", #tp Thread Pointer
    "r5": "00101", #t0 Temporary/alternate link register
    "r6": "00110", #t1-2 Temporaries
    "r7": "00111", #t1-2 Temporaries
    "r8": "01000", #s0/fp Saved register/frame pointer
    "r9": "01001", #s1 Saved Register
    "r10": "01010",#a0-1 Function arguments/ return values
    "r11": "01011",# a0-1 Function arguments/ return values
    "r12": "01100",#Function arguments
    "r13": "01101",#Function arguments
    "r14": "01110",#Function arguments
    "r15": "01111",#Function arguments
    "r16": "10000",#Function arguments
    "r17": "10001",#Function arguments
    "r18": "10010", #s2 Saved registers
    "r19": "10011", #s3 save registers;
    "r20": "10100", #s4 saved register;
    "r21": "10101", #s5 saved register
    "r22": "10110", #s6 saved register
    "r23": "10111", #s7 saved register
    "r24": "11000", #s8 saved register
    "r25": "11001", # s9 saved register
    "r26": "11010", # s10 saved register
    "r27": "11011", # s11 saved register
    "r28": "11100", # t3 Temporaries
    "r29": "11101", # t4 Temporaries
    "r30": "11110", # t5 Temporaries
    "r31": "11111", # t6 Temporaries
}
oppcodes = { 'add': '0110011', 'sub': '0110011', 'sll': '0110011', 'slt': '0110011',
    'sltu': '0110011', 'xor': '0110011', 'srl': '0110011', 'or': '0110011',
    'and': '0110011', 'lw': '0000011', 'addi': '0010011', 'sltiu': '0010011',
    'jalr': '1100111', 'sw': '0100011', 'beq': '1100011', 'bne': '1100011',
    'bge': '1100011', 'bgeu': '1100011', 'blt': '1100011', 'bltu': '1100011',
    'auipc': '0010111', 'lui': '0110111', 'jal': '1101111'}
oppcodesforR= {"add":"000", "sub":"000", "sll":"001","slt":"010",
              "sltu":"011","xor":"100","srl":"101","or":"110","and":"111"}
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
c = assemble_instruction("add r23, r1, r2")
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
    print(final_output)
    print(len(final_output))
identificationforR(c)
