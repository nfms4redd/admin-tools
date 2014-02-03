set -e

getoptString='layer:,datastore:,workspace:'

doc_command="Añade una nueva capa a GeoServer a partir de una tabla de PostGIS.\nEl esquema que contiene la tabla debe haber sido añadido anteriormente con el comando 'add-datastore'"
doc_layer="Tabla que se añadirá a GeoServer"
doc_workspace="Espacio de trabajo de GeoServer que donde se añadirá la capa"
doc_datastore="Nombre del almacén de datos que contiene la tabla a añadir"

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
	echo "ERROR cargando capa '$layer' (code $returnCode): `echo $output | tr -d ' '`"
fi

