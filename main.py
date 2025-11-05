import sys
from typing import List
import re
import os

def get_output_path(filename):
    asm_name = f"{da_nome(filename)}.asm"
    base_dir = "/tmp/compiler-testing-lib/compiler_testing_lib/languages/TypeScript/v3.0"
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
    ind = 0
    i = 0
    for c in filename:
        if c == ".":
            ind = i
        i+=1
    name = filename[0:ind]
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
        while self.position < len(self.source) and (self.source[self.position] == " " or self.source[self.position] == "\n" or self.source[self.position] == "\t" or self.source[self.position] == "\r"):
            self.position += 1
            
        if self.position >= len(self.source):
            self.next = Token("EOF", '')
            self.position += 1

        elif self.source[self.position] == ',':
            self.next = Token("COMMA", ',')
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

        elif self.source[self.position].isalpha() or self.source[self.position] == '_':
            id = ""
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                id += self.source[self.position]
                self.position += 1
            kw = ["log", "if", "while", "else", "readline", "true", "false", "let", "function", "return"]
            types = ["number", "string", "boolean", "void"]
            if id in kw:
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
                elif id == "function":
                    self.next = Token("FUNC", id)
                elif id == "return":
                    self.next = Token("RETURN", id)
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
            if Parser.lex.next.kind == "FUNC":
                filhos.append(Parser.parseFuncDeclaration())
            elif Parser.lex.next.kind == "VAR":
                filhos.append(Parser.parseStatement())
            elif Parser.lex.next.kind == "END":
                Parser.lex.selectNext()
            else:
                filhos.append(Parser.parseStatement())
        return Block(None, filhos)

    def parseFuncDeclaration():
        Parser.lex.selectNext()  # consume 'function'
        if Parser.lex.next.kind != "IDEN":
            raise Exception("[Parser] Era esperado o nome da função")
        func_name = Identifier(Parser.lex.next.value, [])
        Parser.lex.selectNext()
        if Parser.lex.next.kind != "OPEN_PAR":
            raise Exception("[Parser] Era esperado '(' após nome da função")
        Parser.lex.selectNext()

        params = []
        if Parser.lex.next.kind != "CLOSE_PAR":
            while True:
                if Parser.lex.next.kind != "IDEN":
                    raise Exception("[Parser] Era esperado identificador de parâmetro")
                p_name = Identifier(Parser.lex.next.value, [])
                Parser.lex.selectNext()
                if Parser.lex.next.kind != "SEMI":
                    raise Exception("[Parser] Era esperado ':' após nome do parâmetro")
                Parser.lex.selectNext()
                if Parser.lex.next.kind != "TYPE":
                    raise Exception("[Parser] Era esperado tipo do parâmetro")
                p_type = Parser.lex.next.value
                Parser.lex.selectNext()
                params.append(VarDec(p_type, [p_name]))
                if Parser.lex.next.kind == "COMMA":
                    Parser.lex.selectNext()
                    continue
                break
        if Parser.lex.next.kind != "CLOSE_PAR":
            raise Exception("[Parser] Era esperado ')' após parâmetros")
        Parser.lex.selectNext()
        if Parser.lex.next.kind != "SEMI":
            raise Exception("[Parser] Era esperado ':' antes do tipo de retorno")
        Parser.lex.selectNext()
        if Parser.lex.next.kind != "TYPE":
            raise Exception("[Parser] Era esperado tipo de retorno")
        ret_type = Parser.lex.next.value
        Parser.lex.selectNext()
        if Parser.lex.next.kind != "OPEN_BRA":
            raise Exception("[Parser] Era esperado '{' abrindo corpo da função")
        body = Parser.parseBlock()
        return FuncDec(ret_type, [func_name] + params + [body])

    def parseStatement():
        resultado = None

        if Parser.lex.next.kind == "IDEN":
            name = Parser.lex.next.value
            Parser.lex.selectNext()
            if Parser.lex.next.kind == "ASSIGN":
                Parser.lex.selectNext()
                expr_result = Parser.parseBoolExpression()
                resultado = Assignment(None, [Identifier(name, []), expr_result])
                if Parser.lex.next.kind != "END":
                    raise Exception("[Parser] Era esperado ';' ao final da atribuição")
                Parser.lex.selectNext()
            elif Parser.lex.next.kind == "OPEN_PAR":
                args = Parser.parseCallArgs()
                resultado = FuncCall(name, args)
                if Parser.lex.next.kind != "END":
                    raise Exception("[Parser] Era esperado ';' após chamada de função")
                Parser.lex.selectNext()
            else:
                raise Exception("[Parser] Após identificador, era esperado '=' ou '('")

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
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "VAR":
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "IDEN":
                raise Exception("[Parser] Era esperado um Identifier após let")
            iden = Identifier(Parser.lex.next.value, [])
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "SEMI":
                raise Exception("[Parser] Era esperado ':' na declaração de variável")
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "TYPE":
                raise Exception("[Parser] É necessário definir o tipo da variável")
            tipo = Parser.lex.next.value
            Parser.lex.selectNext()
            if Parser.lex.next.kind == "ASSIGN":
                Parser.lex.selectNext()
                expressao = Parser.parseBoolExpression()
                resultado = VarDec(tipo, [iden, expressao])
            else:
                resultado = VarDec(tipo, [iden])
            if Parser.lex.next.kind != "END":
                raise Exception("[Parser] Era esperado ';' ao final da declaração")
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

        elif Parser.lex.next.kind == "RETURN":
            Parser.lex.selectNext()
            expr = Parser.parseBoolExpression()
            resultado = Return(None, [expr])
            if Parser.lex.next.kind != "END":
                raise Exception("[Parser] Era esperado ';' após return")
            Parser.lex.selectNext()

        elif Parser.lex.next.kind == "END":
            Parser.lex.selectNext()
            resultado = NoOp(None, [])

        elif Parser.lex.next.kind == "OPEN_BRA":
            resultado = Parser.parseBlock()

        else:
            raise Exception("[Parser] Instrução inválida")

        return resultado

    def parseCallArgs():
        if Parser.lex.next.kind != "OPEN_PAR":
            raise Exception("[Parser] Era esperado '('")
        Parser.lex.selectNext()
        args = []
        if Parser.lex.next.kind != "CLOSE_PAR":
            while True:
                args.append(Parser.parseBoolExpression())
                if Parser.lex.next.kind == "COMMA":
                    Parser.lex.selectNext()
                    continue
                break
        if Parser.lex.next.kind != "CLOSE_PAR":
            raise Exception("[Parser] Era esperado ')' fechando chamada")
        Parser.lex.selectNext()
        return args
    
    def parseBlock():
        Parser.lex.selectNext()
        filhos = []
        if Parser.lex.next.kind == "CLOSE_BRA":
            Parser.lex.selectNext()
            return Block(None, filhos)
        while Parser.lex.next.kind != "CLOSE_BRA":
            filhos.append(Parser.parseStatement())
        Parser.lex.selectNext()
        return Block(None, filhos)

    def parseBoolExpression():
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
        resultado = Parser.parseExpression()
        while Parser.lex.next.kind in ("GT","LT","EQ"):
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseExpression()])
        return resultado
    
    def parseExpression():
        resultado = Parser.parseTerm()
        while Parser.lex.next.kind in ("PLUS","MINUS"):
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseTerm()])
        return resultado
    
    def parseTerm():
        resultado = Parser.parseFactor()
        while Parser.lex.next.kind in ("MULTI","DIV"):
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()
            resultado = BinOp(operacao, [resultado, Parser.parseFactor()])
        return resultado

    def parseFactor():
        if Parser.lex.next.kind == "INT":
            node = IntVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()
            return node

        elif Parser.lex.next.kind == "IDEN":
            name = Parser.lex.next.value
            Parser.lex.selectNext()
            if Parser.lex.next.kind == "OPEN_PAR":
                args = Parser.parseCallArgs()
                return FuncCall(name, args)
            return Identifier(name, [])

        elif Parser.lex.next.kind == "BOOL":
            node = BoolVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()
            return node

        elif Parser.lex.next.kind == "STR":
            node = StringVal(Parser.lex.next.value, [])
            Parser.lex.selectNext()
            return node

        elif Parser.lex.next.kind == "PLUS":
            Parser.lex.selectNext()
            return UnOp('+', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "MINUS":
            Parser.lex.selectNext()
            return UnOp('-', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "NOT":
            Parser.lex.selectNext()
            return UnOp('!', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "OPEN_PAR":
            Parser.lex.selectNext()
            node = Parser.parseBoolExpression()
            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("Parênteses não foram fechados!")
            Parser.lex.selectNext()
            return node

        elif Parser.lex.next.kind == "READ":
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'read/readline'")
            Parser.lex.selectNext()
            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após 'read/readline('")
            Parser.lex.selectNext()
            return Read(None, [])

        else:
            raise Exception("[Parser] Símbolo Inválido!")

    def run(code):
        Parser.lex = Lexer(code)
        Parser.lex.selectNext()
        result = Parser.parseProgram()
        if Parser.lex.next.kind != "EOF":
            raise Exception("[Parser] Era esperado EOF, mas veio algo diferente!")
        return result 

class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
        self.shift = 0

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        if self.parent is not None:
            return self.parent.getter(key)
        raise Exception(f"[SymbolTable] Variável '{key}' não encontrada")
        
    def setter(self, key, variable):
        if key in self.table:
            var_existente = self.table[key]
            if var_existente.is_function:
                raise Exception(f"[SymbolTable] '{key}' é uma função")
            if var_existente.type != variable.type:
                raise Exception(f"[SymbolTable] Tipos incompatíveis em atribuição: {var_existente.type} <- {variable.type}")
            self.table[key].value = variable.value
            return
        if self.parent is not None:
            self.parent.setter(key, variable)
            return
        raise Exception(f"[SymbolTable] Variável '{key}' não foi declarada previamente")

    def create_variable(self, key, value, type, is_function=False):
        if key in self.table:
            raise Exception(f"[SymbolTable] Variável '{key}' já declarada")
        self.shift += 4
        shift = self.shift
        self.table[key] = Variable(value, type, shift, is_function=is_function)

class Variable:
    def __init__(self, value, type, shift=None, is_function=False):
        self.value = value
        self.type = type
        self.shift = shift
        self.is_function = is_function

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
                    if v2 == 0:
                        raise Exception("[BinOp] Divisão por zero")
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
            Code.append('cmp eax, ecx')
            Code.append('mov ecx, 1')
            Code.append('mov eax, 0')
            if self.value == '===':
                Code.append('cmove eax, ecx')
            elif self.value == '>':
                Code.append('cmovg eax, ecx')
            else:
                Code.append('cmovl eax, ecx')

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
        value_var = self.children[1].evaluate(st)
        st.setter(self.children[0].value, value_var)
    def generate(self, st):
        self.children[1].generate(st)
        Code.append(f'mov [ebp-{st.getter(self.children[0].value).shift}], eax')

class VarDec(Node):
    def evaluate(self, st):
        if len(self.children) == 1:
            st.create_variable(self.children[0].value, None, self.value, is_function=False)
        else:
            valor_inicial = self.children[1].evaluate(st)
            if self.value != valor_inicial.type:
                raise Exception(f"[VarDec] Tipos incompatíveis na declaração: esperado {self.value}, obtido {valor_inicial.type}")
            st.create_variable(self.children[0].value, valor_inicial.value, self.value, is_function=False)
    def generate(self, st):
        Code.append('sub esp, 4')
        st.create_variable(self.children[0].value, None, self.value, is_function=False)
        if len(self.children) == 2:
            self.children[1].generate(st)
            Code.append(f'mov [ebp-{st.getter(self.children[0].value).shift}], eax')

class Return(Node):
    def evaluate(self, st):
        return self.children[0].evaluate(st)

class If(Node):
    def evaluate(self, st):
        cond = self.children[0].evaluate(st)
        if cond.type != "boolean":
            raise Exception("[If] Condição deve ser booleana")
        if len(self.children) == 3:
            if cond.value:
                ret = self.children[1].evaluate(st)
                if ret is not None:
                    return ret
            else:
                ret = self.children[2].evaluate(st)
                if ret is not None:
                    return ret
        else:
            if cond.value:
                ret = self.children[1].evaluate(st)
                if ret is not None:
                    return ret

class While(Node):
    def evaluate(self, st):
        cond = self.children[0].evaluate(st)
        if cond.type != "boolean":
            raise Exception("[While] Condição deve ser booleana")
        while cond.value:
            ret = self.children[1].evaluate(st)
            if ret is not None:
                return ret
            cond = self.children[0].evaluate(st)

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
            if isinstance(child, Block):
                ret = child.evaluate(SymbolTable(parent=st))
            else:
                ret = child.evaluate(st)
            if ret is not None:
                return ret

class FuncDec(Node):
    # value = return type; children = [Identifier, VarDec..., Block]
    def evaluate(self, st):
        name_node = self.children[0]
        ret_type = self.value
        st.create_variable(name_node.value, self, ret_type, is_function=True)

class FuncCall(Node):
    # value = function name; children = [expr...]
    def evaluate(self, st):
        var = st.getter(self.value)
        if not var.is_function:
            raise Exception(f"[FuncCall] '{self.value}' não é uma função")
        func_node = var.value
        decl_children = func_node.children
        func_name = decl_children[0].value
        params = [c for c in decl_children[1:-1] if isinstance(c, VarDec)]
        body = decl_children[-1]
        if len(params) != len(self.children):
            raise Exception(f"[FuncCall] Número de argumentos incorreto em '{func_name}'")
        call_st = SymbolTable(parent=st)
        for i in range(len(params)):
            p_decl = params[i]
            p_id = p_decl.children[0].value
            p_type = p_decl.value
            call_st.create_variable(p_id, None, p_type, is_function=False)
        for i in range(len(params)):
            p_decl = params[i]
            p_id = p_decl.children[0].value
            arg_val = self.children[i].evaluate(st)
            if arg_val.type != p_decl.value:
                raise Exception(f"[FuncCall] Tipo incompatível no argumento {i+1} de '{func_name}': {arg_val.type} != {p_decl.value}")
            call_st.setter(p_id, arg_val)
        ret = body.evaluate(call_st)
        if ret is None:
            if var.type == "void":
                return Variable(None, "void")
            raise Exception(f"[FuncCall] Função '{func_name}' sem return")
        if ret.type != var.type:
            raise Exception(f"[FuncCall] Tipo de retorno incompatível em '{func_name}': {ret.type} != {var.type}")
        return ret

class NoOp(Node):
    pass

class Code:
    instructions = []
    def append(code):
        Code.instructions.append(code)
    def dump(filename):
        header = """section .data
  format_out: db "%d", 10, 0
  format_in: db "%d", 0
  scan_int: dd 0

section .text
  extern printf
  extern scanf
  global _start

_start:
  push ebp
  mov ebp, esp

"""
        footer = """
mov esp, ebp
pop ebp
mov eax, 1
xor ebx, ebx
int 0x80
"""
        with open(filename, 'w') as file:
            file.write(header)
            file.write("\n".join(Code.instructions))
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
    resultado.evaluate(st)
    # Teste

if __name__ == "__main__":
    main()
