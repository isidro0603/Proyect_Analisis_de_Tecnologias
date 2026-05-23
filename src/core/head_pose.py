def detectar_cabeza_inclinada(
    nariz,
    ojo_izq,
    ojo_der,
    umbral=0.05
):

    # Promedio vertical de ojos
    promedio_ojos_y = (
        ojo_izq.y + ojo_der.y
    ) / 2

    # Distancia vertical nariz-ojos
    diferencia = nariz.y - promedio_ojos_y

    # Si baja demasiado -> cabeza inclinada
    if diferencia > umbral:
        return True

    return False