from Directorio import Directorio
from Usuario import Usuario
from Archivo import Archivo

historial = {}


def leer_ruta():
    pass


def ej_useradd(nombre_usuario, lista_usuarios):
    if lista_usuarios.count(nombre_usuario) == 0:
        nuevo_usuario = Usuario(nombre_usuario)
        lista_usuarios.append(nuevo_usuario)
    else:
        print("Ver el mensaje de error que sale en Linux.")


def ej_passwd(nombre_usuario, lista_usuarios, usuario_actual):
    if usuario_actual.nombre == "root":
        esta = False
        for usuario in lista_usuarios:
            if usuario.nombre == nombre_usuario:
                contrasena_ingresada = input("Password: ")
                contrasena_ingresada_dos = input("Password: ")
                if contrasena_ingresada == contrasena_ingresada_dos:
                    usuario.ingresar_contrasena(contrasena_ingresada)
                    esta = True
                else:
                    print("mensaje de error")
        if not esta:
            print("Ver el mensaje de error que sale en Linux.")
    else:
        print("Ver mensaje de error en linux")


def ej_su(nombre_usuario, contrasena, usuarios, usuario_actual):
    esta = False
    for usuario in usuarios:
        if usuario.nombre == nombre_usuario:
            esta = True
            if usuario.contrasena == contrasena:
                historial = {}  # Se reinicia el historial cuando se cambia de usuario.
                return usuario
            else:
                print("ver mensaje de contrasena incorrecta")
                return usuario_actual
    if not esta:
        print("ver error SU en linux")
        return usuario_actual


def ej_whoami(usuario_actual):
    print(usuario_actual.nombre)


def ej_pwd(directorio_actual):
    retorno = ""
    directorio_aux = directorio_actual
    while directorio_aux.directorio_padre is not None:
        retorno = "/" + directorio_aux.nombre + retorno
        directorio_aux = directorio_aux.directorio_padre
    retorno = "/" + directorio_aux.nombre + retorno
    print(retorno)


def ej_mkdir(nombre, directorio_actual, usuario_actual):
    nuevo = Directorio(nombre, usuario_actual)
    nuevo.directorio_padre = directorio_actual
    directorio_actual.subdirectorios.append(nuevo)


def ejecutar_cd(directorio_actual, ruta=str):

    if ruta == "..":
        directorio_actual = directorio_actual.directorio_padre
        

    """ruta_origen_lista = ruta_origen.split("/")
    ruta_destino_lista = ruta_destino.split("/")
    directorio_aux = raiz
    print(directorio_actual)

    if raiz.nombre == ruta_origen_lista[0]: # Caso ruta completa.
        contador = 1
        correcta = True
        while contador != len(ruta_origen_lista)-1 and correcta:
            for i in directorio_aux.subdirectorios:
                if i.nombre == ruta_origen_lista[contador]:
                    contador += 1
                    directorio_aux = i
                else:
                    print("ruta mala, error linux")
                    correcta = False
        if correcta:
            for i in directorio_aux.archivos:
                if i.nombre == ruta_origen_lista[len(ruta_origen_lista)-1]:
                    pass
                    # mover
        
    else: # Caso ruta desde posicion relativa.
        pass"""


def ej_touch(directorio, nombre_archivo, nuevo_propietario, contenido):

    nuevo_archivo = Archivo(nombre_archivo, nuevo_propietario, contenido)
    nuevo_archivo.directorio = directorio
    directorio.archivos.append(nuevo_archivo)


def ej_echo(texto_archivo, nombre_archivo, directorio_actual, usuario_actual):

    esta = False

    """ Consulta, el archivo se asume como creado? """
    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            archivo.contenido += texto_archivo+"\n"
            esta = True

    if not esta:
        ej_touch(directorio_actual, nombre_archivo, usuario_actual, texto_archivo)


def prueba_mostrar_contenido(directorio_actual, usuario_actual):
    for i in directorio_actual.archivos:
        print(i.nombre + i.contenido)


def ej_mv(ruta_origen, ruta_destino, usuario_actual, directorio_actual, raiz):

    # ["/", "a1", "b2"]

    ruta_origen_lista = ruta_origen.split("/")
    ruta_destino_lista = ruta_destino.split("/")
    directorio_aux = raiz
    print(directorio_actual)

    if raiz.nombre == ruta_origen_lista[0]: # Caso ruta completa.
        contador = 1
        correcta = True
        while contador != len(ruta_origen_lista)-1 and correcta:
            for i in directorio_aux.subdirectorios:
                if i.nombre == ruta_origen_lista[contador]:
                    contador += 1
                    directorio_aux = i
                else:
                    print("ruta mala, error linux")
                    correcta = False

        if correcta:
            for i in directorio_aux.archivos:
                if i.nombre == ruta_origen_lista[len(ruta_origen_lista)-1]:
                    pass
                    # mover

    else: # Caso ruta desde posicion relativa.
        pass


def ej_cp():
    pass


def ej_cat(nombre_archivo, directorio_actual, usuario_actual):
    esta = False

    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            print(archivo.contenido)
            esta = True

    if not esta:
        print("cat: "+nombre_archivo+": No such file or directory")


def ej_rm(nombre_archivo, directorio_actual, usuario_actual):
    contador = 0
    esta = False

    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            archivo.contenido = ""
            esta = True
        contador += 1
        directorio_actual.archivos.pop(contador)
    if not esta:
        print("rm: cannot remove " + nombre_archivo + ": No such file or directory")


def cd_aux(ruta, directorio_actual):

    if not directorio_actual.subdirectorios:
        return directorio_actual
    else:
        for directorio in directorio_actual.subdirectorios:
            if ruta[0] == directorio.nombre:
                ruta.pop(0)
                return cd_aux(ruta, directorio)


def ej_cd(ruta, directorio_actual, usuario_actual, lista_directorios):

    ruta_directorios = ruta.split("/")
    ruta_entera = False

    if ruta == "" or ruta == "." or not ruta_directorios or ".txt" in ruta:
        return directorio_actual
    elif ruta == "..":
        return directorio_actual if directorio_actual.directorio_padre is None else directorio_actual.directorio_padre
    elif ruta_entera:
        pass
    elif not ruta_entera:
        return cd_aux(ruta_directorios, directorio_actual)

def ej_lsl(directorio_actual, usuario_actual):
    for archivo in directorio_actual.archivos:
        archivo.mostrar_datos()
    for directorio in directorio_actual.subdirectorios:
        directorio.mostrar_datos()


def ej_his_grep(palabra_buscar):
    palabra_buscar = palabra_buscar.replace('"', '')
    retorno = ""
    for numero, comando in historial.items():
        linea = str(numero) + " " + comando
        if palabra_buscar in linea:
            retorno += linea + "\n"
    print(retorno)


def ej_chmod(valor, nombre_archivo, usuario_actual, directorio_actual):
    permisos_nuevos = ["-", "rwx", "r-x", "r-x"]

    for i in range(3):
        j = i + 1
        if valor[i] == '0':
            permisos_nuevos[j] = "---"
        elif valor[i] == '1':
            permisos_nuevos[j] = "--x"
        elif valor[i] == '2':
            permisos_nuevos[j] = "-w-"
        elif valor[i] == '3':
            permisos_nuevos[j] = "-wx"
        elif valor[i] == '4':
            permisos_nuevos[j] = "r--"
        elif valor[i] == '5':
            permisos_nuevos[j] = "r-x"
        elif valor[i] == '6':
            permisos_nuevos[j] = "rw-"
        elif valor[i] == '7':
            permisos_nuevos[j] = "rwx"

    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            archivo.permisos = permisos_nuevos


def ej_chown(nombre_archivo, nuevo_propietario, usuario_actual, directorio_actual):

    # Solo el root puede cambiar propietarios?

    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            archivo.propietario = nuevo_propietario


def comando_ejecucion(comando_entero, comando_partes, lista_directorios, lista_usuarios, usuario_actual, directorio_actual, raiz):
    if comando_entero != "":
        historial[len(historial) + 1] = comando_entero
    #comando_partes = comando_ejecutar.split(" ")
    comando = comando_partes[0]

    if comando == "useradd":

        ej_useradd(comando_partes[1], lista_usuarios)

    elif comando == "passwd":
        ej_passwd(comando_partes[1], lista_usuarios, usuario_actual)

    elif comando == "pwd":

        ej_pwd(directorio_actual)

    elif comando == "whoami":

        ej_whoami(usuario_actual)

    elif comando == "pwd":

        ej_pwd()

    elif comando == "mkdir":

        try:
            ej_mkdir(comando_partes[1], directorio_actual, usuario_actual)
        except IndexError:
            print("mkdir: missing operand")

    elif comando == "touch":
        try:
            ej_touch(directorio_actual, comando_partes[1], usuario_actual, "")
        except IndexError:
            print("error archivo linux")

    elif comando == "echo":
        comando_partes.pop(0)

        texto_lista = comando_partes[0:len(comando_partes)-2]
        texto = " ".join(texto_lista)

        try:
            ej_echo(texto, comando_partes[len(comando_partes)-1], directorio_actual, usuario_actual)
        except IndexError:
            print("error echo linux")

    elif comando == "mv":
        try:
            ej_mv(comando_partes[1], comando_partes[2], usuario_actual, directorio_actual, raiz)
        except IndexError:
            print("error move linux")

    elif comando == "rm":
        try:
            ej_rm(comando_partes[1], directorio_actual, usuario_actual)
        except IndexError:
            print("error rm linux aaaa")

    elif comando == "cat":
        try:
            ej_cat(comando_partes[1], directorio_actual, usuario_actual)
        except IndexError:
            print("error archivo linux")

    elif comando == "cd":
        try:
            ejecutar_cd(directorio_actual, comando_partes[1])
        except IndexError:
            print("Ver mensaje de error en linux")

    elif comando == "history":
        try:
            if comando == "history" and comando_partes[2] == "grep":
                ej_his_grep(comando_partes[3])
        except IndexError:
            for numero, comando in historial.items():
                print(str(numero) + " " + comando)

    elif comando == "ls":
        ej_lsl(directorio_actual, usuario_actual)

    elif comando == "chmod":
        ej_chmod(comando_partes[1], comando_partes[2], usuario_actual, directorio_actual)
