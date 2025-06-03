# Tratamento de_ elatorio eLog pf

Painel de tratamento de arquivo lista_bens gerado pelo eLog e exportar arquivo padronizado para consumo em outras aplicações.

## Processamento de Listagem geral de bens do eLog

Atualmente a tecnologia utilizada é o painel streamlit, onde o arquivo é carregado manualmente pelo usuário.

- Extract: Aplicativo python que digere um arquivo exportado pelo sistema de gestão patrimonial eLog.
- Transform: Transforma os dados, compila e reordena as colunas, preenche os dados vazios.
- Load: Faz o download do arquivo padronizado para enviar para o painel do BI na intranet do Órgão.

![image](https://github.com/user-attachments/assets/a0f1ede0-0987-457d-acb7-d4ef048b69df)

## Instalação
"""bash
python -m venv .venv
poetry init
pyenv local 3.13.0
poetry shell
poetry install
"""
