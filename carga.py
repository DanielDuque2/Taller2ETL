import pandas as pd
import sqlite3
import logging
from pathlib import Path

# Configuración del log
logging.basicConfig(
    filename="carga.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Carga:
    """
    Clase para realizar la carga de datos transformados hacia:
      - Una base de datos SQLite.
      - Archivos Excel (.xlsx).

    Métodos:
    --------
    - cargar_a_sqlite(nombre_db, nombre_tabla)
    - cargar_a_excel(nombre_archivo)
    - verificar_carga_sqlite(nombre_db, nombre_tabla)
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.registros = len(df)
        self.reportes = []

    def cargar_a_sqlite(self, nombre_db: str = "airbnb_cargado.db", nombre_tabla: str = "datos_airbnb"):
        try:
            conn = sqlite3.connect(nombre_db)
            self.df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            conn.close()

            mensaje = f"Datos cargados en SQLite -> Base: {nombre_db}, Tabla: {nombre_tabla} ({self.registros} registros)."
            self.reportes.append(mensaje)
            logging.info(mensaje)
        except Exception as e:
            logging.error(f"Error al cargar datos en SQLite: {e}")

    def cargar_a_excel(self, nombre_archivo: str = "datos_airbnb.xlsx"):
        try:
            ruta = Path(nombre_archivo)
            self.df.to_excel(ruta, index=False)
            mensaje = f"Archivo Excel creado correctamente: {ruta} ({self.registros} registros)."
            self.reportes.append(mensaje)
            logging.info(mensaje)
        except Exception as e:
            logging.error(f"Error al exportar a Excel: {e}")

    def verificar_carga_sqlite(self, nombre_db: str, nombre_tabla: str):
        try:
            conn = sqlite3.connect(nombre_db)
            query = f"SELECT COUNT(*) FROM {nombre_tabla}"
            resultado = conn.execute(query).fetchone()
            conn.close()

            cantidad_db = resultado[0]
            mensaje = f"Verificación: {cantidad_db} registros en SQLite vs {self.registros} en DataFrame."
            self.reportes.append(mensaje)
            logging.info(mensaje)

            if cantidad_db == self.registros:
                logging.info("✅ Verificación exitosa: Los registros coinciden.")
            else:
                logging.warning("⚠️ Verificación fallida: Cantidades diferentes.")
        except Exception as e:
            logging.error(f"Error al verificar carga en SQLite: {e}")

    def resumen(self):
        print("\nResumen de carga:")
        for r in self.reportes:
            print("-", r)
