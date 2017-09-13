#!/bin/bash

CURDATE=$(date '+%Y%m%d')

if [ -e "/tmp/ai/$CURDATE" ]
then
	rm -fr "/tmp/ai/$CURDATE"
fi

mkdir -p /tmp/ai/$CURDATE
        
for i in {1..7};
do
	/usr/bin/wget -q "http://img0.cptec.inpe.br/~rgrafico/portal_tempo/bandas/tempo/prev_google_"$i"_br.png" -O /tmp/ai/$CURDATE/"prev_google_"$i"_br.png"
done

for i in {1..7};
do
	/usr/bin/gdal_translate -of Gtiff -a_ullr -91.75 10.75 -18 -38.3 -a_srs EPSG:4326 /tmp/ai/$CURDATE/"prev_google_"$i"_br.png" /tmp/ai/$CURDATE/"prev_google_"$i"_br.gtiff"
done

/usr/bin/raster2pgsql -s 4326 -t 2025x1350 -a -F -I -N 0 /tmp/ai/$CURDATE/*.gtiff public.images_forecast > /tmp/ai/$CURDATE/images_forecast.sql

/usr/bin/psql -U postgres -f /tmp/ai/$CURDATE/images_forecast.sql -d previsao

psql -U postgres -d previsao -c "UPDATE public.images_forecast SET data_previsao = CURRENT_DATE + INTERVAL '1 day' * (SUBSTRING(filename from 13 for 1)::int - 1) WHERE data = CURRENT_DATE"
