schema=nfms
encoding=UTF8
databasename=geoserverdata
files=*.shp
host=localhost
port=5432
workspace=nfms
datastore=geoserverdata

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
        --help)
		echo $getoptString | sed -e "s/:,/\n/g" -e "s/://g" | sed -e "s/^/\t--/g"
		exit 0
	;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac        
done
