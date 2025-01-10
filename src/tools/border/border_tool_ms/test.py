import random
import sys
from PIL import Image as PILImage
from PIL import ImageOps as PILImageOps

def applyBorder(input_image_path, output_image_path, size, color):
    """
    Apply a border to the input image and save the result.

    Args:
        parameters (borderParameters): Border parameters including input/output URIs, border size, and border color.
    """
    try:
        #Open the input image
        input_image = PILImage.open(input_image_path).convert("RGB")

        #Generate a random border size and color if not provived
        border_size = size or random.randint(1, 10)
        border_color = color or "#%06x" % random.randint(0, 0xFFFFFF)

        #Apply border using ImageOps.expand 
        bordered_image = PILImageOps.expand(
            input_image,
            border=border_size,
            fill=border_color
        )

        #Save the image with the border
        bordered_image.save(output_image_path)
    
    except Exception as e: 
        raise RuntimeError(f"Failed to apply border: {e}")

if __name__ == "__main__":
    # Ensure the program gets the correct arguments
    if len(sys.argv) < 4:
        print("Usage: python script_name.py <input_image_path> <output_image_path> <size_factor> <color_factor>")
        sys.exit(1)
    # python ../../src/tools/border/border_tool_ms/test.py src/input.jpg out/output.jpg 5 "#FF0000"

    # Get the arguments
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    size_factor = int(sys.argv[3])  
    color_factor = sys.argv[4]

    # Apply the brightness transformation
    applyBorder(input_image_path, output_image_path, size_factor, color_factor)