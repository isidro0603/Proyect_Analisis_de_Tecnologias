# Configuración del modelo del proyecto
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Umbrales de riesgo (Segun Evidencia científica)
UMBRAL_APERTURA_OJOS = 0.015
TIEMPO_LIMITE_ALERTA = 1.7  # segundos, probar intervalos


# Frecuencia de alertas Alertas
FRECUENCIA_BEEP = 1000  # Hz
DURACION_BEEP = 1000    # ms


SERVIDOR_IP = "localhost"
PUERTO = "5000"
URL_API = f"http://{SERVIDOR_IP}:{PUERTO}/api/incidentes" #cambiar la ip y servidor segun la red