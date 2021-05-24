# módulo para trabalhar com pdf
import pdfplumber as p

# módulo para trabalhar com expressões regulares
import re

# módulo para trabalhar com excel
from openpyxl import *

# abrindo o arquivo pdf
with p.open('faturas.pdf') as pdf:
	page = pdf.pages[0] # determinando a página para extrair o texto
	text = page.extract_text() # extraindo o texto

# mostrando o texto extraído
print(text)

print('===================================================================')
print()
print()
print()
print()
print()
print()

# procurando todas as ocorrências de "Pagador" com 're.findall()
pagador = re.findall(r'(?<=Pagador:\s)[A-Z].*', text)
#print(f'Pagador: {pagador}')

# procurando todas as ocorrências de "Valor" com 're.findall()
valor = re.findall(r'(?<=Valor:\s)\d*\.\d*\,\d{2}', text)
#print(f'Valor: {valor}')

# procurando todas as ocorrências de "Vencimento" com 're.findall()
venc = re.findall(r'(?<=Vencimento:\s)\d{2}\/\d{2}\/\d{4}', text)

# trocando a barra da data por hífen(opcional)
venc_formatado = []
for item in venc:
	troca_venc = item.replace('/', '-')
	venc_formatado.append(troca_venc)
#print(f'Vencimento: {venc_formatado}')

# procurando todas as ocorrências de "Beneficiário" com 're.findall()
benefic = re.findall(r'(?<=Beneficiário:\s)[A-Z].*', text)
#print(f'Beneficiário: {benefic}')

# procurando todas as ocorrências da data de pagamento com 're.findall()
data_hora = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}\:\d{2}', text)
#print(f'Data: {data_hora}')

# trocando a barra da data por hífen(opcional)
data_hora_format = []
for i in data_hora:
    troca_data = i.replace('/', '-')
    data_hora_format.append(troca_data)

# adicionando todos os dados de cada pessoa em sequência para posterior transferência para o excel, pois o openpyxl adiciona ao excel dados em forma de listas para preencher a linha inteira de cada registro.
# neste caso, será gerada uma única lista com todos os dados em sequência.
dados = []
for i in range(3):
    dados.append(pagador[i])
    dados.append(valor[i])
    dados.append(venc_formatado[i])
    dados.append(benefic[i])
    dados.append(data_hora_format[i])

# mostrando os dados
print(dados)


# criação do arquivo xlsx através do openpyxl:
wb = Workbook()

# dando o nome plan pra planilha ativa:
plan = wb.active 

# definindo valores de cabeçalho:
plan['A1'] = "Nome"
plan['B1'] = "Valor"
plan['C1'] = "Vencimento"
plan['D1'] = 'Beneficiario'
plan['E1'] = "Data pagto."

################
# função para dividir a lista completa em 5 partes iguais, ou seja, à cada pessoa pertencem 5 itens da lista(pagador, valor, vencimento, beneficiário e data de pagamento). Se dividirmos a lista geral por 5, teremos sublistas com os dados de cada pessoa a serem inseridos à planilha
def dividir_lista(lista, n_elementos):
      
    # looping till length l
    # para cada item na lista num alcance de 0 ao número correspondente ao tamanho da lista, num passo determinado(no caso, será 5):
    for i in range(0, len(lista), n_elementos): 
        yield lista[i:i + n_elementos]
  
# quantos elementos cada lista deve ter
n = 5

# x é igual a lista de sublistas gerada pela função acima e receberá como argumentos a lista bruta e o número de sublistas desejado:
x = list(dividir_lista(dados, n))
print (x)
################

# inserindo na planilha do excel as sublistas dentro da lista 'x' usando um loop.
for i in x:
    plan.append(i)

# salvando planilha
wb.save(filename = 'faturas.xlsx')

#leitura do xlsx
#lwb = load_workbook(filename = 'faturas.xlsx')