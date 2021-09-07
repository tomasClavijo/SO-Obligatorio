import datetime


class Archivo(object):
    nombre = str
    directorio = object
    permisos = []
    fecha = str

    def __init__(self, nombre_nuevo):
        self.nombre = nombre_nuevo
        fecha = datetime.datetime.now()
        self.fecha = fecha.strftime("%b %d %H:%M")
        self.permisos = ["-", "rwx", "r-x", "r-x"]  # Permisos por defecto.
        # [0] si es directorio
        # [1] permisos del propietario
        # [2] permisos del grupo
        # [3] permisos de otros