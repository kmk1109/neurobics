import pymysql
import numpy as np

mp_npy = []
convert_mp_npy = np.fromstring(mp_npy[1:-1], dtype=np.float64, sep=' ')
print(convert_mp_npy)

# access to DB
db = pymysql.connect(host='localhost',
                     port='3306',
                     user='python',
                     passwd='python1234',
                     db='pythondb',
                     charset='utf8')

cursor = db.cursor()

sql = """CREATE TABLE mp_table(
    idx INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mp_X 
    mp_Y
    mp_Z
    mp_V
    
    )"""
 