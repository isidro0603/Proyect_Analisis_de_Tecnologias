import csv
import os

from datetime import datetime

CARPETA = "data"

ARCHIVO = os.path.join(
    CARPETA,
    "incidentes.csv"
)

def inicializar_csv():

    # Crear carpeta automáticamente
    os.makedirs(CARPETA, exist_ok=True)

    # Crear archivo CSV si no existe
    if not os.path.exists(ARCHIVO):

        with open(
            ARCHIVO,
            mode="w",
            newline=""
        ) as archivo:

            writer = csv.writer(archivo)

            writer.writerow([
                "fecha",
                "hora",
                "estado",
                "duracion"
            ])

def guardar_incidente(
    estado,
    duracion
):

    with open(
        ARCHIVO,
        mode="a",
        newline=""
    ) as archivo:

        writer = csv.writer(archivo)

        ahora = datetime.now()

        writer.writerow([
            ahora.date(),
            ahora.strftime("%H:%M:%S"),
            estado,
            round(duracion, 2)
        ])