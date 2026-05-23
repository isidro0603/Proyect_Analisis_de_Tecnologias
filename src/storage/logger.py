import csv
import os

from datetime import datetime

CARPETA = "data"

ARCHIVO = os.path.join(
    CARPETA,
    "incidentes.csv"
)

def inicializar_csv():

    os.makedirs(
        CARPETA,
        exist_ok=True
    )

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
                "evento",
                "duracion"
            ])

def guardar_incidente(
    evento,
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
            evento,
            round(duracion, 2)
        ])