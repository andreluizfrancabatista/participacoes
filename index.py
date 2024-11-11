from datetime import datetime, timedelta
import pytz
import re
import sys
import os
import numpy as np

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
options.add_argument('--enable-unsafe-swiftshader')


# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

"""# Importando as Bibliotecas"""

import pandas as pd
import time
from tqdm import tqdm

"""# Iniciando a Raspagem de Dados"""

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get("https://www.thegreyhoundrecorder.com.au/form-guides/") 
# time.sleep(2)
# wd_Chrome.save_screenshot('screen.png')
date = wd_Chrome.find_elements(By.CSS_SELECTOR, 'h2.meeting-list__title')
dia_corrida = date[0].text
print(dia_corrida)
eventos = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.meeting-list')[0]
fields = eventos.find_elements(By.CSS_SELECTOR, 'h3.meeting-row__title')
links = eventos.find_elements(By.CSS_SELECTOR, 'div.meeting-row__links')
links_list = []
# Timezones
aest_tz = pytz.timezone('Australia/Sydney')  # Sydney segue AEST
brt_tz = pytz.timezone('America/Sao_Paulo')
for link in links:
    try:
        url = link.find_element(By.CSS_SELECTOR, 'a.meetings__row-btn').get_attribute('href')
        links_list.append(url)
    except:
        print('Erro ao pegar links dos fields')
        pass
# print(links_list, len(links_list))

dados = {
    'DATE' : [],
    'TIME' : [],
    'FIELD': [],
    'RACE' : [],
    'BOX'  : [],
    'GREY' : [],
    'RTG'  : []
}

# Para percorrer apenas uma parte da lista usar --> for link in links_list[:5]:
for link in links_list:
    wd_Chrome.get(link)
    field = link.split("form-guides/")[1].split("/")[0]
    date_ = wd_Chrome.find_element(By.CSS_SELECTOR, 'h1.form-guide-meeting__heading').text
    date_ = date_.split('- ')[1]
    date_ = pd.to_datetime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_), format="%d %b %Y")
    races = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.form-guide-field-event')
    box = 'box'
    grey = 'grey'
    rtg = 'rtg'
    for race in races:
        # field já tá salvo
        # print(field)
        # race_number
        race_number = race.find_element(By.CSS_SELECTOR, 'h2.meeting-event__header-race').text
        race_number = f"R{race_number.split(' ')[1]}"
        # time --> FICOU ERRADO
        time_ = race.find_element(By.CSS_SELECTOR, 'div.meeting-event__header-time').text
        time_ = time_.split(' ')[0]
        # Convertendo a string para datetime com o fuso AEST, usando a data de hoje
        aest_time = aest_tz.localize(datetime.strptime(time_, "%I:%M%p"))
        time_ = aest_time.strftime("%H:%M")
        # get rows
        rows = race.find_elements(By.CSS_SELECTOR, 'tr.form-guide-field-selection')
        for row in rows:
            # box_number
            box_number = row.find_element(By.CSS_SELECTOR, 'img.form-guide-field-selection__rug')
            box_number = box_number.get_attribute('alt').split(' ')[1]
            # grey_name
            grey_name = row.find_element(By.CSS_SELECTOR, 'span.form-guide-field-selection__name').text
            # rtg 9th <td>
            try:
                rtg = row.find_element(By.CSS_SELECTOR, 'td:nth-child(9)').text
            except:
                rtg = ''
                pass
            dados['FIELD'].append(field)
            dados['RACE'].append(race_number)
            dados['DATE'].append(date_)
            dados['TIME'].append(time_)
            dados['BOX'].append(box_number)
            dados['GREY'].append(grey_name)
            dados['RTG'].append(rtg)

wd_Chrome.quit()
# Salvar no CSV
df = pd.DataFrame(dados)
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
df.sort_values(by=['TIME', 'FIELD', 'RACE', 'RTG'], ascending=[True, True, True, False], inplace=True)
filename = f"lista_de_corridas/corridas_do_dia_{dia_corrida.split(', ')[1]}.csv"
df.to_csv(filename, sep=";")