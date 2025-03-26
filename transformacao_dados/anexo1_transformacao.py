import pdfplumber
import os
import pandas as pd
import zipfile

pdf_path = os.path.join('.', 'anexos', 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf')

tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()

        if table:
            df_page = pd.DataFrame(table[1:], columns=table[0])  # Ignora a primeira linha se for cabeçalho duplicado
            tables.append(df_page)

# juntar todas as tabelas em um unico lugar
df_total = pd.concat(tables, ignore_index=True)
# Replace é um metodo panda que altera valores definidos dentro das tabelas.
df_total.replace({'OD': 'Odontologia', 'AMB': 'Ambulatorial'}, inplace=True)

os.makedirs('transformacao_dados/saida', exist_ok=True)
csv_path = 'transformacao_dados/saida/Teste_AldairJoseTenorioMoreiraJunior.csv'
df_total.to_csv(csv_path, index=False)

zip_path = 'transformacao_dados/saida/Teste_AldairJoseTenorioMoreiraJunior.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write(csv_path, arcname=os.path.basename(csv_path))

print(f"Transformação finalizada. Arquivo salvo e compactado em: {zip_path}")
