import cv2
import time

from config import settings

from src.hardware.camera import LaptopCamera

from src.core.detector import FaceAnalyzer
from src.core.geometry import calcular_distancia
from src.core.fatigue_logic import FatigueMonitor

from src.alerts.local_alerts import lanzar_alerta_sonora


from src.storage.logger import (
    inicializar_csv,
    guardar_incidente
)

from src.ui.overlay import (
    dibujar_estado,
    dibujar_alertas,
    dibujar_barra
)

# =========================================
# Inicialización
# =========================================

camara = LaptopCamera(device_index=0)

analyzer = FaceAnalyzer()

monitor = FatigueMonitor(
    settings.UMBRAL_APERTURA_OJOS,
    settings.TIEMPO_LIMITE_ALERTA
)

# Crear CSV automáticamente
inicializar_csv()


ultimo_sonido = 0

ultimo_guardado = 0

TIEMPO_ENTRE_SONIDOS = 3

TIEMPO_ENTRE_GUARDADOS = 5

# =========================================
# Bucle principal
# =========================================

while True:

    exito, frame = camara.obtener_frame()

    if not exito:
        print("Error al obtener video.")
        break

    resultados = analyzer.procesar_frame(frame)

    estado = "NORMAL"
    tiempo = 0

    # =========================================
    # Detección facial
    # =========================================

    if resultados and resultados.face_landmarks:

        for rostro_landmarks in resultados.face_landmarks:

            # ---------------------------------
            # Ojo izquierdo
            # ---------------------------------

            arriba_izq = rostro_landmarks[159]
            abajo_izq = rostro_landmarks[145]

            # ---------------------------------
            # Ojo derecho
            # ---------------------------------

            arriba_der = rostro_landmarks[386]
            abajo_der = rostro_landmarks[374]

            # ---------------------------------
            # Distancias
            # ---------------------------------

            dist_izq = calcular_distancia(
                arriba_izq,
                abajo_izq
            )

            dist_der = calcular_distancia(
                arriba_der,
                abajo_der
            )

            promedio = (dist_izq + dist_der) / 2

            # =========================================
            # Evaluar fatiga
            # =========================================

            estado, tiempo = monitor.evaluar(
                promedio
            )

            # =========================================
            # Dibujar landmarks
            # =========================================

            h, w, _ = frame.shape

            for punto in rostro_landmarks:

                x = int(punto.x * w)
                y = int(punto.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    1,
                    (255, 255, 255),
                    -1
                )

            # =========================================
            # Mostrar apertura de ojos
            # =========================================

            cv2.putText(
                frame,
                f"Apertura: {promedio:.3f}",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,255),
                2
            )

            # =========================================
            # ALERTA CRÍTICA
            # =========================================

            if estado == "CRITICO":

                tiempo_actual = time.time()

                # SONIDO CONTROLADO
                if (
                        tiempo_actual - ultimo_sonido
                        > TIEMPO_ENTRE_SONIDOS
                ):
                    lanzar_alerta_sonora()

                    ultimo_sonido = tiempo_actual

                # ALERTAS CONTROLADAS
                if (
                        tiempo_actual - ultimo_guardado
                        > TIEMPO_ENTRE_GUARDADOS
                ):
                    monitor.incrementar_alerta()

                    guardar_incidente(
                        estado,
                        tiempo
                    )

                    ultimo_guardado = tiempo_actual

    # =========================================
    # Interfaz visual
    # =========================================

    dibujar_estado(
        frame,
        estado
    )

    dibujar_alertas(
        frame,
        monitor.total_alertas
    )

    # Barra de fatiga
    nivel = min(
        tiempo / settings.TIEMPO_LIMITE_ALERTA,
        1
    )

    dibujar_barra(
        frame,
        nivel
    )

    # =========================================
    # Mostrar ventana
    # =========================================

    cv2.imshow(
        "Sistema Inteligente de Fatiga",
        frame
    )

    # ESC para salir
    if cv2.waitKey(1) == 27:
        break

# =========================================
# Cierre limpio
# =========================================

camara.liberar()

cv2.destroyAllWindows()