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


PrgC = 0 # Program Counter

PrgCMax = 4*(len(lines_noblank)-1)

if PrgCMax > 255:
    print('Error: Program memory exceeded:no of instr > 64')
    sys.exit()

stackCounter = 32 #for tracking variables don't exceed stack memory


def mem_stat_print():
    outputstr = ''
    outputstr = outputstr + '0x00010000:' + '0b'+ datamem_dict[65536]
    outputstr = outputstr + '\n' + '0x00010004:' + '0b'+ datamem_dict[65540]
    outputstr = outputstr + '\n' + '0x00010008:' + '0b'+ datamem_dict[65544]
    outputstr = outputstr + '\n' + '0x0001000c:' + '0b'+ datamem_dict[65548]
    outputstr = outputstr + '\n' + '0x00010010:' + '0b'+ datamem_dict[65552]
    outputstr = outputstr + '\n' + '0x00010014:' + '0b'+ datamem_dict[65556]
    outputstr = outputstr + '\n' + '0x00010018:' + '0b'+ datamem_dict[65560]
    outputstr = outputstr + '\n' + '0x0001001c:' + '0b'+ datamem_dict[65564]
    outputstr = outputstr + '\n' + '0x00010020:' + '0b'+ datamem_dict[65568]
    outputstr = outputstr + '\n' + '0x00010024:' + '0b'+ datamem_dict[65572]
    outputstr = outputstr + '\n' + '0x00010028:' + '0b'+ datamem_dict[65576]
    outputstr = outputstr + '\n' + '0x0001002c:' + '0b'+ datamem_dict[65580]
    outputstr = outputstr + '\n' + '0x00010030:' + '0b'+ datamem_dict[65584]
    outputstr = outputstr + '\n' + '0x00010034:' + '0b'+ datamem_dict[65588]
    outputstr = outputstr + '\n' + '0x00010038:' + '0b'+ datamem_dict[65592]
    outputstr = outputstr + '\n' + '0x0001003c:' + '0b'+ datamem_dict[65596]
    outputstr = outputstr + '\n' + '0x00010040:' + '0b'+ datamem_dict[65600]
    outputstr = outputstr + '\n' + '0x00010044:' + '0b'+ datamem_dict[65604]
    outputstr = outputstr + '\n' + '0x00010048:' + '0b'+ datamem_dict[65608]
    outputstr = outputstr + '\n' + '0x0001004c:' + '0b'+ datamem_dict[65612]
    outputstr = outputstr + '\n' + '0x00010050:' + '0b'+ datamem_dict[65616]
    outputstr = outputstr + '\n' + '0x00010054:' + '0b'+ datamem_dict[65620]
    outputstr = outputstr + '\n' + '0x00010058:' + '0b'+ datamem_dict[65624]
    outputstr = outputstr + '\n' + '0x0001005c:' + '0b'+ datamem_dict[65628]
    outputstr = outputstr + '\n' + '0x00010060:' + '0b'+ datamem_dict[65632]
    outputstr = outputstr + '\n' + '0x00010064:' + '0b'+ datamem_dict[65636]
    outputstr = outputstr + '\n' + '0x00010068:' + '0b'+ datamem_dict[65640]
    outputstr = outputstr + '\n' + '0x0001006c:' + '0b'+ datamem_dict[65644]
    outputstr = outputstr + '\n' + '0x00010070:' + '0b'+ datamem_dict[65648]
    outputstr = outputstr + '\n' + '0x00010074:' + '0b'+ datamem_dict[65652]
    outputstr = outputstr + '\n' + '0x00010078:' + '0b'+ datamem_dict[65656]
    outputstr = outputstr + '\n' + '0x0001007c:' + '0b'+ datamem_dict[65660]
    # print htake .write( )
    outputfile.write(outputstr)
    



# decimal to binary with sign ext converter
def dec2bin_sext(n,bits):
    n_1 = str(bin(n))
    if n >= 0:
        n_2 = '0' + n_1[2:]
        if len(n_2) > bits:
            x = len(n_2) - bits
            n_2 = n_2[x:]
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
            x = len(n_2) - bits
            n_2 = n_2[x:]
        else:
            n_2 = '1'*(bits-len(n_2)) + n_2
    return n_2

def reg_print():
    
    global PrgC
    outstr = ''
    outstr = outstr +'0b'+ dec2bin_sext(PrgC,32) +' '+ '0b'+ reg_data['zero']
    outstr = outstr + ' ' + '0b'+ reg_data['ra']
    outstr = outstr + ' ' + '0b'+ reg_data['sp']
    outstr = outstr + ' ' + '0b'+ reg_data['gp']
    outstr = outstr + ' ' + '0b'+ reg_data['tp']
    outstr = outstr + ' ' + '0b'+ reg_data['t0']
    outstr = outstr + ' ' + '0b'+ reg_data['t1']
    outstr = outstr + ' ' + '0b'+ reg_data['t2']
    outstr = outstr + ' ' + '0b'+ reg_data['s0']
    outstr = outstr + ' ' + '0b'+ reg_data['s1']
    outstr = outstr + ' ' + '0b'+ reg_data['a0']
    outstr = outstr + ' ' + '0b'+ reg_data['a1']
    outstr = outstr + ' ' + '0b'+ reg_data['a2']
    outstr = outstr + ' ' + '0b'+ reg_data['a3']
    outstr = outstr + ' ' + '0b'+ reg_data['a4']
    outstr = outstr + ' ' + '0b'+ reg_data['a5']
    outstr = outstr + ' ' + '0b'+ reg_data['a6']
    outstr = outstr + ' ' + '0b'+ reg_data['a7']
    outstr = outstr + ' ' + '0b'+ reg_data['s2']
    outstr = outstr + ' ' + '0b'+ reg_data['s3']
    outstr = outstr + ' ' + '0b'+ reg_data['s4']
    outstr = outstr + ' ' + '0b'+ reg_data['s5']
    outstr = outstr + ' ' + '0b'+ reg_data['s6']
    outstr = outstr + ' ' + '0b'+ reg_data['s7']
    outstr = outstr + ' ' + '0b'+ reg_data['s8']
    outstr = outstr + ' ' + '0b'+ reg_data['s9']
    outstr = outstr + ' ' + '0b'+ reg_data['s10']
    outstr = outstr + ' ' + '0b'+ reg_data['s11']
    outstr = outstr + ' ' + '0b'+ reg_data['t3']
    outstr = outstr + ' ' + '0b'+ reg_data['t4']
    outstr = outstr + ' ' + '0b'+ reg_data['t5']
    outstr = outstr + ' ' + '0b'+ reg_data['t6'] + '\n'

    outputfile.write(outstr)
    

def bin2dec(n):
    #print(n)
    if n[0] == '0':
        a = int(n, 2) 
    else:
        a = ''.join('1' if bit == '0' else '0' for bit in n)
        a = int(a, 2) + 1
        a = (-1)* a
    return a

def unsign_bin2dec(n):
    y = int(n,2)
    return y

def twos_comp(binary_str):
    flipped_binary_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    
    twos_comp_result = bin2dec(flipped_binary_str) + 1
    twos_comp_result = dec2bin_sext(twos_comp_result,32)

    return twos_comp_result



def add_signed_binary(bin1, bin2):
    
    # Perform signed binary addition
    a = bin2dec(bin1)
    b = bin2dec(bin2)
    c = a+b
    result = dec2bin_sext(c,32)

    return result

reg_dict = {
    '00000':'zero',
    '00001':'ra',
    '00010':'sp',
    '00011':'gp',
    '00100':'tp',
    '00101':'t0',
    '00110':'t1',
    '00111':'t2',
    '01000':'s0',
    '01001':'s1',
    '01010':'a0',
    '01011':'a1',
    '01100':'a2',
    '01101':'a3',
    '01110':'a4',
    '01111':'a5',
    '10000':'a6',
    '10001':'a7',
    '10010':'s2',
    '10011':'s3',
    '10100':'s4',
    '10101':'s5',
    '10110':'s6',
    '10111':'s7',
    '11000':'s8',
    '11001':'s9',
    '11010':'s10',
    '11011':'s11',
    '11100':'t3',
    '11101':'t4',
    '11110':'t5',
    '11111':'t6',
}

reg_data = {
    'zero': '00000000000000000000000000000000',
    'ra':   '00000000000000000000000000000000',
    'sp':   '00000000000000000000000100000000',
    'gp':   '00000000000000000000000000000000',
    'tp':   '00000000000000000000000000000000',
    't0':   '00000000000000000000000000000000',
    't1':   '00000000000000000000000000000000',
    't2':   '00000000000000000000000000000000',
    's0':   '00000000000000000000000000000000',
    's1':   '00000000000000000000000000000000',
    'a0':   '00000000000000000000000000000000',
    'a1':   '00000000000000000000000000000000',
    'a2':   '00000000000000000000000000000000',
    'a3':   '00000000000000000000000000000000',
    'a4':   '00000000000000000000000000000000',
    'a5':   '00000000000000000000000000000000',
    'a6':   '00000000000000000000000000000000',
    'a7':   '00000000000000000000000000000000',
    's2':   '00000000000000000000000000000000',
    's3':   '00000000000000000000000000000000',
    's4':   '00000000000000000000000000000000',
    's5':   '00000000000000000000000000000000',
    's6':   '00000000000000000000000000000000',
    's7':   '00000000000000000000000000000000',
    's8':   '00000000000000000000000000000000',
    's9':   '00000000000000000000000000000000',
    's10':  '00000000000000000000000000000000',
    's11':  '00000000000000000000000000000000',
    't3':   '00000000000000000000000000000000',
    't4':   '00000000000000000000000000000000',
    't5':   '00000000000000000000000000000000',
    't6':   '00000000000000000000000000000000',
}

datamem_dict = {
    65536: '00000000000000000000000000000000',
    65540: '00000000000000000000000000000000',
    65544: '00000000000000000000000000000000',
    65548: '00000000000000000000000000000000',
    65552: '00000000000000000000000000000000',
    65556: '00000000000000000000000000000000',
    65560: '00000000000000000000000000000000',
    65564: '00000000000000000000000000000000',
    65568: '00000000000000000000000000000000',
    65572: '00000000000000000000000000000000',
    65576: '00000000000000000000000000000000',
    65580: '00000000000000000000000000000000',
    65584: '00000000000000000000000000000000',
    65588: '00000000000000000000000000000000',
    65592: '00000000000000000000000000000000',
    65596: '00000000000000000000000000000000',
    65600: '00000000000000000000000000000000',
    65604: '00000000000000000000000000000000',
    65608: '00000000000000000000000000000000',
    65612: '00000000000000000000000000000000',
    65616: '00000000000000000000000000000000',
    65620: '00000000000000000000000000000000',
    65624: '00000000000000000000000000000000',
    65628: '00000000000000000000000000000000',
    65632: '00000000000000000000000000000000',
    65636: '00000000000000000000000000000000',
    65640: '00000000000000000000000000000000',
    65644: '00000000000000000000000000000000',
    65648: '00000000000000000000000000000000',
    65652: '00000000000000000000000000000000',
    65656: '00000000000000000000000000000000',
    65660: '00000000000000000000000000000000',

}


def R_type_enc(line):
    global outstr
    global PrgC
    global stackCounter

    func7 = line[0:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    rd = line[20:25]

    if func3 == '000':
        if func7 == '0000000':
            reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],reg_data[reg_dict[rs2]])
        elif func7 == '0100000':
            if rs1 == '00000':
                reg_data[reg_dict[rd]] = twos_comp(reg_data[reg_dict[rs2]])
            else:
                x = twos_comp(reg_data[reg_dict[rs2]])
                reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],x)

    elif func3 == '001':
        
        y = unsign_bin2dec(reg_data[reg_dict[rs2]][-5:])
        
        x = bin2dec(reg_data[reg_dict[rs1]])
        z = x << y
        reg_data[reg_dict[rd]] = dec2bin_sext(z,32)
        

    elif func3 == '010':
        a = bin2dec(reg_data[reg_dict[rs1]])
        b = bin2dec(reg_data[reg_dict[rs2]])
        if a < b:
            reg_data[reg_dict[rd]] = dec2bin_sext(1,32)

    elif func3 == '011':
        a = unsign_bin2dec(reg_data[reg_dict[rs1]])
        b = unsign_bin2dec(reg_data[reg_dict[rs2]])
        if a < b:
            reg_data[reg_dict[rd]] = dec2bin_sext(1,32)
    
    elif func3 == '100':
        reg_data[reg_dict[rd]] = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))

    elif func3 == '101':
        
        x = unsign_bin2dec(reg_data[reg_dict[rs2]][-5:])
         
        #y = bin2dec(reg_data[reg_dict[rs1]])
        #z = y >> x
        z = '0'*x + reg_data[reg_dict[rs1]][0:-x]
        #reg_data[reg_dict[rd]] = dec2bin_sext(z,32)
        reg_data[reg_dict[rd]] = z


    elif func3 == '110':
        reg_data[reg_dict[rd]] = ''.join('1' if bit1 == '1' or bit2 == '1' else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))
    
    elif func3 == '111':
        reg_data[reg_dict[rd]] = ''.join('1' if bit1 == '1' and bit2 == '1' else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))
    
    PrgC = PrgC + 4
    reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
    reg_print()
        


def I_type_enc(line):
    global outstr
    global PrgC
    global stackCounter
    
    imm = line[0:12]
    x = bin2dec(imm)
    rs1 = line[12:17]
    func3 = line[17:20]
    rd = line[20:25]
    opcode = line[25:]

    if func3 == '010':
        reg_data[reg_dict[rd]] = datamem_dict[bin2dec(add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32)))]
        PrgC = PrgC + 4
        reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
        reg_print()
        
    elif func3 == '011':
        a = unsign_bin2dec(reg_data[reg_dict[rs1]])
        b = unsign_bin2dec(imm)
        if a < b:
            reg_data[reg_dict[rd]] = dec2bin_sext(1,32)
        PrgC = PrgC + 4
        reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
        reg_print()

    elif func3 == '000':
        if opcode == '0010011':
            
            reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32))
           
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            
            reg_print()
            
        else:
            reg_data[reg_dict[rd]] = dec2bin_sext((PrgC+4),32)
            
            PrgC = add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32))
            
            PrgC = PrgC[:-1] + '0'
            
            PrgC = bin2dec(PrgC)
            
            
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        
            



def S_type_enc(line):
    global outstr
    global PrgC
    global stackCounter

    imm0 = line[0:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    imm1 = line[20:25]
    imm = imm0 + imm1
    x = bin2dec(imm)
    datamem_dict[bin2dec(add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32)))] = reg_data[reg_dict[rs2]]

    PrgC = PrgC + 4
    reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
    reg_print()


def B_type_enc(line):
    global outstr
    global PrgC
    global stackCounter
    #print(line)
    imm1 = line[0]
    imm3 = line[1:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    imm4 = line[20:24]
    imm2 = line[24]
    imm = imm1 + imm2 + imm3 + imm4 + '0'
    #print(imm)
    x = bin2dec(imm)
    #print(x)
    a = bin2dec(reg_data[reg_dict[rs1]])
    b = bin2dec(reg_data[reg_dict[rs2]])
    #print(a)
    #print(b)
    if func3 == '000':
        if a == b:
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()

    elif func3 == '001':
        if a != b:
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()

    elif func3 == '100':
        if a < b:
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            #print('yes')
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()

    elif func3 == '101':
        if a >= b:
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()

    elif func3 == '110':
        if unsign_bin2dec(a) < unsign_bin2dec(b):
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()

    elif func3 == '111':
        if unsign_bin2dec(a) >= unsign_bin2dec(b):
            PrgC = PrgC + x
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()
        else:
            PrgC = PrgC + 4
            reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
            reg_print()


def U_type_enc(line):
    global outstr
    global PrgC
    global stackCounter
    
    imm = line[0:20] + '000000000000'
    rd = line[20:25]
    opcode = line[25:]

    if opcode == '0110111':
        reg_data[reg_dict[rd]] = imm
        PrgC = PrgC + 4
        reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
        reg_print()
    else:
        reg_data[reg_dict[rd]] = add_signed_binary(imm,dec2bin_sext(PrgC,32))
        PrgC = PrgC + 4
        reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
        reg_print()


def J_type_enc(line):
    global outstr
    global PrgC
    global stackCounter
    #print('Yes')
    imm1 = line[0]
    imm4 = line[1:11]
    imm3 = line[11]
    imm2 = line[12:20]
    rd = line[20:25]
    imm = imm1 + imm2 + imm3 + imm4 + '0'
    #print(imm)
    x = bin2dec(imm)
    #print(x)
    reg_data[reg_dict[rd]] = dec2bin_sext((PrgC+4),32)
    PrgC = add_signed_binary(dec2bin_sext(x,32),dec2bin_sext(PrgC,32))
    PrgC = PrgC[:-1] + '0'
    PrgC = bin2dec(PrgC)
    reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
    reg_print()

def rst_enc(line):
    global outstr
    global PrgC
    global stackCounter

    reg_data[reg_dict['00000']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00001']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00010']] = '00000000000000000000000100000000'
    reg_data[reg_dict['00011']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00100']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00101']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00110']] = '00000000000000000000000000000000'
    reg_data[reg_dict['00111']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01000']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01001']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01010']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01011']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01100']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01101']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01110']] = '00000000000000000000000000000000'
    reg_data[reg_dict['01111']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10000']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10001']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10010']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10011']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10100']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10101']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10110']] = '00000000000000000000000000000000'
    reg_data[reg_dict['10111']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11000']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11001']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11010']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11011']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11100']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11101']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11110']] = '00000000000000000000000000000000'
    reg_data[reg_dict['11111']] = '00000000000000000000000000000000'

    PrgC = PrgC + 4
    reg_print()

def rvrs_enc(line):
    global outstr
    global PrgC
    global stackCounter

    rs1 = line[12:17]
    rd = line[20:25]

    reg_data[reg_dict[rd]] = reg_data[reg_dict[rs1]][::-1]
    PrgC = PrgC + 4
    reg_print()

def mul_enc(line):
    global outstr
    global PrgC
    global stackCounter

    func7 = line[0:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    rd = line[20:25]

    a = bin2dec(reg_data[reg_dict[rs1]])
    b = bin2dec(reg_data[reg_dict[rs2]])
    c = a*b
    reg_data[reg_dict[rd]] = dec2bin_sext(c,32)

    PrgC = PrgC + 4
    reg_print()


def instr_Ident(line):
    global PrgC
    opcode= line[-7:]
    if opcode == '0110011':
        R_type_enc(line)

    elif opcode == '0000011':
        I_type_enc(line)

    elif opcode == '0010011':
        I_type_enc(line)

    elif opcode == '1100111':
        I_type_enc(line)

    elif opcode == '0100011':
        S_type_enc(line)

    elif opcode == '1100011':
        B_type_enc(line)
    
    elif opcode == '0110111':
        U_type_enc(line)

    elif opcode == '0010111':
        U_type_enc(line)

    elif opcode == '1101111':
        J_type_enc(line)


    elif opcode == '0000000':
        rst_enc(line)

    elif opcode == '1000000':
        mul_enc(line)

    elif opcode == '1000001':
        rvrs_enc(line)





while(PrgC <= PrgCMax):
    line = lines_noblank[int(PrgC/4)]
    if line == '00000000000000000000000001100011': #virtual halt
        reg_print()
        mem_stat_print()
        break

    if line == '11111111111111111111111111111111': #halt 
        reg_print()
        mem_stat_print()
        break


    instr_Ident(line)
    
