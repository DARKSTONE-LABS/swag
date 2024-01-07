import os
import random
from PIL import Image

def pixelate(image, pixel_size):
    """
    Pixelates the given image to a specified pixel size.
    """
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    return image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )

def apply_color_variation(image):
    """
    Applies a systematic color variation to the image.
    """
    data = image.getdata()
    new_data = []
    for item in data:
        # Adjust the color variation logic as needed
        new_color = tuple(min(255, int(channel * random.uniform(0.8, 1.2))) for channel in item)
        new_data.append(new_color)
    image.putdata(new_data)
    return image

def process_images(input_folder, output_folder, pixel_size):
    """
    Processes images from the input folder and saves them to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, filename in enumerate(os.listdir(input_folder)):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f'{index}.png')

            with Image.open(input_path) as img:
                pixelated_img = pixelate(img, pixel_size)
                color_varied_img = apply_color_variation(pixelated_img)
                color_varied_img.save(output_path)

# Configuration
input_folder = 'assets'
output_folder = 'colorized'
pixel_size = 10  # Adjust the pixel size as needed

process_images(input_folder, output_folder, pixel_size)
