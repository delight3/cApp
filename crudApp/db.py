import pymysql

# Function to establish and return a mySQL database connection using pymysql
def connect_db():
    return pymysql.connect(
        host="localhost", #MySQL host (localhost ehen using XAMPP)
        user="root",  #MySQL username (XAMPP default is 'root')
        password="", #MySQL password (empty by default in XAMPP)
        database="management_db" #Name of the database created in phpMyAdmin
    )