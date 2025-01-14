import asyncio
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Parser:
    def __init__(self, browser: str = "firefox", hide_browser: bool = True):
        self.browser = browser
        self.hide_browser = hide_browser
        self.driver = self.__create_driver()

    async def __format_results(self, res: list[Any]) -> str:
        output = list()
        for i in range(len(res)):
            res[i] = res[i].text
        for x in res:
            if x not in output:
                output.append(x)
        return "\n".join(output)

    def __create_driver(self):
        if self.browser == "firefox":
            if self.hide_browser:
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--headless")
                firefox_options.add_argument("--allow-hosts localhost")
                firefox_options.add_argument('--no-sandbox')
                firefox_options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),
                                           options=firefox_options)
            else:
                driver = webdriver.Firefox()
        elif self.browser == "chrome":
            if self.hide_browser:
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--allow-hosts localhost")
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                          options=chrome_options)
            else:
                driver = webdriver.Chrome()
        else:
            raise ValueError("Browser must be either 'firefox' or 'chrome'")
        return driver

    async def __get_data_from_pop_up_buttons(self, id_button: str, wait_time: int = 5) -> list[Any]:
        self.driver.get("https://collegetsaritsyno.mskobr.ru/postuplenie-v-kolledzh/priemnaya-komissiya")
        await asyncio.sleep(wait_time)
        element = self.driver.find_element(By.ID, id_button)
        self.driver.execute_script("arguments[0].scrollIntoView()", element)
        action = ActionChains(self.driver)
        await asyncio.sleep(wait_time)
        action.click(on_element=element)
        action.perform()
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        res = list(soup.find("div", {"id": id_button}).find_all(["span", "a", "p"]))
        return res

    async def get_docs_list(self):
        result = await self.__get_data_from_pop_up_buttons("lrjg173cfr")
        return await self.__format_results(result)

    async def get_work_schedule(self):
        result = await self.__get_data_from_pop_up_buttons("p2vxdz3j2y")
        return await self.__format_results(result)

    async def get_postpoint_from_army(self):
        result = await self.__get_data_from_pop_up_buttons("f99i0vemzv")
        return await self.__format_results(result)
