# coding=utf-8
import cx_Oracle

conn = cx_Oracle.connect('test/123456@10.20.10.2:49161/XE', encoding="UTF-8", nencoding="UTF-8")
print conn.version
# 用自己的实际数据库用户名、密码、主机ip地址 替换即可
curs = conn.cursor()
SQL = "select * from SYSPROCCTRL"
rr = curs.execute(SQL)
row = curs.fetchall()
for item in row:
    print item[2].decode('utf-8')
print(row)
curs.close()
conn.close()

