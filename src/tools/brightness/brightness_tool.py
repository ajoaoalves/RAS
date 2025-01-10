from PIL import Image, ImageEnhance
import sys

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
            # Open the input image
            input_image = Image.open(parameters.inputImageURI)

            # Save the final image
            final_image = self.apply_brightness(input_image, parameters.brightnessValue)
            final_image.save(parameters.outputImageURI)
