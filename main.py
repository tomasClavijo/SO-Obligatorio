from typing import List
from Usuario import Usuario
from Directorio import Directorio
from Gestion import *
import os


if __name__ == "__main__":

    lista_usuarios = []
    lista_directorios = []

    usuario_principal = Usuario("root")
    usuario_principal.esRoot = True
    raiz = Directorio("directorioPrincipal")
    os.mkdir("directorioPrincipal")


    lista_usuarios.append(usuario_principal)
    lista_directorios.append(raiz)

    usuario_actual = usuario_principal
    directorio_actual = raiz

    while True:
        comando = input(usuario_actual.nombre + "@&_")
        if comando == "exit":
            break
        else:
            comando_ejecucion(comando, lista_directorios, lista_usuarios, usuario_actual, directorio_actual)

    """
    
    listaUsuarios = []
    usuarioActual = Usuario

    print(">")
    comando = input()

    if(comando == "useradd"):
        print("Ingrese nombre: ")
        nombreNuevo = input()

        nuevoUsuario = Usuario(nombreNuevo)
        listaUsuarios.append(nuevoUsuario)
        usuarioActual = nuevoUsuario

    for i in listaUsuarios:
        print(i.nombre)

    print(usuarioActual.nombre)

    directorioActual = Directorio("/")
    listaGlobalDir = []
    listaGlobalDir.append(directorioActual)
    listaGlobalDir.append(Directorio("Sem1"))
    listaGlobalDir.append(Directorio("sem2"))
    listaGlobalDir.append(Directorio("Sem3"))

    if(comando == "mkdir"):
        print("Ingrese nombre dir: ")
        nombreNuevo = input()

        nuevoDir = Directorio(nombreNuevo)
        listaGlobalDir.append(nuevoDir)
    if(comando == "cd"):
        print("ingrese nom: ")
        nombreDir = input()

        encontro = False

        for dir in listaGlobalDir:
            if(dir.nombre == nombreDir):
                directorioActual = dir
                encontro = True
                break
        
        if not(encontro): print("No se encuentra el directorio")
                

    if(comando == "mkdir"):
        print("Ingrese nombre dir: ")
        nombreNuevo = input()

        nuevoDir = Directorio(nombreNuevo)
        listaGlobalDir.append(nuevoDir)


    for i in listaGlobalDir:
        print(i.nombre)
        
    """




