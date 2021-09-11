class Usuario(object):
    nombre = ''
    contrasena = ''

    def __init__(self, nombre_usuario=str):
        self.nombre = nombre_usuario

    def nombre_correcto(self, nombre_ingresado):
        if self.nombre == nombre_ingresado:
            return True

    def ingresar_contrasena(self, nueva_contrasena):
        self.contrasena = nueva_contrasena

    def print_nombre(self):
        print(self.nombre)
