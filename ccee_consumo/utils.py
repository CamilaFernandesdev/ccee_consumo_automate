import pymongo
import pandas as pd
from pathlib import Path


def consumo_tableau_data(filepath):
    path = Path(filepath)

    # Não alterar o método de leitura apenas assim que funciona
    df = pd.read_csv(path, encoding='UTF-16', sep='\t')
    # Date
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    # Tratando os dados de consumo
    df['Consumo (MWm)'] = df['Consumo (MWm)'].str.replace('.','').str.replace(',','.')
    df['Consumo (MWm)'] = pd.to_numeric(df['Consumo (MWm)']).round(5)

    if df.shape[1] == 8:
        df.rename(columns={
            'Data': 'dia',
            'Classe': 'classe',
            'Ambiente': 'ambiente',
            'Ramo de Atividade': 'ramo_de_atividade',
            'Submercado': 'submercado',
            'UF': 'unidade_federativa',
            'Status Migração': 'status_migracao',
            'Consumo (MWm)': 'MW_MED'
    
        }, inplace=True)   
    else:
        print('Os dados sofreram modificação!')

    return df

def mongo_connect(COLLECTION):
    """Create a MongoClient instance and connect to the MongoDB server."""
    client = pymongo.MongoClient("mongodb://user_rw:us3r_rw@nwautomhml/")
    db = client["historico_oficial"]
    collection = db[COLLECTION]
    return collection
    
def update_document_mongo(df: pd.DataFrame, collection: str, batch_size: int) -> dict:
    """Iterate over the rows of the DataFrame and insert each batch of documents."""
    for i in range(0, len(df), batch_size):
        batch = list(df.iloc[i:i+batch_size].to_dict('records'))
        collection = mongo_connect(COLLECTION)
        collection.insert_many(batch)
    
    
    
if __name__ == "__main__":
      
    FILEPATH = 'C:/Users/E805511/Downloads/Detalhamento - Dados (7).csv'
    COLLECTION = 'ccee_consumo_tableau'
    BATCH_SIZE = 1000
    
    df = consumo_tableau_data(FILEPATH)
    documents = update_document_mongo(df, COLLECTION, BATCH_SIZE)
