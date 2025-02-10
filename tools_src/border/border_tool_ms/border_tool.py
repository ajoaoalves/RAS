import random
import boto3

from PIL import Image, ImageOps
from io import BytesIO

from .core.tool import Tool
from .border_request_message import borderParameters

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
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            img_data = response['Body'].read()
            input_image = Image.open(BytesIO(img_data))
            return input_image
        except Exception as e:
            print(f"Error downloading image from S3: {e}")
            raise

    def upload_image(self, bucket_name, object_key, image_stream):
        self.s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_stream)

class BorderTool(Tool):

    def __init__(self):
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # Use the MinIO endpoint from the Docker network
            access_key='ROOTNAME',  
            secret_key='CHANGEME123',  
            region_name='us-east-1'  
        )
    
    def apply_border(self, image: Image.Image, border_size, border_color):
        #Apply border using ImageOps.expand 
        """
        ImageOps.expand(image, border, fill)
        """
        bordered_image = ImageOps.expand(
            image,
            border = border_size,
            fill = border_color
        )
        return bordered_image


    def apply (self, parameters : borderParameters):
        """
        Apply a border to the input image and save the result.

        Args:
            parameters (borderParameters): Border parameters including input/output URIs, border size, and border color.
        """
        bucket_name = 'images'  
        
        try:
            input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)
        except Exception as e: 
            print(f"Error downloading image: {e}")
            return 

        final_image = self.apply_border(input_image, parameters.bordersize, parameters.bordercolor)

        # Save the final image to MinIO
        try:
            with BytesIO() as output_stream:
                final_image.save(output_stream, format='JPEG')  # Save the image to BytesIO
                output_stream.seek(0)
                self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream.getvalue())
            print(f"Image successfully processed and saved to {parameters.outputImageURI}")
        except Exception as e:
            print(f"Error processing and uploading image: {e}")
        