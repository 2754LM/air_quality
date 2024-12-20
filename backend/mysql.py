import pymysql
connection = pymysql.connect(
    host='47.238.226.55',
    user='root',
    password='Aa_123456',
    database='air_database'
)
def check_user(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (username, password))
        return cursor.fetchone() is not None
def check_exist(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s;", (username))
        return cursor.fetchone() is not None
def add_user(username, password):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        connection.commit()
        
if __name__ == '__main__':
    add_user('kano', 'kano')