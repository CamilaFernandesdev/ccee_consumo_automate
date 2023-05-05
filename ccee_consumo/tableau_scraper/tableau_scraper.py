"""
Tableau geralmente usa uma técnica chamada "embbeding" para exibir suas visualizações.
O que significa que as visualizações são exibidas em um iframe separado em vez de diretamente
no código HTML da página.
"""

import time
import tempfile
import logging

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger('teste')
logger.propagate = False



class TableauScraper:
    def __init__(self, url, view_screen: bool = False, download_temporary_folder: bool = True):
        """
        Initialize the TableauScraper class.

        Parameters
        ----------
        url : str
            URL of the webpage to be scraped.
        view_screen : bool, optional
            Whether to show the screen when running or not, by default False.
        """
        self._url = url
        self._view_screen = view_screen
        self._download_temporary_folder = download_temporary_folder

        self.driver = self._open_chrome()
        time.sleep(30)
        self.driver.get(self._url)
        time.sleep(30)
        logger.info("Entered website")

    def _open_chrome(self):
        """
        Open Chrome using Selenium WebDriver.

        Parameters
        ----------
        view_screen : bool, optional
            Whether to show the screen when running or not, by default False.

        Returns
        -------
        WebDriver
            A Chrome WebDriver object.
        """
        options = ChromeOptions()

        if self._view_screen == False:
            options.add_argument("--headless=new")

        # Se False o arquivo tem como local de destino a pasta de downloads
        if self._download_temporary_folder:
            temp_dir = tempfile.gettempdir()
            preference_local_download = {
                "download.default_directory": temp_dir}
            options.add_experimental_option("prefs", preference_local_download)

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-session-crashed-bubble")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument(
            "--disable-features=IsolateOrigins,site-per-process")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")


        driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
        return driver

    def accept_cookies(self, cookies_xpath: str = None) -> None:
        """Para aceitar os cookies.

        Parameters
        ----------
        cookies_xpath: str
            Caminho xpath do banner do cookie, 
            se None executa um código JavaScript para aceitar.
            
        Steps
        -----
            1. Entre na página e em cima do botão aceitar cookies
            2. Clique com botão direito do mouse e selecione a opção Inspecionar
            3. A localização ficará marcada no DevTools
            4. Clique no botão direito do mouse novamente
            5. E copie o item selecionando na opção XPATH

        Examples
        --------
        Como aparece no DevTools, a linha selecionada:
         - <button id="onetrust-accept-btn-handler">Aceitar todos os cookies</button>

        copiado em xpath ficará assim:
            //*[@id="onetrust-accept-btn-handler"]
        """
        try:
            
            if cookies_xpath == None:
                self.driver.execute_script("setCookiePrivacyPolicyAccepted()")
            
            else:    
                cookie_btn = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, cookies_xpath))
                )
                
                cookie_btn.click()
                
            time.sleep(10)
            logger.info("Accepted cookies")
        except:
            logger.debug("No cookies banner or button dont found")

    def _open_tableau(self):
        """Switches to Tableau iframe."""
        self.driver.switch_to.frame(0)
        time.sleep(4)
        logger.info("Switching to iframe Tableau")

    def select_tableau_dashboard(self, css_selector: str):
        """Method to select the Tableau dashboard.

        Parameters
        ----------
        css_selector : str
            The CSS Selector of the Tableau dashboard on the website.

        Returns
        -------
        None

        """
        self._open_tableau()
        elements = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        elements.click()
        logger.info("Selecting dashboard and waiting downloaded page")
        time.sleep(30)

    def select_tableau_rodape(self):
        self.driver.switch_to.default_content()
        logger.info("Switching to principal page")
        self.driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(4)
        self._open_tableau()

    def find_element(self, modo: str, localizador: str, timer=10) -> None:
        """
        Method to find and select an element on a Tableau dashboard.

        Parameters
        ----------
        modo : str
            The search method to use: 'xpath' or 'css'.
        localizador : str
            The locator for the desired element.
        timer : int, optional
            The number of seconds to wait after selecting the element, by default 10 secs.

        Returns
        -------
        None
        """
        modo = str(modo).lower().strip()
        try:
            if modo == "xpath":
                element = self.driver.find_element(By.XPATH, localizador)
                element.click()
                logger.info("Selecting element in dashboard")
                time.sleep(timer)

            elif modo == "css":
                element = self.driver.find_element(
                    By.CSS_SELECTOR, localizador)
                element.click()
                logger.info("Selecting element in dashboard")
                time.sleep(timer)

            else:
                logger.error(
                    "Forneça um modo de busca: xpath ou css"
                    "ou não é posssível localizar o elemento(ícone)."
                )

        except:
            logger.error("Elements dont found")

    def close(self):
        """Quits the webdriver."""
        self.driver.quit()
        logger.info('Chrome closed.')
        
