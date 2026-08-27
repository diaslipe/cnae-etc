# cnae-etc

A Python library focused on automating the extraction, transformation, and consolidation (ETC) pipeline for the open dataset of the National Registry of Legal Entities (CNPJ), publicly released by the Ministry of Finance. The library processes large volumes of data via chunks, optimized for low memory machines, extracts company data based on CNAE codes for primary and/or secondary activities, standardizes encodings, and unifies tables into formats optimized for analysis, such as Parquet and relational databases.

## Authors

- [@felipe_dias](https://github.com/diaslipe)

## Requirements and Installation

1. First, make sure Python is installed on your computer. Press `Win + R`, type `cmd`, and press Enter to open the Windows Command Prompt. Then, run the following command:
```bash
python --version
```
If Python is installed, it will display the version number. Ensure you are using a modern version of Python. You can download the latest version from the official [website](https://www.python.org/).

If you see an error like `'python' is not recognized as an internal or external command`, Python is either not installed or not added to your system's PATH.

2. Install the JupyterLab environment by running the following command in your terminal:
```bash
pip install jupyterlab
```

3. Install this library directly from GitHub by running:
```bash
pip install git+https://github.com/diaslipe/cnae-etc.git
```
