import sys

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

        if Parser.lex.next.kind != "INT":
            raise Exception("[Parser] Primeiro caracter não é um número!")

        resultado = Parser.lex.next.value

        Parser.lex.selectNext()

        while Parser.lex.next.kind == "PLUS" or Parser.lex.next.kind == "MINUS":
            operacao = Parser.lex.next.value
            Parser.lex.selectNext()

            if Parser.lex.next.kind != "INT":
                raise Exception("[Parser] Era esperado um número, mas veio algo diferente!")

            if operacao == '+':
                resultado+=Parser.lex.next.value
            else:
                resultado-=Parser.lex.next.value

            Parser.lex.selectNext()
        
        return resultado

    def run(code):
        Parser.lex = Lexer(code)
        Parser.lex.selectNext()
        result = Parser.parseExpression()
        if Parser.lex.next.kind != "EOF":
            raise Exception("[Parser] Era esperado EOF, mas veio algo diferente!")  
        return result 

def main ():
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    
    resultado = Parser.run(sys.argv[1])
    # resultado = Parser.run("1 + 2- 33")
    print(resultado)

if __name__ == "__main__":
    main()