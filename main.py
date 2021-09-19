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


if __name__ == "__main__":

    lista_usuarios = []
    lista_directorios = []

    usuario_principal = Usuario("root")
    usuario_principal.ingresar_contrasena("root")
    raiz = Directorio("directorioPrincipal", usuario_principal)

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
        else:
            comando_ejecucion(comando, comando_partes, lista_directorios, lista_usuarios, usuario_actual, directorio_actual, raiz)
