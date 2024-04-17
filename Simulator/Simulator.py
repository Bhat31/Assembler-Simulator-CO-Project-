import sys

register_names = {
    "00000": "zero", "00001": "ra", "00010": "sp", "00011": "gp", "00100": "tp",
    "00101": "t0", "00110": "t1", "00111": "t2", "01000": "s0", "01001": "s1",
    "01010": "a0", "01011": "a1", "01100": "a2", "01101": "a3", "01110": "a4",
    "01111": "a5", "10000": "a6", "10001": "a7", "10010": "s2", "10011": "s3",
    "10100": "s4", "10101": "s5", "10110": "s6", "10111": "s7", "11000": "s8",
    "11001": "s9", "11010": "s10", "11011": "s11", "11100": "t3", "11101": "t4",
    "11110": "t5", "11111": "t6"
}

registers = {reg: 0 for reg in register_names}

# Define data memory and stack memory
data_memory = {0x0001_0000 + 4 * i: 0 for i in range(32)}
stack_memory = {0x0000_0100 + 4 * i: 0 for i in range(32)}




def signed(val):
    return val if val >= 0 else 2**32 - val

def sign_extension(binary, num_bits):
    return binary if binary[0] == '0' else '1' * (num_bits - len(binary)) + binary

def twocomp_to_dec(binary):
    return -int(binary[1:], 2) if binary[0] == '1' else int(binary, 2)

def dec_to_twocomp(decimal_num, num_bits):
    new_dec = decimal_num if decimal_num >= 0 else decimal_num + 2**num_bits
    return format(new_dec, '0' + str(num_bits) + 'b')

def unsigned(val):
    return val if val >= 0 else 2**32 + val

class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction
        self.opcode = instruction[-7:]

        # Define separate type lists for each instruction type
        R_type = ["0110011"]
        I_type = ["0000011", "0010011", "1100111"]
        S_type = ["0100011"]
        B_type = ["1100011"]
        U_type = ["0110111", "0010111"]
        J_type = ["1101111"]

        if self.opcode in R_type:
            self.type, self.rs1, self.rs2, self.rd, self.funct3, self.funct7 = "R", instruction[-20:-15], instruction[-25:-20], instruction[-12:-7], instruction[-15:-12], instruction[:7]

        elif self.opcode in I_type:
            self.type, self.rd, self.imm = "I", instruction[-20:-15], instruction[0:12]

        elif self.opcode in U_type:
            self.type, self.rd, self.imm = "U", instruction[-12:-7], instruction[0:20]

        elif self.opcode in S_type:
            self.type, self.rs1, self.rs2, self.imm, self.funct3 = "S", instruction[-20:-15], instruction[-25:-20], instruction[0:7] + instruction[-12:-7], instruction[-15:-12]

        elif self.opcode in B_type:
            self.type, self.rs1, self.rs2, self.imm, self.funct3 = "B", instruction[-20:-15], instruction[-25:-20], instruction[0] + instruction[-8] + instruction[1:7] + instruction[-12:-8] + '0', instruction[-15:-12]

        elif self.opcode in J_type:
            self.type, self.rd, self.imm = "J", instruction[-12:-7], instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'

def regValue(reg):
    return registers[reg]


def regWrite(reg, value):
    if reg != "00000":
        registers[reg] = value

# R-type Instructions
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
    # print(f"rs1: {rs1} imm: {imm}")
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
    # print(f"rs1: {rs1} rs2: {rs2}")
    # print(f"imm: {twocomp_to_dec(instr.imm)//4}")
    if rs1 == rs2:
        pc = pc + twocomp_to_dec(instr.imm)//4
    else:
        pc = pc + 1
    return pc
    # print(f"PC: {pc}")

def bne(instr,pc):
    rs1 = regValue(instr.rs1)
    rs2 = regValue(instr.rs2)
    # print(f"rs1: {rs1} rs2: {rs2}")
    # print(f"rs1: {reg_file[instr.rs1]} rs2: {reg_file[instr.rs2]}")
    # print(f"rs1: {rs1} rs2: {rs2}")
    # print(f"imm: {twocomp_to_dec(instr.imm)//4}")
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
    # print(f"imm: {imm}")
    regWrite(instr.rd, pc*4 + imm)
    # print(f"PC: {pc}")
    # print(f"rd: {instr.rd} {reg_file[instr.rd]} {regValue(instr.rd)}")

def lui(instr):
    imm = twocomp_to_dec(instr.imm) << 12
    # print(f"imm: {imm}")
    regWrite(instr.rd, imm)


# J-type instructions

def jal(instr,pc):
    imm = twocomp_to_dec(instr.imm)//4
    regWrite(instr.rd, (pc + 1)*4)
    pc = pc + imm
    # print(f"PC: {pc}")
    return pc

def main(input_file, output_file):
    PC=0
    instr_dict = {i: line.strip() for i, line in enumerate(open(input_file, "r"))}
    pcCopy = 0

    while pcCopy < len(instr_dict):
        inst = Instruction(instr_dict[pcCopy])
        print(f"{inst.instruction}{inst.opcode}")
        pcCopy += 1

    virtual_halt = "00000000000000000000000001100011"
    halt = False
    all_reg_vals = []

    while PC < len(instr_dict) and not halt:
        current_reg_vals = f"0b{dec_to_twocomp(PC * 4, 32)} "

        if instr_dict[PC] == virtual_halt:
            halt = True
        else:
            inst = Instruction(instr_dict[PC])
            if inst.type == "R":
                if inst.funct7 == "0100000":
                    sub(inst)
                else:
                    R_FUNCTIONS = {"000": add, "001": sll, "010": slt, "011": sltu, "100": xor, "101": srl, "110": or_, "111": and_}
                    R_FUNCTIONS[inst.funct3](inst)

            elif inst.type == "I":
                if inst.opcode == "0000011":
                    lw(inst)
                elif inst.opcode == "1100111":
                    PC = jalr(inst, PC)
                elif inst.opcode == "0010011" and inst.funct3 == "000":
                    addi(inst)
                elif inst.opcode == "0010011" and inst.funct3 == "011":
                    sltiu(inst)

            elif inst.type == "S":
                sw(inst)

            elif inst.type == "B":
                B_FUNCTIONS = {"000": beq, "001": bne, "100": blt, "101": bge, "110": bltu, "111": bgeu}
                PC = B_FUNCTIONS[inst.funct3](inst, PC)

            elif inst.type == "U":
                if inst.opcode == "0110111":
                    lui(inst)
                elif inst.opcode == "0010111":
                    auipc(inst, PC)

            elif inst.type == "J":
                PC = jal(inst, PC)

            if not PC:
                PC += 1

            for reg in registers:
                current_reg_vals += f"0b{bin(registers[reg] if registers[reg] >= 0 else registers[reg] & 0xffffffff)[2:].zfill(32)} "

            all_reg_vals.append(current_reg_vals)

    final_data_mem = [f"0x{hex(mem)[2:].zfill(8)}:0b{bin(data_memory[mem] if data_memory[mem] >= 0 else data_memory[mem] & 0xffffffff)[2:].zfill(32)}" for mem in data_memory]

    with open(output_file, "w") as f:
        f.write("\n".join(all_reg_vals + final_data_mem))
if __name__ == "__main__":
    main("C:/Users/lenovo/Desktop/test1.txt", "C:/Users/lenovo/Desktop/out.txt")
