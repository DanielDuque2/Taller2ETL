import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configuración del log
logging.basicConfig(
    filename="transformacion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Transformacion:
    """
    Clase para realizar transformaciones de limpieza y preparación
    de datos sobre los datasets de Airbnb (listings, calendar o reviews).

    Métodos principales:
    ---------------------
    - limpiar_nulos_duplicados()
    - normalizar_precios()
    - convertir_fechas()
    - derivar_variables_fecha()
    - categorizar_precios()
    - expandir_amenities()
    - transformar()
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df_original = df.copy()  # Para registrar diferencias
        self.informes = []  # Registro de transformaciones

    def limpiar_nulos_duplicados(self):
        registros_antes = len(self.df)
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(how='all', inplace=True)
        registros_despues = len(self.df)
        self.informes.append(
            f"Limpieza de nulos y duplicados: {registros_antes} → {registros_despues}"
        )
        logging.info(self.informes[-1])

    def normalizar_precios(self):
        if 'price' in self.df.columns:
            self.df['price'] = (
                self.df['price']
                .astype(str)
                .str.replace(r'[\$,]', '', regex=True)
                .replace('', np.nan)
                .astype(float)
            )
            self.informes.append("Normalización de precios aplicada.")
            logging.info(self.informes[-1])

    def convertir_fechas(self):
        posibles_fechas = [col for col in self.df.columns if 'date' in col.lower()]
        for col in posibles_fechas:
            try:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce').dt.strftime('%Y-%m-%d')
                self.informes.append(f"Columna '{col}' convertida a formato ISO.")
                logging.info(self.informes[-1])
            except Exception as e:
                logging.warning(f"No se pudo convertir la columna '{col}' a fecha: {e}")

    def derivar_variables_fecha(self):
        posibles_fechas = [col for col in self.df.columns if 'date' in col.lower()]
        for col in posibles_fechas:
            try:
                fechas = pd.to_datetime(self.df[col], errors='coerce')
                self.df[f'{col}_year'] = fechas.dt.year
                self.df[f'{col}_month'] = fechas.dt.month
                self.df[f'{col}_day'] = fechas.dt.day
                self.df[f'{col}_quarter'] = fechas.dt.quarter
                self.informes.append(f"Variables derivadas creadas a partir de '{col}'.")
                logging.info(self.informes[-1])
            except Exception as e:
                logging.warning(f"No se pudieron derivar variables desde '{col}': {e}")

    def categorizar_precios(self):
        if 'price' in self.df.columns:
            try:
                self.df['price_category'] = pd.qcut(
                    self.df['price'], q=4, labels=['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto']
                )
                self.informes.append("Categorización de precios creada.")
                logging.info(self.informes[-1])
            except Exception as e:
                logging.warning(f"No se pudo categorizar precios: {e}")

    def expandir_amenities(self):
        if 'amenities' in self.df.columns:
            try:
                self.df['amenities'] = (
                    self.df['amenities']
                    .astype(str)
                    .str.replace(r'[\{\}\"\[\]]', '', regex=True)
                    .str.split(',')
                )
                todas = pd.Series([a.strip() for lista in self.df['amenities'] for a in lista if a.strip()])
                top10 = todas.value_counts().head(10).index
                for amenidad in top10:
                    colname = f"amenity_{amenidad.replace(' ', '_').lower()}"
                    self.df[colname] = self.df['amenities'].apply(lambda x: 1 if amenidad in x else 0)
                self.informes.append("Expansión de 'amenities' realizada (Top 10).")
                logging.info(self.informes[-1])
            except Exception as e:
                logging.warning(f"No se pudo expandir amenities: {e}")

    def transformar(self):
        logging.info("Inicio de transformación del DataFrame.")
        self.limpiar_nulos_duplicados()
        self.normalizar_precios()
        self.convertir_fechas()
        self.derivar_variables_fecha()
        self.categorizar_precios()
        self.expandir_amenities()
        logging.info("Transformación completada.")
        return self.df

    def resumen(self):
        print("\nResumen de transformaciones:")
        for info in self.informes:
            print("-", info)
        print(f"\nTotal de registros finales: {len(self.df)}")
