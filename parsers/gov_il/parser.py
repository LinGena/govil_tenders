from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from parsers.get_undetected_driver import Undetected
from db.core import PostgreSQLTable


class ParseGovIl(Undetected):
    def __init__(self):
        super().__init__()
        self.domain = 'https://www.gov.il'
        self.db_client = PostgreSQLTable('tamrur_govil')
        self.skip_pages = 0

    def run(self):
        try:
            self._parse()
        except Exception as ex:
            self.logger.error(ex)
        finally:
            self.close_driver()

    def get_url(self) -> str:
        url = self.domain + '/he/collectors/policies?Type=30280ed5-306f-4f0b-a11d-cacf05d36648'
        now = datetime.today()
        from_date_delta = now - timedelta(days=30)
        from_date = from_date_delta.strftime("%Y-%m-%d")
        to_date = now.strftime("%Y-%m-%d")
        link = f'{url}&FromDate={from_date}&ToDate={to_date}'
        if self.skip_pages > 0:
            link = link + f'&skip={self.skip_pages}'
        return link

    def _parse(self):
        self.parse_next_page = False
        src = self.get_page_content(self.get_url(), '//*[@id="Results"]')
        if src:
            self.get_datas(src)
            if self.parse_next_page:
                self.skip_pages += 10
                return self._parse()

    def get_page_content(self, url: str, xpath: str) -> str:
        self.driver.get(url)
        time.sleep(3)
        try:
            self.wait(20, (By.XPATH, xpath))
            return self.driver.page_source
        except TimeoutException:
            raise Exception(f'Something wrong with xpath: {xpath}')
        
    def get_datas(self, page_content: str):
        soup = BeautifulSoup(page_content, 'html.parser')
        result = soup.find('div', id='Results')
        if not result:
            raise Exception('There is not Results block')
        list_items = result.find_all('div', class_='mb-3')
        for list_item in list_items:
            try:
                link = self.domain + list_item.find('a').get('href')
                if self.db_check_link(link):
                    continue
                print('---',link)
                page_data = {}
                page_data['url'] = link
                page_data['title'] = list_item.find('h3').text.strip()
                page_data['description'] = self.get_description(link)
                page_data['decision_number'] = self.get_span_value(list_item, "promotedData_2_0")
                page_data['decision_type'] = self.get_span_value(list_item, "promotedData_0_0")
                page_data['committees'] = self.get_span_value(list_item, "metaData_2_0")
                page_data['publication_date'] = self.convert_to_datetime(self.get_span_value(list_item, "publishDate_0"))
                self.db_client.insert_row(page_data)
                self.logger.info('New entry added')
                self.parse_next_page = True
            except Exception as e:
                print(e)

    def db_check_link(self, link: str) -> bool:
        data = {"url": link}
        if not self.db_client.get_row(data):
            return False
        return True
    
    def convert_to_datetime(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except Exception as ex:
            print(ex)
        return None 

    def get_span_value(self, soup: BeautifulSoup, id_part: str) -> str:
        target_span = soup.find("span", id=lambda x: x and id_part in x)
        if target_span:
            return target_span.text.strip()
        return ''
    
    def get_description(self, url: str) -> str:
        try:
            src = self.get_page_content(url, '//*[@id="root"]')
            if src:
                soup = BeautifulSoup(src, 'html.parser')
                result = soup.find('div', id='root')
                return result.get_text()
        except Exception as ex:
            self.logger.error(ex)
        return ''




