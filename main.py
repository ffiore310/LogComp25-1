import sys
from typing import List
import re
import os

def get_output_path(filename):
    # Extrai o nome sem extensão
    asm_name = f"{da_nome(filename)}.asm"
    
    # Diretório esperado pelo teste
    base_dir = "/tmp/compiler-testing-lib/compiler_testing_lib/languages/TypeScript/v3.0"
    
    # Junta tudo no caminho absoluto correto
    return os.path.join(base_dir, asm_name)

def ts_repr(val):
    if val is True:
        return "true"
    elif val is False:
        return "false"
    elif val is None:
        return "null"
    return str(val)

def da_nome(filename):
    name = ""

    for c in filename:
        if c == ".":
            break
        else:
            name += c
    
    return name

class Prepro:
    comentario = re.compile(r'//[^\r\n]*')

    def filter(source: str) -> str:
        return Prepro.comentario.sub('', source)

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        while self.position < len(self.source) and (self.source[self.position] == " " or self.source[self.position] == "\n"):
            self.position += 1
            
        if self.position >= len(self.source):
            self.next = Token("EOF", '')
            self.position += 1

        elif self.source[self.position] == '-':
            self.next = Token("MINUS", '-')
            self.position += 1

        elif self.source[self.position] == '+':
            self.next = Token("PLUS", '+')
            self.position += 1

        elif self.source[self.position] == '*':
            self.next = Token("MULTI", '*')
            self.position += 1

        elif self.source[self.position] == '/':
            self.next = Token("DIV", '/')
            self.position += 1

        elif self.source[self.position:self.position+2] == '&&':
            self.next = Token("AND", '&&')
            self.position += 2

        elif self.source[self.position:self.position+2] == '||':
            self.next = Token("OR", '||')
            self.position += 2

        elif self.source[self.position] == '!':
            self.next = Token("NOT", '!')
            self.position += 1

        elif self.source[self.position] == '(':
            self.next = Token("OPEN_PAR", '(')
            self.position += 1

        elif self.source[self.position] == ')':
            self.next = Token("CLOSE_PAR", ')')
            self.position += 1

        elif self.source[self.position] == '{':
            self.next = Token("OPEN_BRA", '{')
            self.position += 1

        elif self.source[self.position] == '}':
            self.next = Token("CLOSE_BRA", '}')
            self.position += 1

        elif self.source[self.position] == '=':
            id = ""
            while self.position < len(self.source) and self.source[self.position] == '=':
                id += self.source[self.position]
                self.position += 1
            if id == "=":
                self.next = Token("ASSIGN", id)
            elif id == "==":
                raise Exception("[Lexer] Palavra '==' não existe na linguagem analisada")
            else:
                self.next = Token("EQ", id)

        elif self.source[self.position] == '>':
            self.next = Token("GT", '>')
            self.position += 1

        elif self.source[self.position] == '<':
            self.next = Token("LT", '<')
            self.position += 1

        elif self.source[self.position] == ';':
            self.next = Token("END", ';')
            self.position += 1

        elif self.source[self.position] == ':':
            self.next = Token("SEMI", ':')
            self.position += 1

        elif self.source[self.position] == '"':
            self.position += 1
            id = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                id += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token("STR", id)

        elif self.source[self.position].isalpha():
            id = ""
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                id += self.source[self.position]
                self.position += 1
            list = ["log", "if", "while", "else", "readline", "true", "false", "let"]
            types = ["number", "string", "boolean"]
            if id in list:
                if id == "log":
                    self.next = Token("PRINT", id)
                elif id == "if":
                    self.next = Token("IF", id)
                elif id == "while":
                    self.next = Token("WHILE", id)
                elif id == "else":
                    self.next = Token("ELSE", id)
                elif id == "readline":
                    self.next = Token("READ", id)
                elif id == "let":
                    self.next = Token("VAR", id)
                elif id == "true" or id == "false":
                    self.next = Token("BOOL", id)
            elif id in types:
                self.next = Token("TYPE", id)
            else:
                self.next = Token("IDEN", id)

        elif self.source[self.position].isdigit():
            numero = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                numero += self.source[self.position]
                self.position += 1
            inteiro = int(numero)
            self.next = Token("INT", inteiro)

        else:
            raise Exception("[Lexer] Símbolo não existe no alfabeto da Linguagem (typescript)")

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

class Parser:
    lex = None

    def parseProgram():
        filhos = []

        while Parser.lex.next.kind != "EOF":
            filhos.append(Parser.parseStatement())
            
        return Block(None, filhos)

    def parseStatement():
        resultado = None

        if Parser.lex.next.kind == "IDEN":
            id_node = Identifier(Parser.lex.next.value, [])
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "ASSIGN":
                raise Exception("[Parser] Era esperado '=' após identificador")
            Parser.lex.selectNext()

            expr_result = Parser.parseBoolExpression()
            resultado = Assignment(None, [id_node, expr_result])

            if Parser.lex.next.kind != "END":
                raise Exception("[Parser] Era esperado ';' ao final da atribuição")
            Parser.lex.selectNext()  # consome ';'

        elif Parser.lex.next.kind == "PRINT":
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'print'")
            Parser.lex.selectNext()

            expr_result = Parser.parseBoolExpression()

            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após expressão no print")
            Parser.lex.selectNext()

            resultado = Print(None, [expr_result])

            if Parser.lex.next.kind != "END":
                raise Exception("[Parser] Era esperado ';' ao final do print")
            Parser.lex.selectNext()  # consome ';'

        elif Parser.lex.next.kind == "VAR":
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "IDEN":
                raise Exception("[Parser] Era esperado um Identifier após token de declaração de variável")
            
            iden = Identifier(Parser.lex.next.value, [])
            
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "SEMI":
                raise Exception("[Parser] Era esperado um ':' na declaração de variável")
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "TYPE":
                raise Exception("[Parser] É necessário definir o tipo da variável durante a sua declaração")
            
            tipo = Parser.lex.next.value

            Parser.lex.selectNext()

            if Parser.lex.next.kind == "ASSIGN":
                Parser.lex.selectNext()
                expressao = Parser.parseBoolExpression()
                resultado = VarDec(tipo, [iden, expressao])
            else:
                resultado = VarDec(tipo, [iden])

            if Parser.lex.next.kind != "END":
                raise Exception("[Parser] Era esperado ';' ao final da declaração de variável")
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "WHILE":
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'while'")
            Parser.lex.selectNext()

            condition = Parser.parseBoolExpression()

            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após expressão no while")
            Parser.lex.selectNext()

            loop = Parser.parseStatement()

            resultado = While(None, [condition, loop])

        elif Parser.lex.next.kind == "IF":
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'if'")
            Parser.lex.selectNext()

            condition = Parser.parseBoolExpression()

            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após expressão no if")
            Parser.lex.selectNext()

            bloco1 = Parser.parseStatement()

            if Parser.lex.next.kind == "ELSE":
                Parser.lex.selectNext()
                bloco2 = Parser.parseStatement()
                resultado = If(None, [condition, bloco1, bloco2])
            else:
                resultado = If(None, [condition, bloco1])

        elif Parser.lex.next.kind == "END":
            Parser.lex.selectNext()
            resultado = NoOp(None, [])

        elif Parser.lex.next.kind == "OPEN_BRA":
            resultado = Parser.parseBlock()

        else:
            raise Exception("[Parser] Instrução inválida")

        return resultado
    
    def parseBlock():
        Parser.lex.selectNext()  # consome '{'
        filhos = []

        if Parser.lex.next.kind == "CLOSE_BRA":
            Parser.lex.selectNext()  # consome '}'
            return Block(None, filhos)  # bloco vazio

        # Caso contrário, processa normalmente
        while Parser.lex.next.kind != "CLOSE_BRA":
            filhos.append(Parser.parseStatement())

        Parser.lex.selectNext()  # consome '}'
        return Block(None, filhos)

            
    def parseBoolExpression():
        resultado = 0
        operacao = ''

        resultado = Parser.parseBoolTerm()

        while Parser.lex.next.kind == "OR":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseBoolTerm()])

        return resultado

    def parseBoolTerm():
        resultado = Parser.parseRefExpression()

        while Parser.lex.next.kind == "AND":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseRefExpression()])

        return resultado

    def parseRefExpression():
        resultado = 0
        operacao = ''

        resultado = Parser.parseExpression()

        while Parser.lex.next.kind == "GT" or Parser.lex.next.kind == "LT" or Parser.lex.next.kind == "EQ":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseExpression()])
        
        return resultado
    
    def parseExpression():
        resultado = 0
        operacao = ''

        resultado = Parser.parseTerm()

        while Parser.lex.next.kind == "PLUS" or Parser.lex.next.kind == "MINUS":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseTerm()])
        
        return resultado
    
    def parseTerm():
        resultado = 0
        operacao = ''

        resultado = Parser.parseFactor()

        while Parser.lex.next.kind == "MULTI" or Parser.lex.next.kind == "DIV":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseFactor()])
        
        return resultado

    def parseFactor():
        resultado = 0

        if Parser.lex.next.kind == "INT":
            resultado = IntVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "IDEN":
            resultado = Identifier(Parser.lex.next.value, [])
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "BOOL":
            resultado = BoolVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "STR":
            resultado = StringVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "PLUS":
            Parser.lex.selectNext()
            resultado = UnOp('+', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "MINUS":
            Parser.lex.selectNext()
            resultado = UnOp('-', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "NOT":
            Parser.lex.selectNext()
            resultado = UnOp('!', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "OPEN_PAR":
            Parser.lex.selectNext()
            resultado = Parser.parseBoolExpression()
            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("Parênteses não foram fechados!")
            else:
                Parser.lex.selectNext()

        elif Parser.lex.next.kind == "READ":
            Parser.lex.selectNext()  # consumiu READ

            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'read/readline'")
            Parser.lex.selectNext()  # consumiu '('

            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após 'read/readline('")
            Parser.lex.selectNext()  # consumiu ')'

            resultado = Read(None, [])

        else:
            raise Exception("[Parser] Símbolo Inválido!")

        return resultado
    
    def run(code):
        Parser.lex = Lexer(code)
        Parser.lex.selectNext()
        result = Parser.parseProgram()
        if Parser.lex.next.kind != "EOF":
            raise Exception("[Parser] Era esperado EOF, mas veio algo diferente!")  
        return result 
    
class SymbolTable:
    table = {}
    shift = 0

    @staticmethod
    def getter(key):
        try:
            return SymbolTable.table[key]
        except KeyError:
            raise Exception(f"[SymbolTable] Variável '{key}' não encontrada")
        
    @staticmethod
    def setter(key, variable):
        if key not in SymbolTable.table:
            raise Exception(f"[SymbolTable] Variável '{key}' não foi declarada previamente")
        var_existente = SymbolTable.table[key]

        if var_existente.type != variable.type:
            raise Exception(f"[SymbolTable] Tipos incompatíveis em atribuição: {var_existente.type} <- {variable.type}")
        SymbolTable.table[key].value = variable.value

    @staticmethod
    def create_variable(key, value, type):
        if key in SymbolTable.table:
            raise Exception(f"[SymbolTable] Variável '{key}' já declarada")
        
        SymbolTable.shift += 4
        shift = SymbolTable.shift

        valor = Variable(value, type, shift)
        SymbolTable.table[key] = valor
    
class Variable:
    def __init__(self, value, type, shift):
        self.value = value
        self.type = type
        self.shift = shift

class Node:

    id = 0

    def generate_id():
        Node.id += 1
        return Node.id
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.generate_id()

    def evaluate(self, st):
        pass

    def generate(self, st):
        pass

class IntVal(Node):
    def evaluate(self, st):
        return Variable(self.value, "number")
    
    def generate(self, st):
        Code.append(f'mov eax, {self.value}')
    
class BoolVal(Node):
    def evaluate(self, st):
         return Variable(self.value, "boolean")
    
class StringVal(Node):
    def evaluate(self, st):
         return Variable(self.value, "string")
    
class UnOp(Node):
    def evaluate(self, st):
        child = self.children[0].evaluate(st)
        if self.value == '+':
            if child.type != "number":
                raise Exception("[UnOp] '+' requer número")
            return Variable(+child.value, "number")
        elif self.value == '-':
            if child.type != "number":
                raise Exception("[UnOp] '-' requer número")
            return Variable(-child.value, "number")
        elif self.value == '!':
            if child.type != "boolean":
                raise Exception("[UnOp] '!' requer boolean")
            return Variable(not child.value, "boolean")
        
    def generate(self, st):
        self.children[0].generate(st)
        if self.value == '-':
            Code.append('neg eax')
        elif self.value == '!':
            Code.append('not eax')
    
class BinOp(Node):
    def evaluate(self, st):
        n1 = self.children[0].evaluate(st)
        n2 = self.children[1].evaluate(st)

        t1, t2 = n1.type, n2.type
        v1, v2 = n1.value, n2.value

        if self.value == '+':
            if t1 == t2 == "number":
                return Variable(v1 + v2, "number")
            if t1 == t2 == "string":
                return Variable(v1 + v2, "string")
            if t1 == "string" or t2 == "string":
                return Variable(ts_repr(v1) + ts_repr(v2), "string")
            raise Exception("[BinOp] Tipos inválidos para '+'")

        elif self.value in ('-', '*', '/'):
            if t1 == t2 == "number":
                if self.value == '-':
                    res = v1 - v2
                elif self.value == '*':
                    res = v1*v2
                else:
                    res = v1//v2
                return Variable(res, "number")
            else:
                raise Exception(f"[BinOp] Tipos inválidos para '{self.value}'")

        elif self.value in ('>', '<', '==='):
            if t1 == t2:
                if self.value == '>':
                    res = (v1 > v2)
                elif self.value == '<':
                    res = (v1 < v2)
                else:
                    res = (v1 == v2)
                return Variable(res, "boolean")
            else:
                raise Exception("[BinOp] Comparação entre tipos diferentes")

        elif self.value in ('&&', '||'):
            if t1 == t2 == "boolean":
                if self.value == '&&':
                    res = (v1 and v2)
                else:
                    res = (v1 or v2)
                return Variable(res, "boolean")
            else:
                raise Exception("[BinOp] Tipos inválidos para operador lógico")

        else:
            raise Exception(f"[BinOp] Operador '{self.value}' inválido")
        
    def generate(self, st):
        self.children[1].generate(st)
        Code.append('push eax')
        self.children[0].generate(st)
        Code.append('pop ecx')

        if self.value in ('+', '-', '*', '/', '&&', '||'):
            if self.value == '+':
                Code.append('add eax, ecx')
            elif self.value == '-':
                Code.append('sub eax, ecx')
            elif self.value == '*':
                Code.append('imul ecx')
            elif self.value == '/':
                Code.append('idiv ecx')
            elif self.value == '&&':
                Code.append('and eax, ecx')
            else:
                Code.append('or eax, ecx')
        else:
            Code.append('cmp eax, ecx') #compara eax e ecx. Se a subtracao dos dois for zero, eles sao iguais e um registrador de 1 bit(flag) eh setado para 1. Se for maior seta outra flag para 1 e assim por diante
            Code.append('mov ecx, 1')
            Code.append('mov eax, 0')
            if self.value == '===':
                Code.append('cmove eax, ecx') #copia ecx em eax se forem iguais
            elif self.value == '>':
                Code.append('cmovg eax, ecx') #copia ecx em eax se eax for maior
            else:
                Code.append('cmovl eax, ecx') #copia ecx em eax se eax for maior

class Identifier(Node):
    def evaluate(self, st):
        return st.getter(self.value)
    
    def generate(self, st):
        Code.append(f'mov eax, [ebp-{st.getter(self.value).shift}]')
    
class Print(Node):
    def evaluate(self, st):
        variable = self.children[0].evaluate(st)
        value = variable.value
        if variable.type == "boolean":
            print("true" if value else "false")
        else:
            print(value)
    
    def generate(self, st):
        self.children[0].generate(st)
        Code.append('push eax')
        Code.append('push format_out')
        Code.append('call printf')
        Code.append('add esp, 8')

class Assignment(Node):
    def evaluate(self, st):
        value_var = self.children[1].evaluate(st) #vai ser do tipo Variable
        st.setter(self.children[0].value, value_var) #setter recebe o valor com Variable ja

    def generate(self, st):
        self.children[1].generate(st)
        Code.append(f'mov [ebp-{st.getter(self.children[0].value).shift}], eax')

class VarDec(Node):
    # self.value, para esse no, eh o tipo da variavel
    def evaluate(self, st):
        if len(self.children) == 1:
            st.create_variable(self.children[0].value, None, self.value)
        else:
            valor_inicial = self.children[1].evaluate(st)
            if self.value != valor_inicial.type:
                raise Exception(f"[VarDec] Tipos incompatíveis na declaração: esperado {self.value}, obtido {valor_inicial.type}")
            st.create_variable(self.children[0].value, valor_inicial.value, self.value)

    def generate(self, st):
        Code.append('sub esp, 4')
        st.create_variable(self.children[0].value, None, self.value)
        if len(self.children) == 2:
            self.children[1].generate(st)
            Code.append(f'mov [ebp-{st.getter(self.children[0].value).shift}], eax')
    
            
class If(Node):
    def evaluate(self, st):
        cond = self.children[0].evaluate(st)
        if cond.type != "boolean":
            raise Exception("[If] Condição deve ser booleana")
        
        if len(self.children) == 3:  # tem else
            if cond.value:
                self.children[1].evaluate(st)
            else:
                self.children[2].evaluate(st)
        else:  # não tem else
            if cond.value:
                self.children[1].evaluate(st)
    
    def generate(self, st):
        Code.append(f'if_{self.id}:')
        self.children[0].generate(st)
        Code.append('cmp eax, 0')
        if len(self.children) == 3:
            Code.append(f'je else_{self.id}')
            self.children[1].generate(st)
            Code.append(f'jmp exit_{self.id}')
            Code.append(f'else_{self.id}:')
            self.children[2].generate(st)
            Code.append(f'exit_{self.id}:')
        else:
            Code.append(f'je exit_{self.id}')
            self.children[1].generate(st)
            Code.append(f'exit_{self.id}:')

class While(Node):
    def evaluate(self, st):
        cond = self.children[0].evaluate(st)
        if cond.type != "boolean":
            raise Exception("[While] Condição deve ser booleana")

        while cond.value:
            self.children[1].evaluate(st)
            cond = self.children[0].evaluate(st)

    def generate(self, st):
        Code.append(f'loop_{self.id}:')
        self.children[0].generate(st)
        Code.append('cmp eax, 0')
        Code.append(f'je exit_{self.id}')
        self.children[1].generate(st)
        Code.append(f'jmp loop_{self.id}')
        Code.append(f'exit_{self.id}:')

class Read(Node):
    def evaluate(self, st):
        return Variable(int(input()), "number")
    
    def generate(self, st):
        Code.append('push scan_int')
        Code.append('push format_in')
        Code.append('call scanf')
        Code.append('add esp 8')
        Code.append('mov eax, dword [scan_int]')
    
class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

    def generate(self, st):
        for child in self.children:
            child.generate(st)

class NoOp(Node):
    pass

class Code:

    instructions = []

    def append(code):
        Code.instructions.append(code)

    def dump(filename):
        header = """section .data
  format_out: db "%d", 10, 0 ; format do printf
  format_in: db "%d", 0 ; format do scanf
  scan_int: dd 0 ; 32-bits integer

section .text
  extern printf ; usar _printf para Windows
  extern scanf ; usar _scanf para Windows
  ; extern _ExitProcess@4 ; usar para Windows
  global _start ; início do programa

_start:
  push ebp ; guarda o EBP
  mov ebp, esp ; zera a pilha

"""

        footer = """
        
mov esp, ebp ; reestabelece a pilha
pop ebp

; chamada da interrupcao de saida (Linux)
mov eax, 1
xor ebx, ebx
int 0x80
"""
        with open(filename, 'w') as file:
            #Escrever o cabecalho: ate o inicio do codigo gerado
            file.write(header)

            #Escreve instrucoes armazenadas
            file.write("\n".join(Code.instructions))

            #Escreve as instrucoes finais: apos termino dos codigos gerados
            file.write(footer)

def main ():
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    
    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()
    
    code = Prepro.filter(code)
    resultado = Parser.run(code)
    st = SymbolTable()
    # resultado.evaluate(st)
    resultado.generate(st)
    Code.dump(f"{da_nome(filename)}.asm")
    # output_file = get_output_path(filename)
    # Code.dump(output_file)


if __name__ == "__main__":
    main()