from typing import List
from Usuario import Usuario
from Directorio import Directorio
from Gestion import *
import os


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


def ej_cd2(ruta, lista_directorios, usuario_actual, directorio_actual):

    if ruta != "" or ruta != "." or not (".txt" in ruta):
        if ruta == "..":
            return directorio_actual.directorio_padre
        else:
            ruta_directorios = ruta.split("/")
            for directorio in directorio_actual.subdirectorios:
                if directorio.nombre == ruta_directorios[0]:
                    return directorio



if __name__ == "__main__":

    lista_usuarios = []
    lista_directorios = []

    usuario_principal = Usuario("root")
    usuario_principal.ingresar_contrasena("root")
    raiz = Directorio("directorioPrincipal", usuario_principal)
    raiz.directorio_padre = None

    lista_usuarios.append(usuario_principal)
    lista_directorios.append(raiz)

    usuario_actual = usuario_principal
    directorio_actual = raiz

    while True:
        comando = input(usuario_actual.nombre + "@&_")
        comando_partes = comando.split(" ")
        if comando == "exit":
            break
        elif comando_partes[0] == "su":
            contrasena = input("Password: ")
            usuario_actual = ej_su(comando_partes[1], contrasena, lista_usuarios, usuario_actual)
            pass
        elif comando_partes[0] == "cd":
            directorio_actual = ej_cd2(comando_partes[1], lista_directorios, usuario_actual, directorio_actual)
        else:
            comando_ejecucion(comando, comando_partes, lista_directorios, lista_usuarios, usuario_actual, directorio_actual, raiz)
