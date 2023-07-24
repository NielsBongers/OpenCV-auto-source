import os

os.environ["OPENCV_LOG_LEVEL"] = "FATAL"
import cv2
import numpy as np


class checkWebcam:
    def __init__(self):
        self.ATTEMPT_RESOLUTION = 10000
        self.MAX_SOURCE_COUNT = 10
        self.source_results = []

    def check_webcams(self):
        for source_id in range(0, self.MAX_SOURCE_COUNT):
            check_results = {}

            cap = cv2.VideoCapture(source_id)
            webcam_active = cap.isOpened()

            check_results["id"] = source_id
            check_results["active"] = webcam_active

            if webcam_active:
                success_opening = True
                try:
                    success_opening, img0 = cap.read()
                    check_results["opens"] = success_opening
                    if success_opening:
                        max_value = np.max(img0[:, :, 0])
                        min_value = np.min(img0[:, :, 0])

                        uniform_color = min_value == max_value

                        check_results["uniform color"] = uniform_color

                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ATTEMPT_RESOLUTION)
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.ATTEMPT_RESOLUTION)

                        source_height, source_width = int(
                            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                        ), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

                        check_results["height"] = source_height
                        check_results["width"] = source_width
                        check_results["exception"] = False

                except Exception as e:
                    received_exception = True
                    check_results["exception"] = e

            try:
                cap.release()
            except Exception as e:
                print(f"Failed to release webcam, {e}")

            self.source_results.append(check_results)

        return self.source_results

    def rank_sources(self):
        self.check_webcams()

        maximum_rating = -1
        best_source = ""

        for source in self.source_results:
            rating = 0

            if source["active"] and source["opens"]:
                if not source["uniform color"]:
                    rating = source["height"] * source["width"]
                else:
                    rating = 1

            if rating >= maximum_rating:
                best_source = source
                maximum_rating = rating

        return best_source

    def get_best_source(self):
        best_source = self.rank_sources()

        cap = cv2.VideoCapture(best_source["id"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, best_source["height"])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, best_source["width"])

        return cap


if __name__ == "__main__":
    stuff = checkWebcam()
    cap = stuff.get_best_source()
    ret, img0 = cap.read()

    cv2.imshow("Image", img0)
    cv2.waitKey(0)
