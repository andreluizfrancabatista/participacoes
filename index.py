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
from selenium.webdriver.support.ui import Select
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
wd_Chrome.get("https://www.igrejacristamaranata.org.br/ebd/participacoes/") 
form = WebDriverWait(wd_Chrome, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#icmEbdNacionalForm")))

#CPF
row_cpf = wd_Chrome.find_element(By.CSS_SELECTOR, '.field-cpf')
field_cpf = row_cpf.find_element(By.TAG_NAME, 'input')
field_cpf.send_keys('01411769627')

# FUNÇÃO
# member = WebDriverWait(wd_Chrome, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='icmEbdNacionalForm']/div[3]/div[4]/div[1]/div/div[2]/div/div[1]")))
# member.click()


# Participação
participacao = WebDriverWait(wd_Chrome, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='icmEbdNacionalForm']/div[5]/div/div[1]/input[2]")))
participacao.click()
participacao = WebDriverWait(wd_Chrome, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='icmEbdNacionalForm']/div[5]/div/div[2]/div/div[2]/div[1]/p")))
participacao.send_keys('Minha participação')
participacao = WebDriverWait(wd_Chrome, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='icmEbdNacionalForm']/div[6]/div/div/div/label")))
participacao.click()
time.sleep(5)
wd_Chrome.save_screenshot('screen.png')
wd_Chrome.quit()
