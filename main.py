import cv2
import time
from config import settings
from src.hardware.camera import LaptopCamera  # <- Importamos tu nuevo módulo
from src.core.detector import FaceAnalyzer
from src.core.geometry import calcular_distancia
from src.alerts.local_alerts import lanzar_alerta_sonora

# Inicialización de componentes (Tu infraestructura Edge)
camara = LaptopCamera(device_index=0)
analyzer = FaceAnalyzer()

ojos_cerrados_inicio = None

while True:
    # Captura desde el módulo de hardware
    exito, frame = camara.obtener_frame()
    if not exito:
        print("Error al obtener el flujo de video.")
        break

    # Procesamiento Analítico (IA)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = analyzer.procesar_frame(rgb)

    if resultados.multi_face_landmarks:
        for rostro in resultados.multi_face_landmarks:
            puntos = rostro.landmark

            # Cálculos geométricos
            dist_izq = calcular_distancia(puntos[159], puntos[145])
            dist_der = calcular_distancia(puntos[386], puntos[374])
            promedio = (dist_izq + dist_der) / 2

            # Lógica de Alertas e Incidentes
            if promedio < settings.UMBRAL_APERTURA_OJOS:
                if ojos_cerrados_inicio is None:
                    ojos_cerrados_inicio = time.time()

                tiempo_transcurrido = time.time() - ojos_cerrados_inicio

                if tiempo_transcurrido >= settings.TIEMPO_LIMITE_ALERTA:
                    lanzar_alerta_sonora()
            else:
                ojos_cerrados_inicio = None

    # Interfaz de usuario (UI)
    cv2.imshow("Sistema Anti-Sueno - Control Operativo", frame)

    # Tecla ESC para salir
    if cv2.waitKey(1) == 27:
        break

# Cierre limpio del sistema
camara.liberar()
cv2.destroyAllWindows()