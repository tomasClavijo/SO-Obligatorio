from Directorio import Directorio
from Usuario import Usuario
from Archivo import Archivo


def permisos(usuario_actual, archivo_directorio):
    if archivo_directorio.propietario == usuario_actual:
        return archivo_directorio.permisos[1]
    else:
        return archivo_directorio.permisos[3]


def ej_useradd(nombre_usuario, lista_usuarios, usuario_actual):
    if usuario_actual.nombre == "root":
        existe = False
        for usuario in lista_usuarios:
            if usuario.nombre == nombre_usuario:
                existe = True
        if not existe:
            nuevo_usuario = Usuario(nombre_usuario)
            lista_usuarios.append(nuevo_usuario)
            ej_passwd(nuevo_usuario.nombre, lista_usuarios, usuario_actual)
        else:
            print(f"useradd: user '{nombre_usuario}' already exists")
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

    for archivo in directorio_actual.archivos:
        if archivo.nombre == nombre_archivo:
            ej_rm(archivo.nombre, directorio_actual, nuevo_propietario)

    if "w" in permisos(nuevo_propietario, directorio_actual):
        nuevo_archivo = Archivo(nombre_archivo, nuevo_propietario, contenido)
        nuevo_archivo.directorio = directorio_actual
        directorio_actual.archivos.append(nuevo_archivo)
    else:
        print(f"touch: cannot touch '{nombre_archivo}': Permission denied")


def ej_echo(texto_archivo, nombre_archivo, directorio_actual, usuario_actual):
    esta = False
    for archivo in directorio_actual.archivos:
        if archivo == nombre_archivo:
            esta = True
            if "w" in permisos(usuario_actual, archivo):  # Si se puede escribir el archivo.
                archivo.contenido += texto_archivo + "\n"
            else:
                print(f"bash: {nombre_archivo}: Permission denied")
    if not esta and "w" in permisos(usuario_actual, directorio_actual):
        ej_touch(directorio_actual, nombre_archivo, usuario_actual, texto_archivo)
    else:
        print(f"bash: {nombre_archivo}: Permission denied")


def ej_mv(ruta_origen, ruta_destino, usuario_actual, directorio_actual, lista_directorios):
    nuevo_archivo = object
    esta = False

    ruta_origen_lista = ruta_origen.split("/")
    nuevo_archivo = ruta_origen_lista[len(ruta_origen_lista) - 1]

    ruta_destino_lista = ruta_destino.split("/")

    if ruta_origen == ruta_destino:
        print(f"mv: cannot move '{nuevo_archivo}' to a subdirectory of itself, {nuevo_archivo}/{nuevo_archivo}")

    if len(ruta_origen_lista) == 1 and ruta_origen_lista[0].endswith(".txt"):
        for archivo in directorio_actual.archivos:
            if archivo.nombre == ruta_origen_lista[0]:
                esta = True
                nuevo_archivo = Archivo(archivo.nombre, archivo.propietario, archivo.contenido)
                ej_rm(archivo.nombre, directorio_actual, usuario_actual)
    else:
        ruta_origen_lista.pop(len(ruta_origen_lista) - 1)
        ruta_origen_aux = "/".join(ruta_origen_lista)

        origen = ej_cd(ruta_origen_aux, directorio_actual, usuario_actual, lista_directorios)
        for archivo in origen.archivos:
            if archivo.nombre == nuevo_archivo:
                esta = True
                nuevo_archivo = Archivo(archivo.nombre, archivo.propietario, archivo.contenido)
                ej_rm(archivo.nombre, origen, usuario_actual)

    if esta:
        destino = ej_cd(ruta_destino, directorio_actual, usuario_actual, lista_directorios)
        # Al mover los archivos se deja la metadata orignal de cuando se creo.
        for archivo in destino.archivos:
            if archivo.nombre == ruta_destino_lista[len(ruta_destino_lista) - 1]:
                ej_rm(archivo.nombre, destino, usuario_actual)
        destino.archivos.append(nuevo_archivo)
        nuevo_archivo.directorio = destino


def ej_cp(ruta_origen, ruta_destino, usuario_actual, directorio_actual, lista_directorios):
    archivo_copiar = Archivo(None, None, None)
    esta = False

    ruta_origen_lista = ruta_origen.split("/")
    archivo_origen = ruta_origen_lista[len(ruta_origen_lista) - 1]
    ruta_origen_lista.pop(len(ruta_origen_lista) - 1)

    dir_origen = ej_cd("/".join(ruta_origen_lista), directorio_actual, usuario_actual, lista_directorios)
    for archivo in dir_origen.archivos:
        if archivo.nombre == archivo_origen:
            esta = True
            archivo_copiar.nombre = archivo.nombre
            archivo_copiar.contenido = archivo.contenido
            # Los unicos datos que mantengo al copiar, los demas son nuevos al momento de copiar el archivo.
    if esta:
        dir_destino = ej_cd(ruta_destino, directorio_actual, usuario_actual, lista_directorios)
        if type(dir_destino) is not Directorio:  # Si el ej_cd devuelve un print (que no tiene tipo).
            print(f"cp: cannot create regular file {ruta_destino}: Not a directory")
        else:
            if "w" in permisos(usuario_actual, dir_destino):
                ej_touch(dir_destino, archivo_copiar.nombre, usuario_actual, archivo_copiar.contenido)
                # La metadata del copiado va a ser nueva como si se hubiera creado a mano el archivo.
            else:
                print(f"cp: cannot create regular file {ruta_destino}: Permission denied")
    else:
        print(f"cp: cannot stat {ruta_origen}: No such file or directory")


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


def cd_ruta_especifica(ruta_directorios, ruta, directorio_actual, _directorio_llamada):
    esta = False
    if not directorio_actual.subdirectorios:
        return directorio_actual
    else:
        for directorio in directorio_actual.subdirectorios:
            if ruta_directorios[0] == directorio.nombre:
                esta = True
                ruta_directorios.pop(0) # if ruta directorios es null
                if not ruta_directorios:
                    return directorio
                else:
                    return cd_ruta_especifica(ruta_directorios, ruta, directorio, _directorio_llamada)
        if not esta:
            print(f"bash: cd: {ruta}: No such file or directory")
            return _directorio_llamada


def cd_ruta_entera(ruta_lista, ruta_str, _directorio_actual, directorio_actual):
    ruta_lista.pop(0)   # Elimino el "~".

    # Llego al directorio raiz ("~").
    while directorio_actual.directorio_padre:
        directorio_actual = directorio_actual.directorio_padre

    for directorio in directorio_actual.subdirectorios:
        if directorio.nombre == ruta_lista[0]:
            ruta_lista.pop(0)
            return ej_cd("/".join(ruta_lista), directorio, None, None)


def ej_cd(ruta_str, directorio_actual, usuario_actual, lista_directorios):
    # CD: permisos de ejecucion sobre el directorio.

    ruta_directorios = ruta_str.split("/")
    if ruta_directorios[0] == "~":
        es_ruta_global = True
    else:
        es_ruta_global = False
    if ruta_str == "" or ruta_str == "." or not ruta_directorios or ".txt" in ruta_str:
        return directorio_actual
    elif ruta_str == "..":
        return directorio_actual if directorio_actual.directorio_padre is None else directorio_actual.directorio_padre
    elif es_ruta_global:
        ruta_global_lista = ruta_str.split("/")
        return cd_ruta_entera(ruta_global_lista, ruta_str, directorio_actual, directorio_actual)
    elif not es_ruta_global:
        ruta_especifica_lista = ruta_str.split("/")
        return cd_ruta_especifica(ruta_especifica_lista, ruta_str, directorio_actual, directorio_actual)


def ej_lsl(directorio_actual, usuario_actual):
    # LS: permiso de lectura sobre el directorio.
    if "r" in permisos(usuario_actual, directorio_actual):
        for archivo in directorio_actual.archivos:
            archivo.mostrar_datos()
        for directorio in directorio_actual.subdirectorios:
            directorio.mostrar_datos()
    else:
        print(f"ls: cannot open directory '.': Permission denied")


def ej_his_grep(palabra_buscar, historial):
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
    esta = False
    if ".txt" in nombre_archivo_directorio:
        for archivo in directorio_actual.archivos:
            if archivo.nombre == nombre_archivo_directorio:
                esta = True
                if archivo.propietario == usuario_actual or usuario_actual.nombre == "root":
                    archivo.permisos = permisos_nuevos
                else:
                    print(f"chmod: changing permissions of {nombre_archivo_directorio}: Operation not permitted")
    else:
        for directorio in directorio_actual.subdirectorios:
            if directorio.nombre == nombre_archivo_directorio:
                esta = True
                if directorio.propietario == usuario_actual or usuario_actual.nombre == "root":
                    directorio.permisos = permisos_nuevos
                else:
                    print(f"chmod: changing permissions of {nombre_archivo_directorio}: Operation not permitted")
    if not esta:
        print(f"chmod: cannot access '{nombre_archivo_directorio}': No such file or directory")


def ej_chown(nombre_archivo_directorio, nuevo_propietario, usuario_actual, directorio_actual, lista_usuarios):
    if usuario_actual.nombre == "root":
        esta = False
        nuevo_propietario_objeto = None
        for usuario in lista_usuarios:
            if usuario.nombre == nuevo_propietario:
                nuevo_propietario_objeto = usuario

        if ".txt" in nombre_archivo_directorio:
            for archivo in directorio_actual.archivos:
                if archivo.nombre == nombre_archivo_directorio:
                    esta = True
                    archivo.propietario = nuevo_propietario_objeto
        else:
            for directorio in directorio_actual.subdirectorios:
                if directorio.nombre == nombre_archivo_directorio:
                    esta = True
                    directorio.propietario = nuevo_propietario_objeto
        if not esta:
            print(f"chown: cannot access '{nombre_archivo_directorio}': No such file or directory")
    else:
        print(f"chown: changing ownership of '{nombre_archivo_directorio}': Operation not permitted")


def comando_ejecucion(comando_entero, comando_partes, lista_directorios, lista_usuarios, usuario_actual,
                      directorio_actual, raiz, historial):
    if comando_entero != "":
        historial[len(historial) + 1] = comando_entero
    comando = comando_partes[0]

    if comando == "useradd":
        try:
            ej_useradd(comando_partes[1], lista_usuarios, usuario_actual)
        except IndexError:
            print("useradd: missing operand")

    elif comando == "passwd":
        try:
            ej_passwd(comando_partes[1], lista_usuarios, usuario_actual)
        except IndexError:
            print("passwd: missing operand")

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
            print("touch: missing file operand")

    elif comando == "echo":
        comando_partes.pop(0)

        texto_lista = comando_partes[0:len(comando_partes) - 2]
        texto = " ".join(texto_lista)
        try:
            ej_echo(texto, comando_partes[len(comando_partes) - 1], directorio_actual, usuario_actual)
        except IndexError:
            print("bash: syntax error near unexpected token 'newline'")

    elif comando == "mv":
        try:
            ej_mv(comando_partes[1], comando_partes[2], usuario_actual, directorio_actual, lista_directorios)
        except IndexError:
            print(f"mv: missing destination file operand after {comando_partes[1]}")

    elif comando == "cp":
        try:
            ej_cp(comando_partes[1], comando_partes[2], usuario_actual, directorio_actual, lista_directorios)
        except IndexError:
            print(f"cp: missing file operand or destination file")

    elif comando == "rm":
        try:
            ej_rm(comando_partes[1], directorio_actual, usuario_actual)
        except IndexError:
            print(f"rm: missing operand")

    elif comando == "cat":
        try:
            ej_cat(comando_partes[1], directorio_actual, usuario_actual)
        except IndexError:
            print(f"cat: missing operand")

    elif comando == "history":
        try:
            if comando == "history" and comando_partes[2] == "grep":
                ej_his_grep(comando_partes[3], historial)
        except IndexError:
            for numero, comando in historial.items():
                print(str(numero) + " " + comando)

    elif comando == "ls":
        ej_lsl(directorio_actual, usuario_actual)

    elif comando == "chmod":
        try:
            ej_chmod(comando_partes[1], comando_partes[2], usuario_actual, directorio_actual)
        except IndexError:
            print(f"chmod: missing operand")

    elif comando == "chown":
        try:
            ej_chown(comando_partes[2], comando_partes[1], usuario_actual, directorio_actual, lista_usuarios)
        except IndexError:
            print(f"chown: missing operand")

    else:
        print(f"bash: {comando_entero}: command not found")
