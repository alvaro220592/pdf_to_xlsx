import pdfplumber as p
import re

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
print(f'Pagador: {pagador}')

valor = re.findall(r'(?<=Valor:\s)\d*\.\d*\,\d{2}', text)
print(f'Valor: {valor}')

venc = re.findall(r'(?<=Vencimento:\s)\d{2}\/\d{2}\/\d{4}', text)
print(f'Vencimento: {venc}')

benefic = re.findall(r'(?<=Beneficiário:\s)[A-Z].*', text)
print(f'Beneficiário: {benefic}')

data_hora = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}\:\d{2}', text)
print(f'Data: {data_hora}')