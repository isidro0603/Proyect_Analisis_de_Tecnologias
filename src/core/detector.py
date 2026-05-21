import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceAnalyzer:
    def __init__(self):
        # Configurar las opciones del detector de malla facial moderna
        model_path = os.path.join(os.getcwd(), "face_landmarker.task")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"No se encontró el archivo del modelo en: {model_path}. Por favor descárgalo con wget.")

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1
        )
        # Crear el detector
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def procesar_frame(self, frame_bgr):
        # La nueva API procesa directamente imágenes en el formato de MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_bgr)
        resultado = self.detector.detect(mp_image)
        return resultado