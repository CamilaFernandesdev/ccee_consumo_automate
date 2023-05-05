"""Automatização sharepoint."""

from infra_copel import SharepointSiteCopel
from ccee_consumo.utils import DetalhamentoDados

SITE_SHAREPOINT = "PowerBIInsightsComercializacao"
FOLDER_CONSUMO_CCEE = "Base de Dados/consumo_energia_ccee"
DATA_CONSUMO_CCEE = "Detalhamento - Dados.csv"


def atualizar_dados_sharepoint() -> None:
    """Script para a DAG."""
    # Busca e leitura dos dados
    df = DetalhamentoDados().detalhamento_dados()
    
    sp = SharepointSiteCopel(SITE_SHAREPOINT)
    sp.write_df_to_csv(df, FOLDER_CONSUMO_CCEE, DATA_CONSUMO_CCEE, index=False)
