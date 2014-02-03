set -e

getoptString='crs:,schema:,encoding:,database:,file:'

doc_command="Carga un fichero .shp como una tabla de PostGIS."
doc_crs="Sistema de coordenadas del fichero .shp"
doc_schema="Esquema donde se añadirá la nueva tabla"
doc_encoding="Codificación de caracteres del fichero .dbf"
doc_database="Base de datos que contiene al esquema donde se añadirá la nueva tabla"
doc_file="Fichero .shp a añadir"

source pg-parse.sh

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
