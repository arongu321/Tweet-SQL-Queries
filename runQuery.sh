#!/bin/sh
sql_directory="."
db_files=$(find "$sql_directory" -type f -name 'test*.db' | sort)
rm -r query*
for ((count=1; count<=10; count++));
do
    testCount=0
    for db_file in $db_files;
    do
        testCount=$((testCount+1))
        txtFile="test$testCount.txt"
        jsonl_file="test$testCount.jsonl"
        sql_file="q$count.sql"
        directory="query$count"
        if [ ! -d "$directory" ]; then
            mkdir $directory
        fi
        sqlite3 $db_file < $sql_file > $txtFile
        python3 outputJSON.py $txtFile $count $jsonl_file
        mv $jsonl_file $directory
        mv $txtFile $directory
    done
done
