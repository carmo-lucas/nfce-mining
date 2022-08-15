# Dependencies -----
import sys
import time
from NFCE import header, body

# Grupo 1 é a parte necessária
validacao_url = u"(http\:\/\/www\.fazenda\.pr\.gov\.br\/nfce\/qrcode\?p\=\d{44})(\|\d){3}\|\w{40}"

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

table = get_table(url)

table

tbl = tbl.body.categorize_items(tbl)