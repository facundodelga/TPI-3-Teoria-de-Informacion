import math

def longitudMediaCodigo(diccionario):
        #Se calcula la longitud media del codigo del archivo
        longitudMedia=sum(probabilidad*len(key) for key,probabilidad in diccionario.items())
        return longitudMedia

def entropia(diccionario):
    entropia = 0
    for key in diccionario.keys():
        entropia += diccionario[key] * math.log2(diccionario[key] ** -1)
    return entropia

def ordenaDiccionario(diccionario):
    return dict(sorted(diccionario.items(), key=lambda item: item[1]))

def suma_dicc(diccionario):
    totalCaracteres = 0

    for valor in diccionario.values():
        totalCaracteres += valor

    return totalCaracteres