import xml.etree.ElementTree as ET
from urllib3 import PoolManager

#estados=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR",
#		"PE", "PI", "RJ", "RN", "RO", "RS", "RR", "SC", "SE", "SP", "TO"]

estados = ['AM', 'AL']

http = PoolManager()

for uf in estados:
	doc = http.request('GET', 'http://servicos.cptec.inpe.br/~rserv/estados/cidade-' + uf + '.xml')
	root = ET.fromstring(doc.data)

	data = root.findall("clima")
	print(data[0].attrib.get('data') + ' // ' + data[0].attrib.get('hora'))

	for cidade in root.findall('./clima/estados/estado/cidades/cidade'):
		print(cidade.attrib.get('id') + ' / ' + cidade.attrib.get('nome'))
		for clima in cidade.findall('clima'):
			print('\t' + clima.attrib.get('nm_dia') + ' / ' + clima.attrib.get('ds_dia'))
