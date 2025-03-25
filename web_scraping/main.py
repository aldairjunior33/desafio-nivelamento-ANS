import requests
from bs4 import BeautifulSoup
import os
import zipfile

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Lista de nomes dos anexos que queremos baixar
anexos_nomes = [
    "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
]

# Pasta "Anexos"
os.makedirs('anexos', exist_ok=True)

arquivos_baixados = []

for link in soup.find_all('a', href=True):
    pdf_url = link['href']
    if pdf_url.endswith('.pdf') and any(nome_arquivo in pdf_url for nome_arquivo in anexos_nomes):
        pdf_url = pdf_url if pdf_url.startswith('http') else f"https://www.gov.br{pdf_url}"
        

        file_name = pdf_url.split('/')[-1]
        path_destino = os.path.join('anexos', file_name)
        pdf_response = requests.get(pdf_url)
        
        with open(path_destino,  'wb') as f:
            f.write(pdf_response.content)
        arquivos_baixados.append(path_destino)

        print(f"Arquivo {file_name} baixado com sucesso!")

zip_path = 'anexos.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for arquivo in arquivos_baixados:
        zipf.write(arquivo, arcname=os.path.basename(arquivo))

    print(f"{os.path.basename(arquivo)} adicionado ao {zip_path}")
    print(f"Compactação finalizada: {zip_path}")
