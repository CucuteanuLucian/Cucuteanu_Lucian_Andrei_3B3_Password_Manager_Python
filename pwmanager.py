import sys
import sqlite3

def hash_key_write(password):
    try:
        file = open("hashkey.meta", "w")
        file.write(password)

    except FileNotFoundError:
        print(f"Eroare: Fisier inexistent")
    except Exception as e:
        print(f"Eroare: {e}")


def opendb():
    try:
        print("Pornim baza de date...\n")
        global conn, cursor
        conn = sqlite3.connect("pwmanager.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords 
        (id INTEGER PRIMARY KEY,
        website TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL)
        ''')
        conn.commit()
    except Exception as e:
        print(f"Eroare: {e}")


def add(website, username, password):
    try:
        print("Execut comanda add...\n")
        cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)',
                   (website, username, password))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Eroare: Username existent!\n")

def get(website):
    try:
        print("Execut comanda get...\n")
        query = 'SELECT website, username, password FROM passwords where website = ?'
        cursor.execute(query, (website,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Goala")
        print()
    except Exception as e:
        print(f"Eroare: {e}")


def remove(website):
    try:
        print("Execut comanda remove...\n")
        query = 'DELETE FROM passwords where website = ?'
        cursor.execute(query, (website,))
        conn.commit()
    except Exception as e:
        print(f"Eroare: {e}")

def list():
    try:
        print("Execut comanda list...\n")
        cursor.execute("SELECT * from passwords")
        rows = cursor.fetchall()
        print("Lista bazei de date este:")
        if rows:
            for row in rows:
                print(f"ID: {row[0]} | Website: {row[1]} | Username: {row[2]} | Password: {row[3]}")
        else:
            print("Goala")
        print()
    except Exception as e:
        print(f"Eroare: {e}")


def closedb():
    try:
        print("Inchidem baza de date...")
        conn.close()
    except Exception as e:
        print(f"Eroare: {e}")


def main():
    print("Bine ai venit! Numele proiectului este: Password manager")
    if len(sys.argv) < 2:
        print("Eroare: Prea putine argumente!")
        print("Incearca ca input: \"pwmanager.py <master_password> -<operation> <website> <username> <password>\"")
        exit(0)
    try:
        opendb()
        master_password=sys.argv[1]
        operation=sys.argv[2]
        print(f"Operatia aleasa este: \"{operation}\"\n")
        if operation == '-add':
            if len(sys.argv) != 6:
                print("Input-ul comenzii \"add\" este invalid..")
                exit(0)
            add(sys.argv[3], sys.argv[4], sys.argv[5])
        elif operation == '-get':
            get(sys.argv[3])
        elif operation == '-remove':
            remove(sys.argv[3])
        elif operation == '-list':
            list()
        else:
            print("Eroare: Comanda Invalida!")
            exit(0)
        closedb()

        hash_key_write("ParolaSecreta")
        file = open("hashkey.meta", "r")
        file_buffer = file.read()
        if master_password == file_buffer:
            print("Correct Key!")
        else:
            print("Wrong Key!")
            exit(0)
    except IndexError:
        print("Eroare: Incearca ca input: \"pwmanager.py <master_password> -<operation> <website> <username> <password>\"")
    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == "__main__":
    main()