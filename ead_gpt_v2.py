import os
from openai import OpenAI

# Set your API key
client = OpenAI(api_key=api_key)

def call_openai_api(prompt: str):
    # Call the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Replace with your desired model (e.g., gpt-4o or another version)
        messages=[
            {"role": "developer", "content": "Eres un asistente útil para extraer información de documentos."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message['content']

def extract_info_from_pdf(file_url: str, file_type: str) -> str:
    prompt = f"Extrae la información relevante del siguiente documento PDF ubicado en la URL: {file_url}. El nombre del archivo es {file_type}."
    return call_openai_api(prompt)



def main():
    files_folder = 'files'
    base_url = 'http://your_public_url_base/'  # Replace with your actual base URL

    for file_name in os.listdir(files_folder):
        if file_name.endswith('.pdf'):
            file_url = f"{base_url}{file_name}"
            extracted_info = extract_info_from_pdf(file_url, file_name)
            print(f"Information extracted from {file_name}:\n{extracted_info}\n")

if __name__ == "__main__":
    main()