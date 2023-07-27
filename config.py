# config.py
import os

# MySQL
# database.py
mysql_user = 'cuc_cloud'
mysql_password = 'QQK3aCAxAqj4LtaTk0AI'
mysql_host = '127.0.0.1'
mysql_schema = 'cuc_cloud_database'
#run.py
# Flask 
host = '127.0.0.1'
port = 80
debug = True

#csrf_key='privatekey'
csrf_key = os.urandom(24)
#models/online_user

token_expired = 30*60

storage_path='./testpath'
nacl_sk_path='./nacl_sk_path'

# models/file
# config.py

allowed_file_suffix_list = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


