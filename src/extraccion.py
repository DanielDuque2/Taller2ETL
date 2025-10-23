import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
from logs import Logs

class Extraccion:
    def __init__(self, url, database_name):
        self.url = url
        self.database_name = database_name
        self.client = None
        self.db = None
        self.log = Logs("extraccion")

    def conectar(self):
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[self.database_name]
            self.log.info(f"Conexión exitosa a la BD: {self.database_name}")
        except Exception as e:
            self.log.error(f"Error al conectar con BD: {e}")

    def obtener_datos(self, coleccion):
        try:
            datos = list(self.db[coleccion].find())
            df = pd.DataFrame(datos)
            self.log.info(f"Datos extraídos de '{coleccion}': {len(df)} registros")
            return df
        except Exception as e:
            self.log.error(f"Error al obtener datos de '{coleccion}': {e}")
            return None