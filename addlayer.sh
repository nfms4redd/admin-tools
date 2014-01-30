set -e

getoptString='layer:,datastore:,workspace:'

source parse.sh

if [ ! -v layer ]
then
	echo "Se debe especificar el nombre de la capa. Por ejemplo: --layer provincias"
	exit 1 
fi

output="`curl --write-out \\\\n%{http_code}\\\\n --silent --stderr /dev/null -u admin:geoserver -v -XPOST -H 'Content-Type:text/xml' -d "<featureType><name>$layer</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/$workspace/datastores/$datastore/featuretypes`"
returnCode=`echo "$output" | tail -1`
if [ $returnCode -eq 201 ]; then
	echo "Capa creada con exito: $layer" 
else
	echo "ERROR cargando capa '$layer' (code $returnCode): $output"
fi

