#!/usr/bin/env python3
import array
import sys
import re

# we need as simple as possible brainfuck interpreter, so we can later implement it on fpga

class BF_intrp:
  valid_ops = '><+-.,[]'

  def __init__(self, bytecode = ""):
    self.addr_ptr = 0
    self.prog_ctr = 0
    self.memory = array.array("B", [0])
    self.jmp_stack = []
    self.bytecode = bytecode

  def process(self, op):
    if op == '+':
      try:
        self.memory[self.addr_ptr] += 1
      except:
        BF_intrp.abort("[memory error] byte overflow")

    elif op == '-':
      self.memory[self.addr_ptr] -= 1

    elif op == '>':
      self.addr_ptr += 1
      if self.addr_ptr > len(self.memory) - 1:
        self.memory.extend([0])

    elif op == '<':
      self.addr_ptr -= 1
      if self.addr_ptr < 0:
        BF_intrp.abort("[memory error] hit bound at -1")

    elif op == '.':
      print(chr(self.memory[self.addr_ptr]), end='')

    elif op == ',':
      while 1:
        input_byte = input()
        try:
          self.memory[self.addr_ptr] = int(input_byte)
          break
        except:
          print('Enter number [0-255]')
    
    elif op == '[':
      if self.memory[self.addr_ptr] == 0:
        base_ptr = self.prog_ctr
        while 1:
          if self.bytecode[base_ptr] == ']':
            if len(self.jmp_stack) == 1:
              self.prog_ctr = base_ptr
              return
            else:
              self.jmp_stack.pop()
              
          elif self.bytecode[base_ptr] == '[': 
            self.jmp_stack.append('[')

          base_ptr += 1

    elif op == ']':
      if self.memory[self.addr_ptr] != 0:
        base_ptr = self.prog_ctr
        while 1:
          if self.bytecode[base_ptr] == '[':
            if len(self.jmp_stack) == 1:
              self.prog_ctr = base_ptr
              self.jmp_stack.pop()
              return
            else:
              self.jmp_stack.pop()
              
          elif self.bytecode[base_ptr] == ']': 
            self.jmp_stack.append(']')

          base_ptr -= 1

  def mem_size(self):
    return len(self.memory)
       
  def execute(self):
    self.bytecode = re.sub('[^><+-.,\[\]]', '', self.bytecode)
    while 1:
      self.process(self.bytecode[self.prog_ctr])
      self.prog_ctr += 1
      if self.prog_ctr >= len(self.bytecode):
        print('\n[system] execution end')
        return

  def abort(msg):
    print(msg)
    sys.exit(1)

if __name__ == "__main__":
  #test_bytecode = '++[><[,]]>++.<.'
  #test_bytecode = '+[+.]'
  hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

  #intrp = BF_intrp(test_bytecode)
  intrp = BF_intrp(hello_world)
  intrp.execute()

