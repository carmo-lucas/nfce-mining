from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import dropbox
import sys

def popular_lista_nfce(url):
    return NULL


def criar_tabela(url):
    r = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    page = BeautifulSoup(r.content, 'html.parser')
    
    # Guardar Nome Estabelecimento
    conta_despesa = page.find('div', id="u20").text

    # Guardar CNPJ
    cnpj = page.find_all('div',class_='text')[0].text
    cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", cnpj).group(0)

    # Guardar Data Transação
    data_transacao = page.find('li').text
    data_transacao = re.search(r"((\d+\/){2}\d{4}\s(\d{2}:){2}\d{2})", data_transacao).group(0)

    # Lê a tabela da url
    tabela = pd.read_html(url, encoding='utf8')
    
    # Concatena as informações em um dataframe
    tabela = pd.concat(tabela)
    
    # Remove texto dos valores numéricos
    tabela['vl_total'] = tabela[1].str.replace(u"Vl. Total\s+", "")
    tabela[0] = tabela[0].str.replace(u"\(Código: \d+\)|Qtde.:|UN: |Vl. Unit.:", "")
    
    # Separa os valores em colunas
    tabela[['nome','qtde','unidade','vl_unit']] = tabela[0].str.split(pat = '[ ]{2,}', expand=True)
    
    # Remove colunas que já foram transformadas
    tabela = tabela.drop(columns=[0,1])
    
    # Troca vírgulas por pontos para futura conversão para valores numéricos
    tabela = tabela.replace(",", ".", regex=True)
    
    # Reordena colunas
    tabela = tabela[['nome','qtde','unidade','vl_unit','vl_total']]
    
    # Remove espaços das células e converte para numérico
    tabela[['qtde','vl_unit','vl_total']] = tabela[['qtde','vl_unit','vl_total']].replace(" ", "", regex=True).astype('float64')
    tabela[['conta_despesa','data_transacao']] = conta_despesa, data_transacao
    
    return tabela

def unir_tabelas():
    return NULL



