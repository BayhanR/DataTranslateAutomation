import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.maximize_window()


driver.get("https://www.deepl.com/en/translator")


df = pd.read_csv(r'C:\Users\hp\source\repos\PYTHON\cnn_dailymail\test.csv')


translated_articles = []
translated_highlights = []

try:

    input_area = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="textareasContainer"]/div[1]/section/div/div[1]/d-textarea/div[1]')))
    input_area.click()


    input_text = "Testing, testing . Everything seems to be in order"
    input_area.clear()
    input_area.send_keys(input_text)
    time.sleep(5)

    output_area = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="textareasContainer"]/div[3]/section/div[1]/d-textarea/div/p'))
    )

    translated_text = output_area.get_attribute('innerText')
    print("Çevirilen Metin:", translated_text)

except Exception as e:
    print(f"Bir hata oluştu: {e}")
finally:
    driver.quit()