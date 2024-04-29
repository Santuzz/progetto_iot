import cv2
import argparse
import numpy as np
from ultralytics import YOLO
import supervision as sv
from mqtt_client import MQTTClient
import copy

width = 1920
height = 1080
center_width = width // 2
center_height = height // 2
shift_center = 300 // 2


# Definizione dei vertici per i quattro trapezi
# TODO ridefinire le zone in base alla posizione della cam


ZONE_POLYGON_UPR = np.array([
    [center_width-shift_center, 0],
    [width//2, 0],
    [width//2, center_height-shift_center],
    [center_width-shift_center, center_height-shift_center]
])
ZONE_POLYGON_UPL = np.array([
    [width//2, 0],
    [center_width+shift_center, 0],
    [center_width+shift_center, center_height-shift_center],
    [width//2, center_height-shift_center]
])

ZONE_POLYGON_RTU = np.array([
    [width, center_height-shift_center],
    [width, height//2],
    [center_width+shift_center, height//2],
    [center_width+shift_center, center_height-shift_center]
])

ZONE_POLYGON_RTD = np.array([
    [width, height//2],
    [width, center_height+shift_center],
    [center_width+shift_center, center_height+shift_center],
    [center_width+shift_center, height//2]
])

ZONE_POLYGON_DNR = np.array([
    [center_width+shift_center, height],
    [width//2, height],
    [width//2, center_height+shift_center],
    [center_width+shift_center, center_height+shift_center]
])

ZONE_POLYGON_DNL = np.array([
    [width//2, height],
    [center_width-shift_center, height],
    [center_width-shift_center, center_height+shift_center],
    [width//2, center_height+shift_center]
])

ZONE_POLYGON_LTU = np.array([
    [0, center_height+shift_center],
    [0, height//2],
    [center_width-shift_center, height//2],
    [center_width-shift_center, center_height+shift_center]
])

ZONE_POLYGON_LTD = np.array([
    [0, height//2],
    [0, center_height-shift_center],
    [center_width-shift_center, center_height-shift_center],
    [center_width-shift_center, height//2]
])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", nargs=2, default=[width, height], type=int
    )
    args = parser.parse_args()
    return args

# TODO creare altre quattro zone per identificare quante auto ci sono in ogni strada dopo che hanno attraversato l'incrocio,
#       questo dato ci serve da mandare al server per fare in modo che possa avvisare l'incrocio adiacente nel caso in cui le auto che vadano in una via siano elevate
#   Le zone in questioni dovranno storare il dato delle auto passate per un determinato lasso di tempo, in questo modo si capisce quante sono le auto complessive che hanno preso una determinata strada in un certo lasso di tempo


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zones = [

        sv.PolygonZone(polygon=ZONE_POLYGON_UPR,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_UPL,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_RTU,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_RTD,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_DNR,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_DNL,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_LTU,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_LTD,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
    ]

    zone_annotators = [
        sv.PolygonZoneAnnotator(
            zone=zone, color=sv.Color.RED, thickness=2, text_thickness=4, text_scale=2)
        for zone in zones
    ]

    cars_in_update = [0]*(len(zones)//2)
    cars_out_update = [0]*(len(zones)//2)
    client = MQTTClient()  # create new instance of camera
    client.connect()
    print('\n')
    client.subscribe("data_camera")

    # TODO ottenere il numero di macchine nelle varie zone per poi mandarlo al server.
    # Allo stesso tempo il count deve essere disponibile al bridge dell'arduino con il semaforo
    try:
        while True:
            ret, frame = capture.read()

            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            # riconoscimento delle sole auto (detections.class_id==2)
            detections = detections[detections.class_id == 2]

            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _, _
                in detections
            ]

            frame = box_annotator.annotate(
                scene=frame, detections=detections, labels=labels)
            cars_in = [0]*(len(zones)//2)
            cars_out = [0]*(len(zones)//2)
            for i, zone in enumerate(zones):
                if i % 2 == 0:
                    cars_in[i//2] = zone.current_count
                else:
                    cars_out[i//2] = zone.current_count
                zone.trigger(detections=detections)
                frame = zone_annotators[i].annotate(scene=frame)

            cv2.imshow("yolov8", frame)

            if cv2.waitKey(30) == 27:
                break

            print(cars_in)
            print(cars_out)

            if (np.array_equal(cars_in, cars_in_update) == False):
                client.publish("data_camera_in", cars_in)
                cars_in_update = copy.deepcopy(cars_in)

            # TODO sostituire comunicazione MQTT con HTTP per comunicare al server l'array di macchine in uscita dall'incrocio

            if (np.array_equal(cars_out, cars_out_update) == False):
                client.publish("data_camera_out", cars_out)
                cars_out_update = copy.deepcopy(cars_out)

    except (KeyboardInterrupt):
        print()
        print("Loop interrupted")
        client.disconnect()
        exit(1)


if __name__ == "__main__":
    main()
