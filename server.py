# server.py (Modificado para recibir ráfagas de datos al final)
from flask import Flask, request, jsonify
import csv
import os
import time

app = Flask(__name__)

DATA_DIR = "data"
timestamp_inicio = time.strftime("%Y%m%d_%H%M%S")
CSV_PATH = os.path.join(DATA_DIR, f"incidentes_{timestamp_inicio}.csv")

os.makedirs(DATA_DIR, exist_ok=True)
with open(CSV_PATH, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["vehiculo_id", "fecha_hora", "evento", "duracion_segundos"])

print(f"🚀 Servidor listo esperando el cierre de tu programa en: {CSV_PATH}")


@app.route('/api/incidentes', methods=['POST'])
def recibir_incidentes_masivos():
    lista_alertas = request.json

    if not lista_alertas:
        return jsonify({"status": "No se enviaron datos"}), 400

    with open(CSV_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        for alerta in lista_alertas:
            writer.writerow([
                alerta['vehiculo_id'],
                alerta['fecha_hora'],
                alerta['evento'],
                alerta['duracion_segundos']
            ])

    print(f"📥 ¡Datos guardados! Se escribieron {len(lista_alertas)} filas en el CSV.")
    return jsonify({"status": f"Se guardaron {len(lista_alertas)} registros"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)