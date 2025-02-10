import boto3
from PIL import Image
import numpy as np
from io import BytesIO

from .core.tool import Tool
from .binarization_request_message import BinarizationParameters

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

class Binarization(Tool):

    def __init__(self):
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # Use the MinIO endpoint from the Docker network
            access_key='ROOTNAME',  
            secret_key='CHANGEME123',  
            region_name='us-east-1'  
        )

    def apply_binarization(self, image: Image.Image) -> Image.Image:
        # Convert the image to grayscale if it's not already
        grayscale_image = image.convert("L")

        # Convert the grayscale PIL Image to a NumPy array
        img_array = np.array(grayscale_image)

        # Apply binary thresholding (threshold value = 100)
        threshold = 100
        binarized_array = (img_array > threshold).astype(np.uint8) * 255
        
        # Convert the binarized array back to a PIL Image
        binarized_image = Image.fromarray(binarized_array)
        
        return binarized_image



    def apply(self, parameters: BinarizationParameters):
        """
        Apply the Binarization effect to the input image and save the result.

        Args:
            parameters (BinarizationParameters): binarization parameters.
        """
        
        bucket_name = 'images'  # Replace with your bucket name
        
        input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)

        # Apply binarization effect
        final_image = self.apply_binarization(input_image)

        # Save the final image to MinIO
        with BytesIO() as output_stream:
            final_image.save(output_stream, format='JPEG')  # Save the image to BytesIO
            output_stream.seek(0)
            # Upload the final image to MinIO
            self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream.getvalue())

        #print(f"Image successfully processed and saved to {parameters.outputImageURI}")

