from extraccion import Extraccion
from transformacion import Transformacion
from carga import Carga

# Extracción
extraccion = Extraccion("mongodb://localhost:27017/", "AirBnbDB")
extraccion.conectar()
listings = extraccion.obtener_datos("listado")

# Transformación
transformador = Transformacion(listings)
df_transformado = transformador.transformar()

# Carga
cargador = Carga(df_transformado)
cargador.cargar_a_sqlite()
cargador.cargar_a_excel()
cargador.resumen()