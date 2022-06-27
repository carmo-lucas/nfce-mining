import pandas as pd
import numpy as np

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