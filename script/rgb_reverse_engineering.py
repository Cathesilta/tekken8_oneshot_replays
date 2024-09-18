from PIL import Image

img_path = './colorrgb_reverse_engineering/plat_darker03.jpg'  # Replace with your image path
img = Image.open(img_path)

# Specify the coordinates of the point you want to analyze
# You need to find out the coordinates of the shadow in your image
x, y = 1, 1  # Replace with the coordinates of the shadow

# Get the color
color = img.getpixel((x, y))

print("RGB Value at ({}, {}): {}".format(x, y, color))