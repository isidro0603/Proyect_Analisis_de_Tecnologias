import cv2

def dibujar_estado(frame, estado):

    color = (0,200,0)

    if estado == "ADVERTENCIA":
        color = (0,200,255)

    elif estado == "CRITICO":
        color = (0,0,200)

# para cambiara las letra sen 0.7
# en 20 y 40 es para mover texto
# el 1 es el grosor
    cv2.putText(
        frame,
        f"Estado: {estado}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
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

    ancho = int(120 * nivel)

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
        (20 + ancho,140),
        (0,165,255),
        -1
    )