import subprocess

tests = [
    # Creazione di una nuova crossroad
    "python REST_communication.py --model crossroad --method create --name 'NomeIncrocioSS' --lat 40.7128 --lon -74.0060 --traffic 0.8 --active 'true'",
    # Ottenere informazioni su una crossroad tramite nome
    "python REST_communication.py --model crossroad --method get --name 'NomeIncrocio'",
    # Aggiornare una crossroad esistente tramite nome
    "python REST_communication.py --model crossroad --method update --name 'NomeIncrocio' --lat 43.7128 --lon -74.0060 --traffic 0.9 --active 'false'",

    # Creazione di una nuova webcam
    "python REST_communication.py --model webcam --method create --crossroad 'NomeIncrocioss' --cars '10,1,2' --active 'true'",
    # Ottenere informazioni su una webcam tramite ID
    "python REST_communication.py --model webcam --method get ",
    # Aggiornare una webcam esistente tramite ID
    "python REST_communication.py --model webcam --method update --id 13 --crossroad 'NomeIncrocio' --cars '22,33,4,2' --active 'false'",

    # Creazione di una nuova strada
    "python REST_communication.py --model street --method create --name 'NomeStradaSS' --length 100 --alert 'true'",
    # Ottenere informazioni su una strada tramite nome
    "python REST_communication.py --model street --method get --name 'NomeStradaSS'",
    # Aggiornare una strada esistente tramite nome
    "python REST_communication.py --model street --method update --name 'NomeStradaSS' --crossroad 'NomeIncrocioSS' --length 300 --alert 'false'",

    # Creazione di un nuovo semaforo stradale
    "python REST_communication.py --model trafficlight --method create --crossroad 'NomeIncrocioss' --direction 'LS' --green 0.7 --street 'NomeStradass'",
    # Ottenere informazioni su un semaforo stradale tramite ID
    "python REST_communication.py --model trafficlight --method get --id 1",
    # Aggiornare un semaforo stradale esistente tramite ID
    "python REST_communication.py --model trafficlight --method update --id 1 --crossroad 'NomeIncrocioSS' --direction 'R' --green 0.8 --street 'NomeStradaSS'",
]

delete_test = [
    # Eliminare un crossroad tramite nome
    "python REST_communication.py --model crossroad --method delete --name 'NomeIncrocio'",
    # Eliminare una webcam tramite ID
    "python REST_communication.py --model webcam --method delete --id 7",
    # Eliminare una strada tramite nome
    "python REST_communication.py --model street --method delete --name 'NomeStrada'",
    # Eliminare un semaforo stradale tramite ID
    "python REST_communication.py --model trafficlight --method delete --id 1"

]

for test in tests:
    subprocess.run(test, shell=True)
