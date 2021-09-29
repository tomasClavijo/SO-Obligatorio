from Directorio import Directorio
from Usuario import Usuario
from Archivo import Archivo

historial = {}


def ej_useradd(nombre_usuario, lista_usuarios, usuario_actual):
    if usuario_actual.nombre == "root":
        existe = False
        for usuario in lista_usuarios:
            if usuario.nombre == nombre_usuario:
                existe = True
        if not existe:
            nuevo_usuario = Usuario(nombre_usuario)
            lista_usuarios.append(nuevo_usuario)
    else:
        print(f"{usuario_actual.nombre} is not in the sudoers file.")


def ej_passwd(nombre_usuario, lista_usuarios, usuario_actual):
    if usuario_actual.nombre == "root":
        esta = False
        for usuario in lista_usuarios:
            if usuario.nombre == nombre_usuario:
                contrasena_ingresada = input("New password: ")
                contrasena_ingresada_dos = input("Retype new password: ")
                if contrasena_ingresada == contrasena_ingresada_dos:
                    usuario.ingresar_contrasena(contrasena_ingresada)
                    print("passwd: password updated successfully")
                    esta = True
                else:
                    print("Sorry, passwords do not match.")
                    print("passwd: Authenticacion token manipulation error \n passwd: password unchanged")
        if not esta:
            print(f"passwd: user {nombre_usuario} does not exist")
    else:
        print(f"passwd: You may not view or modify password information for {nombre_usuario}")


def ej_su(nombre_usuario, contrasena, usuarios, usuario_actual):
    esta = False
    for usuario in usuarios:
        if usuario.nombre == nombre_usuario:
            esta = True
            if usuario.contrasena == contrasena:
                historial = {}  # Se reinicia el historial cuando se cambia de usuario.
                return usuario
            else:
                print("su: Authentication failure")
                return usuario_actual
    if not esta:
        print(f"su: user {nombre_usuario} does not exist or the user entry does not contain all the required fields")
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


def ej_mkdir(nombre_directorio, directorio_actual, usuario_actual):
    # MKDIR: permiso de escritura necesario sobre el directorio.
    if "w" in permisos(usuario_actual, directorio_actual):
        nuevo = Directorio(nombre_directorio, usuario_actual)
        nuevo.directorio_padre = directorio_actual
        directorio_actual.subdirectorios.append(nuevo)
    else:
        print(f"mkdir: cannot create directory '{nombre_directorio}': Permission denied")


def ej_touch(directorio_actual, nombre_archivo, nuevo_propietario, contenido):
    # TOUCH: permiso de escritura sobre el directorio.

    if "w" in permisos(nuevo_propietario, directorio_actual):
        nuevo_archivo = Archivo(nombre_archivo, nuevo_propietario, contenido)
        nuevo_archivo.directorio = directorio_actual
        directorio_actual.archivos.append(nuevo_archivo)
    else:
        print(f"touch: cannot touch '{nombre_archivo}': Permission denied")


def permisos(usuario_actual, archivo_directorio):
    if archivo_directorio.propietario == usuario_actual:
        return archivo_directorio.permisos[1]
    else:
        return archivo_directorio.permisos[3]


def ej_echo(texto_archivo, nombre_archivo, directorio_actual, usuario_actual):
    esta = False
    for archivo in directorio_actual.archivos:
        if archivo == nombre_archivo:
            if "w" in permisos(usuario_actual, archivo):  # Si se puede escribir el archivo.
                archivo.contenido += texto_archivo + "\n"
                esta = True
            else:
                print(f"bash: {nombre_archivo}: Permission denied")
    if not esta and "w" in permisos(usuario_actual, directorio_actual):
        ej_touch(directorio_actual, nombre_archivo, usuario_actual, texto_archivo)
    else:
        print(f"bash: {nombre_archivo}: Permission denied")


def ej_mv(ruta_origen, ruta_destino, usuario_actual, directorio_actual, raiz):
    # ["/", "a1", "b2"]

    ruta_origen_lista = ruta_origen.split("/")
    ruta_destino_lista = ruta_destino.split("/")
    directorio_aux = raiz
    print(directorio_actual)

    if raiz.nombre == ruta_origen_lista[0]:  # Caso ruta completa.
        contador = 1
        correcta = True
        while contador != len(ruta_origen_lista) - 1 and correcta:
            for i in directorio_aux.subdirectorios:
                if i.nombre == ruta_origen_lista[contador]:
                    contador += 1
                    directorio_aux = i
                else:
                    print("ruta mala, error linux")
                    correcta = False

        if correcta:
            for i in directorio_aux.archivos:
                if i.nombre == ruta_origen_lista[len(ruta_origen_lista) - 1]:
                    pass
                    # mover

    else:  # Caso ruta desde posicion relativa.
        pass


def ej_cp():
    pass


def ej_cat(nombre_archivo, directorio_actual, usuario_actual):
    esta = False
    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            esta = True
            if "r" in permisos(usuario_actual, archivo):
                print(archivo.contenido)
            else:
                print(f"cat: '{nombre_archivo}': Permission denied")
    if not esta:
        print(f"cat: '{nombre_archivo}': No such file or directory")


def ej_rm(nombre_archivo, directorio_actual, usuario_actual):
    # RM: permisos de lectura y escritura sobre el DIRECTORIO.
    contador = 0
    esta = False
    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            esta = True
            if "r" and "w" in permisos(usuario_actual, directorio_actual):
                archivo.contenido = ""
                directorio_actual.archivos.pop(contador)
            else:
                print(f"rm: cannot remove '{nombre_archivo}': Permission denied")
        contador += 1
    if not esta:
        print(f"rm: cannot remove '{nombre_archivo}': No such file or directory")


def cd_aux(ruta_directorios, _ruta_llamada, directorio_actual, _directorio_llamada):
    esta = False
    if not directorio_actual.subdirectorios:
        return directorio_actual
    else:
        for directorio in directorio_actual.subdirectorios:
            if ruta_directorios[0] == directorio.nombre:
                esta = True
                ruta_directorios.pop(0)
                return cd_aux(ruta_directorios, _ruta_llamada, directorio, _directorio_llamada)
        if not esta:
            print(f"bash: cd: {_ruta_llamada}: No such file or directory")
            return _directorio_llamada


def ej_cd(ruta, directorio_actual, usuario_actual, lista_directorios):

    # CD: permisos de ejecucion sobre el directorio. TODO

    ruta_directorios = ruta.split("/")
    ruta_entera = False

    if ruta == "" or ruta == "." or not ruta_directorios or ".txt" in ruta:
        return directorio_actual
    elif ruta == "..":
        return directorio_actual if directorio_actual.directorio_padre is None else directorio_actual.directorio_padre
    elif ruta_entera:
        pass
    elif not ruta_entera:
        return cd_aux(ruta_directorios, ruta, directorio_actual, directorio_actual)


def ej_lsl(directorio_actual, usuario_actual):
    # LS: permiso de lectura sobre el directorio.
    if "r" in permisos(usuario_actual, directorio_actual):
        for archivo in directorio_actual.archivos:
            archivo.mostrar_datos()
        for directorio in directorio_actual.subdirectorios:
            directorio.mostrar_datos()
    else:
        print(f"ls: cannot open directory '.': Permission denied")


def ej_his_grep(palabra_buscar):
    palabra_buscar = palabra_buscar.replace('"', '')
    retorno = ""
    for numero, comando in historial.items():
        linea = str(numero) + " " + comando
        if palabra_buscar in linea:
            retorno += linea + "\n"
    print(retorno)


def ej_chmod(valor, nombre_archivo_directorio, usuario_actual, directorio_actual):
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

    if ".txt" in nombre_archivo_directorio:
        for archivo in directorio_actual.archivos:
            if archivo.nombre == nombre_archivo_directorio:
                if archivo.propietario == usuario_actual or usuario_actual.nombre == "root":
                    archivo.permisos = permisos_nuevos
                else:
                    print(f"chmod: changing permissions of {nombre_archivo_directorio}: Operation not permitted")
    else:
        for directorio in directorio_actual.subdirectorios:
            if directorio.nombre == nombre_archivo_directorio:
                if directorio.propietario == usuario_actual or usuario_actual.nombre == "root":
                    directorio.permisos = permisos_nuevos
                else:
                    print(f"chmod: changing permissions of {nombre_archivo_directorio}: Operation not permitted")


def ej_chown(nombre_archivo, nuevo_propietario, usuario_actual, directorio_actual):
    if usuario_actual.nombre == "root":
        contrasena = input("Password: ")
        if usuario_actual.contrasena == contrasena:
            if ".txt" in nombre_archivo:
                for archivo in directorio_actual.archivos:
                    if archivo.nombre == nombre_archivo:
                        archivo.propietario = nuevo_propietario
            else:
                for directorio in directorio_actual.subdirectorios:
                    if directorio.nombre == nombre_archivo:
                        directorio.propietario = nuevo_propietario
        else:
            print("password incorrecta")
    else:
        print("error solo el root puede cambiar permisos.")


def comando_ejecucion(comando_entero, comando_partes, lista_directorios, lista_usuarios, usuario_actual,
                      directorio_actual, raiz):
    if comando_entero != "":
        historial[len(historial) + 1] = comando_entero
    comando = comando_partes[0]

    if comando == "useradd":

        ej_useradd(comando_partes[1], lista_usuarios, usuario_actual)

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

        texto_lista = comando_partes[0:len(comando_partes) - 2]
        texto = " ".join(texto_lista)

        try:
            ej_echo(texto, comando_partes[len(comando_partes) - 1], directorio_actual, usuario_actual)
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
