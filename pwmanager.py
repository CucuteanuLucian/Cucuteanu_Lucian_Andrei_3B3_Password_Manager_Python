import sys
import sqlite3

def xor_op(x, y):
    if len(x)!=len(y):
        print("Dimensiuni diferite")
        exit(0)
    n=len(x)
    rez=''
    for i in range(0, n):
        rez += str(int(x[i]) ^ int(y[i]))
    return rez

def not_op(x):
    rez=''
    n=len(x)
    for i in range(0,n):
        if x[i]=='0':
            rez+='1'
        else:
            rez+='0'
    return rez


def and_op(x,y):
    if len(x) != len(y):
        print("Dimensiuni diferite")
        exit(0)
    n=len(x)
    rez=''
    for i in range(0,n):
        rez += str(int(x[i]) & int(y[i]))
    return rez


def or_op(x,y):
    if len(x) != len(y):
        print("Dimensiuni diferite")
        exit(0)
    n=len(x)
    rez=''
    for i in range(0,n):
        rez += str(int(x[i]) | int(y[i]))
    return rez


def binary_add(x,y):
    if len(x) != len(y):
        print("Dimensiuni diferite")
        exit(0)
    rez = bin(int(x, 2) + int(y, 2))[2:]
    if len(rez) > 32:
        rez = rez[1:]
    while len(rez) < 32:
        rez = '0'+rez
    return rez

def sha1(password):
    ascii_codes = []
    for c in password:
        ascii_codes.append(ord(c))
    #print(ascii_codes)
    bin_ascii_codes = []
    for b in ascii_codes:
        bin_ascii_codes.append(bin(b)[2:])
    #print(bin_ascii_codes)
    eight_bin_ascii_codes = []
    for b in bin_ascii_codes:
        while len(b)<8:
            b="0" + b
        eight_bin_ascii_codes.append(b)
    #print("eight_bin_ascii_codes:", eight_bin_ascii_codes)
    joined_eight_bin_ascii_codes = "".join(eight_bin_ascii_codes)
    #print("joined_eight_bin_ascii_codes:", joined_eight_bin_ascii_codes)
    one_joined_eight_bin_ascii_codes = joined_eight_bin_ascii_codes + "1"
    #print("one_joined_eight_bin_ascii_codes:", one_joined_eight_bin_ascii_codes)
    while len(one_joined_eight_bin_ascii_codes) % 512 != 448:
        one_joined_eight_bin_ascii_codes += "0"
    padded_by_zero_until_mod_512_neq_448=one_joined_eight_bin_ascii_codes
    #print("padded_by_zero_until_mod_512_neq_448:", padded_by_zero_until_mod_512_neq_448)
    #print("padded_by_zero_until_mod_512_neq_448_length:", len(padded_by_zero_until_mod_512_neq_448))
    last_64_length_of_binary_ascii_password=bin(len(joined_eight_bin_ascii_codes))[2:]
    #print("last_64_length_of_binary_ascii_password:", last_64_length_of_binary_ascii_password)
    while len(last_64_length_of_binary_ascii_password)<64:
        last_64_length_of_binary_ascii_password="0"+last_64_length_of_binary_ascii_password
    padded_till_64_bits=last_64_length_of_binary_ascii_password
    #print("padded_till_64_bits:", padded_till_64_bits)
    #print("padded_till_64_bits length:", len(padded_till_64_bits))
    final_concat=padded_by_zero_until_mod_512_neq_448+padded_till_64_bits
    #print("final_concat:", final_concat)
    #print("final_concat_length:", len(final_concat))

    chunks_512 = []
    nr_chunks_512=len(final_concat)//512
    #print(nr_chunks_512)

    for i in range(0, nr_chunks_512):
        chunks_512.append(final_concat[i*512:(i+1)*512])
    #print(chunks_512)

    nr_chunks_32 = 512 // 32  #16
    for chunk_512 in chunks_512:
        chunk_512 = "".join(chunk_512)
        chunks_32 = []
        for i in range(0, nr_chunks_32):
            chunks_32.append(chunk_512[i * 32:(i + 1) * 32])
        #print(chunks_32)

        #print(chunks_32[0])
        #print(chunks_32[1])
        #print(xor_op(chunks_32[0],chunks_32[1]))
        for i in range(16,80):
            temp_chunk = xor_op(xor_op(xor_op(chunks_32[i-3], chunks_32[i-8]), chunks_32[i-14]), chunks_32[i-16])
            temp_chunk=temp_chunk[1:]+temp_chunk[:1]    #shiftat la stanga cu 1
            chunks_32.append(temp_chunk)

        #print(chunks_32)
        #print(len(chunks_32))

    h0 = '01100111010001010010001100000001'
    h1 = '11101111110011011010101110001001'
    h2 = '10011000101110101101110011111110'
    h3 = '00010000001100100101010001110110'
    h4 = '11000011110100101110000111110000'

    a=h0
    b=h1
    c=h2
    d=h3
    e=h4

    for i in range(0,80):
        if i<20:

            first=and_op(b,c)
            second=and_op(not_op(b),d)
            f=or_op(first, second)
            k='01011010100000100111100110011001'
        elif i < 40:

            first=xor_op(b,c)
            f=xor_op(first, d)
            k='01101110110110011110101110100001'
        elif i < 60:

            first=and_op(b,c)
            second=and_op(b,d)
            third=and_op(c,d)
            f=or_op(or_op(first,second), third)
            k='10001111000110111011110011011100'
        elif i < 80:

            first = xor_op(b, c)
            f = xor_op(first, d)
            k='11001010011000101100000111010110'
        #temp=binary_add(binary_add(binary_add(binary_add((a[5:]+a[:5]), f), e), chunks_32[i]), k)
        t_a=a[5:]+a[:5]
        temp=binary_add(t_a, f)
        temp=binary_add(temp, e)
        temp = binary_add(temp, k)
        temp=binary_add(temp, chunks_32[i])

        e=d
        d=c
        c=b[30:]+b[:30]
        b=a
        a=temp

    h0 = binary_add(h0, a)
    h1 = binary_add(h1, b)
    h2 = binary_add(h2, c)
    h3 = binary_add(h3, d)
    h4 = binary_add(h4, e)

    #print(h0+h1+h2+h3+h4)
    hex_h0 = str(hex(int(h0, 2))[2:])
    hex_h1 = str(hex(int(h1, 2))[2:])
    hex_h2 = str(hex(int(h2, 2))[2:])
    hex_h3 = str(hex(int(h3, 2))[2:])
    hex_h4 = str(hex(int(h4, 2))[2:])
    rez_final=hex_h0+hex_h1+hex_h2+hex_h3+hex_h4
    #print(rez_final)
    return rez_final

def hash_key_write(password):
    try:
        file = open("hashkey.meta", "w")
        file.write(sha1(password))

    except FileNotFoundError:
        print(f"Eroare: Fisier inexistent")
    except Exception as e:
        print(f"Eroare: {e}")


def cripteaza(password, key):
    n = len(key)
    rez = ""
    for i in range(0, len(password)):
        key_byte = key[(i * 2) % n : (i * 2 + 2)% n]
        key_byte = int(key_byte, 16)
        rez += chr(ord(password[i]) ^ key_byte)
    #print(rez)
    return rez


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


def add(website, username, password, logged, key):
    try:
        if logged == True:
            print("Execut comanda add...\n")
            cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)',
                           (website, username, cripteaza(password, key)))
            conn.commit()
            print("Adaugat cu succes!\n")
        else:
            print("Eroare: Nu poti adauga in baza de date: parola introdusa este incorecta!\n")
    except sqlite3.IntegrityError as e:
        print("Eroare: Username existent!\n")

def get(website, logged, key):
    try:
        print("Execut comanda get...\n")
        query = 'SELECT website, username, password FROM passwords where website = ?'
        cursor.execute(query, (website,))
        rows = cursor.fetchall()
        if logged == False:
            if rows:
                for row in rows:
                    print(f"Website: {row[0]} | Username: {row[1]} | Password: {row[2]}")
            else:
                print("Goala")
            print()
        else:
            if rows:
                for row in rows:
                    print(f"Website: {row[0]} | Username: {row[1]} | Password: {cripteaza(row[2], key)}")
            else:
                print("Goala")
            print()
    except Exception as e:
        print(f"Eroare: {e}")


def remove(website, logged):
    try:
        if logged == True:
            print("Execut comanda remove...\n")
            query = 'DELETE FROM passwords where website = ?'
            cursor.execute(query, (website,))
            conn.commit()
        else:
            print("Eroare: Nu poti sterge din baza de date: Parola introdusa este incorecta!\n")
    except Exception as e:
        print(f"Eroare: {e}")

def list(logged, key):
    try:
        print("Execut comanda list...\n")
        cursor.execute("SELECT * from passwords")
        rows = cursor.fetchall()
        print("Lista bazei de date este:")
        if logged==False:
            if rows:
                for row in rows:
                    print(f"ID: {row[0]} | Website: {row[1]} | Username: {row[2]} | Password: {row[3]}")
            else:
                print("Goala")
            print()
        else:
            if rows:
                for row in rows:
                    print(f"ID: {row[0]} | Website: {row[1]} | Username: {row[2]} | Password: {cripteaza(row[3], key)}")
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
        # hash_key_write("ParolaSecreta")
        file = open("hashkey.meta", "r")
        file_buffer = file.read()
        if sha1(master_password) == file_buffer:
            print("Parola corecta, bine ai revenit!\n")
            logged=True
        else:
            print("Parola Incorecta!\n")
            logged=False
        file.close()

        operation=sys.argv[2]
        #print(f"Operatia aleasa este: \"{operation}\"\n")
        if operation == '-add':
            if len(sys.argv) != 6:
                print("Input-ul comenzii \"add\" este invalid..")
                exit(0)
            add(sys.argv[3], sys.argv[4], sys.argv[5], logged, file_buffer)
        elif operation == '-get':
            get(sys.argv[3], logged, file_buffer)
        elif operation == '-remove':
            remove(sys.argv[3], logged)
        elif operation == '-list':
            list(logged, file_buffer)
        else:
            print("Eroare: Comanda Invalida!")
            exit(0)
        closedb()

    except IndexError:
        print("Eroare: Incearca ca input: \"pwmanager.py <master_password> -<operation> <website> <username> <password>\"")
    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == "__main__":
    main()