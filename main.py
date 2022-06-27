# Dependencies -----
from bs4 import BeautifulSoup
import requests

import re
import pandas as pd

import numpy as np

import dropbox

import sys
import time


# Grupo 1 é a parte necessária
validacao_url = u"(http\:\/\/www\.fazenda\.pr\.gov\.br\/nfce\/qrcode\?p\=\d{44})(\|\d){3}\|\w{40}"
url = "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41220576189406002250651160003910901081932515|2|1|1|8172512119B92F5F4BBCF8D1E4FF617D304FD593"

def importar_lista_url_nfce():
    
    return True

def sanitizar_lista_url_nfce():
    
    return True

# Funções para extrair informações da página

def request_nfce_page(url):

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    page = BeautifulSoup(r.content, 'html.parser')
    return page

# Função para extrair metadados conta despesa, data da transação, número da nfce e cnpj
def get_metadata(page):

    cd    = fetch_expense_account(page)
    cnpj  = fetch_cnpj(page)
    dt    = fetch_transaction_date(page)
    num   = fetch_nfce_number(page)
    chave = fetch_access_key(page)
    meta = {
        "conta_despesa": cd,
        "cnpj": cnpj,
        "data_transacao": dt,
        "numero_nfce": num,
        "chave_acesso": chave
        }
    
    return meta

def fetch_expense_account(page):

    conta_despesa = page.find('div', id="u20").text
    print(conta_despesa)
    return conta_despesa

def fetch_cnpj(page):

    cnpj = page.find_all('div', class_='text')[0].text
    cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", cnpj).group(0)
    print(cnpj)
    return cnpj

def fetch_transaction_date(page):
    
    data_transacao = page.find('li').text
    data_transacao = re.search(r"((\d+\/){2}\d{4}\s(\d{2}:){2}\d{2})", data_transacao).group(0)
    return data_transacao

def fetch_nfce_number(page):
    
    numero_nfce = page.find('li').text
    numero_nfce = re.search(r"Número: (\d+)", numero_nfce).group(1)
    return numero_nfce

def fetch_access_key(page):
    
    chave_acesso = page.find("span", {"class": "chave"}).text
    chave_acesso = re.sub(" ", "", chave_acesso)
    return chave_acesso


get_metadata(page)







page = request_nfce_page(url)

cnpj = fetch_cnpj(page)
nfce = fetch_nfce_number(page)

chave = fetch_access_key(page)















def read_raw_table(url):

    tbl_suja = pd.read_html(url, encoding='utf8')
    tbl_suja = pd.concat(tbl_suja)
    return tbl_suja

# Funções para limpar os dados da tabela extraída da página
def clean_strings(tbl):

    texto_indesejado = u"\(Código: \d+\)|Qtde.:|UN: |Vl. Unit.:"

    # Remove texto dos valores numéricos
    tbl['vl_total'] = tbl[1].str.replace(u"Vl. Total\s+", "")
    tbl[0] = tbl[0].str.replace(texto_indesejado, "")
    return tbl

def separate_columns(tbl):
    # Separa os valores em colunas

    tbl[['nome', 'qtde', 'unidade', 'vl_unit']] = tbl[0].str.split(pat='[ ]{2,}', expand=True)

    # Remove colunas que já foram transformadas

    # pat='[ ]{2,}' significa dois ou mais espaços

    tbl = tbl.drop(columns=[0, 1])

    return tbl

def parse_doubles(tbl):    # Troca vírgulas por pontos para futura conversão para valores numéricos
    tbl = tbl.replace(",", ".", regex=True)
    # Remove espaços das células e converte para numérico
    tbl[['qtde', 'vl_unit', 'vl_total']] = tbl[['qtde', 'vl_unit','vl_total']].replace(" ", "", regex=True).astype('float64')
    tbl[['conta_despesa', 'data_transacao']] = conta_despesa, data_transacao
    return tbl

def clean_raw_data(tbl):
    tbl = clean_strings(tbl)
    tbl = separate_columns(tbl)
    tbl = parse_doubles(tbl)
    return tbl

def generate_items_table(url):
    page          = request_nfce_page(url)
    conta_despesa = fetch_expense_account(page)
    cnpj          = fetch_cnpj(page)
    tbl           = read_raw_table(url)
    tbl           = clean_raw_data(tbl)
    
    return tbl

tabela = generate_items_table(url)

print(tabela)

# def popular_tabela_inicial(lista_url_nfce):
#     tabela = pd.DataFrame()
#     for i in lista_nfce_url.itertuples():
#         print(i)
#         itens_novos = gerar_tabela_itens(i[2])
#         time.sleep(np.random.rand()*3)
#         tabela = pd.concat([tabela, itens_novos], axis=0, ignore_index=True)
#     return tabela
# data_ate_agora = unir_tabelas()
# data_ate_agora.to_csv("data/extraido.csv")
# # dbx.dropbox_download_file("/nfce.csv", local_file_path="data/raw_data.csv")
# lista_nfce_suja = pd.read_csv('data/raw_data.csv')
# lista_nfce_limpa = lista_nfce_suja[lista_nfce_suja.link.str.match(validacao_url)]
# lista_nfce_suja['itens'] = criar_tabela(lista_nfce_suja['link'])