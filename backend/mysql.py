import pymysql

def check_user(username, password):
    connection = pymysql.connect(
        host='47.238.226.55',
        user='root',
        password='Aa_123456',
        database='air_database'
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (username, password))
        return cursor.fetchone() is not None

if __name__ == '__main__':
    print(check_user('a', '1'))