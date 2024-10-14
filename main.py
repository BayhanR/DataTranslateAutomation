import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Selenium Setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.deepl.com/en/translator")

def csv_isle_ve_kaydet(giris_dosya, cikis_dosya):
    # CSV dosyasını oku
    df = pd.read_csv(giris_dosya)

    # İşlenecek veriler listesi
    yeni_veriler = []

    # CSV dosyasındaki her bir satırı gezinme
    for index, row in df.iterrows():
        article = row['article']
        summary = row['highlights']

        # Çeviri işlemi
        cevrilmis_article = translate(article)
        cevrilmis_summary = translate(summary)

        # Yeni verileri listeye ekleme
        yeni_veriler.append({
            'id': index + 1,
            'translated_article': cevrilmis_article,
            'translated_summary': cevrilmis_summary
        })

    # Yeni DataFrame oluşturma
    yeni_df = pd.DataFrame(yeni_veriler)

    # Dosya yoksa başlıklarıyla birlikte yeni bir CSV dosyası oluştur
    if not os.path.isfile(cikis_dosya):
        print(f"Dosya '{cikis_dosya}' oluşturuluyor...")
        yeni_df.to_csv(cikis_dosya, mode='w', header=True, index=False)
    else:  # Dosya varsa üzerine veri ekle
        print(f"Dosya '{cikis_dosya}' mevcut. Veriler ekleniyor...")
        yeni_df.to_csv(cikis_dosya, mode='a', header=False, index=False)

def translate(text):
    try:
        input_area = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="textareasContainer"]/div[1]/section/div/div[1]/d-textarea/div[1]')))
        input_area.click()

        # Metni temizleyip gönder
        input_area.clear()
        input_area.send_keys(text)
        time.sleep(5)

        # Çevirilen metni alma
        output_area = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="textareasContainer"]/div[3]/section/div[1]/d-textarea/div/p'))
        )
        translatedText = output_area.get_attribute('innerText')
        print("Çevirilen Metin:", translatedText)
        return translatedText
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return text  # Hata olursa orijinal metni döndür

# Çalıştırma
csv_isle_ve_kaydet(
    r'C:\Users\hp\source\repos\PYTHON\cnn_dailymail\test.csv',  
    r'C:\Users\hp\source\repos\PYTHON\cnn_dailymail\texsResukt.csv'
)
