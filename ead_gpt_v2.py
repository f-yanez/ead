import os
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

    return completion.choices[0].message['content']

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
    return call_openai_api(prompt, file_url)

def main():
    files_list = [
        'https://github.com/f-yanez/ead/blob/main/files/titulo_propiedad_vehiculo-ABC123.pdf',
    ]

    for file_url in files_list:
        if file_url.endswith('.pdf'):
            file_name = file_url.split('/')[-1]
            file_type = file_name.split('-')[0]
            extracted_info = extract_info_from_pdf(file_url, file_type)
            print(f"Information extracted from {file_name}:\n{extracted_info}\n")

if __name__ == "__main__":
    main()