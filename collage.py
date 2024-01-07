import os
from PIL import Image

def create_collage(input_folder, output_filename, images_per_row, image_size):
    """
    Creates a collage from images in the input folder and saves it to the output filename.
    """
    # Gather all image paths and sort them numerically
    image_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.png')]
    image_paths.sort(key=lambda f: int(os.path.splitext(os.path.basename(f))[0]))

    if not image_paths:
        raise ValueError("No images found in the input folder.")

    # Calculate the number of rows for the collage
    num_images = len(image_paths)
    num_rows = (num_images + images_per_row - 1) // images_per_row
    collage_width = images_per_row * image_size[0]
    collage_height = num_rows * image_size[1]

    # Create a new blank image for the collage
    collage = Image.new('RGBA', (collage_width, collage_height))

    # Place each image into the collage
    for index, image_path in enumerate(image_paths):
        with Image.open(image_path) as img:
            img = img.resize(image_size, Image.Resampling.LANCZOS)
            x = (index % images_per_row) * image_size[0]
            y = (index // images_per_row) * image_size[1]
            collage.paste(img, (x, y))

    collage.save(output_filename)

# Configuration
input_folder = 'colorized'
output_filename = 'collage.png'
images_per_row = 16  # Adjust as needed for the number of images per row
image_size = (100, 100)  # Size of each image in the collage

create_collage(input_folder, output_filename, images_per_row, image_size)
