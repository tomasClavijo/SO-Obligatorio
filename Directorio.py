import datetime


class Directorio(object):
    nombre = str
    directorio_padre = object
    archivos = []
    subdirectorios = []
    permisos = []
    fecha = str
    propietario = object

    def __init__(self, nombre_nuevo, nuevo_propietario):
        self.nombre = nombre_nuevo
        self.subdirectorios = []
        self.archivos = []
        self.propietario = nuevo_propietario
        fecha = datetime.datetime.now()
        self.fecha = fecha.strftime("%b %d %H:%M")
        self.permisos = ["d", "rwx", "r-x", "r-x"]  # Permisos por defecto.
        # [0] si es directorio
        # [1] permisos del propietario
        # [2] permisos del grupo
        # [3] permisos de otros

    def es_hijo_de(self, padre=object):
        self.directorio_padre = padre

    def imprimir(self):
        print(self.nombre + "~~~" + self.fecha + "~~~" + self.permisos)

    def mostrar_datos(self):
        permisos = ""
        for permiso in self.permisos:
            permisos += permiso
        print(permisos + " " + self.propietario.nombre + self.fecha + " " + self.nombre)
