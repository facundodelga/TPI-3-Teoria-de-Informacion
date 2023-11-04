class NodoHuffman:
    def __init__(self, caracter = -1, frecuencia = -1):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

def construir_arbol_huffman(frecuencias):
    nodos = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    while len(nodos) > 1:
        nodos = sorted(nodos, key=lambda x: x.frecuencia)
        izquierda = nodos.pop(0)
        derecha = nodos.pop(0)
        nuevo_nodo = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nuevo_nodo.izquierda = izquierda
        nuevo_nodo.derecha = derecha
        nodos.append(nuevo_nodo)
    return nodos[0]

def generar_codigos_huffman(arbol, codigo_actual, codigos):
    if arbol.caracter:
        codigos[arbol.caracter] = codigo_actual.lstrip()
    if arbol.izquierda:
        generar_codigos_huffman(arbol.izquierda, codigo_actual + "0", codigos)
    if arbol.derecha:
        generar_codigos_huffman(arbol.derecha, codigo_actual + "1", codigos)

def mostrar_arbol_huffman(arbol, nivel=0, prefijo="R:"):
    if arbol.caracter:
        print("  " * nivel + f"{prefijo}{arbol.caracter} ({arbol.frecuencia})")
    if arbol.izquierda:
        mostrar_arbol_huffman(arbol.izquierda, nivel + 1, "I:")
    if arbol.derecha:
        mostrar_arbol_huffman(arbol.derecha, nivel + 1, "D:")