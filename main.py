# Dependencies -----
import sys
import time
import pandas as pd
import re
from NFCE import header, body, parser




# Grupo 1 é a parte necessária
validacao_url = u"(http\:\/\/www\.fazenda\.pr\.gov\.br\/nfce\/qrcode\?p\=\d{44})(\|\d){3}\|\w{40}"

links = pd.read_csv('data/nfce.csv')

table1 = get_table(links['link'][3])
table2 = get_table(links['link'][4])

df = pd.concat([table1, table2])


url = "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41220576189406002250651160003910901081932515|2|1|1|8172512119B92F5F4BBCF8D1E4FF617D304FD593"

def get_table(url):
    metadata = header.get_metadata(url)
    page = header.request_nfce_page(url)
    tbl = body.read_raw_table(url)
    tbl = body.clean_strings(tbl)
    tbl = body.separate_columns(tbl)
    tbl = body.parse_doubles(tbl)
    tbl = body.fetch_ID(tbl, metadata)
    return tbl

def concatenate_tables(links):
    all_data = pd.DataFrame()
    
    for url in links['link']:
        if re.match(validacao_url, url):
            print(url)
        else:
            continue
        table = get_table(url)
        all_data = pd.concat([all_data, table])
        print(all_data)
        time.sleep(1)
    
    return all_data


# all_tables = concatenate_tables(links)

# all_tables.to_csv('data/mined.csv')

