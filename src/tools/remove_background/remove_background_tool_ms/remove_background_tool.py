from PIL import Image, ImageOps, ImageChops

from .core.tool import Tool
from .remove_background_request_message import RemoveBackgroundParameters


class RemoveBackgroundTool(Tool):

    def apply(self, parameters: RemoveBackgroundParameters):
        """
        Apply background removal to the input image and save the result.

        Args:
            parameters (RemoveBackgroundParameters): Parameters including input/output URIs.
        """
        try:

            input_image = Image.open(parameters.inputImageURI).convert("RGBA")

            # Create a white background for comparison
            white_bg = Image.new("RGBA", input_image.size, (255, 255, 255, 255))

            # Calculate the difference between the image and white background
            diff = ImageChops.difference(input_image, white_bg)

            # Convert difference to grayscale and create a mask
            diff_gray = diff.convert("L")
            mask = diff_gray.point(lambda p: 255 if p > 50 else 0)

            # Apply the mask to make the background transparent
            input_image.putalpha(mask)

            input_image.save(parameters.outputImageURI)

        except Exception as e:
            raise RuntimeError(f"Failed to remove background: {e}")

