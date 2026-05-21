import cv2
import time
from config import settings
from src.hardware.camera import LaptopCamera
from src.core.detector import FaceAnalyzer
from src.core.geometry import calcular_distancia
from src.alerts.local_alerts import lanzar_alerta_sonora

# Inicialización de componentes
camara = LaptopCamera(device_index=0)
analyzer = FaceAnalyzer()

ojos_cerrados_inicio = None

while True:
    exito, frame = camara.obtain_frame() if hasattr(camara, 'obtain_frame') else camara.obtener_frame()
    if not exito:
        print("Error al obtener el flujo de video.")
        break

    # Procesamiento Analítico (La nueva API prefiere BGR directamente o el formato convertido internamente)
    resultados = analyzer.procesar_frame(frame)

    # NUEVA ESTRUCTURA: Verificar si se detectaron rostros
    if resultados and resultados.face_landmarks:

        # Iteramos sobre los rostros detectados (usualmente 1 por tu configuración)
        for rostro_landmarks in resultados.face_landmarks:

            # En la nueva API, 'rostro_landmarks' ya es la lista de puntos (puntos[159], etc.)
            # Ojo izquierdo
            arriba_izq = rostro_landmarks[159]
            abajo_izq = rostro_landmarks[145]

            # Ojo derecho
            arriba_der = rostro_landmarks[386]
            abajo_der = rostro_landmarks[374]

            # Cálculos geométricos
            dist_izq = calcular_distancia(arriba_izq, abajo_izq)
            dist_der = calcular_distancia(arriba_der, abajo_der)
            promedio = (dist_izq + dist_der) / 2

            # Desplegar información en el frame
            cv2.putText(
                frame,
                f"Apertura ojos: {promedio:.3f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Lógica de Alertas e Incidentes (Mitigación de Riesgos)
            if promedio < settings.UMBRAL_APERTURA_OJOS:
                if ojos_cerrados_inicio is None:
                    ojos_cerrados_inicio = time.time()  # Inicia el cronómetro

                # Calculamos el tiempo transcurrido en CADA frame mientras los ojos sigan cerrados
                tiempo_transcurrido = time.time() - ojos_cerrados_inicio

                # Alerta visual preventiva + Contador de segundos
                cv2.putText(
                    frame,
                    f"Abre los ojos! ({tiempo_transcurrido:.1f}s)",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                # Si supera el umbral crítico (ej. 2 segundos), se dispara la respuesta operativa
                if tiempo_transcurrido >= settings.TIEMPO_LIMITE_ALERTA:
                    cv2.putText(
                        frame,
                        "ALERTA CRITICA!!!",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        4
                    )
                    lanzar_alerta_sonora()
            else:
                # Si abres los ojos, el cronómetro se reinicia a cero inmediatamente
                ojos_cerrados_inicio = None

    # Interfaz de usuario (UI)
    cv2.imshow("Sistema Anti-Sueno - Control Operativo", frame)

    # Tecla ESC para salir
    if cv2.waitKey(1) == 27:
        break

# Cierre limpio del sistema
camara.liberar()
cv2.destroyAllWindows()