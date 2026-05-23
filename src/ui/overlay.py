import cv2

def dibujar_estado(frame, estado):

    color = (0,255,0)

    if estado == "ADVERTENCIA":
        color = (0,255,255)

    elif estado == "CRITICO":
        color = (0,0,255)

    cv2.putText(
        frame,
        f"Estado: {estado}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

def dibujar_alertas(frame, total):

    cv2.putText(
        frame,
        f"Alertas: {total}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,0),
        2
    )

def dibujar_barra(frame, nivel):

    ancho = int(200 * nivel)

    cv2.rectangle(
        frame,
        (20,120),
        (220,150),
        (255,255,255),
        2
    )

    cv2.rectangle(
        frame,
        (20,120),
        (20 + ancho,150),
        (0,0,255),
        -1
    )