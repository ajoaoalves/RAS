import cv2
from ultralytics import YOLO

from .core.tool import Tool
from .count_objects_request_message import CountObjectsParameters


class CountObjects(Tool):

    def __init__(self, model_path: str = "yolov8n.pt") -> None:
        """
        Initialize the CountObjects tool with the path to the YOLO model.

        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def apply(self, parameters: CountObjectsParameters) -> dict:
        """
        Detect and count objects in an input image.

        Args:
            parameters (CountObjectsParameters): Parameters containing the input image path.

        Returns:
            dict: A dictionary with detected object classes as keys and their counts as values.
        """
        # Load the image
        image = cv2.imread(parameters.inputImageURI)
        if image is None:
            raise FileNotFoundError("Imagem não encontrada.")

        # Perform predictions
        results = self.model(image)

        # Filter and count detections by class
        detections = results[0].boxes
        object_counts = {}

        for box in detections:
            class_id = int(box.cls)
            class_name = self.model.names.get(class_id, "unknown")
            object_counts[class_name] = object_counts.get(class_name, 0) + 1

        # Save the output image with detections
        if parameters.outputImageURI:
            output_image = results[0].plot()
            cv2.imwrite(parameters.outputImageURI, output_image)

        # Return the object counts
        return object_counts
