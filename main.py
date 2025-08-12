import sys

def verifica(expressao: str):
    if not expressao:
        raise ValueError("Expressão vazia.")
    
    print(expressao.strip())
    
    if expressao.strip() != expressao:
        raise ValueError("Use exatamente um espaço entre lista (sem espaços no início/fim).")
    if "\t" in expressao or "\n" in expressao:
        raise ValueError("Use apenas espaço simples como separador (sem TAB/linhas).")

    lista = expressao.split(" ") 
    if "" in lista:
        raise ValueError("Use exatamente um espaço entre cada número e operador (nada de dois espaços).")
    if len(lista) % 2 == 0:
        raise ValueError("A expressão deve terminar em número (padrão: número op número op número ...).")

    for i, tok in enumerate(lista):
        if i % 2 == 0: 
            if not tok.isdigit():
                raise ValueError(f"Esperado número inteiro na posição {i+1}, obtido '{tok}'.")
        else:           
            if tok not in {"+", "-"}:
                raise ValueError(f"Esperado operador '+' ou '-' na posição {i+1}, obtido '{tok}'.")

    print("Expressão está na formatação correta")
    return lista


def calculadora(expressao):

    print(f"A expressão recebida foi: {expressao}")
    
    lista = verifica(expressao)
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