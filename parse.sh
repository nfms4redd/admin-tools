schema=nfms
encoding=UTF8
databasename=geoserverdata
files=*.shp
host=localhost
port=5432
workspace=nfms
datastore=geoserverdata

usage() {
	if [ -z "$doc_crs" ]; then doc_crs="Sistema de coordenadas"; fi
	if [ -z "$doc_schema" ]; then doc_schema="Esquema de la base de datos"; fi
	if [ -z "$doc_encoding" ]; then doc_encoding="Codificación de caracteres"; fi
	if [ -z "$doc_database" ]; then doc_database="Nombre de la base de datos"; fi
	if [ -z "$doc_datastore" ]; then doc_datastore="Almacén de datos en GeoServer"; fi
	if [ -z "$doc_file" ]; then doc_file="Fichero"; fi
	if [ -z "$doc_password" ]; then doc_password="Contraseña"; fi
	if [ -z "$doc_port" ]; then doc_port="Puerto"; fi
	if [ -z "$doc_folder" ]; then doc_folder="Directorio"; fi
	if [ -z "$doc_workspace" ]; then doc_workspace="Espacio de trabajo"; fi
	if [ -z "$doc_host" ]; then doc_host="Host"; fi
	if [ -z "$doc_layer" ]; then doc_layer="Nombre de la capa"; fi

	options=`echo $getoptString | sed -e "s/:,/\n/g" -e "s/://g" | sed -e "s/^/\t--/g"`
    help=$(printf "    ")
	for i in $options
	do
		case $i in
			--crs) aux=$doc_crs;;
	        --schema) aux=$doc_schema;;
	        --encoding) aux=$doc_encoding;;
	        --database) aux=$doc_database;;
	        --datastore) aux=$doc_datastore;;
	        --file) aux=$doc_file;;
	        --files) aux=$doc_files;;
	        --password) aux=$doc_password;;
	        --port) aux=$doc_port;;
	        --folder) aux=$doc_folder;;
	        --workspace) aux=$doc_workspace;;
	        --host) aux=$doc_host;;
	        --layer) aux=$doc_layer;;
			--help) aux="Muestra esta ayuda";;
			*) aux="";;
		esac
		printf -v help -- "$help$i#\t$aux\n    "
	done

    if [ -n "$doc_command" ]; then printf -- "$doc_command\n\n"; fi
	printf -- "Opciones:\n$help" | column -t -s "#"
}

getoptString=${getoptString},help
args=`getopt -o "" --long "$getoptString" -n "$0" -- "$@"`
if [ $? != 0 ] ; then exit 1 ; fi
eval set -- "$args"

while true ; do
    case "$1" in
        --crs) crs=$2; shift 2;;
        --schema) schema=$2; shift 2;;
        --encoding) encoding=$2; shift 2;;
        --database) databasename=$2; shift 2;;
        --datastore) datastore=$2; shift 2;;
        --file) file=$2; shift 2;;
        --files) files=$2; shift 2;;
        --password) password=$2; shift 2;;
        --port) port=$2; shift 2;;
        --folder) folder=$2; shift 2;;
        --workspace) workspace=$2; shift 2;;
        --host) host=$2; shift 2;;
        --layer) layer=$2; shift 2;;
        --help) usage; exit 0;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac        
done
