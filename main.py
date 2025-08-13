import sys

def limpa(expressao):
    for i in range(len(expressao) - 2):
        if expressao[i].isdigit() and expressao[i+1] == ' ' and expressao[i+2].isdigit():
            raise Exception("Espaço inválido dentro de número")
    return expressao.replace(" ", "")

def verifica(expressao):
    if not expressao:
        raise Exception("Expressão vazia")

    lista = []
    i = 0
    n = len(expressao)
    esperando_numero = True

    while i < n:
        if esperando_numero:
            if not expressao[i].isdigit():
                raise Exception("Esperado número")
            start = i
            while i < n and expressao[i].isdigit():
                i += 1
            lista.append(expressao[start:i])
            esperando_numero = False 
        else:
            if expressao[i] not in ['+', '-']:
                raise Exception("Esperado operador")
            lista.append(expressao[i])
            i += 1
            esperando_numero = True 

    if esperando_numero:
        raise Exception("Expressão termina com operador")

    return lista

def calculadora(expressao):

    # print(f"A expressão recebida foi: {expressao}")
    
    expressao_limpa = limpa(expressao)
    # print(expressao_limpa)

    lista = verifica(expressao_limpa)
    # print(lista)

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
    if len(sys.argv) < 2:
        print("Nenhuma expressão foi passada.")
        return
    argumento = sys.argv[1]
    resultado = calculadora(argumento)
    print(resultado)

if __name__ == "__main__":
    main()