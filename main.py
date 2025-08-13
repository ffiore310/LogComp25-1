import sys

def limpa(expressao):
    expressao_limpa = expressao.replace(" ","")
    return expressao_limpa

def verifica(expressao):

    operador = False
    valor = ""
    lista = []

    for i, c in enumerate(expressao):
        print(c)
        if i == 0:
            if c == '+' or c == '-':
                raise ValueError("Expressao comeca com um operador!")
            else:
                valor += c
        else:
            if operador:
                if c == '+' or c == '-':
                    raise ValueError("Expressao invalida: um operador seguido do outro!")
                else:
                    if i == len(expressao)-1:
                        valor+=c
                        lista.append(valor)
                    else:
                        valor += c
                        operador = False
            elif c == '+' or c == '-':
                lista.append(valor)
                lista.append(c)
                operador = True
                valor = ""
            else:
                if i == len(expressao)-1:
                        valor+=c
                        lista.append(valor)
                else:
                    valor += c

    return lista

def calculadora(expressao):

    print(f"A expressão recebida foi: {expressao}")
    
    expressao_limpa = limpa(expressao)
    print(expressao_limpa)

    lista = verifica(expressao_limpa)
    print(lista)

    operador = ""
    resultado = 0
    index = 0

    for e in lista:
        if e == '+' or e == '-':
            operador = e
        elif e == ' ':
            pass
        else:
            if index == 0:
                numero = int(e)
                resultado = numero
            else:
                if operador == '+':
                    numero = int(e)
                    resultado = resultado + numero
                else:
                    numero = int(e)
                    resultado = resultado - numero

        index += 1

    return resultado


def main ():
    # string = "  Olá Mundo!  "
    # print(string.replace(" ",""))
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    argumento = sys.argv[1]
    resultado = calculadora(argumento)
    print(resultado)

if __name__ == "__main__":
    main()