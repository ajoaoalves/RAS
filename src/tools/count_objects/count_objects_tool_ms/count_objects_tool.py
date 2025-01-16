import cv2
from ultralytics import YOLO

from .core.tool import Tool
from .count_objects_request_message import CountObjectsParameters


class CountObjects(Tool):

    def __init__(self, model_path: str = "yolov8n.pt") -> None:
        """
        Initialize the CountPeople tool with the path to the YOLO model.

        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def apply(self, parameters: CountObjectsParameters) -> dict:
        """
        Detect and count the number of objects in an input image.

        Args:
            parameters (CountPeopleParameters): Parameters containing the input image path.

        Returns:
            dict: A dictionary with object classes as keys and their counts as values.
        """
        # Load the image
        image = cv2.imread(parameters.inputImageURI)
        if image is None:
            raise FileNotFoundError("Imagem não encontrada.")

        # Perform predictions
        results = self.model(image)

        # Initialize a dictionary to store counts
        counts = {}

        # Iterate over all detections
        detections = results[0].boxes
        for box in detections:
            class_id = int(box.cls)
            class_name = self.model.names[class_id]
            # Increment the count for the detected class
            counts[class_name] = counts.get(class_name, 0) + 1

        # Return the counts dictionary
        return counts
