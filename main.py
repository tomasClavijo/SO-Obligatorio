from typing import List
from Usuario import Usuario
from Directorio import Directorio
from Gestion import *
import os


if __name__ == "__main__":

    lista_usuarios = []
    lista_directorios = []

    usuario_principal = Usuario("root")
    raiz = Directorio("directorioPrincipal", usuario_principal)

    lista_usuarios.append(usuario_principal)
    lista_directorios.append(raiz)

    usuario_actual = usuario_principal
    directorio_actual = raiz

    while True:
        comando = input(usuario_actual.nombre + "@&_")
        if comando == "exit":
            break
        else:
            comando_ejecucion(comando, lista_directorios, lista_usuarios, usuario_actual, directorio_actual, raiz)
