import datetime


class Archivo(object):
    nombre = str
    directorio = object
    permisos = []
    fecha = str
    #archivo_txt = object
    contenido = ""
    propietario = object

    def __init__(self, nombre_nuevo, nuevo_propietario, contenido):
        self.nombre = nombre_nuevo
        self.propietario = nuevo_propietario
        self.contenido = contenido
        fecha = datetime.datetime.now()
        self.fecha = fecha.strftime("%b %d %H:%M")
        self.permisos = ["-", "rwx", "r-x", "r-x"]  # Permisos por defecto.
        # [0] si es directorio
        # [1] permisos del propietario
        # [2] permisos del grupo
        # [3] permisos de otros

    def mostrar_datos(self):
        permisos = ""
        for permiso in self.permisos:
            permisos += permiso
        print(permisos + " " + self.propietario.nombre + self.fecha + " " + self.nombre)
