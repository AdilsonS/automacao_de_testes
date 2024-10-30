import pathlib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions

#Função criada para obter webdriver do Chrome, no meu ambiente estava tendo erro ao obter como indicado na aula, por isso a necessidade dessas tratativas.
def start_driver():
    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    except:
        chrome_driver_path = "/home/adilson/.cache/selenium/chromedriver/linux64/130.0.6723.69/chromedriver"
        chrome_binary_path = "/usr/bin/google-chrome"
        
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary_path
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    finally:
        return driver

def test():
    try:
        driver = start_driver()        
        file_path = pathlib.Path(__file__).parent / "sample-exercise.html"
        driver.get(f"file://{file_path}")
        
        title = driver.title
        assert title == "Sample page"
        time.sleep(2)
        
        text_box = driver.find_element(by=By.ID, value="input")
        generate_button = driver.find_element(by=By.NAME, value="generate")
        submit_button = driver.find_element(by=By.NAME, value="button")
        
        generate_button.click()        
        generated_value = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located( (By.ID, "my-value") )
        )
        generated_text = generated_value.text
        
        text_box.clear()
        text_box.send_keys(generated_text)
        submit_button.click()
        time.sleep(2)
        
        alert = WebDriverWait(driver, 5).until(
            EC.alert_is_present()
        )
        alert.accept()
        
        message = driver.find_element(by=By.ID, value="result")
        value = message.text
        assert value == f"It workls! {generated_text}!"
        time.sleep(2)        
    finally:
        driver.quit()
