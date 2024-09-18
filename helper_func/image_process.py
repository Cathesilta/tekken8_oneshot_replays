from PIL import Image, ImageDraw

# Load your image
# image = Image.open('./images/test_image.jpg')

def apply_gradient_shadow_top(img, shadow_height_fraction_1=0.1, shadow_height_Fraction_2=0.3, base_opacity=0.95):
    # Load the image
    width, height = img.size
    
    top_shadow_1_height = int(height * shadow_height_fraction_1)
    top_shadow_2_height = int(height * shadow_height_Fraction_2) - top_shadow_1_height
    # Create a gradient image for the shadow
    shadow_1 = Image.new('RGBA', (width, top_shadow_1_height), color=0)
    draw_1 = ImageDraw.Draw(shadow_1)
    shadow_2 = Image.new('RGBA', (width, top_shadow_2_height), color=0)
    draw_2 = ImageDraw.Draw(shadow_2)

    # Generate gradient
    for y in range(shadow_1.height):
        opacity = int(255 * (0.6 + 0.3 * (1-y / shadow_1.height)))
        draw_1.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))
        
        
        
    for y in range(shadow_2.height):
        opacity = int(255 * (0.6 * (1-y / shadow_2.height)))
        draw_2.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))        
    

    # Apply the shadow to the original image
    img.paste(shadow_1, (0, 0), shadow_1)
    img.paste(shadow_2, (0, top_shadow_1_height), shadow_2)
    return img
    
def apply_gradient_shadow_bottom_Tekken8(img, shadow_start_fraction=0.1, shadow_end_fraction=0.3):
    # Load the image

    width, height = img.size

    # Calculate the shadow height and starting position
    shadow_height = int(height * (shadow_end_fraction - shadow_start_fraction))
    shadow_start_position = int(height * (1 - shadow_end_fraction))

    # Create a gradient image for the shadow
    shadow = Image.new('RGBA', (width, shadow_height), color=0)
    draw = ImageDraw.Draw(shadow)

    # Generate gradient
    for y in range(shadow.height):
        opacity = int(255 * ((shadow.height - y) / shadow.height))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))

    # Apply the shadow to the original image
    img.paste(shadow, (0, shadow_start_position), shadow)
    return img
    
def apply_darker_gradient_shadow_bottom_Tekken8(image_path, shadow_start_fraction=0.035, shadow_end_fraction=0.28, base_opacity=0.9):
    # Load the image
    with Image.open(image_path) as img:
        width, height = img.size

        # Calculate the shadow height and starting position
        shadow_height = int(height * (shadow_end_fraction - shadow_start_fraction))
        shadow_start_position = int(height * (1 - shadow_end_fraction))

        # Create a gradient image for the shadow
        shadow = Image.new('RGBA', (width, shadow_height), color=0)
        draw = ImageDraw.Draw(shadow)

        # Generate gradient with increased base opacity
        for y in range(shadow.height):
            opacity = int(255 * (base_opacity + (1 - base_opacity) * ((shadow.height - y) / shadow.height)))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))

        # Apply the shadow to the original image
        img.paste(shadow, (0, shadow_start_position), shadow)
        return img
    

def apply_symmetric_gradient_banners_Tekken8(img, y1 = 800,y2 = 1010, initial_banner_fraction=0.05, banner_fraction_2=0.35, banner_fraction_3 = 0.5):
    # Load the image
    width, height = img.size

    # Calculate the widths for the banners
    initial_banner_width = int(width * initial_banner_fraction)
    banner_width_2 = int(width * banner_fraction_2) - initial_banner_width
    banner_width_3 = int(width*banner_fraction_3) - initial_banner_width - banner_width_2

    # Create gradient images for the banners
    initial_left_banner = Image.new('RGBA', (initial_banner_width, height), color=0)
    banner_left_2 = Image.new('RGBA', (banner_width_2, height), color=0)
    banner_left_3 = Image.new('RGBA', (banner_width_3, height), color=0)
    initial_right_banner = Image.new('RGBA', (initial_banner_width, height), color=0)
    banner_right_2 = Image.new('RGBA', (banner_width_2, height), color=0)
    banner_right_3 = Image.new('RGBA', (banner_width_3, height), color=0)

    # Define draw objects for each banner
    draw_initial_left = ImageDraw.Draw(initial_left_banner)
    draw_left_2 = ImageDraw.Draw(banner_left_2)
    draw_left_3 = ImageDraw.Draw(banner_left_3)
    draw_initial_right = ImageDraw.Draw(initial_right_banner)
    draw_right_2 = ImageDraw.Draw(banner_right_2)
    draw_right_3 = ImageDraw.Draw(banner_right_3)
    

    # Generate gradients for each banner
    for x in range(initial_banner_width):
        opacity_left = int(255 * (0.9 * (x / initial_banner_width)))
        opacity_right = int(255 * (0.9 * ((initial_banner_width - x) / initial_banner_width)))
        draw_initial_left.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_left))
        draw_initial_right.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_right))

    for x in range(banner_width_2):
        opacity_left = int(255 * (0.9 + 0.05 * (x / banner_width_2)))
        opacity_right = int(255 * (0.9 + 0.05 * ((banner_width_2 - x) / banner_width_2)))
        draw_left_2.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_left))
        draw_right_2.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_right))
        
    for x in range(banner_width_3):
        opacity_left = int(255 * (1 - 0.95 * (x / banner_width_3)))
        opacity_right = int(255 * (1 - 0.95 * ((banner_width_3 - x) / banner_width_3)))
        draw_left_3.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_left))
        draw_right_3.line([(x, y1), (x, y2)], fill=(0, 0, 0, opacity_right))       

    # Apply the left banners to the original image
    img.paste(initial_left_banner, (0, 0), initial_left_banner)
    img.paste(banner_left_2, (initial_banner_width, 0), banner_left_2)
    img.paste(banner_left_3, (initial_banner_width+banner_width_2, 0), banner_left_3)

    # Apply the right banners to the original image
    right_initial_position = width - initial_banner_width
    right_position_2 = right_initial_position - banner_width_2
    right_position_3 = right_position_2 - banner_width_3
    img.paste(initial_right_banner, (right_initial_position, 0), initial_right_banner)
    img.paste(banner_right_2, (right_position_2, 0), banner_right_2)
    img.paste(banner_right_3, (right_position_3, 0), banner_right_3)

    return img
    
# result_image = apply_shadow('./images/test_image.jpg')
# result_image.show()


def overlay_image(background_image, overlay_image, position, size):
    # Load the background and overlay images

    # Resize overlay image
    overlay_image = overlay_image.resize(size, Image.LANCZOS)

    # Paste the overlay image on the background
    background_image.paste(overlay_image, position, overlay_image)
    
    return background_image
    # Save the result or display it
    background.show()  # This will display the image
    # background.save('output.png')  # This will save the image