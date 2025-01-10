import cv2
from ultralytics import YOLO

from .core.tool import Tool
from .count_people_request_message import CountPeopleParameters


class CountPeople(Tool):

    def __init__(self, model_path: str = "yolov8n.pt") -> None:
        """
        Initialize the CountPeople tool with the path to the YOLO model.

        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def apply(self, parameters: CountPeopleParameters) -> int:
        """
        Detect and count the number of people in an input image.

        Args:
            parameters (CountPeopleParameters): Parameters containing the input image path.

        Returns:
            int: Number of people detected in the image.
        """
        # Load the image
        image = cv2.imread(parameters.inputImageURI)
        if image is None:
            raise FileNotFoundError("Imagem não encontrada.")

        # Perform predictions
        results = self.model(image)

        # Filter detections of people
        detections = results[0].boxes
        people = [
            box for box in detections
            if int(box.cls) in self.model.names and self.model.names[int(box.cls)] == 'person'
        ]

        # Save the output image with detections
        if parameters.outputImageURI:
            output_image = results[0].plot()
            cv2.imwrite(parameters.outputImageURI, output_image)

        # Return the number of people detected
        return len(people)
