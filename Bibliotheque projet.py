import mysql.connector as MC

############################################
######## CONNEXION AU SERVEUR MYSQL ########
############################################

conn = MC.connect(host="localhost",user="root",password="78110Bs78")
cursor = conn.cursor()

try:
    cursor.execute("USE biblio_eh_ns;")
except:
    cursor.execute("CREATE DATABASE IF NOT EXISTS biblio_eh_ns;")
    conn.commit()
    cursor.execute("USE biblio_eh_ns;")

try:
    #####################################
    ######## CREATION DES TABLES ########
    #####################################

    ### Table contenant les abonnés
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS abonnes (
        id_abonne SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        nom VARCHAR(50) NOT NULL,
        prenom VARCHAR(50) NOT NULL,
        age INT NOT NULL, 
        PRIMARY KEY(id_abonne)
    );
    """)

    ### Table contenant les livres
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bibliotheque (
        id_livre SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        titre_livre VARCHAR(50) NOT NULL,
        code_rayon INT NOT NULL,
        auteur VARCHAR(50) NOT NULL, 
        editeur VARCHAR(50) NOT NULL,
        date_acquisition DATETIME NOT NULL,
        etat VARCHAR(10), 
        reservation INT,
        id_abonne SMALLINT REFERENCES abonnes(id_abonne),
        PRIMARY KEY(id_livre)
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

    #######################################################
    ######## INSERTION DES VALEURS DANS LES TABLES ########
    #######################################################
    cursor.execute("SELECT * FROM bibliotheque")
    test_livres = cursor.fetchall()
    if len(test_livres) == 0:
        for i in livres:
            cursor.execute("""INSERT INTO bibliotheque (id_livre, titre_livre, code_rayon, auteur, editeur, date_acquisition) VALUES(NULL, %s, %s, %s, %s, %s)""", i)
        conn.commit()

    ############################################
    ######## CONNEXION DE L'UTILISATEUR ########
    ############################################
    print('Bienvenue !')
    hasAccount = int(input("Options disponibles :\n - [1] Oui\n - [2] Non\nAvez-vous déjà un compte ? "))
    if hasAccount == 1:
        id_account = int(input("Quel est votre identifiant ? "))
        prenom_account = str(input("Quel est votre prénom ? ")).lower()
        cursor.execute(f"SELECT * FROM abonnes WHERE id_abonne = '{id_account}' AND prenom = '{prenom_account}'")
        account_details = cursor.fetchone()
    else:
        prenom_account = str(input("Quel est votre prénom ? ")).lower()
        nom_account = str(input("Quel est votre nom ? ")).lower()
        age_account = int(input("Quel âge avez-vous ? "))
        cursor.execute(f"SELECT * FROM abonnes WHERE nom = '{nom_account}' AND prenom = '{prenom_account}' AND age = '{age_account}'")
        accountExists = cursor.fetchone()
        if accountExists:
            print("Cette personne possède déjà un compte !")
            account_details = None
        else:
            # ERREURS ICI
            print(nom_account, prenom_account, age_account)
            cursor.execute(f"INSERT INTO abonnes VALUES (NULL, '{nom_account}', '{prenom_account}', '{age_account}')")
            
            cursor.execute(f"SELECT * FROM abonnes WHERE nom = '{nom_account}' AND prenom = '{prenom_account}' AND age = '{age_account}'")
            
            account_details = cursor.fetchone()

    if account_details:
        ### Si l'utilisateur est connecté
        print('\nBienvenue sur le portail de votre bibliothèque !\nMenu principal :')
        while True:
            requete = int(input("\nOptions disponibles :\n - [1] Recherche par titre\n - [2] Recherche par auteur\n - [3] Réservation d'une oeuvre\n - [4] Retour d'une oeuvre\nQue voulez-vous faire ? "))

            if requete == 1: 
                print('')
                titre_livre_recherche = str(input('Quelle est le titre de votre livre ? '))
                liste_mots = titre_livre_recherche.split()
                liste_resultats = []
                for mot in liste_mots:
                    if len(mot) >= 3 and mot != 'les':
                        cursor.execute(f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre FROM bibliotheque WHERE titre_livre LIKE '%{mot}%'")
                        resultat = cursor.fetchall()
                try:
                    if len(resultat) > 0:
                        for row in resultat:
                            livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}"
                            if livre_data not in liste_resultats:
                                liste_resultats.append(livre_data)
                        print('')
                        print('Votre recherche a donné les résultats suivants :')
                        for res in liste_resultats:
                            print('')
                            print(f" - {res}")
                        del resultat
                    else:
                        print('')
                        print("Votre recherche n'a donné aucun résultat.")
                        del resultat
                except:
                    print('')
                    print("Votre recherche n'a donné aucun résultat.")
                    pass
            
            elif requete == 2:
                print('')
                auteur_recherche = str(input("Quelle est le nom de l'auteur ? "))
                liste_mots = auteur_recherche.split()
                liste_resultats = []
                for mot in liste_mots:
                    if len(mot) >= 3 and mot != 'les':
                        cursor.execute(f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre FROM bibliotheque WHERE auteur LIKE '%{mot}%'")
                        resultat = cursor.fetchall()
                try:
                    if len(resultat) > 0:
                        for row in resultat:
                            livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}"
                            if livre_data not in liste_resultats:
                                liste_resultats.append(livre_data)
                        print('')
                        print('Votre recherche a donné les résultats suivants :')
                        for res in liste_resultats:
                            print('')
                            print(f" - {res}")
                        del resultat
                    else:
                        print('')
                        print("Votre recherche n'a donné aucun résultat.")
                        del resultat
                except:
                    print('')
                    print("Votre recherche n'a donné aucun résultat.")
                    pass

            elif requete == 3:
                print('')
                identifiant = int(input("Quel est l'identifiant de votre livre ? "))
                cursor.execute(f"SELECT * FROM bibliotheque WHERE id_livre = '{identifiant}'")
                etat = cursor.fetchall()
                print('')
                if etat[0][6] == None:
                    cursor.execute(f"UPDATE bibliotheque SET etat = 'reserve' WHERE id_livre = {identifiant}")
                    conn.commit()
                    print('Réservation effectuée avec succès')
                else:
                    print("Le livre est déjà réservé")

            elif requete == 4:
                print('')
                identifiant = int(input("Quel est l'identifiant de votre livre ? "))
                cursor.execute(f"SELECT * FROM bibliotheque WHERE id_livre = '{identifiant}'")
                etat = cursor.fetchall()
                print('')
                if etat[0][6] == 'reserve':
                    cursor.execute(f"UPDATE bibliotheque SET etat = NULL WHERE id_livre = {identifiant}")
                    conn.commit()
                    print('Retour effectué avec succès')
                else:
                    print("Le livre n'est pas réservé")


except Exception as e:
    print(e)

 

finally:
    conn.commit()
    conn.close()
