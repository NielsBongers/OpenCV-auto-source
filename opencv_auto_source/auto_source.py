import os

os.environ["OPENCV_LOG_LEVEL"] = "FATAL"
import logging

import cv2
import numpy as np

logging.getLogger("opencv_auto_source").addHandler(logging.NullHandler())


class autoSelectSource:
    """A class to check and rank available webcams."""

    def __init__(self, MAX_SOURCE_COUNT: int = 10):
        """Initializes the checkWebcam object with default values.

        Args:
            MAX_SOURCE_COUNT (int, optional): Number of sources to check. More sources means the code takes longer to run. Defaults to 10.
        """
        self.ATTEMPT_RESOLUTION = 10000
        self.MAX_SOURCE_COUNT = MAX_SOURCE_COUNT
        self.source_results = []
        self.ranking_results = []

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
                    logging.exception(f"Failed to read webcam, {e}")
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

        maximum_rank = -1
        best_source = ""

        for source in self.source_results:
            rank = 0

            if source["active"] and source["opens"]:
                if not source["uniform color"]:
                    rank = source["height"] * source["width"]
                else:
                    rank = 1

            self.ranking_results.append((rank, source))

            if rank >= maximum_rank:
                best_source = source
                maximum_rank = rank

        self.ranking_results.sort(key=lambda rank: rank[0], reverse=True)

        return best_source

    def get_best_source(self, number_sources: int = 1) -> list:
        """Gets the best webcam source and opens it.

        Args:
            number_sources (int, optional): Number of sources to return. Defaults to 1.

        Returns:
            list: A list of cv2.VideoCapture objects representing the best webcam sources.
        """
        self.rank_sources()
        selected_sources = self.ranking_results[0:number_sources]

        return_caps = []

        for rank, source in selected_sources:
            cap = cv2.VideoCapture(source["id"])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, source["height"])
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, source["width"])

            logging.info(f"Selecting webcam {source['id']}")

            if source["uniform color"]:
                logging.warning(f"Webcam shows uniform color.")

            return_caps.append(cap)

        return return_caps
