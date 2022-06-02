# Não achei uma forma de importar modulos através de um outro módulo
# from py import dependencias as deps

from py import funcoes as foo


table_1 = foo.criar_tabela(
"http://www.fazenda.pr.gov.br/nfce/qrcode?p=41220578413325001750650710000900881697143635|2|1|1|8F59F48C89393FBEE062A0FB9088C8E19562178A")


print(table_1)


