from Directorio import Directorio
from Usuario import Usuario
from Archivo import Archivo


def ej_useradd(nombre_usuario, lista_usuarios):
    if lista_usuarios.count(nombre_usuario) == 0:
        nuevo_usuario = Usuario(nombre_usuario)
        lista_usuarios.append(nuevo_usuario)
    else:
        print("Ver el mensaje de error que sale en Linux.")


def ej_passwd(nombre_usuario, lista_usuarios):
    esta = False
    for usuario in lista_usuarios:
        if usuario.nombre == nombre_usuario:
            contrasena_ingresada = input("Ingrese contrasena (ver en Linux como lo preguntan): ")
            usuario.ingresar_contrasena(contrasena_ingresada)
            esta = True
    if esta:
        pass
    else:
        print("Ver el mensaje de error que sale en Linux.")


def ej_su(nombre_usuario, lista_usuarios, usuario_actual, contrasena):
    if lista_usuarios.count(nombre_usuario) == 1:
        for usuario in lista_usuarios:
            if usuario.nombre == nombre_usuario and usuario.contrasena == contrasena:
                usuario_actual = usuario


def ej_whoami(usuario_actual):
    print(usuario_actual.nombre)


def ej_pwd(lista_directorios):
    ruta = ""
    for directorio in lista_directorios:
        ruta += directorio.nombre
    print(ruta)


def ej_mkdir(directorio_actual, nombre):
    directorio_actual.subdirectorios.append(Directorio(nombre))


def ejecutar_cd(directorio_padre=Directorio, ruta=str):
    pass


def ej_touch(directorio, nombre_archivo, nuevo_propietario):

    # f = open(nombre_archivo, "w+")
    # nuevo_archivo.archivo_txt = f
    nuevo_archivo = Archivo(nombre_archivo, nuevo_propietario)
    nuevo_archivo.directorio = directorio
    directorio.archivos.append(nuevo_archivo)


def ej_echo():
    pass


def ej_mv():
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


def ej_rm():
    pass


def ej_lsl():
    pass


def ej_history():
    pass


def ej_chmod():
    pass


def ej_chown():
    pass


def mostrar_todo():     # Solo de prueba
    pass


def comando_ejecucion(comando_ejecutar, lista_directorios, lista_usuarios, usuario_actual, directorio_actual):
    comando_partes = comando_ejecutar.split(" ", 3)
    comando = comando_partes[0]

    if comando == "useradd":

        ej_useradd(comando_partes[1], lista_usuarios)

    elif comando == "passwd":
        ej_passwd(comando_partes[1], lista_usuarios)

    elif comando == "su":
        contrasena = input("Ingrese contrasena (ver en Linux como lo preguntan): ")
        ej_su(comando_partes[1], lista_usuarios, usuario_actual, contrasena)

    elif comando == "pwd":

        ej_pwd(lista_directorios)

    elif comando == "whoami":

        ej_whoami(usuario_actual)

    elif comando == "pwd":

        ej_pwd()

    elif comando == "mkdir":

        try:
            ej_mkdir(directorio_actual, comando_partes[1])
        except IndexError:
            print("mkdir: missing operand")

    elif comando == "touch":
        try:
            ej_touch(directorio_actual, comando_partes[1], usuario_actual)
        except IndexError:
            print("error archivo linux")

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

    elif comando == "ls":
        for directorio in directorio_actual.subdirectorios:
            print(directorio.nombre)
        for archivo in directorio_actual.archivos:
            print(archivo.nombre)

    """switcher = {
        "cd": ejecutar_cd(),
        "useradd": ejecutar_useradd(),
        "passwd": ejecutar_passwd(),
        "su": ej_su(),
        "whoami": ej_whoami(usuario_actual),
        "pwd": ej_pwd(lista_directorios),
        "mkdir": ek_mkdir(),
        "touch": ej_touch(),
        "echo": ej_echo(),
        "mv": ej_mv(),
        "cp": ej_cp(),
        "cat": ej_cat(),
        "rm": ej_rm(),
        "ls -l": ej_lsl(),
        "history": ej_history(),
        "chmod": ej_chmod(),
        "chown": ej_chown()
        # comandoPrimero | comandoSegundo
        # history | grep
    }
    switcher.get(comando)"""
