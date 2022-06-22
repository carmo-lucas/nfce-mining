# Não achei uma forma de importar modulos através de um outro módulo
# from py import dependencias as deps
# from py import funcoes as foo
# from py import dropbox as dbx

# Dependencias -----

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

def solicitar_pagina_nfce(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    page = BeautifulSoup(r.content, 'html.parser')
    return page

# Função para extrair metadados conta despesa, data da transação, número da nfce e cnpj
def achar_metadados(page):
    
    def achar_conta_despesa(page):
        conta_despesa = page.find('div', id="u20").text
        print(conta_despesa)
        return conta_despesa

    def achar_cnpj(page):
        cnpj = page.find_all('div', class_='text')[0].text
        cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", cnpj).group(0)
        print(cnpj)
        return cnpj

    def achar_data_transacao(page):
        data_transacao = page.find('li').text
        data_transacao = re.search(r"((\d+\/){2}\d{4}\s(\d{2}:){2}\d{2})", data_transacao).group(0)
        print(data_transacao)
        return data_transacao

    def achar_num_nfce(page):
        numero_nfce = page.find('li').text
        numero_nfce = re.search(r"Número: (\d+)", numero_nfce).group(1)
        print(numero_nfce)
        return numero_nfce

    def achar_chave_acesso(page):
        chave_acesso = page.find
        chave_acesso = re.search(r"\d{11}", chave_acesso)
        print(chave_acesso)
        return chave_acesso

    cd    = achar_conta_despesa(page)
    cnpj  = achar_cnpj(page)
    dt    = achar_data_transacao(page)
    num   = achar_num_nfce(page)
    chave = achar_chave_acesso(page)
    
    meta = {
        "conta_despesa": cd,
        "cnpj": cnpj,
        "data_transacao": dt,
        "numero_nfce": num,
        "chave_acesso": chave
        }

    return meta

page = solicitar_pagina_nfce(url)

meta = achar_info_cabecalho(page)












def ler_tabela_suja(url):
    tbl_suja = pd.read_html(url, encoding='utf8')
    tbl_suja = pd.concat(tbl_suja)
    return tbl_suja



# Funções para limpar os dados da tabela extraída da página

def remover_texto_indesejado(tbl):
    texto_indesejado = u"\(Código: \d+\)|Qtde.:|UN: |Vl. Unit.:"

    # Remove texto dos valores numéricos
    tbl['vl_total'] = tbl[1].str.replace(u"Vl. Total\s+", "")
    tbl[0] = tbl[0].str.replace(texto_indesejado, "")
    return tbl



def separar_colunas(tbl):
    # Separa os valores em colunas
    tbl[['nome', 'qtde', 'unidade', 'vl_unit']] = tbl[0].str.split(pat='[ ]{2,}', expand=True)
    # Remove colunas que já foram transformadas
    # pat='[ ]{2,}' significa dois ou mais espaços
    tbl = tbl.drop(columns=[0, 1])
    return tbl



def formatar_valores_numericos(tbl):
    # Troca vírgulas por pontos para futura conversão para valores numéricos
    tbl = tbl.replace(",", ".", regex=True)
    # Remove espaços das células e converte para numérico
    tbl[['qtde', 'vl_unit', 'vl_total']] = tbl[['qtde', 'vl_unit','vl_total']].replace(" ", "", regex=True).astype('float64')
    tbl[['conta_despesa', 'data_transacao']] = conta_despesa, data_transacao
    return tbl


def limpar_tabela_suja(tbl):

    tbl = remover_texto_indesejado(tbl)
    tbl = separar_colunas(tbl)
    tbl = formatar_valores_numericos(tbl)
    return tbl


def gerar_tabela_itens(url):

    page          = solicitar_pagina_nfce(url)
    conta_despesa = achar_conta_despesa(page)
    cnpj          = achar_cnpj(page)
    tbl           = ler_tabela_suja(url)
    tbl           = limpar_tabela_suja(tbl)
    
    return tbl


tabela = gerar_tabela_itens(url)

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