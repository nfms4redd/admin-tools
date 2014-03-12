set -e

source default.sh

getoptString='layer:,datastore:,workspace:'

help="uso: `basename $0` --layer LAYER [--workspace WORKSPACE] [--datastore DATASTORE]

Añade una nueva capa a GeoServer a partir de una tabla de PostGIS.
El esquema que contiene la tabla debe haber sido añadido anteriormente a GeoServer como un datastore.

Opciones:
	--layer		Tabla que se añadirá a GeoServer.
	--workspace	Espacio de trabajo de GeoServer que donde se añadirá la capa. Valor por defecto: $workspace
	--datastore	Nombre del almacén de datos que contiene la tabla a añadir. Valor por defecto: $datastore"

source parse.sh

if [ ! -v layer ]
then
	echo "Se debe especificar el nombre de la capa. Por ejemplo: --layer provincias"
	exit 1 
fi

set +e

output="`curl --write-out \\\\n%{http_code}\\\\n --silent --stderr /dev/null -u admin:geoserver -v -XPOST -H 'Content-Type:text/xml' -d "<featureType><name>$layer</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/$workspace/datastores/$datastore/featuretypes`"
returnCode=`echo "$output" | tail -1`

if [ $returnCode -eq 201 ]; then
	echo "Capa creada con exito: $layer" 
else
	echo "ERROR cargando capa '$layer' (code $returnCode): $output"
fi

