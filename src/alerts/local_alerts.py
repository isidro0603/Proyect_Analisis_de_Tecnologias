import winsound
from config import settings

def lanzar_alerta_sonora():

    print("¡¡¡ALERTA DE FATIGA DETECTADA!!!")

    winsound.Beep(
        settings.FRECUENCIA_BEEP,
        settings.DURACION_BEEP
    )