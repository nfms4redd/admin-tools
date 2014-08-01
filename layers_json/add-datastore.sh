set -e

source default.sh

getoptString='host:,port:,database:,schema:,password:,workspace:,datastore:'

help="uso: `basename $0` [--host HOST] [--port PORT]
		[--database DATABASE] [--schema SCHEMA] --password PASSWORD
		[--workspace WORKSPACE] [--datastore DATASTORE]

Añade un nuevo almacén de datos a GeoServer a partir de una base de datos PostGIS.

Opciones:
	--host		Servidor de la base de datos PostGIS. Valor por defecto: $host
	--port		Puerto de la base de datos PostGIS. Valor por defecto: $port
	--database	Nombre de la base de datos que contiene el esquema a añadir. Valor por defecto: $databasename
	--schema	Esquema de PostGIS que se añadirá como almacén de datos. Valor por defecto: $schema
	--password	Contraseña del usuario 'geoserver' en la base de datos PostGIS.
	--workspace	Espacio de trabajo de GeoServer donde se añadirá el almacén de datos. Valor por defecto: $workspace
	--datastore	Nombre del almacén de datos que se creará en GeoServer. Valor por defecto: $datastore"

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
