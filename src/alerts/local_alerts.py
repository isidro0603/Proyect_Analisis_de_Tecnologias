import os
import sys
import subprocess
from config import settings

# Intentar cargar winsound solo si es Windows
if sys.platform == "win32":
    try:
        import winsound
    except ImportError:
        winsound = None
else:
    winsound = None


def lanzar_alerta_sonora():
    """Respuesta local inmediata. Reproduce alarma.mp3 de forma multiplataforma."""
    print("¡¡¡ALERTA DE FATIGA DETECTADA!!!")

    # Construir la ruta absoluta hacia src/alerts/alarma.mp3
    ruta_alerta = os.path.dirname(os.path.abspath(__file__))
    ruta_mp3 = os.path.join(ruta_alerta, "alarma.mp3")

    if sys.platform == "win32":
        # En Windows reproducimos el MP3 usando la interfaz del sistema
        # Si falla, cae al Beep tradicional como respaldo
        try:
            os.startfile(ruta_mp3)
        except Exception:
            if winsound:
                winsound.Beep(settings.FRECUENCIA_BEEP, settings.DURACION_BEEP)
    else:
        # En Linux usamos mpg123 para reproducir el MP3 en segundo plano
        # El argumento '-q' es para modo silencioso (no llena la terminal de texto)
        try:
            subprocess.Popen(["mpg123", "-q", ruta_mp3])
        except FileNotFoundError:
            # Respaldo si no está instalado mpg123: pitido de la terminal
            sys.stdout.write('\x07')
            sys.stdout.flush()