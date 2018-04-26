itr=0
pass=0
while read author; do
    # pass $3 entries from authors list before you start the extraction
    if [ $pass -ge $3 ];
    then 
        # extract tweets in a batch of 100 authors in a single run.
        if [ $itr -lt 100 ]; 
        then
            echo $itr $pass $author
            itr=` expr $itr + 1`
            echo $author >> $2
            python Exporter.py --username "$author" --since 2018-01-01 --until 2018-04-25 --maxtweets 20000 --output tweets/$author.json >> $2&
            #cp output_got.csv tweets/$author.json
        fi
    fi
    pass=`expr $pass + 1`
done < $1