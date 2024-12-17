import asyncio
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, browser: str = "firefox", hide_browser: bool = True):
        self.browser = browser
        self.hide_browser = hide_browser

    import asyncio

    async def __format_results(self, res: list[Any]) -> str:
        output = asyncio.Queue()

        async def process_item(item):
            try:
                item_text = await self.get_text(item)
            except Exception as e:
                print(f"Error processing item: {e}")
                return
            if item_text is not None:
                await output.put(item_text)

        tasks = [process_item(item) for item in res]

        await asyncio.gather(*tasks)

        unique_output = []
        while not output.empty():
            item = await output.get()
            if item not in unique_output:
                unique_output.append(item)
            output.task_done()

        await output.join()

        return "\n".join(unique_output)

    async def get_text(self, item: Any) -> str | None:
        await asyncio.sleep(1)
        if hasattr(item, "text"):
            return item.text
        elif isinstance(item, str):
            return item
        else:
            return None

    async def __generate_driver(self):
        driver = await asyncio.to_thread(self._create_driver)
        return driver

    def _create_driver(self):
        if self.browser == "firefox":
            if self.hide_browser:
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--headless")
                driver = webdriver.Firefox(options=firefox_options)
            else:
                driver = webdriver.Firefox()
        elif self.browser == "chrome":
            if self.hide_browser:
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(options=chrome_options)
            else:
                driver = webdriver.Chrome()
        else:
            raise ValueError("Browser must be either 'firefox' or 'chrome'")
        return driver

    async def __get_data_from_pop_up_buttons(self, id_button: str, wait_time: int = 1) -> list[Any]:
        driver = await self.__generate_driver()
        driver.get("https://collegetsaritsyno.mskobr.ru/postuplenie-v-kolledzh/priemnaya-komissiya")
        await asyncio.sleep(wait_time)
        element = await asyncio.to_thread(driver.find_element, By.ID, id_button)
        await asyncio.to_thread(driver.execute_script, "arguments[0].scrollIntoView()", element)
        action = ActionChains(driver)
        await asyncio.sleep(wait_time)
        await asyncio.to_thread(action.click, on_element=element)
        await asyncio.to_thread(action.perform)
        html = await asyncio.to_thread(lambda: driver.page_source)
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
