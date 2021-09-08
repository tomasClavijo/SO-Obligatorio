import datetime


class Directorio(object):
    nombre = str
    directorio_padre = object
    archivos = []
    subdirectorios = []
    permisos = []
    fecha = str

    def __init__(self, nombre_nuevo):
        self.nombre = nombre_nuevo
        self.subdirectorios = []
        self.archivos = []
        fecha = datetime.datetime.now()
        self.fecha = fecha.strftime("%b %d %H:%M")
        self.permisos = ["d", "rwx", "r-x", "r-x"]  # Permisos por defecto.
        # [0] si es directorio
        # [1] permisos del propietario
        # [2] permisos del grupo
        # [3] permisos de otros

    def es_hijo_de(self, padre=object):
        self.directorio_padre = padre
