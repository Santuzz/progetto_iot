import cv2
import argparse

from ultralytics import YOLO
import supervision as sv

import numpy as np

WIDTH = 1920
HEIGHT = 1080
# l'idea è quella di crare un rettangolo per ogni strada in modo da capire quante macchine sono presenti in ogni singola strada che porta all'incrocio
# rettangolo che occupa metà del video
ZONE_POLYGON = np.array([
    [0, 0],
    [WIDTH//2, 0],
    [WIDTH//2, HEIGHT],
    [0, HEIGHT]
])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", nargs=2, default=[WIDTH, HEIGHT], type=int
    )
    args = parser.parse_args()
    return args


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

    zone = sv.PolygonZone(polygon=ZONE_POLYGON,
                          frame_resolution_wh=tuple(args.webcam_resolution))

    # utilizzato per visualizzare nella webcam il numero di oggetti all'interno di ZONE_POLYGON
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color=sv.Color.RED,
        thickness=2,
        text_thickness=4,
        text_scale=2
    )
    while True:
        ret, frame = capture.read()

        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        # cambia la linea sotto per decidere come far riconoscere a YOLO
        # Guarda il file YOLOv8_class_id.py per il class_id dei vari oggetti riconoscibili
        detections = detections[detections.class_id == 76]
        print(detections)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, _, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame, detections=detections, labels=labels)

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()
