import pdfplumber as p
import re
from openpyxl import *


with p.open('faturas.pdf') as pdf:
	page = pdf.pages[0]
	text = page.extract_text()

	print(text)

print('===================================================================')
print()
print()
print()
print()
print()
print()


pagador = re.findall(r'(?<=Pagador:\s)[A-Z].*', text)
#print(f'Pagador: {pagador}')

valor = re.findall(r'(?<=Valor:\s)\d*\.\d*\,\d{2}', text)
#print(f'Valor: {valor}')

valor_format = []
for i in valor:
    troca_valor = i.replace(',', ' ')
    valor_format.append(troca_valor)

venc = re.findall(r'(?<=Vencimento:\s)\d{2}\/\d{2}\/\d{4}', text)

# o excel nao aceitou data com barra nesse caso, entao troquei por hifen
venc_formatado = []
for item in venc:
	troca_venc = item.replace('/', '-')
	venc_formatado.append(troca_venc)
#print(f'Vencimento: {venc_formatado}')


benefic = re.findall(r'(?<=Beneficiário:\s)[A-Z].*', text)
#print(f'Beneficiário: {benefic}')

data_hora = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}\:\d{2}', text)
#print(f'Data: {data_hora}')

data_hora_format = []
for i in data_hora:
    troca_data = i.replace('/', '-')
    data_hora_format.append(troca_data)

# ordenando os dados:
dados = []
for i in range(3):
    dados.append(pagador[i])
    dados.append(valor_format[i])
    dados.append(venc_formatado[i])
    dados.append(benefic[i])
    dados.append(data_hora_format[i])

print(dados)


# criação do xlsx:
wb = Workbook()

plan = wb.active #dando o nome plan pra planilha ativa

plan['A1'] = "Nome"
plan['B1'] = "Valor"
plan['C1'] = "Vencimento"
plan['D1'] = 'Beneficiario'
plan['E1'] = "Data pagto."

################
# Yield successive n-sized
# chunks from l.
def dividir_lista(lista, n_elementos):
      
    # looping till length l
    for i in range(0, len(lista), n_elementos): 
        yield lista[i:i + n_elementos]
  
# How many elements each
# list should have
n = 5
  
x = list(dividir_lista(dados, 5))
print (x)
################

for i in x:
    plan.append(i)

# salvando planilha
wb.save(filename = 'faturas.xlsx')

#leitura do xlsx
lwb = load_workbook(filename = 'faturas.xlsx')