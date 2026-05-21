import winsound
from config import settings

def lanzar_alerta_sonora():
    """Respuesta local inmediata ante fatiga severa."""
    winsound.Beep(settings.FRECUENCIA_BEEP, settings.DURACION_BEEP)

def registrar_evento_institucional():
    """Genera activos de información para la posterior analítica masiva (Big Data)."""
    # Aquí añadirías la lógica para guardar en la carpeta data/logs o enviar a una API
    pass