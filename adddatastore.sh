set -e

getoptString='host:,port:,database:,schema:,password:,workspace:,datastore:'

doc_command="Añade un nuevo almacén de datos a GeoServer a partir de una base de datos PostGIS."
doc_host="Servidor de la base de datos PostGIS"
doc_port="Puerto de la base de datos PostGIS"
doc_database="Nombre de la base de datos que contiene el esquema a añadir"
doc_schema="Esquema de PostGIS que se añadirá como almacén de datos"
doc_password="Contraseña del usuario 'geoserver' en la base de datos PostGIS"
doc_workspace="Espacio de trabajo de GeoServer donde se añadirá el almacén de datos"
doc_datastore="Nombre del almacén de datos que se creará en GeoServer"

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
