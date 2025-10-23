# Proyecto ETL AirBnb

## Descripción del proyecto y objetivo

Este proyecto implementa un pipeline ETL (Extracción, Transformación y Carga) para procesar datos de AirBnb. El objetivo es extraer datos desde una base MongoDB, transformarlos para análisis (limpieza, normalización, enriquecimiento) y cargarlos en formatos accesibles como SQLite y Excel, facilitando el análisis exploratorio y visualización.

## Instrucciones de instalación

1. **Clonar el repositorio**
   ```sh
   git clone https://github.com/usuario/Taller2ETL.git
   cd Taller2ETL
   ```

2. **Crear entorno virtual**
   ```sh
   python -m venv venvAirBnB
   #Activar el entorno creado:
    #Si estás en Linux
        source venvAirBnB/bin/activate   
    #Si estás en Windows: 
        venvAirBnB\Scripts\activate.bat
   ```

3. **Instalar dependencias**
   ```sh
   pip install -r requirements.txt
   ```

4. **Ejecutar el pipeline principal**
   ```sh
   python src/pruebaEjecucion.py
   ```
   *Debe estar corriendo la instancia del servidor Mongo con las colecciones AirBnB*

## Integrantes del grupo y responsabilidades

- **Juan Daniel Duque Estrada:** Extracción de datos, conexión a MongoDB y análisis exploratorio ([`Extraccion`](src/extraccion.py)) ([notebooks/exploracion_airbnb.ipynb](notebooks/exploracion_airbnb.ipynb))

- **David Ramirez Velez:** Transformación y limpieza de datos ([`Transformacion`](src/transformacion.py))

- **Simón Alejandro Vanegas:** Carga de datos a SQLite y Excel y visualización de los datos([`Carga`](src/carga.py)) ([notebooks/exploracion_airbnb.ipynb](notebooks/exploracion_airbnb.ipynb))

- **Todos los integrantes:** Gestión de logs y documentación ([`Logs`](src/logs.py), README)

## Ejemplo de ejecución del ETL
###      Este mismo se encuentra en el archivo pruebaEjecucion.py que se encuentra en el src. Se deben modificar los nombres para que correspondan con el nombre de la base datos y las colecciones.

```python
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
```

Archivos generados:
- `airbnb_cargado.db` (SQLite)
- `datos_airbnb.xlsx` (Excel)
- Logs en [logs/](logs/)

Para análisis y visualización, consulta el notebook [notebooks/exploracion_airbnb.ipynb](notebooks/exploracion_airbnb.ipynb).