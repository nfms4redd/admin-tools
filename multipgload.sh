getoptString='crs:,schema:,encoding:,database:,files:,folder:'

source pg_parse.sh

if [ ! -v folder ]
then
	echo "Se debe especificar un directorio: --folder directorio"
	exit 1 
fi

echo "" > /tmp/pgload.log
for i in `find $folder -name $files`;
do
	echo "## CARGANDO $i ##" >> /tmp/pgload.log 
	./pgload.sh --crs $crs --encoding $encoding --file $i --database $databasename --schema $schema 1>> /tmp/pgload.log 2>>/tmp/pgload.log
	if [ $? -eq 0 ]; then
		echo "### LOG ### Cargado con exito: $i" >> /tmp/pgload.log
	else
		echo "### LOG ### ERROR $i" >> /tmp/pgload.log
	fi
done
cat /tmp/pgload.log | grep \#\#\#
echo 
echo 'Para más información, ver /tmp/pgload.log'
echo
