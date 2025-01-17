import boto3

from io import BytesIO
from PIL import Image, ImageOps

from .core.tool import Tool
from .crop_request_message import cropParameters


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


class CropTool(Tool):
    def __init__(self):
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # MinIO endpoint
            access_key="ROOTNAME",
            secret_key="CHANGEME123",
            region_name="us-east-1",
        )

    def crop_image(self, image: Image.Image, crop_box):
        """
        Crop the input image using the specified crop box.

        Args:
            image (Image.Image): The input image to crop.
            crop_box (tuple): A tuple of four values (left, upper, right, lower) 
                            defining the region to keep.

        Returns:
            Image.Image: The cropped image.
        """
        cropped_image = image.crop(crop_box)
        return cropped_image


    def apply_crop(self, parameters: cropParameters):
        """
        Crop the input image using specified parameters and save the result.

        Args:
            parameters (cropParameters): Parameters including input/output URIs and crop box (left, upper, right, lower).
        """
        bucket_name = 'images'
        
        try:
            # Download the input image
            input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)
        except Exception as e:
            print(f"Error downloading image: {e}")
            return

        try:
            # Apply cropping to the image
            final_image = self.crop_image(input_image, parameters.crop_box)

            # Save the cropped image to MinIO
            with BytesIO() as output_stream:
                final_image.save(output_stream, format='JPEG')  # Save the image to BytesIO
                output_stream.seek(0)
                self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream.getvalue())
            print(f"Image successfully cropped and saved to {parameters.outputImageURI}")
        except Exception as e:
            print(f"Error processing and uploading image: {e}")
