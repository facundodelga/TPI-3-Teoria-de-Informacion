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

import struct
import Util
import ArbolHuffman
from ArbolHuffman import NodoHuffman

def comprimir(archivo,diccionario): 

        with open("archivoC.bin", "wb") as fc:
            # Cantidad de codigos que se almacenan en el diccionario
            cantCodigos = len(diccionario)
            fc.write(struct.pack('B',cantCodigos))

            for key,value in diccionario.items():
                
                # Caracter que representa el codigo en el archivo original
                caracter = struct.pack('c',key.encode("ascii"))
                fc.write(caracter)

                # Cantidad de bits que tiene la cadena del codigo
                cantbits = struct.pack('B',len(value))
                fc.write(cantbits)
                
                # Se guarda la cadena dinamicamente
                codigo = struct.pack('I',int(value,2))
                fc.write(codigo)

            with open(archivo, "rt") as arch:
                original = arch.read()
                
                # Se codifica el archivo original en los bits generados
                bits = ""
                for c in original:
                    bits += diccionario[c]

            # int(bits_comprimidos[i:i+8], 2) toma el segmento de 8 bits y 
            # lo convierte en un número entero interpretando los bits como una representación binaria. 
            # El segundo argumento 2 en int(..., 2) indica que estamos interpretando la cadena como binaria.
            
            # Se codifica el archivo original en los bits generados en bytes
            bytescomprimidos = bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8))

            fc.write(bytescomprimidos)

def descomprimir():
    diccionario = {}
    with open("archivoC.bin","rb") as file:
        n=1

# Comienzo del script
filename = "tp3_sample1.txt"

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
    ArbolHuffman.generar_codigos_huffman(arbolH, key, codigos)

print(codigos)

codConProb = {}

for key,value in codigos.items():
    codConProb[value] = probCaracteres[key]

print("Entropia de la fuente: " + str(Util.entropia(probCaracteres)))
print("Longitud media: " + str(Util.longitudMediaCodigo(codConProb)))

# longitudMediaCodigo(codigos)

comprimir(filename,codigos)








