import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(file_paths, output_path):
    # (Unchanged merge logic)
    merger = PdfMerger()
    try:
        for pdf in file_paths:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        return True
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False

def split_pdf(input_path, output_dir):
    try:
        reader = PdfReader(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_filename = f"{base_name}_page_{i+1}.pdf"
            with open(os.path.join(output_dir, output_filename), "wb") as output_stream:
                writer.write(output_stream)
        return True
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return False

def crop_pdf(input_path, output_path, margin=10):
    # Simple crop (removing margins) logic as placeholder
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            # Modify the media box directly (cropping)
            # This is a basic example; real cropping needs coordinate inputs
            page.cropbox.lower_left = (float(page.cropbox.lower_left[0]) + margin, float(page.cropbox.lower_left[1]) + margin)
            page.cropbox.upper_right = (float(page.cropbox.upper_right[0]) - margin, float(page.cropbox.upper_right[1]) - margin)
            writer.add_page(page)

        with open(output_path, "wb") as output_stream:
            writer.write(output_stream)
        return True
    except Exception as e:
        print(f"Error cropping PDF: {e}")
        return False

