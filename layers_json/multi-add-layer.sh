source default.sh

getoptString='datastore:,workspace:'

help="uso: `basename $0` [--datastore DATASTORE] [--workspace WORKSPACE]

Añade varias capas a GeoServer, especificándolas una a una. Pulsar Ctrl+D para terminar de añadir capas.

Opciones:
	--datastore	El almacén de datos que contiene las capas a añadir. Valor por defecto: $datastore
	--workspace	El espacio de trabajo donde está el almacén de datos. Valor por defecto: $workspace"

source parse.sh

echo "">/tmp/gsload.log
while read line; do
	if [ -z "$line" ]; then
		continue
	fi

	output=`add-layer.sh --layer $line --workspace $workspace --datastore $datastore`
	echo "### LOG ### $output" >> /tmp/gsload.log
done
cat /tmp/gsload.log | grep \#\#\#
echo
echo 'Para más información, ver /tmp/gsload.log'
echo
