from logging.handlers import RotatingFileHandler
import logging
from pathlib import Path

# Crear directorio de logs si no existe
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "server.log"

LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ColoredFormatter(logging.Formatter):
  """Formatter personalizado con códigos ANSI para la consola."""

  RESET = "\033[0m"
  COLORS = {
      logging.DEBUG: "\033[36m",  # Cian
      logging.INFO: "\033[32m",  # Verde
      logging.WARNING: "\033[33m",  # Amarillo
      logging.ERROR: "\033[31m",  # Rojo
      logging.CRITICAL: "\033[1;31m",  # Rojo Negrita
  }

  def format(self, record: logging.LogRecord) -> str:
    # Seleccionar color por nivel
    color = self.COLORS.get(record.levelno, self.RESET)

    # Formatear fecha en tono gris discreto
    asctime = self.formatTime(record, DATE_FORMAT)
    colored_asctime = f"\033[90m{asctime}\033[0m"

    # Formatear el nivel del log con color
    colored_levelname = f"{color}{record.levelname:<8}{self.RESET}"

    # Formatear el nombre del módulo
    colored_name = f"\033[1;34m[{record.name}]\033[0m"

    # Ensamblar mensaje
    message = record.getMessage()

    # Si hay traceback/excepción, pintarlo en rojo
    if record.exc_info:
      if not record.exc_text:
        record.exc_text = self.formatException(record.exc_info)

    if record.exc_text:
      message = f"{message}\n\033[31m{record.exc_text}\033[0m"

    return f"{colored_asctime} {colored_levelname} {colored_name}: {message}"


def setup_logger(name: str = "HTTPServer") -> logging.Logger:
    """Crea y retorna un logger configurado con consola a color y archivo rotativo."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)   
    # Evitar duplicar handlers si se llama varias veces
    if logger.hasHandlers():
        return logger 
    # 1. Handler para Consola (Pantalla con colores)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)  
    # 2. Handler para Archivo (Limpio sin caracteres ANSI)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler) 
    return logger

logger = setup_logger("HTTP_SERVER")