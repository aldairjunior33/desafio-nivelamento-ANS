import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)

# Usa o BeautifulSoup para analisar o HTML
soup = BeautifulSoup(response.content, 'html.parser')

pdf_links = []
for link in soup.find_all('a', href=True):
    if link['href'].endswith('.pdf'):
        pdf_links.append(link['href'])

# Baixar os arquivos PDF
for pdf_url in pdf_links:
    file_name = pdf_url.split('/')[-1]
    pdf_response = requests.get(pdf_url)
    with open(file_name, 'wb') as f:
        f.write(pdf_response.content)
    print(f"Arquivo {file_name} baixado com sucesso!")
