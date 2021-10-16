import sqlite3


# Connect to database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def main():
    connection = sqlite3.connect("database.db")

    with open("schema.sql") as file:
        connection.executescript(file.read())

    # Add a default user
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))

    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
