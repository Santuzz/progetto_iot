# move to IoTWebsiteREST/djangoproject and run python3 init_db.py


import random
import datetime
from REST.models import Crossroad, Webcam, Trafficlight
import os
import django
import datetime  # Importa il modulo datetime per la gestione delle date

# Configura l'ambiente di Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')
django.setup()


def init_db():
    print("Creazione db")
    # Creare istanze
    crossroad_1 = Crossroad(
        name="incrocio_4", latitude="10.10", longitude="20.20", cars_count="0,1,0,0")
    crossroad_1.save()
    webcam = Webcam(crossroad=crossroad_1)
    webcam.save()

    for i in range(4):
        Trafficlight(
            direction="A",
            green_value=0.5,
            crossroad=crossroad_1
        ).save()


def erase_db():
    # Cancella tutti i dati nei modelli
    print("Cancellazione db")
    Webcam.objects.all().delete()
    Crossroad.objects.all().delete()


if __name__ == 'main':
    print("qua")
    # erase_db()
    # init_db()
