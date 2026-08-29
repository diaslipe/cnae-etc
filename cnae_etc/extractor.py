import os  
import pandas as pd 
from constants import AQUACULTURE_CNAES, TARGET_COLUMNS, SEP, ENCODING, CHUNKSIZE

def extract_values(month_year: str, src: str):
    """
    Extract rows from a large Brazilian dataset based on fixed interest CNAEs.
    Extrai linhas de um dataset brasileiro grande com base em CNAEs fixos de interesse.
    """

    # garante que a pasta 'extracted' existe
    os.makedirs("extracted", exist_ok=True)

    # define caminho completo do arquivo de saída
    output_path = os.path.join("extracted", f"extracted_{month_year}.csv")

    # se já existir arquivo com esse nome, cria sufixos _00, _01...
    if os.path.exists(output_path):
        i = 0
        while True:
            candidate = os.path.join("extracted", f"extracted_{month_year}_{i:02d}.csv")
            if not os.path.exists(candidate):
                output_path = candidate
                break
            i += 1

    # inicializa arquivo vazio com separador definido
    pd.DataFrame().to_csv(output_path, index=False, header=False, sep=SEP)

    total_extracted = 0  # contador de linhas extraídas
    n_chunk = 0          # contador de blocos lidos

    # leitura do arquivo em chunks (blocos) para não estourar memória
    for chunk in pd.read_csv(src, sep=SEP, encoding=ENCODING,
                             dtype=str, chunksize=CHUNKSIZE, engine="python",
                             on_bad_lines="skip", header=None, quotechar='"'):

        n_chunk += 1  # incrementa número do chunk

        # diagnóstico do primeiro chunk
        if n_chunk == 1:
            print(f"🔍 Chunk 1 detected with {len(chunk.columns)} columns using sep='{SEP}'")
            if len(chunk.columns) < max(TARGET_COLUMNS) + 1:
                print("⚠️ Possible parsing issue — fewer columns than expected.")

        # seleciona colunas válidas
        cols = [c for c in TARGET_COLUMNS if c < len(chunk.columns)]
        if not cols:
            print(f"⚠️ No valid columns found in chunk {n_chunk}. Skipping...")
            continue

        # normaliza colunas alvo (remove espaços extras)
        for col in cols:
            chunk[col] = chunk[col].astype(str).str.strip()

        # cria flags de interesse (verifica se CNAE está na lista)
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

