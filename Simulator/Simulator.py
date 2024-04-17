import sys
register_names = {
    "00000": "zero", "00001": "ra", "00010": "sp", "00011": "gp", "00100": "tp", "00101": "t0", "00110": "t1", "00111": "t2", "01000": "s0", "01001": "s1","01010": "a0", "01011": "a1", "01100": "a2", "01101": "a3", "01110": "a4",
    "01111": "a5", "10000": "a6", "10001": "a7", "10010": "s2", "10011": "s3","10100": "s4", "10101": "s5", "10110": "s6", "10111": "s7", "11000": "s8","11001": "s9", "11010": "s10", "11011": "s11", "11100": "t3", "11101": "t4",
    "11110": "t5", "11111": "t6"
}

registers = {reg: 0 for reg in register_names}
# DATA MEMORY
data_memory = {0x0001_0000 + 4 * i: 0 for i in range(32)}
# STACK MEMORY
stack_memory = {0x0000_0100 + 4 * i: 0 for i in range(32)}
# opcodes
R = ["0110011"]
I = ["0000011", "0010011", "1100111"]
S = ["0100011"]
B = ["1100011"]
U = ["0110111", "0010111"]
J = ["1101111"]

def regValue(reg):
    return registers[reg]
def regWrite(reg, value):
    if reg != "00000":
        registers[reg] = value
def sext(binary, num_bits):
    if binary[0] == "1":
        return "1" * (num_bits - len(binary)) + binary
    else:
        return "0" * (num_bits - len(binary)) + binary

def dec_to_twocomp(decimal_num, num_bits):
    if decimal_num >= 0:
        binary_str = bin(decimal_num)[2:].zfill(num_bits)
    else:
        positive_binary = bin(abs(decimal_num))[2:].zfill(num_bits)
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
        inverted_binary = bin(int(inverted_binary, 2) + 1)[2:].zfill(num_bits)
        binary_str = inverted_binary

    return binary_str

def twocomp_to_dec(binary_str):
    if binary_str[0] == '1':   
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        positive_binary = bin(int(inverted_binary, 2) + 1)[2:]    
        decimal_num = -int(positive_binary, 2)
    else:
        decimal_num = int(binary_str, 2)
    
    return decimal_num
def unsigned(val):
    if val >= 0:
        return val
    else:
        return 2**32 + val
class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction
        self.opcode = instruction[-7:]

        if self.opcode in R:
            self.type = "R"
            self.rs1 = instruction[-20:-15]
            self.rs2 = instruction[-25:-20]
            self.rd = instruction[-12:-7]
            self.funct3 = instruction[-15:-12]
            self.funct7 = instruction[:7]

        elif self.opcode in I:
            self.type = "I"
            self.rs1 = instruction[-20:-15]
            self.rd = instruction[-12:-7]
            self.imm = instruction[0:12]
            self.funct3 = instruction[-15:-12]

        elif self.opcode in S:
            self.type = "S"
            self.rs1 = instruction[-20:-15]
            self.rs2 = instruction[-25:-20]
            self.imm = instruction[0:7] + instruction[-12:-7]
            self.funct3 = instruction[-15:-12]
        
        elif self.opcode in B:
            self.type = "B"
            self.rs1 = instruction[-20:-15]
            self.rs2 = instruction[-25:-20]
            self.imm = instruction[0] + instruction[-8] + instruction[1:7] + instruction[-12:-8] + '0'
            self.funct3 = instruction[-15:-12]
        
        elif self.opcode in U:
            self.type = "U"
            self.rd = instruction[-12:-7]
            self.imm = instruction[0:20]
        
        elif self.opcode in J:
            self.type = "J"
            self.rd = instruction[-12:-7]
            self.imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
# R-type instructions
def add(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 + rs2
    regWrite(instr.rd, rd)

def sub(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 - rs2
    regWrite(instr.rd, rd)

def slt(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = 1 if rs1 < rs2 else 0
    regWrite(instr.rd, rd)

def sltu(instr):
    rs1 = unsigned(regValue(instr.rs1))
    rs2 = unsigned(regValue(instr.rs2))
    rd = 1 if rs1 < rs2 else 0
    regWrite(instr.rd, rd)

def xor(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 ^ rs2
    regWrite(instr.rd, rd)

def and_(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 & rs2
    regWrite(instr.rd, rd)

def or_(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 | rs2
    regWrite(instr.rd, rd)

def sll(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 << (rs2 & 0b11111)
    regWrite(instr.rd, rd)

def srl(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    rd = rs1 >> (rs2 & 0b11111)
    regWrite(instr.rd, rd)
# I-type instructions
def lw(instr):
    rs1 = regValue(instr.rs1)
    imm = int(instr.imm, 2)
    addr = rs1 + imm
    regWrite(instr.rd, data_memory[addr])

def addi(instr):
    rs1 = regValue(instr.rs1)
    imm = twocomp_to_dec(instr.imm)
    rd = rs1 + imm
    regWrite(instr.rd, rd)

def sltiu(instr):
    rs1 = unsigned(regValue(instr.rs1))
    imm = int(instr.imm, 2)
    rd = 1 if rs1 < imm else 0
    regWrite(instr.rd, rd)

def jalr(instr,pc):
    print('JALR')
    rs1 = regValue(instr.rs1)//4
    imm = twocomp_to_dec(instr.imm)//4
    regWrite(instr.rd, pc + 1)
    pc = rs1 + imm
    return pc
# S-type instructions
def sw(instr):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    imm = int(instr.imm, 2)
    addr = rs1 + imm
    data_memory[addr] = rs2
# B-type instructions
def beq(instr,pc):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
  
    if rs1 == rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc
    # print(f"PC: {pc}")

def bne(instr,pc):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    if rs1 != rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    # print(f"PC: {pc}")
    return pc

def blt(instr,pc):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    if rs1 < rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc

def bge(instr,pc):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    if rs1 >= rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc

def bltu(instr,pc):
    rs1 = unsigned(regValue(instr.rs1))
    rs2 = unsigned(regValue(instr.rs2))
    if rs1 < rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc

def bgeu(instr,pc):
    rs1 = unsigned(regValue(instr.rs1))
    rs2 = unsigned(regValue(instr.rs2))
    if rs1 >= rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc
# U-type instructions
def auipc(instr,pc):
    imm = twocomp_to_dec(instr.imm) << 12
    regWrite(instr.rd, pc*4 + imm)
def lui(instr):
    imm = twocomp_to_dec(instr.imm) << 12

    regWrite(instr.rd, imm)
# J-type instructions

def jal(instr,pc):
    imm = twocomp_to_dec(instr.imm)//4
    regWrite(instr.rd, (pc + 1)*4)
    pc = pc + imm
    return pc
def main(input_file,output_file):   
    PC = 0
    instr_dict = {}

    with open(input_file, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            instr_dict[i] = lines[i].strip()


    pcCopy = 0
    while pcCopy < len(instr_dict):
        instr = Instruction(instr_dict[pcCopy])
        print(f"{instr.instruction}{instr.opcode}")
        pcCopy+=1

    virtual_halt = "00000000000000000000000001100011"
    halt = False

    all_reg_vals = []
    final_data_mem = []

    while PC < len(instr_dict) and not halt:

        current_reg_vals=""
        pc_update = False
        if instr_dict[PC] == virtual_halt:
            halt = True

        else:
            instr = Instruction(instr_dict[PC])

            if instr.type == "R":
                if instr.funct7 == "0100000":
                    sub(instr)
                else:
                    if instr.funct3 == "000":
                        add(instr)
                    elif instr.funct3 == "001":
                        sll(instr)
                    elif instr.funct3 == "010":
                        slt(instr)
                    elif instr.funct3 == "011":
                        sltu(instr)
                    elif instr.funct3 == "100":
                        xor(instr)
                    elif instr.funct3 == "101":
                        srl(instr)
                    elif instr.funct3 == "110":
                        or_(instr)
                    elif instr.funct3 == "111":
                        and_(instr)

            elif instr.type == "I":
                if instr.opcode == "0000011":
                    lw(instr)
                elif instr.opcode == "1100111":
                    PC = jalr(instr, PC)
                    pc_update = True
                elif instr.opcode == "0010011":
                    if instr.funct3 == "000":
                        addi(instr)
                    elif instr.funct3 == "011":
                        sltiu(instr)

            elif instr.type == "S":
                sw(instr)

            elif instr.type == "B":
                if instr.funct3 == "000":
                    PC = beq(instr, PC)
                elif instr.funct3 == "001":
                    PC = bne(instr, PC)
                elif instr.funct3 == "100":
                    PC = blt(instr, PC)
                elif instr.funct3 == "101":
                    PC = bge(instr, PC)
                elif instr.funct3 == "110":
                    PC = bltu(instr, PC)
                elif instr.funct3 == "111":
                    PC = bgeu(instr, PC)
                pc_update = True

            elif instr.type == "U":
                if instr.opcode == "0110111":
                    lui(instr)
                elif instr.opcode == "0010111":
                    auipc(instr, PC)

            elif instr.type == "J":
                PC=jal(instr, PC)
                pc_update = True

            if pc_update==False:
                PC += 1

        current_reg_vals += f"0b{dec_to_twocomp(PC*4, 32)} "

        for reg in registers:
            if registers[reg] >= 0:
                current_reg_vals += (f"0b{bin(registers[reg])[2:].zfill(32)} ")
            else:
                current_reg_vals += (f"0b{bin(registers[reg] & 0xffffffff)[2:].zfill(32)} ")

        if not halt:
            all_reg_vals.append(current_reg_vals)
    for mem in data_memory:
        if data_memory[mem] >= 0:
            final_data_mem.append(f"0x{hex(mem)[2:].zfill(8)}:0b{bin(data_memory[mem])[2:].zfill(32)}")
        else:
            final_data_mem.append(f"0x{hex(mem)[2:].zfill(8)}:0b{bin(data_memory[mem] & 0xffffffff)[2:].zfill(32)}")
    with open(output_file, "w") as f:
      for val in all_reg_vals + final_data_mem:
        f.write(f"{val}\n")
if __name__ == "__main__":
    main("C:/Users/lenovo/Desktop/s_test4.txt", "C:/Users/lenovo/Desktop/out.txt")
