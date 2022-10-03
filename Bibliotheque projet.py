import mysql.connector as MC 
conn = MC.connect(host="localhost",user="root",password="78110Bs78", database="biblio")
cursor = conn.cursor()

try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bibliotheque (
        id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        titre_livre varchar(50) NOT NULL,
        code_rayon int NOT NULL,
        auteurs varchar(50) NOT NULL, 
        editeurs varchar(50) NOT NULL,
        date_acquisition datetime NOT NULL,
        PRIMARY KEY(id)
    );
    """)
    livres = [
        ("Belle", "10", "Marsden Todd", "Editions Atlas", "2019-06-16 12:35:58"),

    ]
    
    for i in livres:
        cursor.execute("""INSERT INTO bibliotheque (id, titre_livre, code_rayon, auteurs, editeurs, date_acquisition) VALUES(NULL, %s, %s, %s, %s, %s)""", i)


    cursor.execute("SELECT * FROM bibliotheque")
    resultat = cursor.fetchall()
    for i in resultat:
        print(i)

except Exception as e:
    print(e)

finally:
    conn.commit()
    conn.close()
