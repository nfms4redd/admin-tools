set -e

getoptString='workspace:'

help="Crea un nuevo espacio de trabajo en GeoServer con el nombre especificado.

Opciones:
	--workspace 	Nombre del espacio de trabajo que se creará"

source parse.sh

curl -u admin:geoserver -v -XPOST -H 'Content-type:text/xml' -d "<workspace><name>$workspace</name></workspace>" http://localhost:8080/geoserver/rest/workspaces

set +e
