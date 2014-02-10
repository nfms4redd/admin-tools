getoptString='datastore:,workspace:'

help="Añade varias capas a GeoServer, especificándolas una a una. Pulsar Ctrl+D para terminar de añadir capas.

Opciones:
	--datastore	El almacén de datos que contiene las capas a añadir
	--workspace	El espacio de trabajo donde está el almacén de datos"

source parse.sh

echo "">/tmp/gsload.log
while read line; do
	if [ -z "$line" ]; then
		continue
	fi

	output=`./add-layer.sh --layer $line --workspace $workspace --datastore $datastore`
	echo "### LOG ### $output" >> /tmp/gsload.log
done
cat /tmp/gsload.log | grep \#\#\#
echo
echo 'Para más información, ver /tmp/gsload.log'
echo
