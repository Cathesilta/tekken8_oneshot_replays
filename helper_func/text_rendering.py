from PIL import Image,ImageDraw


def getsize(font, text):
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom - top

def create_gold_gradient(width, height):
    gradient = Image.new('RGBA', (width, height), color=0)
    draw = ImageDraw.Draw(gradient)

    for i in range(height):
        # Define the color transition
        if i < height / 4:
            # Transition from mediocre gold to dark gold
            r, g, b = 212 - i, 175 - i, 55 - i
        elif i < height / 2:
            # Very bright gold
            r, g, b = 255, 215, 0
        else:
            # Transition from light gold to dark gold
            factor = (i - height / 2) / (height / 2)
            r, g, b = 255 - int(43 * factor), 215 - int(160 * factor), 0

        draw.line([(0, i), (width, i)], fill=(r, g, b))

    return gradient

def create_plat_gradient(width, height):
    gradient = Image.new('RGBA', (width, height), color=0)
    draw = ImageDraw.Draw(gradient)

    for i in range(height):
        # Define the color transition
        if 0 <= i < 1/4 * height:
            # Transition from mediocre gold to dark gold
            r, g, b = max(36 - i,0), max(93 - i,0), max(81 - i,0)
            # r, g, b = 0,0,0
        elif 1/4 * height <= i <  height / 2:
            # Very bright gold
            r, g, b = 108, 187, 140
        else:
            # Transition from light gold to dark gold
            factor = (i - height / 2) / (height / 2)
            r, g, b = 108 * int(1 - factor), 187 - int(1 - factor), 140 - int(1 - factor)


        draw.line([(0, i), (width, i)], fill=(r, g, b))

    return gradient