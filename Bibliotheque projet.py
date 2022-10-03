import mysql.connector as MC 

conn = MC.connect(host="localhost",user="root",password="1234", database="biblio")
cursor = conn.cursor()


requete = input("\nQue voulez-vous faire ?\n [1] Recherche d'une oeuvre en fonction de son titre\n [2]Réservation d'une oeuvre\n")

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
        ("Isolation totale", "9", "Marsden Todd", "Editions Atlas", "2019-06-26 12:35:58"),
        ("Isolation totale", "9", "Merritt Garcia", "Editions Atlas", "2019-06-26 12:35:58"),
        ("La marche du siècle", "6", "Tucker Patton", "Gallimard", "2019-05-22 12:35:58"),
        ("Lagon Bleu", "4", "Scott Villarreal", "Milady", "2019-02-17 12:35:58"),
        ("Le trône écarlate", "10", "Fritz Dennis", "Eyrolles", "2019-08-19 12:35:58"),
        ("Le trône écarlate", "10", "Fritz Dennis", "Gallimard", "2019-03-12 12:35:58"),
        ("Le trône écarlate", "10", "Fritz Dennis", "Hachette", "2019-08-18 12:35:58"),
        ("Les 9 couronnes", "1", "John Harris", "Hachette", "2019-08-18 12:35:58"),
        ("Les 9 couronnes", "1", "Nathan Barber", "Hachette", "2019-02-12 12:35:58"),
        ("Les fleurs du Mal", "5", "John Harris", "Editions Atlas", "2019-01-30 12:35:58"),
        ("Les fleurs du Mal", "5", "Oscar Paul", "Editions Atlas", "2019-01-30 12:35:58"),
        ("Les fleurs du Mal", "5", "John Harris", "Flammarion", "2019-08-10 12:35:58"),
        ("Les fleurs du Mal", "5", "Oscar Paul", "Flammarion", "2019-08-10 12:35:58"),
        ("Puits sans fond", "2", "Oscar Paul", "Eyrolles", "2019-04-23 12:35:58"),
        ("Puits sans fond", "2", "Nathan Barber", "Eyrolles", "2019-04-23 12:35:58"),
        ("Trois dans un appartement", "4", "Alfonso Fuentes", "Bayard", "2019-06-16 12:35:58"),
        ("Vol de nuit", "2", "Marshall Mccoy", "Editions Atlas", "2019-06-16 12:35:58"),
    ]
    
    for i in livres:
        cursor.execute("""INSERT INTO bibliotheque (id, titre_livre, code_rayon, auteurs, editeurs, date_acquisition) VALUES(NULL, %s, %s, %s, %s, %s)""", i)


    cursor.execute("SELECT * FROM bibliotheque")
    resultat = cursor.fetchall()
    for i in resultat:
        print(i)

    if requete == '1' : 
        titre_livre_recherche = input('Quelle est le titre de votre livre ? ')
        cursor.execute("""SELECT id, titre_livre, code_rayon, auteurs, editeurs, date_acquisition FROM bibliotheque WHERE titre_livre = LIKE  '%' + titre_livre_recherche + '% """)
        resultat = cursor.fetchall()
        for row in resultat:
            print('{0}, {1}, {2}, {3}, {4}, {5},'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
        

    if requete == '2' :
        print("Pas disponible")
        

except Exception as e:
    print(e)

 

finally:
    conn.commit()
    conn.close()








