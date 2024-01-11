import os
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

# Pixelate function
def pixelate(image, pixel_size):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    return image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )

# Apply hue shift function
def apply_hue_shift(image, hue_shift):
    data = image.getdata()
    new_data = []

    for color in data:
        if len(color) == 4:  # RGBA images
            r, g, b, a = color
            hue, saturation, value = rgb_to_hsv(r, g, b)
            new_hue = (hue + hue_shift) % 360
            r, g, b = hsv_to_rgb(new_hue, saturation, value)
            new_color = (r, g, b, a)
        else:  # RGB images
            r, g, b = color
            hue, saturation, value = rgb_to_hsv(r, g, b)
            new_hue = (hue + hue_shift) % 360
            new_color = hsv_to_rgb(new_hue, saturation, value)

        new_data.append(new_color)

    image.putdata(new_data)
    return image

# RGB to HSV conversion function
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

# HSV to RGB conversion function
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

def process_images(input_path, output_folder, pixel_size, num_hues, update_preview):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_hues):
        hue_shift = (360 / num_hues) * i

        with Image.open(input_path) as img:
            pixelated_img = pixelate(img, pixel_size)
            hue_shifted_img = apply_hue_shift(pixelated_img, hue_shift)
            update_preview(hue_shifted_img)  # Update the preview for each image

            # Save the processed image
            output_path = os.path.join(output_folder, f'{i}.png')
            hue_shifted_img.save(output_path)

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("swag256")

        # File selection button
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack()

        # Start processing button
        self.start_button = tk.Button(root, text="Start Processing", command=self.start_processing)
        self.start_button.pack()

        # Image preview
        self.image_label = tk.Label(root)
        self.image_label.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename()
        self.input_image_path = file_path

    def start_processing(self):
        output_folder = '256swagimages'
        pixel_size = 10 
        num_hues = 256  
        threading.Thread(target=process_images, args=(self.input_image_path, output_folder, pixel_size, num_hues, self.update_preview)).start()

    def update_preview(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.tk_image)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()