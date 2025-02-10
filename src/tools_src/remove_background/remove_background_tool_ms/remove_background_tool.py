import boto3
from PIL import Image, ImageChops
import numpy as np
from io import BytesIO

from .core.tool import Tool
from .remove_background_request_message import RemoveBackgroundParameters


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
        input_image = Image.open(BytesIO(img_data)).convert("RGBA")
        return input_image

    def upload_image(self, bucket_name, object_key, image_stream):
        self.s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_stream)


class RemoveBackgroundTool(Tool):

    def __init__(self):
        self.s3_client = S3Client(
            endpoint_url="http://minio:9000",  # EndPoint MinIO dentro de Docker
            access_key='ROOTNAME',  
            secret_key='CHANGEME123',  
            region_name='us-east-1'  
        )

    def apply(self, parameters: RemoveBackgroundParameters):
        """
        Aplica la eliminación de fondo a una imagen y guarda el resultado en MinIO.

        Args:
            parameters (RemoveBackgroundParameters): Parámetros que incluyen input/output URIs.
        """
        try:
            bucket_name = "images"  # Asegúrate de que este es el nombre correcto del bucket en MinIO
            
            # Descargar imagen de MinIO
            input_image = self.s3_client.download_image(bucket_name, parameters.inputImageURI)

            # Crear un fondo blanco
            white_bg = Image.new("RGBA", input_image.size, (255, 255, 255, 255))

            # Calcular la diferencia entre la imagen y el fondo blanco
            diff = ImageChops.difference(input_image, white_bg)

            # Convertir la diferencia a escala de grises y crear una máscara
            diff_gray = diff.convert("L")
            mask = diff_gray.point(lambda p: 255 if p > 50 else 0)

            # Aplicar la máscara para hacer el fondo transparente
            input_image.putalpha(mask)

            # Guardar la imagen final en MinIO
            with BytesIO() as output_stream:
                input_image.save(output_stream, format="PNG")  # Se guarda en PNG para soportar transparencia
                output_stream.seek(0)
                self.s3_client.upload_image(bucket_name, parameters.outputImageURI, output_stream.getvalue())

        except Exception as e:
            raise RuntimeError(f"Failed to remove background: {e}")
