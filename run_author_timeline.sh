itr=0
pass=0
while read author; do
    # pass $3 entries from authors list before you start the extraction
    if [ $pass -ge $3 ];
    then
        # extract tweets in a batch of 100 authors in a single run.
        if [ $itr -lt 500 ]; 
        then
            author_list_id=$(awk '{print $2}' <<< $author) 
            author=$(awk '{print $1}' <<< $author)
            if [ "$author_list_id" != "" ]; 
            then
                echo "$itr $pass,  author $author, author_list_id $author_list_id"
                itr=` expr $itr + 1`
                echo $author >> $2
                python Exporter.py --username "$author" --author_list_id "$author_list_id" --since 2018-01-01 --until 2018-10-09 --maxtweets 40000 --output tweets/$author.json >> $2&
            fi
        fi
    fi
    pass=`expr $pass + 1`
done < $1