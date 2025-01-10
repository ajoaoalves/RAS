import random

from PIL import Image, ImageOps

from .core.tool import Tool
from .border_request_message import borderParameters


class BorderTool(Tool):

    def apply (self, parameters : borderParameters):
        """
        Apply a border to the input image and save the result.

        Args:
            parameters (borderParameters): Border parameters including input/output URIs, border size, and border color.
        """
        try:
            #Open the input image
            input_image = Image.open(parameters.inputImageURI).convert("RGB")

            #Generate a random border size and color if not provived
            border_size = parameters.bordersize or random.randint(1, 10)
            border_color = parameters.bordercolor or "#%06x" % random.randint(0, 0xFFFFFF)

            #Apply border using ImageOps.expand 
            """
            ImageOps.expand(image, border, fill)
            """
            bordered_image = ImageOps.expand(
                input_image,
                border = border_size,
                fill = border_color
            )

            #Save the image with the border
            bordered_image.save(parameters.outputImageURI)
        
        except Exception as e: 
            raise RuntimeError(f"Failed to apply border: {e}")