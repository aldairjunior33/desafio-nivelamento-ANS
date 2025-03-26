import pdfplumber
import os
import pandas as pd

pdf_path = os.path.join('.', 'anexos', 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf')

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n + Página {i+1}")

        table = page.extract_table()

        if table:
            df = pd.DataFrame(table[1:], columns=table[0])  # Ignora a primeira linha se for cabeçalho duplicado
            print(df.head())  # Mostra apenas as primeiras linhas da tabela
        else:
            print("⚠️ Nenhuma tabela encontrada nesta página.")