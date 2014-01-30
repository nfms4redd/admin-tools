set -e

getoptString='host:,port:,datastore:,schema:,password:,workspace:'

source parse.sh

if [ ! -v password ]
then
	echo "Se debe especificar el password para acceder a los datos del almacén. Ejemplo: --password nfms"
	exit 1 
fi

echo '<dataStore>\
	<name>$datastore</name>\
	<connectionParameters>\
		<host>$host</host>\
		<port>$port</port>\
		<database>$databasename</database>\
		<schema>$schema</schema>\
		<user>geoserver</user>\
		<passwd>$password</passwd>\
		<dbtype>postgis</dbtype>\
	</connectionParameters>\
</dataStore>\' > /tmp/adddatastore.tmp 

sed -i -e "s/\$datastore/$datastore/" -e "s/\$host/$host/" -e "s/\$port/$port/" -e "s/\$databasename/$databasename/" -e "s/\$schema/$schema/" -e "s/\$password/$password/" /tmp/adddatastore.tmp

curl -u admin:geoserver -v -XPOST -H 'Content-type:text/xml' -T /tmp/adddatastore.tmp http://localhost:8080/geoserver/rest/workspaces/$workspace/datastores

rm /tmp/adddatastore.tmp
