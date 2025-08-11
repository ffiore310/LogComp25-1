import sys

def calculadora(expressao):

    print(f"A expressão recebida foi: {expressao}")
    lista = expressao.split()
    print(lista)

    operador = " "
    resultado = []
    argumento = 0
    index = 0

    for e in lista:
        if e == '+' or e == '-':
            print("Entrou no if +")
            operador = e
            print(operador)
        else:
            if index == 0:
                print("Entrou no if index")
                numero = int(e)
                argumento = numero
            else:
                if operador == '+':
                    numero = int(e)
                    operacao = argumento + numero
                    resultado.append(operacao)
                else:
                    numero = int(e)
                    operacao = argumento - numero
                    resultado.append(operacao)

        index += 1

    return resultado[0]


def main ():
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    argumento = sys.argv[1]
    resultado = calculadora(argumento)
    print(resultado)

if __name__ == "__main__":
    main()