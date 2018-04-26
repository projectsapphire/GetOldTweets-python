dir=$1

for filename in `ls $dir/`
do 
    filename=$dir/$filename
    echo "loading $filename"
    mongoimport -h [host] -d [database] -c [collection] -u [username] --port [port] -p [password] --type json --file $filename --jsonArray  --upsert --upsertFields id
done