"""Automatização: Consumo CCEE."""

import logging
from datetime import datetime
from airflow.decorators import dag
from airflow.decorators import task



@dag(
    schedule_interval="@weekly",
    start_date=datetime(2023, 5, 6),
    catchup=False,
    tags=["consumo_energetico", "CCEE", "MongoDB", "PowerBI", "SharePoint"],
)
def ccee_consumo():
    """DAG de geração da collection 'ccee_geracao_tableau'."""

    @task
    def automate_download_data():
        from ccee_consumo.tableau.script_download import tableau_consumo_download_data

        return tableau_consumo_download_data()

    @task
    def update_mongo():
        from ccee_consumo.mongo.script import atualizar_dados_mongo

        return atualizar_dados_mongo()

    @task
    def update_sharepoint():
        from ccee_consumo.sharepoint.script import atualizar_dados_sharepoint

        return atualizar_dados_sharepoint()
    
    @task 
    def delete_file():
        from ccee_consumo.data.detalhamento_dados import DetalhamentoDados
        
        return DetalhamentoDados().delete_file()
    
    automate_download_data() >> update_mongo() >> update_sharepoint() >> delete_file()


dag = ccee_consumo()
