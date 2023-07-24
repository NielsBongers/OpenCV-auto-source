import os

os.environ["OPENCV_LOG_LEVEL"] = "FATAL"
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("opencv_auto_source").addHandler(logging.NullHandler())


class autoSelectSource:
    """A class to check and rank available webcams."""

    def __init__(self, MAX_SOURCE_COUNT=10):
        """Initializes the checkWebcam object with default values.

        Args:
            MAX_SOURCE_COUNT (int, optional): Number of sources to check. More sources means the code takes longer to run. Defaults to 10.
        """
        self.ATTEMPT_RESOLUTION = 10000
        self.MAX_SOURCE_COUNT = MAX_SOURCE_COUNT
        self.source_results = []

    def check_webcams(self) -> list:
        """Checks the availability and quality of each webcam source.

        Returns:
            list: A list of dictionaries containing the results of checking each source.
            Each dictionary has the following keys:
                id: An integer representing the source id.
                active: A boolean indicating whether the source is active or not.
                opens: A boolean indicating whether the source can be opened or not.
                uniform color: A boolean indicating whether the source image has a uniform color or not.
                height: An integer representing the source image height in pixels.
                width: An integer representing the source image width in pixels.
                exception: A boolean or an exception object indicating whether an exception occurred while checking the source or not.
        """
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
                logging.warning(f"Failed to release webcam, {e}")

            self.source_results.append(check_results)

        return self.source_results

    def rank_sources(self) -> dict:
        """Ranks the available webcam sources based on their quality.

        Returns:
            dict: A dictionary containing the best source and its attributes.
        """
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

    def get_best_source(self) -> cv2.VideoCapture:
        """Gets the best webcam source and opens it.

        Returns:
            cv2.VideoCapture: A cv2.VideoCapture object representing the best webcam source.
        """
        best_source = self.rank_sources()

        cap = cv2.VideoCapture(best_source["id"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, best_source["height"])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, best_source["width"])

        return cap


A = autoSelectSource().check_webcams()

print(A)
