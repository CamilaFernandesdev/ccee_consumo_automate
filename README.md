# Automatização de Download, manipulação e atualização dos dados

Os dados são referentes ao consumo energético brasileiro fornecido pela CCEE.


## Módulos
1. Tableu Scraper

    Utilização do selenium para fazer o download dos dados disponível no site.

2. Detalhamento Dados
    Após baixado o arquivo, pega o arquivo salvo na pasta temporária 

3.  Update Mongo

    Verificação das informações no banco de dados e atualização no MongoDB
    Caso tenha novas informações

4. Sharepoint

    Atualiza a planinha disponível no sharepoint, onde a mesma é linkada com um 
    dashboard no Power BI.

Biblioteca em python para facilitar automatização de download de dados do Tableau.

## Como instalar

### Modo editável local/desenvolvimento

**No diretório onde foi clonado**, executar:
```
pip install -e .
```
Assim, o caminho local ficará no PATH do python.
