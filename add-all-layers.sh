set -e

getoptString='schema:,database:,datastore:,workspace:'

help="Añade a GeoServer todas las tablas de un esquema de una base de datos PostGIS

Opciones:
	--schema	Esquema que se añadirá a GeoServer
	--database	Base de datos que contiene el esquema a añadir
	--datastore	El almacén de datos que contiene las capas a añadir
	--workspace	El espacio de trabajo donde está el almacén de datos"

source parse.sh

psql -t -U geoserver -d $databasename -c "select table_name from information_schema.tables where table_schema='"$schema"'" | sed -e "s/^\s//g" | ./multi-add-layer.sh --workspace $workspace --datastore $datastore
