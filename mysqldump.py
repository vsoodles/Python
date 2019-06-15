#!/usr/bin/env python

import os,sys
from datetime import datetime, timedelta
import commands
import time
import gzip
import shutil
import boto3

s3 = boto3.resource('s3')
bucket = "bucket-name"

now = datetime.datetime.now()
dmy = now.strftime('%d-%m-%Y')

date_1_days_ago = datetime.datetime.now() - timedelta(days=1)
ddmy = date_1_days_ago.strftime('%d-%m-%Y')



DB1Location = '/home/user/devops/backups/db1'
DB2Location = '/home/user/devops/backups/db2'
DUMP1 = 'mysqldump -uuser -ppassword  db1 > {}.db1.sql'.format(dmy)
DUMP2 = 'mysqldump -uuser -ppassword  db2 > {}.db2.sql'.format(dmy)

if not os.path.exists(DB1Location):
        os.makedirs(DB1Location)


os.chdir('{}'.format(DB1Location))
os.system(DUMP1)

with open('{}.db1.sql'.format(dmy), 'rb') as f_in:
    with gzip.open('{}.db1.sql.gz'.format(dmy), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


s3.Bucket(bucket).upload_file("{}.db1.sql.gz".format(dmy), "backups/{}.db1.sql.gz".format(dmy))

file1 = "{}.db1.sql.gz".format(ddmy)

if os.path.exists(file1):
    os.remove(file1)
else:
    print("Sorry, I can not remove %s file." %file1)





if not os.path.exists(DB2Location):
        os.makedirs(DB2Location)

os.chdir('{}'.format(DB2Location))
os.system(DUMP2)

with open('{}.db2.sql'.format(dmy), 'rb') as f_in:
    with gzip.open('{}.db2.sql.gz'.format(dmy), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

s3.Bucket(bucket).upload_file("{}.db2.sql.gz".format(dmy), "backup/{}.db2.sql.gz".format(dmy))


file2 = "{}.db2.sql.gz".format(ddmy)

if os.path.exists(file2):
    os.remove(file2)
else:
    print("Sorry, I can not remove %s file." %file2)


