from PIL import Image
import os

# Set the path to the folder containing your frames
folder_path = 'candles'

# Function to extract numerical part of the filename for sorting
def extract_number(filename):
    return int(''.join(filter(str.isdigit, filename)))

# List all files in the folder, sort them numerically, and keep only image files
frame_files = sorted(
    (f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))),
    key=extract_number
)

# Adjust this to change the GIF's frame duration (in milliseconds)
frame_duration = 100

# Initialize list to hold the image frames
frames = []

# Loop through the sorted files and add them to the frame list
for frame in frame_files:
    with Image.open(os.path.join(folder_path, frame)) as img:
        frames.append(img.copy())

# Save the frames as a GIF
frames[0].save('candles.gif', save_all=True, append_images=frames[1:], optimize=False, duration=frame_duration, loop=0)

print("WHOA that swag gif is so REAL")
