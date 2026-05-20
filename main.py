import cv2
import mediapipe as mp
import math
import time
import winsound

# Face 
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Distancia
def distancia(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

# Cámara
cap = cv2.VideoCapture(0)

ojos_cerrados_inicio = None
TIEMPO_LIMITE = 2

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultados = face_mesh.process(rgb)

    if resultados.multi_face_landmarks:

        for rostro in resultados.multi_face_landmarks:

            puntos = rostro.landmark

            # Ojo izquierdo
            arriba_izq = puntos[159]
            abajo_izq = puntos[145]

            # Ojo derecho
            arriba_der = puntos[386]
            abajo_der = puntos[374]

            # Distancias
            dist_izq = distancia(arriba_izq, abajo_izq)
            dist_der = distancia(arriba_der, abajo_der)

            promedio = (dist_izq + dist_der) / 2

            cv2.putText(
                frame,
                f"Apertura ojos: {promedio:.3f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Detectar sueño para el conductor

            if promedio < 0.015:

                if ojos_cerrados_inicio is None:
                    ojos_cerrados_inicio = time.time()  # inicios del cronometro

                tiempo = time.time() - ojos_cerrados_inicio # cañcuñla el tiempo transcurridos

                cv2.putText(
                    frame,
                    "Abre los hojos",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )
       # si pasa el limite  de dos segundos envai unaalerta
                if tiempo >= TIEMPO_LIMITE:

                    cv2.putText(
                        frame,
                        "ALERTAAA!!!",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        4
                    )

                    winsound.Beep(1000, 1000)

            else:
                ojos_cerrados_inicio = None

    cv2.imshow("Sistema Anti-Sueno", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()