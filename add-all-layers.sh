set -e

source default.sh

getoptString='schema:,database:,datastore:,workspace:'

help="uso: `basename $0` [--schema SCHEMA] [--database DATABASE]
		[--datastore DATASTORE] [--workspace WORKSPACE]

Añade a GeoServer todas las tablas de un esquema de una base de datos PostGIS

Opciones:
	--schema	Esquema que se añadirá a GeoServer. Valor por defecto: $schema
	--database	Base de datos que contiene el esquema a añadir. Valor por defecto: $databasename
	--datastore	El almacén de datos que contiene las capas a añadir. Valor por defecto: $datastore
	--workspace	El espacio de trabajo donde está el almacén de datos. Valor por defecto: $workspace"

source parse.sh

psql -t -U geoserver -d $databasename -c "select table_name from information_schema.tables where table_schema='"$schema"'" | sed -e "s/^\s//g" | ./multi-add-layer.sh --workspace $workspace --datastore $datastore
