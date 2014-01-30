set -e

getoptString='crs:,schema:,encoding:,database:,file:'

source pg_parse.sh

if [ ! -v file ]
then
	echo "Se debe especificar un fichero: --file fichero"
	exit 1 
fi

filename=`basename $file`
shp2pgsql -g geom -s $crs -W $encoding $file $schema.${filename%.shp} > /tmp/pgload-script.sql && psql -v ON_ERROR_STOP=1 -U geoserver -d $databasename -f /tmp/pgload-script.sql
if [ $? -ne 0 ]; then
	exit 1
fi

rm /tmp/pgload-script.sql
