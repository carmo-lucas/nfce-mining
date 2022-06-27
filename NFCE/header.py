from bs4 import BeautifulSoup
import requests
import re

# Funções para extrair informações da página
def request_nfce_page(url):

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    page = BeautifulSoup(r.content, 'html.parser')
    return page


def fetch_expense_account(page):

    conta_despesa = page.find('div', id="u20").text
    return conta_despesa

def fetch_cnpj(page):

    cnpj = page.find_all('div', class_='text')[0].text
    cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", cnpj).group(0)
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

# Função para extrair metadados conta despesa, data da transação, número da nfce e cnpj
def get_metadata(url):

    page  = request_nfce_page(url)

    cd    = fetch_expense_account(page)
    cnpj  = fetch_cnpj(page)
    dt    = fetch_transaction_date(page)
    num   = fetch_nfce_number(page)
    chave = fetch_access_key(page)
    meta  = {
        "conta_despesa": cd,
        "cnpj": cnpj,
        "data_transacao": dt,
        "numero_nfce": num,
        "chave_acesso": chave
        }
    
    return meta
