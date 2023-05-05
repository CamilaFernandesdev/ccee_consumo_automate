"""Script para a DAG."""
from ccee_consumo.data.detalhamento_dados import DetalhamentoDados
from ccee_consumo.mongo.update_mongo import UpdateMongo


 # VARIÁVEIS
COLLECTION = "ccee_consumo_tableau"
DICIONARIO = {
    "dia": ["(?i)^data[s]?$"],
    "classe": ["(?i)^Classe[s]?$"],
    "ambiente": ["(?i)^Ambiente[s]?$"],
    "ramo_de_atividade": ["(?i)^ramo[s]? *de *atividade[s]?$"],
    "submercado": ["(?i)^Submercado[s]?$"],
    "unidade_federativa": ["(?i)^[Uu][Ff]?$", "(?i)^Estado[s]?$"],
    "status_migracao": [
        "(?i)^Status *[de]? *Migração$",
        "(?i)^Status *[de]? *Migracao$",
    ],
    "MW_MED": ["(?i)^Consumo *\\([Mm][Ww][Mm]\\)$"],
}

def atualizar_dados_mongo():
    """Processo de automatização.

    Parameters
    ----------
        df : pd.DataFrame
            DESCRIPTION.
        collection : str
            DESCRIPTION.
        dicionario : dict [str: list[str]]


    Returns
    -------
    None.
    """
   

    # Localiza, lê os dados e retorna um dataframe
    df = DetalhamentoDados().detalhamento_dados()
    
    # Passos para a aulização dos dados no mongo
    # Os métodos retornam as variáveis para verificação e encontrar de erros
    update_mongo = UpdateMongo(df=df, collection=COLLECTION, dicionario=DICIONARIO)
    update_mongo.last_document_information()
    update_mongo.verification_methods(columns_number=8)
    update_mongo.dados_para_upload()
    update_mongo.update_mongo()
