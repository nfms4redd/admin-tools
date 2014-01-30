getoptString='datastore:,workspace:'

source parse.sh

echo "">/tmp/gsload.log
while read line; do

	if [ -z "$line" ]; then
		continue
	fi

	output=`./addlayer.sh --layer $line --workspace $workspace --datastore $datastore`
	echo "### LOG ### $output" >> /tmp/gsload.log
done
cat /tmp/gsload.log | grep \#\#\#
echo
echo 'Para más información, ver /tmp/gsload.log'
echo
