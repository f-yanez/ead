import fitz  # PyMuPDF
from PIL import Image
import os

# Define the folder containing the PDF files
folder_path = "files"

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        
        # Loop through each page in the PDF
        for page_number in range(len(pdf_document)):
            # Get the page
            page = pdf_document.load_page(page_number)
            
            # Render page to an image (pixmap)
            pix = page.get_pixmap()
            
            # Save the image in PNG format
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            output_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_page_{page_number + 1}.png")
            image.save(output_path, "PNG")

print("All PDF pages converted to PNG successfully!")
