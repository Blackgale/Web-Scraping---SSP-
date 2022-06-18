import pandas as pd
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time as time
import pandas as pd

# Abrindo o navegador
url = 'http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx'
browser = webdriver.Chrome(executable_path= r'.\chromedriver.exe')
browser.get(url)
git remote add origin https://github.com/Blackgale/Web-Scraping---SSP-.git


################## Selecionando a tabela de interesse através do click

#### Task 1 - Clicar no botão : Ocorrencias registradas por Mês
browser.find_element_by_xpath('//*[@id="conteudo_btnMensal"]').click()


################## Buscando as informações necessárias

# Task 2 - Fixar a lista de colunas do dataframe final
lista_indicadores = ['Ano', 'Municipio', 'Região']
for i in range(2,25):
    temp = browser.find_element_by_xpath('//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr['+str(i)+']/td[1]').text
    lista_indicadores.append(temp)
    
    
# Task 3 - Buscar todas as regioes do dropdown
lista_regioes  = browser.find_element_by_xpath('//*[@id="conteudo_ddlRegioes"]').text.split('\n')
lista_regioes.remove('Todos') # Remover das opções o valor "Todos"

################## Cria um dataframe vazio com as colunas que utilizamos

# Task 4 -  cria um dataframe vazio com a lista de colunas
df = pd.DataFrame(columns=lista_indicadores)


for regiao in lista_regioes:
    
    # Seleciona o valor da regiao no dropdown de regiões
    browser.find_elements_by_xpath('//*[@id="conteudo_ddlRegioes"]')[0].send_keys(regiao)

    time.sleep(0.1)

    # Busca as cidades disponiveis na regiao selecionada
    lista_mun = browser.find_elements_by_xpath('//*[@id="conteudo_ddlMunicipios"]')[0].text.split('\n')
    lista_mun.remove('Todos')
    
    print(regiao)
    
    for muncipio in lista_mun:
        
        ############################################## Busca valores da tabela 2020
        lista_valores = [2020,muncipio,regiao]
        
        for i in range(2,25):

            # Dados de 2020
            temp = browser.find_element_by_xpath('//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr['+str(i)+']/td[14]').text
            lista_valores.append(int(temp.replace('.','')))
            
        # Cria o dataframe temporario com uma linha para esta cidade - 2020   
        df_temp = pd.DataFrame([lista_valores], columns = lista_indicadores)
        df = df.append(df_temp)

            
        ############################################## Busca valores da tabela 2019
        lista_valores = [2019,muncipio,regiao]   
        
        for i in range(2,25):  
            # Dados de 2019
            temp = browser.find_element_by_xpath('//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr['+str(i)+']/td[14]').text
            lista_valores.append(int(temp.replace('.','')))
        
        # Cria o dataframe temporario com uma linha para esta cidade - 2019   
        df_temp = pd.DataFrame([lista_valores], columns = lista_indicadores )
        df = df.append(df_temp)
        
    time.sleep(0.1)
   
   
print(df.head())

path = 'web_scraper_seguranca.xlsx'

print(path)

df.to_excel(path, index= False)