import os  
import pandas as pd 
from constants import AQUACULTURE_CNAES, TARGET_COLUMNS, SEP, ENCODING, CHUNKSIZE

def extract_data(month_year: str, src: str):
    """
    Extracts rows from the open dataset of the National Registry of Legal Entities (CNPJ) based on fixed interest CNAEs values.
    Extrai linhas do conjunto de dados aberto do Cadastro Nacional da Pessoa Jurídica (CNPJ) com base em valores fixos de CNAE.
    """

    # Ensure that a directory named 'extracted' exists to receive the extracted data
    # Garanta que existe um diretório chamado 'extracted' para receber os dados extraídos
    os.makedirs("extracted", exist_ok=True)

    # Define the output file full path
    # Defina o caminho completo do arquivo de saída
    output_path = os.path.join("extracted", f"extracted_{month_year}.csv")

    # If a file with this name already exists, make sufixes _00, _01...
    # Se já existir arquivo com esse nome, crie sufixos _00, _01...
    if os.path.exists(output_path):
        i = 0
        while True:
            candidate = os.path.join("extracted", f"extracted_{month_year}_{i:02d}.csv")
            if not os.path.exists(candidate):
                output_path = candidate
                break
            i += 1

    # Initialize an empty file with defined column delimiter (sep)
    # Inicialize um arquivo vazio com um delimitador de coluna definido (sep)
    pd.DataFrame().to_csv(output_path, index=False, header=False, sep=SEP)

    total_extracted = 0  # contador de linhas extraídas
    n_chunk = 0          # contador de blocos lidos

    # Read data source file by chunks avoiding run out of memory
    # Leia o arquivo de origem de dados em blocos para evitar esgotar a memória
    for chunk in pd.read_csv(src, sep=SEP, encoding=ENCODING,
                             dtype=str, chunksize=CHUNKSIZE, engine="python",
                             on_bad_lines="skip", header=None, quotechar='"'):

        n_chunk += 1  # incrementa número do chunk

        # First data chunk diagnostics                          
        # Diagnóstico do primeiro bloco de dados
        if n_chunk == 1:
            print(f"🔍 Chunk 1 detected with {len(chunk.columns)} columns using sep='{SEP}'")
            if len(chunk.columns) < max(TARGET_COLUMNS) + 1:
                print("⚠️ Possible parsing issue — fewer columns than expected.")

        # Select valid columns
        # Selecione colunas válidas
        cols = [c for c in TARGET_COLUMNS if c < len(chunk.columns)]
        if not cols:
            print(f"⚠️ No valid columns found in chunk {n_chunk}. Skipping...")
            continue
        
        # Normalize target columns (remove extra spaces)
        # Normalize colunas alvo (remove espaços extras)
        for col in cols:
            chunk[col] = chunk[col].astype(str).str.strip()

        # Create interest flags (check if a CNAE of interest is in the list)
        # Crie flags de interesse (verifique se um CNAE de interesse está na lista)
        flags = []
        for col in cols:
            flag = chunk[col].apply(
                lambda x: any(val.strip() in AQUACULTURE_CNAES for val in str(x).split(",")) if pd.notna(x) else False
            )
            flags.append(flag)

        # combina flags (and_or → pelo menos uma coluna tem CNAE de interesse)
        chunk["has_interest"] = pd.concat(flags, axis=1).any(axis=1)

        # filtra apenas linhas de interesse
        filtered = chunk[chunk["has_interest"]].copy()
        filtered["month_year"] = month_year  # adiciona coluna com período

        # salva linhas filtradas no arquivo de saída (append)
        filtered.to_csv(output_path, mode="a", index=False, header=False, sep=SEP)
        total_extracted += filtered.shape[0]  # atualiza contador

        print(f"Chunk {n_chunk} — Rows extracted: {filtered.shape[0]} (Total: {total_extracted})")

    # mensagem final
    print(f"\n✅ Extraction completed for {src}")
    print(f"Total rows extracted: {total_extracted}")
    print(f"File saved at: {os.path.abspath(output_path)}")

