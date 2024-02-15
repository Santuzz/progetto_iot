from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static', )


@app.route('/greetings/<recipient>', methods=['GET'])
def hello(recipient):
    return render_template('hello.html', recipient=recipient)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', path=request.path), 404


@app.route('/stored_data', methods=['GET'])
def stored_data():
    data_list = []
    # Leggi il file JSON esistente
    with open('data.json', 'r') as json_file:
        existing_data = json.load(json_file)

    # Estrai la lista di sensori dal dizionario
    sensors = existing_data.get('sensors', [])

    # Aggiungi ogni sensore alla lista data_list
    for sensor in sensors:
        data_list.append(sensor)
    # Qui puoi creare una visualizzazione dei dati salvati
    print(data_list)
    return render_template('stored_data.html', data=data_list)


@app.route('/send_data', methods=['POST'])
def send_data():
    try:
        # Ricevi i dati inviati dall'Arduino come JSON
        data = request.get_json()

        # Leggi il file JSON esistente
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)

        # Estrai la lista esistente dal dizionario
        sensors = existing_data.get('sensors', [])
        sensor_name = data["name"]
        sensor_found = False

        for sensor in sensors:
            if sensor['name'] == sensor_name:
                # Aggiungi il nuovo dato alla lista di dati del sensore
                sensor['data'].insert(0, data['data'])
                sensor_found = True
                break

        # Se il sensore non esiste, crea un nuovo sensore con i dati
        if not sensor_found:
            new_sensor = {
                'name': sensor_name,
                'data': [data['data']]
            }
            sensors.append(new_sensor)
        # Sovrascrivi il file JSON con i dati aggiornati
        with open('data.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        return jsonify({"message": "Dati ricevuti correttamente"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================================
# API Routes
# ============================================================

@app.route('/api/get_data', methods=['GET'])
def api_get_latest_data():
    with open('data.json', 'r') as json_file:
        existing_data = json.load(json_file)
    return jsonify({'data': existing_data})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
