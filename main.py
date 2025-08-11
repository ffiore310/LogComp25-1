import sys

def calculadora(expressao):

    print(f"A expressão recebida foi: {expressao}")
    lista = expressao.split()
    print(lista)

    operador = " "
    resultado = 0
    index = 0

    for e in lista:
        if e == '+' or e == '-':
            operador = e
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
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    argumento = sys.argv[1]
    resultado = calculadora(argumento)
    print(resultado)

if __name__ == "__main__":
    main()