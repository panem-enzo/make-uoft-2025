import cv2
import numpy as np
import urllib.request
import cvlib as cv
from cvlib.object_detection import draw_bbox
import threading

# Replace with ESP32's actual IP
ESP32_IP = '172.20.10.10'
url = f'http://{ESP32_IP}:81/stream'

def fetch_frame():
    """Fetch a frame from the ESP32 camera stream."""
    try:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        return cv2.imdecode(imgnp, -1)
    except Exception as e:
        print("Error fetching frame:", e)
        return None

def live_feed():
    """Display live camera feed."""
    cv2.namedWindow("Live Transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        im = fetch_frame()
        if im is not None:
            cv2.imshow('Live Transmission', im)

        key = cv2.waitKey(5)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def object_detection():
    """Run object detection on live stream."""
    cv2.namedWindow("Object Detection", cv2.WINDOW_AUTOSIZE)
    while True:
        im = fetch_frame()
        if im is not None:
            bbox, label, conf = cv.detect_common_objects(im)
            im = draw_bbox(im, bbox, label, conf)
            cv2.imshow('Object Detection', im)

        key = cv2.waitKey(5)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Starting video stream...")

    # Run live feed and object detection in separate threads
    thread1 = threading.Thread(target=live_feed)
    thread2 = threading.Thread(target=object_detection)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
