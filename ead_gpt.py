import openai
from openai import OpenAI
import json
import os
import csv
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pytesseract import image_to_string

# Set your API key
client = OpenAI(api_key=api_key)

def extract_text_from_pdf2(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as pdf_file:
        # Read and extract text
        reader = PdfReader(pdf_file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
        return extracted_text.strip()
    
def extract_text_from_image_pdf(pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        # OCR the image
        text += image_to_string(image)
    return text

def write_prompt(text: str) -> str:
    prompt = f"""Por favor, extrae la siguiente información del [TEXTO] de un documento PDF en formato JSON (nota que algunos campos puede que estén vacíos):
                nombre,
                cedula_rif,
                placa,
                serial_NIV,
                serial_carroceria,
                serial_chasis,
                serial_motor,
                tc,
                marca,
                modelo,
                color,
                ano_fabricacion,
                ano_modelo,
                clase,
                tipo,
                uso,
                nro_puestos,
                nro_ejes,
                tara,
                cap_carga:
                servicio,
                fecha,
                intt_nro
                
                
                [TEXTO]:
                {text}"""
    return prompt

def call_openai_api(prompt: str):
    # Call the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Replace with your desired model (e.g., gpt-4o or another version)
        messages=[
            {"role": "developer", "content": "Eres un asistente útil para extraer información de documentos."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def parse_response(response):
    try:
        start = response.index("{")
        end = response.rindex("}") + 1
        response = response[start:end]
        response_json = json.loads(response)
        return response_json
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return None

def save_to_csv(data, csv_path):
    if not data:
        print("No data to save.")
        return

    # Extract column names from the first item in the data dictionary
    columns = ["pdf_file"] + list(next(iter(data.values())).keys())

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        for pdf_file, item in data.items():
            item["pdf_file"] = pdf_file
            writer.writerow(item)

def main(pdf_files, csv_path):
    all_data = {}
    for pdf_path in pdf_files:
        text = extract_text_from_image_pdf(pdf_path)
        print(f"Extracted text from {pdf_path}:")
        print(text)
        print("Calling OpenAI API...")
        prompt = write_prompt(text)
        response = call_openai_api(prompt)
        print(response)
        parsed_response = parse_response(response)
        if parsed_response:
            print(f"Extracted Information from {pdf_path}:")
            print(json.dumps(parsed_response, indent=4))
            all_data[pdf_path] = parsed_response
        else:
            print(f"Failed to extract information from {pdf_path}.")
    if all_data:
        save_to_csv(all_data, csv_path)

if __name__ == "__main__":
    # Create a list of all PDF files in the "files" folder
    pdf_folder = "files"
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    # Save the results to a single CSV file
    csv_path = "output.csv"
    main(pdf_files, csv_path)