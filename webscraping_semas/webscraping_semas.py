import os
import csv
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm.notebook import tqdm


def escreve_csv(data, arquivo):
    with open(arquivo, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(data)

# Carrega os Códigos de Imóvel da CARGILL
lista_cars = pd.read_csv("semas_pa.csv", sep=";", usecols=['car'])['car'].values.tolist()
#lista_cars = lista_cars[0:30]
lista_cars

# Abre o navegador
navegador = webdriver.Chrome()

# Entra na página
navegador.get("http://car.semas.pa.gov.br/#/consulta/mapa")

time.sleep(5)

# Escolhe no ratio itens a opção Número do recibo
navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/select').send_keys("Número do recibo", Keys.ENTER)

for car in tqdm(lista_cars):

      done = True

      while done:

            try:

                  # buscador do CAR
                  navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/div[1]/input').clear()
                  
                  navegador.find_element(By.XPATH, '//*[(@placeholder="UF-1302405-E6D3.395B.6D27.4F42.AE22.DD56.987C.DD52")]').send_keys(car, Keys.ENTER)
                  
                  time.sleep(1)
                  
                  # verificador de CAR não encontrado
                  try:
                        navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/div[2]/ul/li/div[2]')
                  except:
                        notcar = navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/div[2]/ul/li')
                        print(f'{car}: {notcar.text}')
                        break
                  
                        
                  time.sleep(1)

                  # centralizar no mapa a fazenda de interesse
                  navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/div[2]/ul/li/div[1]/i[2]').click()

                  time.sleep(1)

                  # botão de fazenda clicável
                  navegador.find_element(By.XPATH, '//*[@id="mapa-principal"]/div[1]/div[2]/div[3]/img').click()

                  time.sleep(1)

                  # clicar no botão da ficha do imóvel
                  navegador.find_element(By.XPATH, '//*[@id="mapa-principal"]/div[1]/div[2]/div[4]/div[2]/div[1]/div/div/button[2]').click()

                  time.sleep(1)

                  # Domínio
                  navegador.find_element(By.XPATH, '//*[@id="modalFichaImovelResumida"]/div/div/div[2]/ul/li[3]/a').click()

                  time.sleep(1)

                  # pegar formulário de nome
                  nome = navegador.find_element(By.XPATH, '//*[@id="dominio"]/table/tbody/tr[1]/td')

                  # pegar formulário de cpf
                  cpf = navegador.find_element(By.XPATH, '//*[@id="dominio"]/table/tbody/tr[2]/td')

                  # pegar formulário de tipo de pessoa física ou jurídica
                  tipo = navegador.find_element(By.XPATH, '//*[@id="dominio"]/table/tbody/tr[3]/td')

                  # informações concatenadas
                  data = (car, nome.text, cpf.text, tipo.text)

                  # fechar a janela da ficha do imóvel
                  navegador.find_element(By.XPATH, '//*[@id="modalFichaImovelResumida"]/div/div/div[1]/button').click()

                  time.sleep(1)
                  
                  # nome ou caminho do arquivo gerado e função de incremento no csv
                  arquivo = "semas_pa_dominial.csv"
                  escreve_csv(data, arquivo)

                  done = False

            except:
                  print(f'erro em puxar informação do {car}')

                  navegador.close()

                  navegador = webdriver.Chrome()

                  time.sleep(3)
                  #navegador.close()
                  #navegador = webdriver.Chrome()
                  navegador.get("http://car.semas.pa.gov.br/#/consulta/mapa")

                  time.sleep(5)

                  # Escolhe no ratio itens a opção Número do recibo
                  navegador.find_element(By.XPATH, '//*[@id="consultaMapa"]/div[2]/div[5]/fieldset[1]/div/select').send_keys("Número do recibo", Keys.ENTER)


navegador.close()