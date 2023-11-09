import heapq
class NodoHuffman:
    def __init__(self, caracter = -1, frecuencia = -1):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(frecuencias):
    cola_prioridad = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(cola_prioridad)

    while len(cola_prioridad) > 1:
        nodo_izq = heapq.heappop(cola_prioridad)
        nodo_der = heapq.heappop(cola_prioridad)
        nuevo_nodo = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nuevo_nodo.izquierda = nodo_izq
        nuevo_nodo.derecha = nodo_der
        heapq.heappush(cola_prioridad, nuevo_nodo)

    return cola_prioridad[0]

def generar_codigos_huffman(arbol, caracter, codigo_actual, codigos):
    if arbol.caracter and arbol.caracter == caracter:
        codigos[arbol.caracter] = codigo_actual.lstrip()
    if arbol.izquierda:
        generar_codigos_huffman(arbol.izquierda, caracter,codigo_actual + "0", codigos)
    if arbol.derecha:
        generar_codigos_huffman(arbol.derecha, caracter,codigo_actual + "1", codigos)

def mostrar_arbol_huffman(arbol, nivel=0, prefijo="R:"):
    if arbol.caracter:
        print("  " * nivel + f"{prefijo}{arbol.caracter} ({arbol.frecuencia})")
    if arbol.izquierda:
        mostrar_arbol_huffman(arbol.izquierda, nivel + 1, "I:")
    if arbol.derecha:
        mostrar_arbol_huffman(arbol.derecha, nivel + 1, "D:")


