from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import sys
from django.utils.timezone import now
from mqtt_integration.MQTT_client import MQTT_client
import time

try:
    from config import read_increment
except ImportError:
    sys.path.append('..')
    from config import read_increment, read_mqtt


def publish_message(crossroad, message):
    topic = "data_traffic/" + crossroad.replace(" ", "_")
    client = MQTT_client("django")
    client.start(topic)
    client.publish(message)
    time.sleep(1)
    client.stop()


def traffic_update(instance):
    # Ottengo tutte le relazioni SC della street presente nella relazione SC che ha cambiato valore
    related_street_crossroads = StreetCrossroad.objects.filter(
        street=instance.street).exclude(crossroad=instance.crossroad)
    plus_time = 0  # plus_time nel bridge
    traffic_cross = {}
    road_o = 0
    road_v = 0
    for rel in related_street_crossroads:
        # per ogni crossroad trovata dalle relazioni trovo le sue street
        streets_linked_to_crossroad = Street.objects.filter(
            streetcrossroad__crossroad__name=rel.crossroad).distinct()
        # Trovo tutte le relazioni che hanno le street di un crossroad escudendo quelle con il crossroad stesso
        street_crossroads_excluding_initial = StreetCrossroad.objects.filter(
            street__in=streets_linked_to_crossroad).exclude(crossroad__name=rel.crossroad)
        for rel_s in street_crossroads_excluding_initial:
            # Per ogni street delle relazioni vado a prendere la relazione che ha con il crossroad che ci interessa,
            # in questo modo capisco se il valore di cars delle street trovate va aggiunto oppure sottratto
            rel_original = StreetCrossroad.objects.get(street=rel_s.street, crossroad=rel.crossroad)
            if rel_original.index % 2 == 0:
                road_v += rel_s.cars
            else:
                road_o += rel_s.cars
        if road_o == 0 and road_v == 0:
            plus_time = 0
        elif road_v-road_o > 0:
            if road_v-road_o < 4:
                plus_time = 1
            elif road_v-road_o < 8:
                plus_time = 2
            else:
                plus_time = 3
        else:
            if road_v-road_o > -4:
                plus_time = -1
            elif road_v-road_o > -8:
                plus_time = -2
            else:
                plus_time = -3
        result = plus_time*read_increment()
        rel.crossroad.plus_time = result
        rel.crossroad.last_send = now()
        rel.crossroad.save()
        traffic_cross[rel.crossroad.name] = plus_time
        plus_time = 0
    # ritorno tutti gli incroci che hanno cambiato il proprio traffic_level
    # per via del cambiamento del numero di macchine nella relazione SC iniziale
    return traffic_cross


@ receiver(post_save, sender=StreetCrossroad)
def handle_cars_update(sender, instance, created, **kwargs):
    if not created:  # Questo garantisce che il segnale reagisca solo agli aggiornamenti, non alla creazione
        # Esegui il calcolo solo se 'cars' è cambiato
        traffic_cross = traffic_update(instance)
        print("Crossroad changed: "+str(traffic_cross))

        # tramite MQTT invio ad ogni incrocio ritornato il valore aggiornato del traffic_level
        for crossroad, plus_time in traffic_cross.items():
            publish_message(crossroad, str(plus_time))
            # publish_message(crossroad, str(traffic_level))
