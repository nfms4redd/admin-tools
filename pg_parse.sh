source parse.sh

if [ ! -v crs ]
then
	echo "El sistema de referencia de coordenadas del fichero debe ser especificado. Ejemplo: --crs 4326"
	exit 1 
fi

