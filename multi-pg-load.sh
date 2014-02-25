source default.sh

getoptString='crs:,schema:,encoding:,database:,files:,folder:'

help="Añade varios ficheros .shp como tablas en PostGIS.

Opciones:
	--crs		Sistema de referencia del fichero .shp
	--schema	Esquema de la base de datos donde se añadirán las tablas. Valor por defecto: $schema
	--encoding	Codificación de caracteres de los ficheros .dbf. Valor por defecto: $encoding
	--database	Base de datos que contiene el esquema donde se añadirán las tablas. Valor por defecto: $databasename
	--files		Expresión para filtrar los ficheros. Valor por defecto: $files
	--folder	Directorio que contiene los ficheros a añadir. Los ficheros pueden estar en cualquier subdirectorio dentro del directorio especificado"

source pg-parse.sh

if [ ! -v folder ]
then
	echo "Se debe especificar un directorio: --folder directorio"
	exit 1 
fi

echo "" > /tmp/pgload.log

for i in `find $folder -name $files`;
do
	echo "## CARGANDO $i ##" >> /tmp/pgload.log 
	./pg-load.sh --crs $crs --encoding $encoding --file $i --database $databasename --schema $schema 1>> /tmp/pgload.log 2>>/tmp/pgload.log
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
