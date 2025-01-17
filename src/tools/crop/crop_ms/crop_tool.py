import random
from PIL import Image

from .core.tool import Tool
from .crop_request_message import cropParameters


class CropTool(Tool):

    def __init__(self):
        """
        Initialize the CropTool. This tool does not require S3 and will work with local files.
        """
        pass

    def apply_crop(self, image: Image.Image, crop_box) -> Image.Image:
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

    def apply(self, parameters: cropParameters):
        """
        Crop the input image using specified parameters and save the result.

        Args:
            parameters (cropParameters): Parameters including input/output URIs and crop box (left, upper, right, lower).
        """
        input_image_path = parameters.inputImageURI
        output_image_path = parameters.outputImageURI
        crop_box = parameters.crop_box

        try:
            # Open the input image
            input_image = Image.open(input_image_path).convert("RGBA")
            print("******CHEGUEI*******")
            # Apply cropping to the image
            final_image = self.crop_image(input_image, crop_box).convert("RGB")

            # Save the cropped image
            final_image.save(output_image_path)
            print(f"Image successfully cropped and saved to {output_image_path}")

        except Exception as e:
            print(f"Error processing and saving the cropped image: {e}")
