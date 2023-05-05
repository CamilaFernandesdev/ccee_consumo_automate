from ccee_consumo.tableau.tableau_scraper import TableauScraper

# CONSTANTES - URL E ELEMENTOS DA TELA
URL = "https://www.ccee.org.br/web/guest/dados-e-analises/consumo"
SELECT_CSV = ".f81g0pf:nth-child(2)"
COOKIES_XPATH = '//*[@id="alertaCookie"]/div/div[3]/button'
ICONE_DOWNLOAD = '//*[@id="download-ToolbarButton"]/span[1]'
DETALHAMENTO_DADOS = ".f7ypqvd"
TABELA_REFERENCIA_CRUZADA = ".fdofgby:nth-child(4)"
DASHBOARD_DOWNLOAD_DADOS = ".tabLastPoint .tabScrollerContentWindow"


cookie = "btn btn-primary btn-lg box-cookie__button"
def tableau_consumo_download_data(view_screen=False, download_temporary_folder=True):
    """Descreva."""
    tableau_scraper = None

    try:
        tableau_scraper = TableauScraper(
            URL,
            view_screen=view_screen,
            download_temporary_folder=download_temporary_folder,
        )
        tableau_scraper.accept_cookies()
        tableau_scraper.select_tableau_dashboard(DASHBOARD_DOWNLOAD_DADOS)
        tableau_scraper.select_tableau_rodape()
        # click elements tableu
        tableau_scraper.find_element("xpath", ICONE_DOWNLOAD)
        tableau_scraper.find_element("css", TABELA_REFERENCIA_CRUZADA)
        tableau_scraper.find_element("css", SELECT_CSV)
        print("Started download, wait 3 minutes.")
        tableau_scraper.find_element("css", DETALHAMENTO_DADOS, 180)
        
    finally:
        if tableau_scraper is None:
            print("O objeto tableau_scraper não foi criado corretamente")

        else:
            tableau_scraper.close()
            print("Chrome closed.")


tableau_consumo_download_data(True, False)
