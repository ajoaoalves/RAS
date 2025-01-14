import boto3
from PIL import Image, ImageEnhance
from io import BytesIO

from .core.tool import Tool
from .brightness_request_message import BrightnessParameters

class Brightness(Tool):

    def apply_brightness(self, image: Image.Image, brightnessValue) -> Image.Image:
        enhancer = ImageEnhance.Brightness(image)
        img_brightened = enhancer.enhance(brightnessValue)
        return img_brightened
    
    def apply(self, parameters: BrightnessParameters):
        """
        Apply the Brightness effect to the input image and save the result.

        Args:
            parameters (BrightnessParameters): brightness parameters.
        """
        # Configure boto3 to access MinIO (S3-compatible)
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:9000',  # Replace with your MinIO URL
            aws_access_key_id='ROOTNAME',  # Replace with your MinIO access key
            aws_secret_access_key='CHANGEME123',  # Replace with your MinIO secret key
            region_name='us-east-1',  # Replace with your region
        )

        # Load the input image from MinIO (S3-compatible)
        bucket_name = 'images'  # Replace with your bucket name
        object_key = parameters.inputImageURI  # The key of the image in MinIO (S3)

        # Download the image from MinIO
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        img_data = response['Body'].read()

        # Open the image using PIL
        input_image = Image.open(BytesIO(img_data))

        # Apply brightness effect
        final_image = self.apply_brightness(input_image, parameters.brightnessValue)

        # Save the final image to MinIO
        output_image_uri = parameters.outputImageURI  # The key to save the output image
        with BytesIO() as output_stream:
            final_image.save(output_stream, format='JPEG')  # Save the image to BytesIO
            output_stream.seek(0)
            # Upload the final image to MinIO
            s3_client.put_object(Bucket=bucket_name, Key=output_image_uri, Body=output_stream)

        print(f"Image successfully processed and saved to {output_image_uri}")
