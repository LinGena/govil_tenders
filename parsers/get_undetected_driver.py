import os
import uuid
import time
import shutil
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.logger import Logger


class Undetected():
    def __init__(self):
        self.logger = Logger().get_logger(__name__)
        self.install_driver()

    def install_driver(self):
        self.start_displat()
        self.get_options()
        self.get_driver()

    def start_displat(self):
        self.display = Display()
        self.display.start()
    
    def get_options(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--allow-insecure-localhost')

    def get_driver(self):
        self.folder_temp = os.path.join(os.getcwd(), f"chrome_temp/temp_{uuid.uuid4().hex}")
        os.makedirs(self.folder_temp, exist_ok=True)
        time.sleep(1)
        self.driver = uc.Chrome(version_main=int(os.getenv('CHROME_VERSION')),
                                user_data_dir=self.folder_temp,
                                options=self.options)
        self.wait = lambda time_w, criteria: WebDriverWait(self.driver, time_w).until(
            EC.presence_of_element_located(criteria))

    def __del__(self):
        self.close_driver()

    def close_driver(self):
        try:
            self.driver.close()
        except:            
            pass
        try:
            self.driver.quit()
        except:            
            pass
        try:
            self.display.stop()
        except:            
            pass
        try:
            time.sleep(1)
            if hasattr(self, "folder_temp") and self.folder_temp:
                if os.path.exists(self.folder_temp):
                    shutil.rmtree(self.folder_temp) 
        except:            
            pass

    def move_and_click(self, element):
        chain = ActionChains(self.driver)
        chain.reset_actions()
        if element is not None:
            chain.move_to_element(element)
            chain.click()
        chain.perform()
        chain.reset_actions()