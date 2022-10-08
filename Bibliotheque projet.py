import mysql.connector as MC 

conn = MC.connect(host="localhost",user="root",password="1234", database="biblio")
cursor = conn.cursor()



try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bibliotheque (
        id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        titre_livre VARCHAR(50) NOT NULL,
        code_rayon INT NOT NULL,
        auteurs VARCHAR(50) NOT NULL, 
        editeurs VARCHAR(50) NOT NULL,
        date_acquisition DATETIME NOT NULL,
        etat VARCHAR(10), 
        reservation INT, 
        PRIMARY KEY(id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS abonnes (
        id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        nom VARCHAR(50) NOT NULL,
        prenom VARCHAR(50) NOT NULL,
        age INT NOT NULL, 
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
    
    cursor.execute("SELECT * FROM bibliotheque")
    test_livres = cursor.fetchall()
    if len(test_livres) == 0:
        for i in livres:
            cursor.execute("""INSERT INTO bibliotheque (id, titre_livre, code_rayon, auteurs, editeurs, date_acquisition) VALUES(NULL, %s, %s, %s, %s, %s)""", i)


    cursor.execute("SELECT * FROM bibliotheque")
    resultat = cursor.fetchall()
    # for i in resultat:
    #     print(i)
    while True:
        requete = int(input("\nOptions disponibles :\n - [1] Recherche par titre\n - [2] Recherche par auteur\n - [3] Réservation d'une oeuvre\n - [4] Retour d'une oeuvre\n - [5] Nouveau abonné\nQue voulez-vous faire ? "))

        if requete == 1: 
            titre_livre_recherche = str(input('Quelle est le titre de votre livre ? '))
            liste_mots = titre_livre_recherche.split()
            liste_resultats = []
            for mot in liste_mots:
                if len(mot) >= 3 and mot != 'les':
                    cursor.execute(f"SELECT titre_livre, auteurs, editeurs, code_rayon, id FROM bibliotheque WHERE titre_livre LIKE '%{mot}%'")
                    resultat = cursor.fetchall()
            if len(resultat) > 0:
                for row in resultat:
                    livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}\n"
                    if livre_data not in liste_resultats:
                        liste_resultats.append(livre_data)
                print('Votre recherche a donné les résultats suivants : \n')
                for res in liste_resultats:
                    print(res)
            else:
                print("Votre recherche n'a donné aucun résultat.")
        
        elif requete == 2:
            auteur_recherche = str(input("Quelle est le nom de l'auteur ? "))
            liste_mots = auteur_recherche.split()
            liste_resultats = []
            for mot in liste_mots:
                if len(mot) >= 3 and mot != 'les':
                    cursor.execute(f"SELECT titre_livre, auteurs, editeurs, code_rayon, id FROM bibliotheque WHERE auteurs LIKE '%{mot}%'")
                    resultat = cursor.fetchall()
            if len(resultat) > 0:
                for row in resultat:
                    livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}\n"
                    if livre_data not in liste_resultats:
                        liste_resultats.append(livre_data)
                print('Votre recherche a donné les résultats suivants : \n')
                for res in liste_resultats:
                    print(res)
            else:
                print("Votre recherche n'a donné aucun résultat.")

        elif requete == 3:
            print('')
            identifiant = int(input("Quel est l'identifiant de votre livre ? "))
            cursor.execute(f"SELECT * FROM bibliotheque WHERE id = '{identifiant}'")
            etat = cursor.fetchall()
            print('')
            if etat[0][6] == None:
                cursor.execute(f"UPDATE bibliotheque SET etat = 'reserve' WHERE id = {identifiant}")
                conn.commit()
                print('Réservation effectuée avec succès')
            else:
                print("Le livre est déjà réservé")

        elif requete == 4:
            print('')
            identifiant = int(input("Quel est l'identifiant de votre livre ? "))
            cursor.execute(f"SELECT * FROM bibliotheque WHERE id = '{identifiant}'")
            etat = cursor.fetchall()
            print('')
            if etat[0][6] == 'reserve':
                cursor.execute(f"UPDATE bibliotheque SET etat = NULL WHERE id = {identifiant}")
                conn.commit()
                print('Retour effectué avec succès')
            else:
                print("Le livre n'est pas réservé")
        """
        elif requete == 5 : 
            print ('')
            inscription_abonné = str(input('Vous êtes nouveau ? '))
            if inscription_abonné == 'oui' or 'Oui' : 
                nom = str(input('Quel est votre nom ? '))
                prenom = str(input('Quel est votre prénom ? '))
                age = int(input('Quel est votre âge ? '))
                cursor.execute(f"INSERT INTO abonnes = '{nom}'")
                cursor.commit()
                cursor.execute(f"INSERT INTO abonnes  = '{prenom}'")
                cursor.commit()
                cursor.execute(f"INSERT INTO abonnes  = '{age}'")
                cursor.commit()
                cursor.execute(f"SELECT id FROM abonnes WHERE nom and prenom and age = '{nom}' and '{prenom}' and '{age}'")
                cursor.commit()
                print("Vous êtes inscrit ! Voici votre identifiant", id)
            
            else : 
                print("Vous n'êtes pas inscrit")
            """


except Exception as e:
    print(e)

 

finally:
    conn.commit()
    conn.close()
