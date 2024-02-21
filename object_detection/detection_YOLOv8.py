import cv2
import argparse
import numpy as np
from ultralytics import YOLO
import supervision as sv

width = 1920
height = 1080
center_width = width // 2
center_height = height // 2
shift_center = 300 // 2


# Definizione dei vertici per i quattro triangoli isosceli
ZONE_POLYGON_UP = np.array([
    [0, 0],
    [width, 0],
    [center_width+shift_center, center_height-shift_center],
    [center_width-shift_center, center_height-shift_center]
])

ZONE_POLYGON_RT = np.array([
    [width, 0],
    [width, height],
    [center_width+shift_center, center_height+shift_center],
    [center_width+shift_center, center_height-shift_center]
])

ZONE_POLYGON_DN = np.array([
    [width, height],
    [0, height],
    [center_width-shift_center, center_height+shift_center],
    [center_width+shift_center, center_height+shift_center]
])

ZONE_POLYGON_LT = np.array([
    [0, height],
    [0, 0],
    [center_width-shift_center, center_height-shift_center],
    [center_width-shift_center, center_height+shift_center]
])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", nargs=2, default=[width, height], type=int
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

    zones = [
        sv.PolygonZone(polygon=ZONE_POLYGON_UP,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_RT,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_DN,
                       frame_resolution_wh=tuple(args.webcam_resolution)),
        sv.PolygonZone(polygon=ZONE_POLYGON_LT,
                       frame_resolution_wh=tuple(args.webcam_resolution))
    ]

    zone_annotators = [
        sv.PolygonZoneAnnotator(
            zone=zone, color=sv.Color.RED, thickness=2, text_thickness=4, text_scale=2)
        for zone in zones
    ]
    # TODO ottenere il numero di macchine nelle varie zone per poi mandarlo al server
    while True:
        ret, frame = capture.read()

        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.class_id == 76]
        print(detections)

        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, _, _
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame, detections=detections, labels=labels)

        for i, zone in enumerate(zones):
            zone.trigger(detections=detections)
            frame = zone_annotators[i].annotate(scene=frame)

        cv2.imshow("yolov8", frame)

        if cv2.waitKey(30) == 27:
            break


if __name__ == "__main__":
    main()
