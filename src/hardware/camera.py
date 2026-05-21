import cv2

class LaptopCamera:
    def __init__(self, device_index=0):
        """
        Inicializa la cámara de la laptop.
        device_index=0 usualmente apunta a la cámara integrada.
        """
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            raise RuntimeError("No se pudo acceder a la cámara de la laptop.")

    def obtener_frame(self):
        """
        Captura un frame, lo voltea para el efecto espejo y lo retorna.
        """
        ret, frame = self.cap.read()
        if not ret:
            return False, None

        # Efecto espejo (común para monitoreo en cabina/escritorio)
        frame = cv2.flip(frame, 1)
        return True, frame

    def liberar(self):
        """Libera el recurso de la cámara al cerrar el sistema."""
        self.cap.release()