# Desarrollar un programa que pueda ser ejecutado por consola del siguiente modo:

# tpi3 original.txt compressed.bin {-c|-d}

# Donde:

# tpi3 es el programa ejecutable
# original.txt es un archivo de texto ASCII
# compressed.bin es un archivo binario
# -c y -d son flags que indican la acción a realizar
# El programa debe realizar las siguientes acciones:

# Si se incluye el flag -c, realizar una compresión sin pérdidas del archivo original.txt y almacenarla en el archivo compressed.bin.
# Si se incluye el flag -d, descomprimir el archivo compressed.bin obtenido en el inciso anterior y recuperar el archivo original.txt.
# Calcular la tasa de compresión, el rendimiento y la redundancia.

import math

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

def ordenaDiccionario(diccionario):
    return dict(sorted(diccionario.items(), key=lambda item: item[1]))

def suma_dicc(diccionario):
    totalCaracteres = 0

    for valor in diccionario.values():
        totalCaracteres += valor

    return totalCaracteres

def huffman(diccionario):
    dicc_aux = dict(diccionario)
    while(len(dicc_aux.keys()) != 1):
        primeros2 = list(dicc_aux)[:2]
        
        valor1 = dicc_aux[primeros2[0]]
        valor = dicc_aux[primeros2[1]] + valor1
        
        union = str(primeros2[0]) + str(primeros2[1])

        dicc_aux[union] = valor
        
        dicc_aux.pop(primeros2[0])
        dicc_aux.pop(primeros2[1])
        
        dicc_aux = ordenaDiccionario(dicc_aux)
    
    return dicc_aux

def entropia(diccionario):
    entropia = 0
    for key in diccionario.keys():
        entropia += diccionario[key] * math.log2(diccionario[key] ** -1)
    return entropia

# Comienzo del script
filename = "tp3_sample0.txt"

caracteres = {}

# Abrir archivo y leer caracter por caracter
with open(filename, 'rt') as file:
    for line in file:
        for caracter in line:
            if(caracter in caracteres):
                caracteres[caracter] += 1
            else:
                caracteres[caracter] = 1

# print(caracteres)

# Se obtiene el total de caracteres que se leyeron del archivo contando los espacios
totalCaracteres = suma_dicc(caracteres)

probCaracteres = {}

# Se calcula la probabilidad de cada caracter
for key in caracteres.keys():
    probCaracteres[key] = caracteres[key] / totalCaracteres # Para sacar la probilidad no redondeamos para que la probabilidad sume 1

# Se ordena el diccionario de menor a mayor en probabilidad de cada caracter
probCaracteres = ordenaDiccionario(probCaracteres)

# Aplicacion de Huffman
arbolH = NodoHuffman()

# Cargo el arbol binario para luego obtener los codigos de cada caracter
arbolH = construir_arbol_huffman(probCaracteres) 

# mostrar_arbol_huffman(arbolH)
codigos = {}
for key in probCaracteres.keys(): 
    generar_codigos_huffman(arbolH, key, codigos)

print(codigos)

print("Entropia de la fuente: " + str(entropia(probCaracteres)))











