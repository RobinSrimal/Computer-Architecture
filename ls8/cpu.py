"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        # stack pointer
        self.reg[7] = 0xF4
        # flag registry 
        self.flag = 0

        self.pc = 0
        

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":

            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "CMP":
            
            self.flag = ((self.reg[reg_a] < self.reg[reg_b]) << 2) | \
                        ((self.reg[reg_a] > self.reg[reg_b]) << 1) | \
                        ((self.reg[reg_a] == self.reg[reg_b]) << 0)

        elif op == "AND":

            self.reg[reg_a] &= self.reg[reg_b]

        elif op == "OR":

            self.reg[reg_a] |= self.reg[reg_b]

        elif op == "XOR":

            self.reg[reg_a] ^= self.reg[reg_b]

        elif op == "NOT":

            self.reg[reg_a] = ~self.reg[reg_a]

        elif op == "SHL":

            self.reg[reg_a] = self.reg[reg_a] << reg_b

        elif op == "SHR":

            self.reg[reg_a] = self.reg[reg_a] >> reg_b

        elif op == "MOD":

            self.reg[reg_a] %= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, location):

        if 0 <= location <= 255:

            return self.ram[location]

        else:

            print("incorrect input")

    def ram_write(self, location, value):

        if 0 <= location <= 255:

            self.ram[location] = value
        
        else:

            print("incorrect input")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:

            
            # write to registry
            if self.ram[self.pc] == 0b10000010:

                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]

                self.pc += 3
                
            # print from registry
            if self.ram[self.pc] == 0b01000111:

                print(self.reg[self.ram[self.pc + 1]])

                self.pc += 2

            # halt
            if self.ram[self.pc] == 0b00000001:

                sys.exit()


            # multiply
            if self.ram[self.pc] == 0b10100010:

                self.reg[self.ram[self.pc + 1]] *= self.reg[self.ram[self.pc + 2]]

                self.pc += 3

            # push on stack
            if self.ram[self.pc] == 0b01000101:

                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.reg[self.ram[self.pc +1]]

                self.pc += 2
                

            # pop from stack
            if self.ram[self.pc] == 0b01000110:

                self.reg[self.ram[self.pc + 1]] = self.ram[self.reg[7]]

                self.reg[7] +=  1
                self.pc += 2

            # compare registries
            if self.ram[self.pc] == 0b10100111:

                self.alu("CMP", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3
            
            # jump command
            if self.ram[self.pc] == 0b0101010:

                self.pc = self.reg[self.ram[self.pc + 1]]

            # JEQ
            if self.ram[self.pc] == 0b01010101:

                if self.flag & 1:

                    self.pc = self.reg[self.ram[self.pc +1]]

                else:

                    self.pc += 2

            # JNE
            if self.ram[self.pc] ==  0b01010110:

                if not self.flag & 1:

                    self.pc = self.reg[self.ram[self.pc +1]]

                else:

                    self.pc += 2


            # SUB
            if self.ram[self.pc] == 0b10100001:

                self.alu("SUB", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3

            # AND
            if self.ram[self.pc] == 0b10101000:

                self.alu("AND", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3


            # OR
            if self.ram[self.pc] == 0b10101010:

                self.alu("OR", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3

            #XOR
            if self.ram[self.pc] == 0b10101011:

                self.alu("XOR", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3

            #NOT
            if self.ram[self.pc] == 0b01101001:

                self.alu("NOT", self.ram[self.pc +1] , None)
                self.pc += 2

            #SHL
            if self.ram[self.pc] == 0b10101100:

                self.alu("SHL", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3

            #SHR
            if self.ram[self.pc] == 0b10101101:

                self.alu("SHR", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3

            #MOD
            if self.ram[self.pc] == 0b10100100:

                self.alu("MOD", self.ram[self.pc +1] , self.ram[self.pc + 2])
                self.pc += 3







            

            

