import os
import math
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

def apply_hue_shift(image, hue_shift):
    """
    Applies a hue shift to the image.
    """
    data = image.getdata()
    new_data = []

    for color in data:
        # Handle RGBA images
        if len(color) == 4:  # If the image has an alpha channel
            r, g, b, a = color
            hue, saturation, value = rgb_to_hsv(r, g, b)
            new_hue = (hue + hue_shift) % 360
            r, g, b = hsv_to_rgb(new_hue, saturation, value)
            new_color = (r, g, b, a)
        else:  # For RGB images
            r, g, b = color
            hue, saturation, value = rgb_to_hsv(r, g, b)
            new_hue = (hue + hue_shift) % 360
            new_color = hsv_to_rgb(new_hue, saturation, value)

        new_data.append(new_color)

    image.putdata(new_data)
    return image

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h, s, v

def hsv_to_rgb(h, s, v):
    h = h % 360
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def process_images(input_folder, output_folder, pixel_size, num_hues):
    """
    Processes images from the input folder and saves them to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filename = os.listdir(input_folder)[0]  # Assuming only one image to process and replicate

    for i in range(num_hues):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f'{i}.png')
        hue_shift = (360 / num_hues) * i  # Calculate the hue shift

        with Image.open(input_path) as img:
            pixelated_img = pixelate(img, pixel_size)
            hue_shifted_img = apply_hue_shift(pixelated_img, hue_shift)
            hue_shifted_img.save(output_path)

# Configuration
input_folder = 'hgf'
output_folder = 'colorized'
pixel_size = 10  # Adjust the pixel size as needed
num_hues = 256  # Number of unique hues

process_images(input_folder, output_folder, pixel_size, num_hues)
