import sys
from typing import List
import re

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
        elif self.source[self.position] == '(':
            self.next = Token("OPEN_PAR", '(')
            self.position += 1
        elif self.source[self.position] == ')':
            self.next = Token("CLOSE_PAR", ')')
            self.position += 1
        elif self.source[self.position] == '=':
            self.next = Token("ASSIGN", '=')
            self.position += 1
        elif self.source[self.position] == ';':
            self.next = Token("END", ';')
            self.position += 1
        elif self.source[self.position].isalpha():
            id = ""
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                id += self.source[self.position]
                self.position += 1
            list = ["log"]
            if id in list:
                self.next = Token("PRINT", id)    
            else:
                self.next = Token("IDEN", id)
        else:
            numero = ""
            while self.position < len(self.source) and self.source[self.position].isdigit(): #aqui eu deveria tratar o caso de uma palavra começar com caracteres especiais: raise error
                numero += self.source[self.position]
                self.position += 1
            inteiro = int(numero)
            self.next = Token("INT", inteiro)

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

class Parser:
    lex = None

    def parseProgram():
        filhos = []

        while Parser.lex.next.kind != "EOF":
            stmt = Parser.parseStatement()
            filhos.append(stmt)

            if Parser.lex.next.kind == "END":
                Parser.lex.selectNext()
            elif Parser.lex.next.kind != "EOF":
                raise Exception("[Parser] Era esperado ';' ao final da instrução")

        return Block(None, filhos)

    def parseStatement():
        resultado = None

        if Parser.lex.next.kind == "IDEN":
            id_node = Identifier(Parser.lex.next.value, [])
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "ASSIGN":
                raise Exception("[Parser] Era esperado '=' após identificador")
            Parser.lex.selectNext()

            expr = Parser.parseExpression()
            resultado = Assignment(None, [id_node, expr])

        elif Parser.lex.next.kind == "PRINT":
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "OPEN_PAR":
                raise Exception("[Parser] Era esperado '(' após 'print'")
            Parser.lex.selectNext()

            expr = Parser.parseExpression()

            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("[Parser] Era esperado ')' após expressão no print")
            Parser.lex.selectNext()

            resultado = Print(None, [expr])

        elif Parser.lex.next.kind == "END":
            resultado = NoOp(None, [])

        else:
            raise Exception("[Parser] Instrução inválida")

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
        
        elif Parser.lex.next.kind == "OPEN_PAR":
            Parser.lex.selectNext()
            resultado = Parser.parseExpression()
            if Parser.lex.next.kind != "CLOSE_PAR":
                raise Exception("Parênteses não foram fechados!")
            else:
                Parser.lex.selectNext()

        elif Parser.lex.next.kind == "PLUS":
            Parser.lex.selectNext()
            resultado = UnOp('+', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "MINUS":
            Parser.lex.selectNext()
            resultado = UnOp('-', [Parser.parseFactor()])

        elif Parser.lex.next.kind == "IDEN":
            resultado = Identifier(Parser.lex.next.value, [])
            Parser.lex.selectNext()

        else:
            raise Exception("Símbolo Inválido!")
        
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

    @staticmethod
    def getter(key):
        try:
            return SymbolTable.table[key]
        except KeyError:
            raise Exception(f"[SymbolTable] Variável '{key}' não encontrada")

    @staticmethod
    def setter(key, value):
        SymbolTable.table[key] = value
    
class Variable:
    def __init__(self, value):
        self.value = value

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass

class IntVal(Node):
    def evaluate(self, st):
        return self.value
    
class UnOp(Node):
    def evaluate(self, st):
        if self.value == '+':
            return self.children[0].evaluate(st)
        else:
            return -self.children[0].evaluate(st)
    
class BinOp(Node):
    def evaluate(self, st):
        n1 = self.children[0].evaluate(st)
        n2 = self.children[1].evaluate(st)
        if self.value == '+':
            return n1 + n2
        elif self.value == '*':
            return n1 * n2
        elif self.value == '/':
            return n1 // n2
        else:
            return n1 - n2

class Identifier(Node):
    def evaluate(self, st):
        return st.getter(self.value).value
    
class Print(Node):
    def evaluate(self, st):
        expr = self.children[0].evaluate(st) #mesma coisa que acontece no evaluate de Assingment
        print(expr)

class Assignment(Node):
    def evaluate(self, st):
        st.setter(self.children[0].value, Variable(self.children[1].evaluate(st)))

class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class NoOp(Node):
    pass

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

if __name__ == "__main__":
    main()