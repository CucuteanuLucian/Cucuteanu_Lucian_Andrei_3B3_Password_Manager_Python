import sys
import sqlite3

class PM:
    def __init__(self):
        print("Pornim baza de date...\n")
        global conn, cursor
        conn = sqlite3.connect("pwmanager.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords 
        (id INTEGER PRIMARY KEY, website TEXT NOT NULL,
        username TEXT NOT NULL,
        password BLOB NOT NULL,
        salt BLOB NOT NULL )''')
        conn.commit()

    def add(self, website, username, password):
        print("Execut comanda add...\n")
        salt="abcd"
        cursor.execute('INSERT INTO passwords (website, username, password, salt) VALUES (?, ?, ?, ?)',
                       (website, username, password, salt))
        conn.commit()


    def get(self, website):
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


    def remove(self, website):
        print("Execut comanda remove...\n")
        query = 'DELETE FROM passwords where website = ?'
        cursor.execute(query, (website,))
        conn.commit()

    def list(self):
        print("Execut comanda list...\n")
        cursor.execute("SELECT * from passwords")
        rows = cursor.fetchall()
        print("Lista bazei de date este:")
        if rows:
            for row in rows:
                print(row)
        else:
            print("Goala")
        print()

    def closedb(self):
        print("Inchidem baza de date...\n")
        conn.close()


def main():
    print("Bine ai venit! Numele proiectului este: Password manager")
    if len(sys.argv) < 2:
        print("Eroare: Prea putine argumente!")
        print("Incearca ca input: \"pwmanager.py <master_password> -<operation> <website> <username> <password>\"")
        exit(0)
    try:
        general = PM()
        operation=sys.argv[2]
        print(f"Operatia aleasa este: \"{operation}\"\n")
        if operation == '-add':
            if len(sys.argv) != 6:
                print("Input-ul comenzii \"add\" este invalid..")
                exit(0)
            general.add(sys.argv[3], sys.argv[4], sys.argv[5])
        elif operation == '-get':
            general.get(sys.argv[3])
        elif operation == '-remove':
            general.remove(sys.argv[3])
        elif operation == '-list':
            general.list()
        else:
            print("Eroare: Comanda Invalida!")
            exit(0)
        general.closedb()
    except IndexError:
        print("Eroare: Incearca ca input: \"pwmanager.py <master_password> -<operation> <website> <username> <password>\"")
    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == "__main__":
    main()