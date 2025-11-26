# 查看数据库中的数据
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 先查看数据库中有哪些表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("数据库中的表:", tables)

# 如果有表，则查询第一个表的数据
if tables:
    table_name = tables[0][0]
    cursor.execute(f"SELECT * FROM {table_name}")
    print(f"{table_name} 表中的数据:", cursor.fetchall())
else:
    print("数据库中没有表，需要先创建表并插入数据")

conn.close()
