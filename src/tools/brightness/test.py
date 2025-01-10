from PIL import Image, ImageEnhance
import sys

def apply_brightness(input_image_path, output_image_path, brightness_factor):
    # Open the image file
    with Image.open(input_image_path) as img:
        # Enhance the brightness
        enhancer = ImageEnhance.Brightness(img)
        img_brightened = enhancer.enhance(brightness_factor)

        # Save the modified image
        img_brightened.save(output_image_path)
        print(f"Image saved to {output_image_path}")

if __name__ == "__main__":
    # Ensure the program gets the correct arguments
    if len(sys.argv) < 4:
        print("Usage: python script_name.py <input_image_path> <output_image_path> <brightness_factor>")
        sys.exit(1)

    # Get the arguments
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    brightness_factor = float(sys.argv[3])  # The factor by which to adjust the brightness

    # Apply the brightness transformation
    apply_brightness(input_image_path, output_image_path, brightness_factor)
