import pandas as pd
from pymongo import MongoClient
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(
    filename="extraccion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Extraccion:
    def __init__(self, url, database_name):
        self.url = url
        self.database_name = database_name
        self.client = None
        self.db = None

    def conectar(self):
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[self.database_name]
            logging.info(f"Conexión establecida con la base de datos: {self.database_name}")
        except Exception as e:
            logging.error(f"Error al conectar con la base de datos: {e}")

    def obtener_datos(self, coleccion):
        try:
            datos = list(self.db[coleccion].find())
            df = pd.DataFrame(datos)
            logging.info(f"Datos extraídos de la colección '{coleccion}': {len(df)} registros")
            return df
        except Exception as e:
            logging.error(f"Error al obtener datos de la colección '{coleccion}': {e}")