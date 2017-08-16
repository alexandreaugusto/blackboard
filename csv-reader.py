import csv
import sys
import psycopg2

f = open(sys.argv[1], 'rt')

sql = """ UPDATE public.municipios_br
                SET cod_cptec = %s, uf = %s
                WHERE cod_ibge = %s"""

updated_rows = 0

try:
	conn = psycopg2.connect("dbname='previsao' user='postgres' host='localhost' password='postgres.'")
	cursor = conn.cursor()
	reader = csv.reader(f)
	next(reader, None)
	for row in reader:
		if row[0].strip() != '':
			cursor.execute(sql, (row[1], row[3], row[0]))
			updated_rows = updated_rows + cursor.rowcount
	conn.commit()
	cursor.close()
finally:
	f.close()

print(updated_rows)