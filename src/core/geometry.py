import math

def calcular_distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos de MediaPipe."""
    return math.hypot(p2.x - p1.x, p2.y - p1.y)