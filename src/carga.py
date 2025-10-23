import sqlite3
import pandas as pd
from logs import Logs
from pathlib import Path

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
        self.log = Logs("carga")
        self.log.info(f"Iniciando carga de {self.registros} registros")

    def cargar_a_sqlite(self, nombre_db: str = "airbnb_cargado.db", nombre_tabla: str = "datos_airbnb"):
        try:
            conn = sqlite3.connect(nombre_db)
            self.df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            conn.close()

            mensaje = f"Cargado en SQLite: {nombre_db} | Tabla: {nombre_tabla} ({self.registros} registros)"
            self.reportes.append(mensaje)
            self.log.info(mensaje)
        except Exception as e:
            error_msg = f"Error al cargar en SQLite: {e}"
            self.log.error(error_msg)

    def cargar_a_excel(self, nombre_archivo: str = "datos_airbnb.xlsx"):
        try:
            ruta = Path(nombre_archivo)
            self.df.to_excel(ruta, index=False)
            
            mensaje = f"Archivo Excel creado: {ruta} ({self.registros} registros)"
            self.reportes.append(mensaje)
            self.log.info(mensaje)
        except Exception as e:
            error_msg = f"Error al exportar a Excel: {e}"
            self.log.error(error_msg)

    def verificar_carga_sqlite(self, nombre_db: str, nombre_tabla: str):
        try:
            conn = sqlite3.connect(nombre_db)
            query = f"SELECT COUNT(*) FROM {nombre_tabla}"
            resultado = conn.execute(query).fetchone()
            conn.close()

            cantidad_db = resultado[0]
            if cantidad_db == self.registros:
                self.log.info(f"Verificación exitosa: {cantidad_db} registros en BD coinciden")
            else:
                self.log.warning(f"Discrepancia: BD={cantidad_db} vs DataFrame={self.registros}")
        except Exception as e:
            self.log.error(f"Error verificando carga en SQLite: {e}")

    def resumen(self):
        print("\nResumen de carga:")
        for r in self.reportes:
            print("-", r)
