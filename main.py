from typing import List
from Usuario import Usuario
from Directorio import Directorio
from Gestion import *
import os


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
            directorio_actual = ej_cd(comando_partes[1], directorio_actual, usuario_actual, lista_directorios)
            #directorio_actual = retorno if retorno is not None else print("bash: cd: " + comando_partes[1] + " :No such file or directory")
        else:
            comando_ejecucion(comando, comando_partes, lista_directorios, lista_usuarios, usuario_actual, directorio_actual, raiz)
