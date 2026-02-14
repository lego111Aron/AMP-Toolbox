import os
from PIL import Image

def convert_image(input_path, output_path, format):
    """
    Converts an image to a specified format (png, jpg).
    """
    try:
        with Image.open(input_path) as img:
            rgb_im = img.convert('RGB')
            rgb_im.save(output_path)
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def convert_to_pdf(input_path, output_path):
    """
    Converts supported files (images) to PDF.
    """
    try:
        image = Image.open(input_path)
        pdf_bytes = image.convert('RGB')
        pdf_bytes.save(output_path)
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        return False
