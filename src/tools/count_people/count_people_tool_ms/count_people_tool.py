import boto3
from ultralytics import YOLO

from .core.tool import Tool
from .count_people_request_message import CountPeopleParameters

class S3Client:
    def __init__(self, endpoint_url, access_key, secret_key, region_name):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

    def download_image(self, bucket_name, object_key):
        response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        img_data = response['Body'].read()
        input_image = Image.open(BytesIO(img_data))
        return input_image

    def upload_image(self, bucket_name, object_key, image_stream):
        self.s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_stream)

class CountPeople(Tool):

    def __init__(self, model_path: str = "yolov8n.pt") -> None:
        """
        Initialize the CountPeople tool with the path to the YOLO model.

        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # Use the MinIO endpoint from the Docker network
            access_key='ROOTNAME',  
            secret_key='CHANGEME123',  
            region_name='us-east-1'  
        )
        
        self.model = YOLO(model_path)

    def apply(self, parameters: CountPeopleParameters) -> int:
        """
        Detect and count the number of people in an input image.

        Args:
            parameters (CountPeopleParameters): Parameters containing the input image path.

        Returns:
            int: Number of people detected in the image.
        """
        
        bucket_name = 'images'
        
        # Load the image
        image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)
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

        # Return the number of people detected
        return len(people)
