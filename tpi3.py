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

import sys
import Util
import ArbolHuffman
from ArbolHuffman import NodoHuffman
import pickle
import copy
import os

def persistencia(arbol, datos_comprimidos, filename):
    data = {
        "Arbol Huffman" : arbol,
        "TextoC" : datos_comprimidos
    }
    
    with open(filename, "wb") as file:
        pickle.dump(data, file)

def obtenerEstructurasC(archivo):
    caracteres = {}
    # Abrir archivo y leer caracter por caracter
    with open(filename, 'rt') as file:
        texto = file.read()
    
    for caracter in texto:
        if(caracter in caracteres):
            caracteres[caracter] += 1
        else:
            caracteres[caracter] = 1
        
    # Se obtiene el total de caracteres que se leyeron del archivo contando los espacios
    totalCaracteres = Util.suma_dicc(caracteres)

    probCaracteres = {}

    # Se calcula la probabilidad de cada caracter
    for key in caracteres.keys():
        probCaracteres[key] = caracteres[key] / totalCaracteres # Para sacar la probilidad no redondeamos para que la probabilidad sume 1

    # Se ordena el diccionario de menor a mayor en probabilidad de cada caracter
    probCaracteres = Util.ordenaDiccionario(probCaracteres)

        # Aplicacion de Huffman
    arbolH = NodoHuffman()

    # Cargo el arbol binario para luego obtener los codigos de cada caracter
    arbolH = ArbolHuffman.construir_arbol_huffman(probCaracteres) 

    # ArbolHuffman.mostrar_arbol_huffman(arbolH)
    codigos = {}
    for key in probCaracteres.keys(): 
        ArbolHuffman.generar_codigos_huffman(arbolH, key, "",codigos)
    # print(codigos)

    codConProb = {}

    for key,value in codigos.items():
        codConProb[value] = probCaracteres[key]

    return texto, codigos, codConProb, arbolH, probCaracteres


def obtenerEstructurasD(arbolHuffman, texto):
    caracteres = {}
    
    for caracter in texto:
        if(caracter in caracteres):
            caracteres[caracter] += 1
        else:
            caracteres[caracter] = 1
            
    totalCaracteres = Util.suma_dicc(caracteres)

    probCaracteres = {}

    # Se calcula la probabilidad de cada caracter
    for key in caracteres.keys():
        probCaracteres[key] = caracteres[key] / totalCaracteres # Para sacar la probilidad no redondeamos para que la probabilidad sume 1

    # Se ordena el diccionario de menor a mayor en probabilidad de cada caracter
    probCaracteres = Util.ordenaDiccionario(probCaracteres)

    codigos = {}
    for key in probCaracteres.keys(): 
        ArbolHuffman.generar_codigos_huffman(arbolHuffman, key, "",codigos)

    codConProb = {}

    for key,value in codigos.items():
        codConProb[value] = probCaracteres[key]
    
    return codConProb, probCaracteres

def comprimir(archivo): 

    texto, codigos, codConProb, arbolH, probCaracteres = obtenerEstructurasC(archivo)
    
    # Se codifica el archivo original en los bits generados
    bits = "1"
    for c in texto:
        bits += codigos[c]
    
    while(len(bits) % 8 != 0):
        bits += codigos[' ']
    
    # int(bits_comprimidos[i:i+8], 2) toma el segmento de 8 bits y 
    # lo convierte en un número entero interpretando los bits como una representación binaria. 
    # El segundo argumento 2 en int(..., 2) indica que estamos interpretando la cadena como binaria.
    
    # Se codifica el archivo original en los bits generados en bytes
    bytescomprimidos = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    # print(bin(int.from_bytes(bytescomprimidos[:100],byteorder="big")))
    
    return bytescomprimidos, codigos, codConProb, arbolH, probCaracteres

def descomprimir(texto, arbol, filename):
    
    textoComprimido = bin(int.from_bytes(texto, byteorder="big"))[2:]
    cadenaBinaria = ""
    textoDescomprimido = ""
    textoComprimido = textoComprimido[1:]
    for bit in textoComprimido:
        cadenaBinaria += bit
        
        caracter = buscaCaracter(arbol, cadenaBinaria)
        
        if(caracter):
            textoDescomprimido += caracter
            cadenaBinaria = ""
        
    with open(filename, "wt") as f:
        f.write(textoDescomprimido)
    
    return textoDescomprimido

def buscaCaracter(arbol, binario):
    nodo = copy.copy(arbol)
    i = 0
    while(nodo.caracter is None and i < len(binario)):
        if('0' == binario[i]):
            nodo = nodo.izquierda
        else:
            nodo = nodo.derecha
        
        i += 1
    
    return nodo.caracter

def cargarDatos(filename):
    with open(filename,"rb") as file:
        data = pickle.load(file)
        arbol = data["Arbol Huffman"]
        texto = data["TextoC"]
    
    return arbol,texto




# # Comienzo del script


# Esto define la cantidad de caracteres que se pueden usar para una interpretacion de un int 
#(Establece la limitación de la longitud de conversión de cadenas enteras utilizada por este intérprete)
sys.set_int_max_str_digits(0)
vectorDeParametros = list(sys.argv)
# print(vectorDeParametros)
if(len(vectorDeParametros) > 2):
    # filename = "tp3_sampleA.txt" 
    filename = vectorDeParametros[1]
    compressed = vectorDeParametros[2]
    
    if(vectorDeParametros[3] == "-c"):

        compresion, codigos, codigosConProb, arbol, probCaracteres = comprimir(filename)
        persistencia(arbol,compresion,compressed)

    elif(vectorDeParametros[3] == "-d"):
        arbolH = NodoHuffman()

        arbolH, texto = cargarDatos(compressed)

        textoOriginal = descomprimir(texto,arbolH,filename)
        
        codigosConProb, probCaracteres = obtenerEstructurasD(arbolH, textoOriginal)
        
    entropia = Util.entropia(probCaracteres)
    longitud = Util.longitudMediaCodigo(codigosConProb)
        
    rendimiento = Util.rendimiento(entropia,longitud)
    redundancia = Util.redundancia(entropia,longitud)
    
    
    print("Rendimiento: " + str(rendimiento))
    print("Redundancia: " + str(redundancia))
    
    print("Tasa de compresion: " + str(Util.tasaDeCompresion(filename, compressed)) + "%")












