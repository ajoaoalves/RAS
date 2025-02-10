import boto3
from PIL import Image
from io import BytesIO

from .core.tool import Tool
from .resize_request_message import ResizeParameters

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

class ResizeTool(Tool):

    def __init__(self):
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # Use the MinIO endpoint from the Docker network
            access_key='ROOTNAME',  
            secret_key='CHANGEME123',  
            region_name='us-east-1'  
        )

    def apply(self, parameters: ResizeParameters):
        """
        Resize the input image and save the result.

        Args:
            parameters (ResizeParameters): resize parameters.
        """
        
        bucket_name = 'images'

        # Download the input image
        input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)

        # Resize the input image
        size = (parameters.width, parameters.height)
        resized_image = input_image.resize(size)

        # Save the resized image
        with BytesIO() as output_stream:
            resized_image.save(output_stream, format='JPEG')
            output_stream.seek(0)
            self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream.getvalue())