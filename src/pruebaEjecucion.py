from extraccion import Extraccion
from transformacion import Transformacion
from carga import Carga

# Extracción
extraccion = Extraccion("mongodb://localhost:27017/", "AirBnbDB")
extraccion.conectar()
coleccion = "listado"
listings = extraccion.obtener_datos(coleccion)

# Transformación
transformador = Transformacion(listings)
df_transformado = transformador.transformar()

# Carga
cargador = Carga(df_transformado)
cargador.cargar_a_sqlite(f"{coleccion}.db", coleccion)
cargador.cargar_a_excel(f"{coleccion}.xlsx")
cargador.resumen()