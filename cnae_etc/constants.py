"""
Global constants for data extraction.
Constantes globais para a de extração de dados.

This file centralizes fixed values such as CNAEs of interest,
target columns, delimiters, encoding, and chunk size.
Este arquivo centraliza valores fixos como CNAEs de interesse,
colunas alvo, delimitadores, codificação e tamanho de fatia de dados.
"""


# Set of aquaculture interest CNAEs
# Conjunto de CNAEs de interesse para aquicultura
AQUACULTURE_CNAES = {'0321301','0321302','0321303','0321304','0321305','0321399','0322101','0322102','0322103','0322104','0322105','0322106','0322107','0322199'}

# Target columns in the bigdata that has CNAEs
# Colunas alvo no bigdata que contém CNAEs
TARGET_COLUMNS = [11,12]

# Column delimeter
# Delimitador de colunas 
SEP = ';'

# Bigdata's file encoding
# Codificação do arquivo bigdata
ENCODING = 'latin1'

# Data slice size processed each time
# Tamanho da fatia de dados processada por vez
CHUNKSIZE = 500000
