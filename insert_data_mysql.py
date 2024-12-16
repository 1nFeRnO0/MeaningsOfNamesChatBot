import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'name_meanings'
}

# Подключение к базе данных
try:
    db_connection = mysql.connector.connect(**DB_CONFIG)
    db_cursor = db_connection.cursor()
    print("Успешное подключение к базе данных.")
except mysql.connector.Error as err:
    print(f"Ошибка подключения к базе данных: {err}")
    exit(1)

# db_cursor.execute('CREATE DATABASE name_meanings;')

# Создание таблицы, если её ещё нет
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    meaning TEXT NOT NULL
)
''')

# Данные для вставки
names_and_meanings = [
    ("Иван", "Божья милость"),
    ("Мария", "Горькая, печальная"),
    ("Александр", "Защитник людей"),
    ("Екатерина", "Чистая, непорочная"),
    ("Дмитрий", "Посвященный Деметре"),
    ("Анна", "Благодать"),
    ("Михаил", "Кто как Бог"),
    ("София", "Мудрость"),
    ("Виктор", "Победитель"),
    ("Ольга", "Святая, священная")
]

# Вставка данных в таблицу
try:
    db_cursor.executemany("INSERT INTO names (name, meaning) VALUES (%s, %s)", names_and_meanings)
    db_connection.commit()
    print(f"Успешно добавлено {db_cursor.rowcount} записей.")
except mysql.connector.Error as err:
    print(f"Ошибка вставки данных: {err}")
finally:
    db_cursor.close()
    db_connection.close()
