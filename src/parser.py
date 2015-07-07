import ply.yacc as yacc
        
from lexer import tokens

class Instruction(object):

    def __init__(self, opcode, operands, condition=None):
        self.opcode = opcode
        self.condition = condition
        
        self.operands = operands
        
    def __repr__(self):
        return "Instruction: {0}.{1} {2}".format(self.opcode,
                                                self.condition,
                                                self.operands)

class Label(object):

    def __init__(self, name, offset=None):
        self.name = name
        self.offset = offset
        
    def __repr__(self):
        return "Label: {0}".format(self.name)
    
class Register(object):

    def __init__(self, index):
        self.index = index
    
    def __repr__(self):
        return "Register: {0}".format(self.index)
        
class Pointer(object):

    def __init__(self, base, offset=None):
        self.base = base
        self.offset = offset
        
    def __repr__(self):
        return "Pointer: <{0}> + <{1}>".format(self.base, self.offset)

start = "line"
        
def p_register_operand(p):
    'register_operand : REGISTER'
    p[0] = Register(p[1])
            
def p_literal_operand(p):
    'literal_operand : LITERAL'
    p[0] = p[1]
    
def p_label_operand(p):
    'label_operand : LABEL'
    p[0] = Label(p[1])
    
def p_numeric_operand(p):
    '''numeric_operand : register_operand
                        | literal_operand'''
    p[0] = p[1]
    
def p_operand(p):
    '''operand : register_operand
                | literal_operand
                | label_operand
                | pointer_operand'''
    p[0] = p[1]
                
def p_pointer_operand(p):
    '''pointer_operand : LBRACKET numeric_operand RBRACKET
                        | LBRACKET register_operand RBRACKET'''
    p[0] = Pointer(p[2])
    
def p_pointer_operand_offset(p):
    #Relative addressing with offsets (e.g. ldr r2, [r3] or 
    # ldr r2, [$label, #4])
    '''pointer_operand : LBRACKET label_operand COMMA numeric_operand RBRACKET
                        | LBRACKET register_operand COMMA numeric_operand RBRACKET'''
                        
    p[0] = Pointer(p[2], p[4])
    
def p_mem_operand(p):
    '''mem_operand : label_operand
                    | pointer_operand''' 
    p[0] = p[1]             

def p_operand_list(p):
    'operand_list : operand COMMA operand'
    p[0] = [p[1], p[3]]
    
def p_long_operand_list(p):
    'operand_list : operand COMMA operand_list'
    p[0] = [p[1]] + p[3]
    
def p_instruction(p):
    '''instruction : OPCODE CONDITION operand_list
                    | OPCODE operand_list
                    | OPCODE operand'''
    if len(p) > 4:
        p[0] = Instruction(p[1], p[3], p[2])
    else:
        p[0] = Instruction(p[1], p[2]) 
    
def p_line(p):
    '''line : instruction NEWLINE
            | instruction'''
    p[0] = p[1]
    
parser = yacc.yacc()

data = """add.eq r1, r3
sub r2, [$mem, #4] 
add r2, #3
add r3, r4
"""

for line in data.split("\n"):
    if len(line) > 0:
        print(parser.parse(line))
