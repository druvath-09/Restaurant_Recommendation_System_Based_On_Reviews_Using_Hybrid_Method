import pymysql

def connection():
    con=pymysql.connect(host='localhost', user='root',password='',database='restaurant',charset='utf8')

    return con

def create_customer_table():
    con = connection()
    cursor = con.cursor()
    create_query = """
    CREATE TABLE IF NOT EXISTS customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        phone VARCHAR(15)
    )
    """
    cursor.execute(create_query)
    con.commit()
    con.close()
    print("Customer table created successfully.")

# Call it once to create the table
create_customer_table()