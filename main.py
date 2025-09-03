import sys
from typing import List

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == " ":
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
        else:
            numero = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
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
            resultado = BinOp(operacao, [resultado, Parser.parseTerm()])
        
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

        else:
            raise Exception("Símbolo Inválido!")
        
        return resultado

    def run(code):
        Parser.lex = Lexer(code)
        Parser.lex.selectNext()
        result = Parser.parseExpression()
        if Parser.lex.next.kind != "EOF":
            raise Exception("[Parser] Era esperado EOF, mas veio algo diferente!")  
        return result 
    
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class IntVal(Node):
    def evaluate(self):
        return self.value
    
class UnOp(Node):
    def evaluate(self):
        if self.value == '+':
            return self.children[0].evaluate()
        else:
            return -self.children[0].evaluate()
    
class BinOp(Node):
    def evaluate(self):
        n1 = self.children[0].evaluate()
        n2 = self.children[1].evaluate()
        if self.value == '+':
            return n1 + n2
        else:
            return n1 - n2

def main ():
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    
    resultado = Parser.run(sys.argv[1])
    result = resultado.evaluate()
    # resultado = Parser.run("1+2*3")
    print(result)

if __name__ == "__main__":
    main()