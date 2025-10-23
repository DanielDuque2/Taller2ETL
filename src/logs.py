import os
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

class Logs:
    def __init__(self, nombre_modulo: str, per_execution: bool = False, run_id: Optional[str] = None):
        self.nombre_modulo = nombre_modulo
        self.logs_dir = Path("../logs")
        self.logs_dir.mkdir(exist_ok=True)

        # Si se proporciona run_id se usa tal cual (permite sincronizar entre procesos)
        if run_id:
            timestamp = run_id
        else:
            # Si se solicita archivo por ejecución, intentamos reutilizar un timestamp global
            if per_execution:
                # Revisar variable de entorno para run timestamp
                env_key = "LOG_RUN_TIMESTAMP"
                if env_key in os.environ:
                    timestamp = os.environ[env_key]
                else:
                    # Crear timestamp con segundos para minimizar colisiones
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    os.environ[env_key] = timestamp
            else:
                # archivo por módulo (por defecto): incluir segundos para minimizar colisiones
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        if per_execution:
            nombre_archivo = f"log_{timestamp}.log"
        else:
            nombre_archivo = f"log_{timestamp}_{nombre_modulo}.log"

        self.archivo_log = self.logs_dir / nombre_archivo

        # Configurar logger
        self.logger = logging.getLogger(nombre_modulo)
        self.logger.setLevel(logging.DEBUG)

        # limpiamos handlers previos para asegurar que usemos nuestro archivo/format
        self.logger.handlers.clear()
        self.logger.propagate = False

        # Handler para archivo
        file_handler = logging.FileHandler(self.archivo_log, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formato detallado
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Añadir handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Mensaje inicial
        self.info(f"Iniciando ejecución del módulo: {nombre_modulo} (log: {self.archivo_log})")

    def info(self, mensaje: str):
        """Registra un mensaje informativo."""
        self.logger.info(mensaje)

    def warning(self, mensaje: str):
        """Registra una advertencia."""
        self.logger.warning(mensaje)

    def error(self, mensaje: str):
        """Registra un error."""
        self.logger.error(mensaje)

    def debug(self, mensaje: str):
        """Registra un mensaje de debug."""
        self.logger.debug(mensaje)

    def ruta_archivo(self) -> str:
        """Retorna la ruta del archivo de log generado."""
        return str(self.archivo_log)

    def obtener_contenido(self) -> str:
        """Retorna el contenido completo del archivo de log."""
        if self.archivo_log.exists():
            with open(self.archivo_log, 'r', encoding='utf-8') as f:
                return f.read()
        return "Archivo de log no encontrado."
