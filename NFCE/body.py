import pandas as pd
import numpy as np
from NFCE import header

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
    # pat='[ ]{2,}' significa dois ou mais espaços
    tbl[['nome', 'qtde', 'unidade', 'vl_unit']] = tbl[0].str.split(pat='[ ]{2,}', expand=True)

    # Remove colunas que já foram transformadas
    tbl = tbl.drop(columns=[0, 1])

    return tbl

def parse_doubles(tbl):
# TODO: Pensar em como melhorar essa função parse_doubles para ser um pouco mais robusta, remover os dois argumentos
    
    # Troca vírgulas por pontos para futura conversão para valores numéricos
    tbl = tbl.replace(",", ".", regex=True)
    # Remove espaços das células e converte para numérico
    tbl[['qtde', 'vl_unit', 'vl_total']] = tbl[['qtde', 'vl_unit','vl_total']].replace(" ", "", regex=True).astype('float64')
    return tbl

def fetch_ID(tbl, meta):
    tbl[['ID']] = meta["chave_acesso"] # isso não é uma boa ideia
    return tbl