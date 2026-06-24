from PIL import Image
import os

def overlay_logo(image_path, logo_path, output_path):
    """
    Overlay a transparent logo on the bottom-right corner of an image.
    Resizes logo to 15% of the base image width.
    """
    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo to 15% of image width
    logo_width = int(img.width * 0.15)
    logo_height = int(logo.height * (logo_width / logo.width))
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

    # Position: bottom-right with 20px padding
    x = img.width - logo_width - 20
    y = img.height - logo_height - 20

    img.paste(logo, (x, y), logo)
    img.save(output_path, "PNG", quality=95)
    return output_path