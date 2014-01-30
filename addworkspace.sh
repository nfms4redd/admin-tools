set -e

getoptString='workspace:'

source parse.sh

curl -u admin:geoserver -v -XPOST -H 'Content-type:text/xml' -d "<workspace><name>$workspace</name></workspace>" http://localhost:8080/geoserver/rest/workspaces

set +e
