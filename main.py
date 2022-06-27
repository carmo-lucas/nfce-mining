# Dependencies -----
import sys
import time
from NFCE import header
from NFCE import body


# Grupo 1 é a parte necessária
validacao_url = u"(http\:\/\/www\.fazenda\.pr\.gov\.br\/nfce\/qrcode\?p\=\d{44})(\|\d){3}\|\w{40}"
url = "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41220576189406002250651160003910901081932515|2|1|1|8172512119B92F5F4BBCF8D1E4FF617D304FD593"


header.get_metadata(url)

body.read_raw_table(url)



