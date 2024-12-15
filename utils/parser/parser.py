import time
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, browser: str = "firefox", hide_browser: bool = True):
        self.browser = browser
        self.hide_browser = hide_browser

    async def __format_results(self, res: list[Any]) -> str:
        output = list()
        for i in range(len(res)):
            res[i] = res[i].text
        for x in res:
            if x not in output:
                output.append(x)
        return "\n".join(output)

    async def __generate_driver(self):
        if self.browser == "firefox":
            if self.hide_browser:
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument("--headless")
                driver = webdriver.Firefox(options=firefox_options)
            else:
                driver = webdriver.Firefox()
        elif self.browser == "chrome":
            if self.hide_browser:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(options=chrome_options)
            else:
                driver = webdriver.Chrome()
        else:
            raise ValueError("Browser must be either 'firefox' or 'chrome'")
        return driver

    async def __get_data_from_pop_up_buttons(self, id_button: str, wait_time: int = 3) -> list[Any]:
        driver = await self.__generate_driver()
        driver.get("https://collegetsaritsyno.mskobr.ru/postuplenie-v-kolledzh/priemnaya-komissiya")
        time.sleep(wait_time)
        element = driver.find_element(By.ID, id_button)
        driver.execute_script("arguments[0].scrollIntoView()", element)
        action = ActionChains(driver)
        time.sleep(wait_time)
        action.click(on_element=element)
        action.perform()
        html = driver.page_source
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