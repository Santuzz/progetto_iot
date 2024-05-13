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
    traffic_level = 0  # plus_time nel bridge
    traffic_cross = {}
    for rel in related_street_crossroads:
        # per ogni crossroad trovata dalle relazioni trovo le sue street
        streets_linked_to_crossroad = Street.objects.filter(
            streetcrossroad__crossroad__name=rel.crossroad).distinct()
        # Trovo tutte le relazioni che hanno le street di un crossroad escudendo quelle con il crossroad stesso
        street_crossroads_excluding_initial = StreetCrossroad.objects.filter(
            street__in=streets_linked_to_crossroad).exclude(crossroad__name=rel.crossroad)
        for rel_s in street_crossroads_excluding_initial:
            # Per ogni street delle relazioni vado a prendere la relazione che ha con il crossroad che ci interessa, in questo modo capisco se il valore di cars delle street trovate va aggiunto oppure sottratto
            rel_original = StreetCrossroad.objects.get(street=rel_s.street, crossroad=rel.crossroad)
            if rel_original.index % 2 == 0:
                traffic_level += rel_s.cars
            else:
                traffic_level -= rel_s.cars

        result = traffic_level*read_increment()
        rel.crossroad.traffic_level = result
        rel.crossroad.last_send = now()
        rel.crossroad.save()
        traffic_cross[rel.crossroad.name] = traffic_level
        traffic_level = 0
    # ritorno tutti gli incroci che hanno cambiato il proprio traffic_level per via del cambiamento del numero di macchine nella relazione SC iniziale
    return traffic_cross


@ receiver(post_save, sender=StreetCrossroad)
def handle_cars_update(sender, instance, created, **kwargs):
    if not created:  # Questo garantisce che il segnale reagisca solo agli aggiornamenti, non alla creazione
        # Esegui il calcolo solo se 'cars' è cambiato
        traffic_cross = traffic_update(instance)
        print("Crossroad changed: "+str(traffic_cross))

        # tramite MQTT invio ad ogni incrocio ritornato il valore aggiornato del traffic_level
        for crossroad, traffic_level in traffic_cross.items():
            publish_message(crossroad, str(10*traffic_level))
            # publish_message(crossroad, str(traffic_level))
