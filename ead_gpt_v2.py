import os
import json
import csv
from openai import OpenAI

# Set your API key
client = OpenAI(api_key=api_key)

def call_openai_api(prompt: str, file_url: str = str):
    # Call the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{file_url}",
                        }
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    content = completion.choices[0].message.content

    return content

def extract_info_from_pdf(file_url: str, file_type: str) -> str:
    prompt = f"""
        Por favor, extrae la siguiente información del de la imagen proporcionada en el URL en formato JSON (nota que algunos campos puede que estén vacíos):
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
                intt_nro"""
    return parse_response(call_openai_api(prompt, file_url))

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
    columns = ["pdf_file"] + list(next(iter(data.values())).keys()) if data else []

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists and columns:
            writer.writeheader()
        for pdf_file, item in data.items():
            item["pdf_file"] = pdf_file
            writer.writerow(item)

def main():
    base_url = 'https://raw.githubusercontent.com/f-yanez/ead/refs/heads/main/files/'
    files_folder = 'files/'
    
    files_list = [
        base_url + file_name for file_name in os.listdir(files_folder) if file_name.endswith('.png')
    ]

    all_data = {}

    for file_url in files_list:
        if file_url.endswith('.png'):
            file_name = file_url.split('/')[-1]
            file_type = file_name.split('-')[0]
            extracted_info_json = extract_info_from_pdf(file_url, file_type)
            if extracted_info_json:
                print(json.dumps(extracted_info_json, indent=4))
                all_data[file_name] = extracted_info_json
            else:
                print(f"Failed to extract information from {file_name}.")
    if all_data:
        save_to_csv(all_data, f"extracted_info_{file_type}.csv")

if __name__ == "__main__":
    main()