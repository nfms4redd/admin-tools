getoptString='datastore:,workspace:'

doc_command="Añade varias capas a GeoServer, especificándolas una a una. Pulsar Ctrl+D para terminar de añadir capas."
doc_datastore="El almacén de datos que contiene las capas a añadir"
doc_workspace="El espacio de trabajo donde está el almacén de datos"

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
