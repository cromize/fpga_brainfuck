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
    self.bytecode = bytecode

  def loop_iter(self, body_start, body_end, forward):
    # TODO: maybe make it find all occurrence and add, subtract instead of looping
    found_count = 0 
    while 1:
      if self.bytecode[self.prog_ctr] == body_end:
        found_count -= 1
      elif self.bytecode[self.prog_ctr] == body_start:
        found_count += 1
      if not found_count:
        return 
      if forward: self.prog_ctr += 1
      else: self.prog_ctr -= 1

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
        self.loop_iter('[', ']', 1)

    elif op == ']':
      if self.memory[self.addr_ptr] != 0:
        self.loop_iter(']', '[', 0)

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

  # test 30000 cells
  test = "++++[>++++++<-]>[>+++++>+++++++<<-]>>++++<[[>[[>>+<<-]<]>>>-]>-[>+>+<<-]>] +++++[>+++++++<<++>-]>.<<. "

  intrp = BF_intrp(hello_world)
  #intrp = BF_intrp(test)
  intrp.execute()
