set -e

getoptString='schema:,database:,datastore:,workspace:'

doc_command="Añade a GeoServer todas las tablas de un esquema de una base de datos PostGIS"
doc_schema="Esquema que se añadirá a GeoServer"
doc_database="Base de datos que contiene el esquema a añadir"
doc_datastore="El almacén de datos que contiene las capas a añadir"
doc_workspace="El espacio de trabajo donde está el almacén de datos"

source parse.sh

psql -t -U geoserver -d $databasename -c "select table_name from information_schema.tables where table_schema='"$schema"'" | sed -e "s/^\s//g" | ./multi-add-layer.sh --workspace $workspace --datastore $datastore
