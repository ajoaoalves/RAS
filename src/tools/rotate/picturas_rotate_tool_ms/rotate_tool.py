from PIL import Image
import sys

from .core.tool import Tool
from .rotate_request_message import RotateParameters


class Rotate(Tool):

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
            input_image = Image.open(parameters.inputImageURI)

            # Apply the rotate
            final_image = self.apply_rotate(input_image, parameters.rotateAngle)

            # Save the final image
            final_image.save(parameters.outputImageURI)
