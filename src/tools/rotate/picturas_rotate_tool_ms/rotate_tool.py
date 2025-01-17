from PIL import Image
import boto3
from io import BytesIO

from .core.tool import Tool
from .rotate_request_message import RotateParameters


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
class Rotate(Tool):
        def __init__(self):
            self.s3_client = S3Client(
                endpoint_url="http://minio:9000",  # Use the MinIO endpoint from the Docker network
                access_key='ROOTNAME',  
                secret_key='CHANGEME123',  
                region_name='us-east-1'
            )
            
        def apply_rotate(self, image: Image.Image, rotate_angle: float) -> Image.Image:
            """
            Rotate the image by the specified angle.

            Args:
                image (Image.Image): The input image.
                rotate_angle (float): The angle to rotate the image, in degrees.

            Returns:
                Image.Image: The rotated image.
            """
            img_rotated = image.rotate(rotate_angle, expand=True)
            return img_rotated

        
        def apply(self, parameters: RotateParameters):
            """
            Apply the Rotate effect to the input image and save the result.

            Args:
                parameters (RotateParameters): rotate parameters.
            """
            # Open the input image
            bucket_name = 'images'
            input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)
            
            # Apply the rotate effect
            final_image = self.apply_rotate(input_image, parameters.angle)
            
            # Save the final image to MinIO
            with BytesIO() as output_stream:
                final_image.save(output_stream, format='JPEG')
                output_stream.seek(0)
                self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream)
            
            
