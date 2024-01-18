#!/bin/sh

pip3 install faker
pip3 install requests

# Test 4 Data
python3 generateData2.py 200 5 100 120 180 120 100 250 test4Data.sql
sqlite3 test4.db < tables.sql
sqlite3 test4.db < test4Data.sql

# Test 5 Data
python3 generateData2.py 300 20 400 200 500 360 250 500 test5Data.sql
sqlite3 test5.db < tables.sql
sqlite3 test5.db < test5Data.sql

# Test 6 Data
python3 generateData2.py 500 40 600 400 700 500 400 700 test6Data.sql
sqlite3 test6.db < tables.sql
sqlite3 test6.db < test6Data.sql

# Test 7 Data
python3 generateData2.py 100 2 90 50 80 85 60 40 test7Data.sql
sqlite3 test7.db < tables.sql
sqlite3 test7.db < test7Data.sql