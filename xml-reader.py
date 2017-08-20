import xml.etree.ElementTree as ET
from urllib3 import PoolManager
import datetime
import psycopg2

estados=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR",
		"PE", "PI", "RJ", "RN", "RO", "RS", "RR", "SC", "SE", "SP", "TO"]

#estados = ['AL']

sql = """ INSERT INTO public.previsoes_tempo
                (id_municipio, id_condicao, data, data_previsao, created_at, updated_at)
                SELECT (SELECT gid FROM public.municipios_br WHERE cod_cptec = %s),
                (SELECT id FROM public.condicoes_tempo WHERE sigla = %s), %s, %s, NOW(), %s
                WHERE EXISTS (SELECT gid FROM public.municipios_br WHERE cod_cptec = %s) """

http = PoolManager()

inserted_rows = 0

try:
	conn = psycopg2.connect("dbname='previsao' user='postgres' host='localhost' password='postgres.'")
	cursor = conn.cursor()

	for uf in estados:
		doc = http.request('GET', 'http://servicos.cptec.inpe.br/~rserv/estados/cidade-' + uf + '.xml')
		root = ET.fromstring(doc.data)

		data = root.findall("clima")
		data_atualizacao = datetime.datetime.strptime(data[0].attrib.get('data') + data[0].attrib.get('hora'), "%d/%m/%Y%H:%M")

		estado = root.findall("clima/estados/estado")

		print("Lendo estado >> " + estado[0].attrib.get('nome') + " (" + uf + ")")

		for cidade in root.findall('./clima/estados/estado/cidades/cidade'):
			#print(cidade.attrib.get('id') + ' / ' + cidade.attrib.get('nome'))
			for clima in cidade.findall('clima'):
				#print('\t' + clima.attrib.get('nm_dia') + ' / ' + clima.attrib.get('ds_dia'))
				data_prev = datetime.datetime.strptime(clima.attrib.get('nm_dia'), '%d/%m/%Y').date()
				cursor.execute(sql, (cidade.attrib.get('id'), clima.attrib.get('ds_dia'), data_atualizacao,
								data_prev, data_atualizacao.strftime("%Y/%m/%d %H:%M:%S.%f-03"), cidade.attrib.get('id')))
				inserted_rows = inserted_rows + cursor.rowcount

	conn.commit()
	conn.close()
except psycopg2.Error as e:
	print(e.pgerror)
	print(e.diag.message_detail)
finally:
	print(inserted_rows)