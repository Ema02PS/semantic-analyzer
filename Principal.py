from HashTable import HashTable

# Proyecto II - Marck Rojas Delgado & Emmanuel Pérez Sánchez. Grupo 4

# FIXME: Toda llave que se abra debe cerrarse. Aplica para: if, while y funciones.

stringsplit4 = ""
tokens = [' ']
ids = []
igual = "="
datatype = ['int', 'string', 'char', 'float', 'double']
operators = ['+', '-', '*', '/', '=', '<']
punct = ['(', ')', '{', '}', '[', ']', ',']
key_words = ['class', 'exec', 'assert', 'lambda', 'def',
             'except', 'global', 'import', 'return', 'print',
             'yield', 'for', 'elif', 'else', 'continue', 'if', 'not',
             'break', 'from', 'or', 'true', 'and', 'false', 'while']

# Ayuda a localizar
contadorFunciones = -1
# Cuenta el número de veces que sale '{'
contadorAbro = 0
# Cuenta el número de veces que sale '}'
contadorCierro = 0
# Lleva un conteo por la línea actual
contadorLinea = 0
tablahashglobales = HashTable()
listatablashashlocales = []
# Modo local / Modo global
modo = 0
relleno = ""
tablahashlocales = None

# Definición de los metodos

def DescartarGlobal(string):
    """El metodo DescartaGlobal es utilizado para analizar si una variable global es apta
    para guardarla en la tabla de variables globales. Si es el caso, la guarda en esta"""
    string = string.split()
    if not (string[0] in datatype) or (string[0] in key_words) or not (string[2] in igual):
        return True  # Si retorna True es que la descarta
    else:
        tipoglobal = string[0]
        simbologlobal = string[1]
        valorglobal = string[3]
        tablahashglobales.__setitem__(simbologlobal, tipoglobal, "var", valorglobal)
        return False


def vacio(string):
    """El metodo vacío se utiliza para controlar errores si la linea que esta leyendo es vacia"""
    if string == '':
        return True
    else:
        return False


def MasDeunCaracter(string):  # Esta funcion lo que hace es verificarme si la linea
    """El método MasDeunCaracter sirve para aseguararse de que el programa
    no intente analizar una linea que solamente tiene un caracter"""
    if len(string) > 1:  # que esta leyendo tiene mas de un caraceter o no
        return True
    else:
        return False


def ContadoresDeLlaves(string):
    """El metodo ContadorLLaves sirve para que el programa este conciente
    de cuando se abren y se cierran las llaves en un if, while o una funcion"""
    global contadorAbro
    global contadorCierro
    # Necesito este if del contador para que mi programa sepa cuando pasar a modo global
    if string.find('{') != -1:
        contadorAbro = contadorAbro + 1
        # Necesito este if del contador para que mi programa sepa cuando pasar a modo global
    if string.find('}') != -1:
        contadorCierro = contadorCierro + 1


def DevuelveTipo(string, contador):
    """El método DevuelveTipo se utiliza cuando el programa encontró una instrucción return.
    Sirve para conocer el tipo de dato de lo que esta intentando retornar"""
    tablahashlocalesdt = listatablashashlocales[contador]
    if tablahashlocalesdt.buscar(string):
        return tablahashlocalesdt.__getitem__(string)[1]
    else:
        return tablahashglobales.__getitem__(string)[1]


def BuscaGlobal(string):
    """El método BuscaGlobal se utiliza en la segunda lectura. Sirve para conocer si una variable
    global esta declarada o no. Para darse cuenta de esto, busca la variable en la tabla de globales"""
    if tablahashglobales.buscar(string):
        return True
    else:
        return False


def BuscaLocal(string, contador):
    """El método BuscaLocal se utiliza en la segunda lectura. Sirve para conocer si una variable local esta declarada.
    Para esto primero busca la variable en la tabla de variables locales de la funcion que le corresponde y si no la
    encuentra ahí, procede a buscarla en tabla de globales"""
    tablahashFuncion = listatablashashlocales[contador]
    if tablahashFuncion.buscar(string):
        return True
    else:
        if tablahashglobales.buscar(string):
            return True
        else:
            return False


def BuscaenReturn(string, contador):
    """El metodo BuscaenReturn se utiliza en la segunda lectura. Sirve para conocer si las variables que esta intentando
    retornar una función estan declaradas o no. Para esto se apoya en la lógica del método BuscaLocal"""
    for r in range(0, len(string)):  # Revisando la linea del return
        if not BuscaLocal(string[r], contador):
            return False
    return True


# Caracteres que en la segunda
# lectura van a ser ignorados
mapeo = {
    ord('='): ' ',
    ord('('): ' ',
    ord(' '): ' ',
    ord('+'): ' ',
    ord('-'): ' ',
    ord('*'): ' ',
    ord('/'): ' ',
    ord('>'): ' ',
    ord('<'): ' ',
    ord(')'): ' ',
    ord('{'): ' ',
    ord('}'): ' ',
    ord('['): None,
    ord(']'): None,
    ord(','): ' ',
    ord(':'): None,
    ord(';'): None,
    ord('.'): None
}


def Variables(string):
    """"El método Variables se utiliza en la segunda lectura. La funcion del
    método es extraer las variables de cualquier linea que esté analizando"""

    # Este primer if sirve para tratar casos en
    # los que se haga un igualacion de un string"
    verificar = string
    if verificar.find('=') != -1 and verificar.find('"') != -1:
        verificar = verificar.split()
        unicavariable = [verificar[0]]
        return unicavariable
    else:
        string = string.translate(mapeo)
        string = string.split()
        variableslinea = []
        for j in range(0, len(string)):
            if not string[j].isnumeric() and string[j] not in key_words and not string[j] in datatype:
                variableslinea.append(string[j])
        variableslinea = list(set(variableslinea))
        return variableslinea


# Resumen del funcionamiento
"""El programa funciona mediante una primera lectura del archivo .txt, donde cada linea del código contenido en 
el documento es almacenada en una cadena de caracteres, la cual se procederá a diseccionar, evaluar, y clasificar 
mediante multitud de recorridos y verificaciones para determinar si los elementos que la componen como variables 
y funciones pueden ser almacenadas en una tabla de símbolos, implementada a través de una estructura de tabla hash.
Una segunda lectura es llevada a cabo una vez que las tablas guardaron las variables y funciones aptas, en esta ocasión
se podrán realizar búsquedas especialmente, para corroborar que la contextualización del código sea correcta, mostrando
mediante la consola el número de línea donde el código analizado tuvo algún error de tipo semántico."""

# ................................................PRIMERA LECTURA......................................................
with open("codigo.txt") as f_obj:
    lines = f_obj.readlines()
for line in lines:
    linea = line.rstrip()
    linea_aux = line.split()
    ContadoresDeLlaves(linea)
    # Iguala una linea vacia a un valor que los metodos pueden descartar
    if vacio(linea):
        linea = "descarte esto"
    else:
        # Si hay menos de un caracter en una linea, evita que pase al if siguiente
        if MasDeunCaracter(linea_aux):
            if (linea_aux[0] in datatype or not linea_aux[0] in key_words) and linea_aux[1].find('(') != -1:
                # Pasando a a modo local (1)
                modo = 1

                # Esta es la tabla hash para ingresar variables y funciones
                tablahashlocales = HashTable()

        # Esta es la verificación para pasar a modo global
        # Si el contador de llaves que abren es igual
        # al contador de llaves que cierran
        # ............................................MODO GLOBAL.......................................................
        if contadorAbro == contadorCierro:
            modo = 0
            if tablahashlocales is not None:
                listatablashashlocales.append(tablahashlocales)
                tablahashlocales = None

        if modo == 0:
            DescartarGlobal(linea)

# ....................................................MODO LOCAL........................................................

        elif modo == 1:

            stringsplit1 = linea.split()
            # Aqui estoy validando si lo que estoy leyendo es o no una funcion
            if MasDeunCaracter(linea_aux):
                if (stringsplit1[0] in datatype or not stringsplit1[0] in key_words) and stringsplit1[1].find(
                        '(') != -1:
                    stringsplit2 = linea.split("(")[1]
                    # Guarda el contenido de los parámetros
                    stringsplit3 = stringsplit2.split(")")[0]

                    # Guarda el tipo de dato de la función
                    stringsplit4 = linea.split()[0]

                    # Guarda el nombre de la función
                    stringsplit5 = linea.split()[1]
                    stringsplit6 = stringsplit5.split('(')[0]

                    # Guarda las variables de los parámetros
                    stringsplit7 = stringsplit3.split(",")

                    # Me inserta los simbolos con su tipo en posiciones de la lista
                    tablahashglobales.__setitem__(stringsplit6, stringsplit4, "func", "")

                    # Si no hay parámetros la función continúa sin saltar al else
                    if stringsplit3 == "":
                        relleno = ""
                    else:
                        null = ""
                        for i in range(0, len(stringsplit7)):
                            variable = stringsplit7[i]
                            variable = variable.split()

                            if (variable[0] in key_words) or not (variable[0] in datatype) or variable[0] in null:
                                break
                            else:
                                # Inserción de las variables obtenidas por parámetro
                                tablahashlocales.__setitem__(variable[1], variable[0], "var", " ")
                else:
                    # Este caso es cuando la verificacion del primer if denegó que la linea se tratase de una función
                    if not (stringsplit1[0] in datatype) or (stringsplit1[0] in key_words) or not (
                            stringsplit1[2] in igual):
                        relleno = ""
                    else:
                        tipolocal = stringsplit1[0]
                        simbololocal = stringsplit1[1]
                        valorlocal = stringsplit1[3]
                        tablahashlocales.__setitem__(simbololocal, tipolocal, "var", valorlocal)

# ...................................................SEGUNDA LECTURA....................................................

with open("codigo.txt") as f_obj:
    lines = f_obj.readlines()
for line in lines:
    # Llevando el conteo de las lineas
    # para mostrar donde sucedio el error
    contadorLinea = contadorLinea + 1
    linea = line.rstrip()
    linea_aux = line.split()
    # Buscando llaves "{" / "}" e
    # incrementando sus contadores
    ContadoresDeLlaves(linea)
    # En caso de toparse con una
    # línea vacía, la descarta
    if vacio(linea):
        linea = "descarte esto"
    else:
        # Si hay menos de un caracter en
        # una linea no pasa al siguiente if
        if MasDeunCaracter(linea_aux):
            # Este if solo hace que me decida por entrar al modo local, funciona si detecta una funcion
            if (linea_aux[0] in datatype or not linea_aux[0] in key_words) and linea_aux[1].find('(') != -1:
                # Modo local (1)
                modo = 1
                contadorFunciones = contadorFunciones + 1
        # Regresando al modo global
        # .................................................MODO GLOBAL..................................................
        if contadorAbro == contadorCierro:
            # Modo global (0)
            modo = 0
            # Buscando variables globales
            variables = Variables(linea)
            for i in range(0, len(variables)):
                if not BuscaGlobal(variables[i]):
                    print("(", contadorLinea, ")", "ERROR: La variable", variables[i], "no está declarada")
        # ..................................................MODO LOCAL..................................................
        elif modo == 1:
            stringsplit1 = linea.split()
            if MasDeunCaracter(linea_aux):
                # Este if es el que me analiza la funcion, en este es donde buscamos si esta bien declarada o no
                if (stringsplit1[0] in datatype or not stringsplit1[0] in key_words) and stringsplit1[1].find(
                        '(') != -1:

                    # Guarda el contenido de los parámetros
                    stringsplit2 = linea.split("(")[1]
                    stringsplit3 = stringsplit2.split(")")[0]

                    # Guarda el tipo de dato de la función
                    stringsplit4 = linea.split()[0]

                    # Guarda el nombre de la función
                    stringsplit5 = linea.split()[1]
                    stringsplit6 = stringsplit5.split('(')[0]

                    # Guarda las variables de los parámetros
                    stringsplit7 = stringsplit3.split(",")

                    # Si no hay parámetros la función continúa sin saltar al else
                    if stringsplit3 == "":
                        relleno = ""
                    else:
                        null = ""
                        for i in range(0, len(stringsplit7)):
                            variable = stringsplit7[i]
                            variable = variable.split()
                            if (variable[0] in key_words) or not (variable[0] in datatype) or variable[0] in null:
                                relleno = ""
                            else:
                                relleno = ""
                else:
                    # Buscando variables locales
                    locales = Variables(linea)
                    if linea_aux[0] == "return" and BuscaenReturn(locales, contadorFunciones):
                        if stringsplit4 != DevuelveTipo(linea_aux[1], contadorFunciones):
                            print("(", contadorLinea, ")", "ERROR: El tipo de dato de la función es: '", stringsplit4,
                                  "' y el valor de retorno es: '", DevuelveTipo(linea_aux[1], contadorFunciones), "'")
                    else:
                        for i in range(0, len(locales)):
                            if not BuscaLocal(locales[i], contadorFunciones):
                                print("(", contadorLinea, ")", "ERROR: La variable", locales[i],
                                      "no está declarada")
