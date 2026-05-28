import time
from src.alerts.local_alerts import registrar_alerta_en_memoria


class FatigueMonitor:

    def __init__(self, umbral, tiempo_limite):
        self.umbral = umbral
        self.tiempo_limite = tiempo_limite
        self.ojos_cerrados_inicio = None
        self.total_alertas = 0

        self.alerta_disparada = False

    def evaluar(self, promedio):
        estado = "NORMAL"
        tiempo = 0

        if promedio < self.umbral:
            if self.ojos_cerrados_inicio is None:
                self.ojos_cerrados_inicio = time.time()

            tiempo = time.time() - self.ojos_cerrados_inicio

            if tiempo >= self.tiempo_limite:
                estado = "CRITICO"

                if not self.alerta_disparada:
                    self.incrementar_alerta()
                    registrar_alerta_en_memoria(tiempo)
                    self.alerta_disparada = True
            else:
                estado = "ADVERTENCIA"

        else:
            self.ojos_cerrados_inicio = None
            self.alerta_disparada = False

        return estado, tiempo

    def incrementar_alerta(self):
        self.total_alertas += 1