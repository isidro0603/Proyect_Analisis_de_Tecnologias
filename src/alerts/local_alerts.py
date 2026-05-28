import os
import sys
import requests
import time
from config import settings
from config.settings import URL_API

# Si está en Windows, importa winsound de forma segura
if sys.platform == "win32":
    import winsound

historial_local = []


def lanzar_alerta_sonora():
    print("¡¡¡ALERTA DE FATIGA DETECTADA!!!")

    if sys.platform == "win32":
        winsound.Beep(
            settings.FRECUENCIA_BEEP,
            settings.DURACION_BEEP
        )
    else:
        sys.stdout.write('\a')
        sys.stdout.flush()


def registrar_alerta_en_memoria(duracion_ojos_cerrados):
    evento = {
        "vehiculo_id": "UABC-01",
        "fecha_hora": time.strftime("%Y-%m-%d %H:%M:%S"),
        "evento": "Fatiga detectada",
        "duracion_segundos": round(duracion_ojos_cerrados, 2)
    }
    historial_local.append(evento)
    print(f"📦 Alerta guardada localmente (Total acumulado: {len(historial_local)})")


def enviar_todo_al_servidor():
    if not historial_local:
        print("\n🛑 Saliendo... No se generaron alertas en esta sesión.")
        return

    print(f"\n📡 Enviando {len(historial_local)} incidentes acumulados al servidor...")
    try:
        response = requests.post(URL_API, json=historial_local, timeout=5)
        if response.status_code == 201:
            print("💾 ¡Exito! Todos los datos fueron recibidos y guardados por el servidor.")
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar con el servidor. Los datos no se guardaron.")