import cv2
import time

from config import settings

from src.hardware.camera import LaptopCamera

from src.core.detector import FaceAnalyzer
from src.core.geometry import calcular_distancia
from src.core.fatigue_logic import FatigueMonitor

from src.alerts.local_alerts import (
    lanzar_alerta_sonora,
    enviar_todo_al_servidor  # 📌 1. IMPORTAMOS LA FUNCIÓN DE ENVÍO FINAL
)

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

try:
    while True:

        exito, frame = camara.obtener_frame()

        if not exito:
            print("Error al obtener video.")
            break

        gris = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gris = cv2.equalizeHist(gris)

        gris = cv2.convertScaleAbs(
            gris,
            alpha=1.5,
            beta=30
        )

        frame_nocturno = cv2.cvtColor(
            gris,
            cv2.COLOR_GRAY2BGR
        )

        resultados = analyzer.procesar_frame(
            frame_nocturno
        )

        frame = frame_nocturno

        estado = "NORMAL"
        tiempo = 0

        if resultados and resultados.face_landmarks:

            for rostro_landmarks in resultados.face_landmarks:

                arriba_izq = rostro_landmarks[159]
                abajo_izq = rostro_landmarks[145]

                arriba_der = rostro_landmarks[386]
                abajo_der = rostro_landmarks[374]

                dist_izq = calcular_distancia(
                    arriba_izq,
                    abajo_izq
                )

                dist_der = calcular_distancia(
                    arriba_der,
                    abajo_der
                )

                promedio = (dist_izq + dist_der) / 2

                estado, tiempo = monitor.evaluar(
                    promedio
                )

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

                cv2.putText(
                    frame,
                    f"Apertura: {promedio:.3f}",
                    (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,0),
                    2
                )

                if estado == "CRITICO":

                    tiempo_actual = time.time()

                    if (
                            tiempo_actual - ultimo_sonido
                            > TIEMPO_ENTRE_SONIDOS
                    ):
                        lanzar_alerta_sonora()

                        ultimo_sonido = tiempo_actual

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
        dibujar_estado(
            frame,
            estado
        )

        dibujar_alertas(
            frame,
            monitor.total_alertas
        )

        nivel = min(
            tiempo / settings.TIEMPO_LIMITE_ALERTA,
            1
        )

        dibujar_barra(
            frame,
            nivel
        )

        cv2.imshow(
            "Sistema Inteligente de Fatiga",
            frame
        )

        if cv2.waitKey(1) == 27:
            print("\n🛑 Se presionó ESC. Cerrando sistema...")
            break

except KeyboardInterrupt:
    print("\n🛑 Se detectó Ctrl+C. Deteniendo sistema...")

finally:

    print("🔌 Liberando cámara...")
    camara.liberar()
    cv2.destroyAllWindows()

    enviar_todo_al_servidor()
    print("👋 Programa finalizado con éxito.")