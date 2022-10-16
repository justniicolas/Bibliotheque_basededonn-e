import mysql.connector as MC
from datetime import date
from datetime import datetime, timedelta
import locale

############################################
############ INSERTION TIME ################
############################################
locale.setlocale(locale.LC_ALL, "french")

date_jour = date.today()
hier_jour = date_jour - timedelta(1)
demain_jour = date_jour + timedelta(1)
semaine_prochaine = date_jour + timedelta(7)

############################################
######## CONNEXION AU SERVEUR MYSQL ########
############################################

conn = MC.connect(host="localhost", user="root", password="78110Bs78")
cursor = conn.cursor()

try:
    cursor.execute("USE biblio_eh_ns;")
except:
    cursor.execute("CREATE DATABASE IF NOT EXISTS biblio_eh_ns;")
    conn.commit()
    cursor.execute("USE biblio_eh_ns;")


#####################################
######## CREATION DES TABLES ########
#####################################

# Table contenant les abonnés
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS abonnes (
    id_abonne SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    age INT NOT NULL, 
    courriel VARCHAR(70) NOT NULL, 
    PRIMARY KEY(id_abonne)
);
"""
)

# Table contenant les livres
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS bibliotheque (
    id_livre SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
    titre_livre VARCHAR(50) NOT NULL,
    code_rayon INT NOT NULL,
    auteur VARCHAR(50) NOT NULL, 
    editeur VARCHAR(50) NOT NULL,
    date_acquisition DATETIME NOT NULL,
    etat VARCHAR(10), 
    reservation VARCHAR(10),
    id_abonne SMALLINT REFERENCES abonnes(id_abonne),
    PRIMARY KEY(id_livre)
);
"""
)

livres = [
    ("Belle", "10", "Marsden Todd", "Editions Atlas", "2019-06-16 12:35:58"),
    ("Isolation totale", "9", "Marsden Todd", "Editions Atlas", "2019-06-26 12:35:58"),
    (
        "Isolation totale",
        "9",
        "Merritt Garcia",
        "Editions Atlas",
        "2019-06-26 12:35:58",
    ),
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
    (
        "Trois dans un appartement",
        "4",
        "Alfonso Fuentes",
        "Bayard",
        "2019-06-16 12:35:58",
    ),
    ("Vol de nuit", "2", "Marshall Mccoy", "Editions Atlas", "2019-06-16 12:35:58"),
]

#######################################################
######## INSERTION DES VALEURS DANS LES TABLES ########
#######################################################
cursor.execute("SELECT * FROM bibliotheque")
test_livres = cursor.fetchall()
if len(test_livres) == 0:
    for i in livres:
        cursor.execute(
            """INSERT INTO bibliotheque (id_livre, titre_livre, code_rayon, auteur, editeur, date_acquisition) VALUES(NULL, %s, %s, %s, %s, %s)""",
            i,
        )
    conn.commit()

############################################
######## CONNEXION DE L'UTILISATEUR ########
############################################
print("Bienvenue !")

hasAccount = int(
    input("Options disponibles :\n - [1] Oui\n - [2] Non\nAvez-vous déjà un compte ? ")
)
while True:
    if hasAccount == 1:
        id_account = int(input("Quel est votre identifiant ? "))
        prenom_account = str(input("Quel est votre prénom ? ")).lower()
        cursor.execute(
            f"SELECT * FROM abonnes WHERE id_abonne = '{id_account}' AND prenom = '{prenom_account}'"
        )
        account_details = cursor.fetchone()
        if account_details:
            break
        else:
            print("This user doesnt exist")
    else:
        prenom_account = str(input("Quel est votre prénom ? ")).lower()
        nom_account = str(input("Quel est votre nom ? ")).lower()
        age_account = int(input("Quel âge avez-vous ? "))
        courriel_account = str(input("Quel est votre adresse mail ? ")).lower()
        cursor.execute(
            f"SELECT * FROM abonnes WHERE nom = '{nom_account}' AND prenom = '{prenom_account}' AND age = '{age_account}' AND courriel = '{courriel_account}'"
        )
        accountExists = cursor.fetchone()
        conn.commit()

        if accountExists:
            print("Cette personne possède déjà un compte !")
            account_details = None
        else:
            print(nom_account, prenom_account, age_account, courriel_account)
            cursor.execute(
                f"INSERT INTO abonnes VALUES (NULL, '{nom_account}', '{prenom_account}', '{age_account}', '{courriel_account}')"
            )
            conn.commit()
            cursor.execute(
                f"SELECT * FROM abonnes WHERE nom = '{nom_account}' AND prenom = '{prenom_account}' AND age = '{age_account}' AND courriel = '{courriel_account}' "
            )
            account_details = cursor.fetchone()
            print(f"Votre identifiant est {account_details[0]}, NE LE PERDEZ PAS !")
            break

if account_details:
    # Si l'utilisateur est connecté
    print("\nBienvenue sur le portail de votre bibliothèque !\nMenu principal :")
    while True:
        requete = int(
            input(
                "\nOptions disponibles :\n - [1] Recherche par titre\n - [2] Recherche par auteur\n - [3] Recherche par éditeur\n - [4] Réservation d'une oeuvre\n - [5] Retour d'une oeuvre\n - [6] Recherche du nom de l'abonné ayant réservé un livre\n - [7] Recherche de l'adresse mail de l'abonné ayant réservé un livre\n - [8] Date de réservation d'un livre\n - [9] Livre à rendre demain\n - [10] Livre en retard\nQue voulez-vous faire ? "
            )
        )

        if requete == 1:
            print("")
            titre_livre_recherche = str(input("Quelle est le titre de votre livre ? "))
            liste_mots = titre_livre_recherche.split()
            liste_resultats = []
            for mot in liste_mots:
                if len(mot) >= 3 and mot != "les":
                    cursor.execute(
                        f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre FROM bibliotheque WHERE titre_livre LIKE '%{mot}%'"
                    )
                    resultat = cursor.fetchall()
            try:
                if len(resultat) > 0:
                    for row in resultat:
                        livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}"
                        if livre_data not in liste_resultats:
                            liste_resultats.append(livre_data)
                    print("")
                    print("Votre recherche a donné les résultats suivants :")
                    for res in liste_resultats:
                        print("")
                        print(f" - {res}")
                    del resultat
                else:
                    print("")
                    print("Votre recherche n'a donné aucun résultat.")
                    del resultat
            except:
                print("")
                print("Votre recherche n'a donné aucun résultat.")
                pass

        elif requete == 2:
            print("")
            auteur_recherche = str(input("Quel est le nom de l'auteur ? "))
            liste_mots = auteur_recherche.split()
            liste_resultats = []
            for mot in liste_mots:
                if len(mot) >= 3 and mot != "les":
                    cursor.execute(
                        f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre FROM bibliotheque WHERE auteur LIKE '%{mot}%'"
                    )
                    resultat = cursor.fetchall()
            try:
                if len(resultat) > 0:
                    for row in resultat:
                        livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}"
                        if livre_data not in liste_resultats:
                            liste_resultats.append(livre_data)
                    print("")
                    print("Votre recherche a donné les résultats suivants :")
                    for res in liste_resultats:
                        print("")
                        print(f" - {res}")
                    del resultat
                else:
                    print("")
                    print("Votre recherche n'a donné aucun résultat.")
                    del resultat
            except:
                print("")
                print("Votre recherche n'a donné aucun résultat.")
                pass

        elif requete == 3:
            print("")
            editeur_recherche = str(input("Quel est l'éditeur ? "))
            liste_mots = editeur_recherche.split()
            liste_resultats = []
            for mot in liste_mots:
                if len(mot) >= 3 and mot != "les":
                    cursor.execute(
                        f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre FROM bibliotheque WHERE editeur LIKE '%{mot}%'"
                    )
                    resultat = cursor.fetchall()
            try:
                if len(resultat) > 0:
                    for row in resultat:
                        livre_data = f"{row[0]}, écrit par {row[1]}, aux éditions {row[2]} --- Rayon : {row[3]} --- Identifiant : {row[4]}"
                        if livre_data not in liste_resultats:
                            liste_resultats.append(livre_data)
                    print("")
                    print("Votre recherche a donné les résultats suivants :")
                    for res in liste_resultats:
                        print("")
                        print(f" - {res}")
                    del resultat
                else:
                    print("")
                    print("Votre recherche n'a donné aucun résultat.")
                    del resultat
            except:
                print("")
                print("Votre recherche n'a donné aucun résultat.")
                pass

        elif requete == 4:
            print("")
            identifiant = int(input("Quel est l'identifiant de votre livre ? "))
            cursor.execute(
                f"SELECT * FROM bibliotheque WHERE id_livre = '{identifiant}'"
            )
            etat = cursor.fetchall()
            print("")
            if etat[0][6] == None:

                cursor.execute(
                    f"UPDATE bibliotheque SET reservation = '{date_jour}' WHERE id_livre = '{identifiant}'"
                )
                conn.commit()
                cursor.execute(
                    f"UPDATE bibliotheque SET etat = 'reserve'  WHERE id_livre = '{identifiant}'"
                )
                conn.commit()
                cursor.execute(
                    f"UPDATE bibliotheque SET id_abonne = '{account_details[0]}' WHERE id_livre = '{identifiant}'"
                )
                conn.commit()

                date_object = date_jour + timedelta(7)
                date_string = date_object.strftime("%d %B %Y")

                print("Réservation effectuée avec succès")
                print("La réservation a une durée de 7 jours.")
                print(f"Le livre devra être rendu le {date_string}")

            else:
                print("Le livre est déjà réservé")

        elif requete == 5:
            print("")
            identifiant = int(input("Quel est l'identifiant de votre livre ? "))
            cursor.execute(
                f"SELECT * FROM bibliotheque WHERE id_livre = '{identifiant}'"
            )
            etat = cursor.fetchall()
            print("")
            if etat[0][6] == "reserve":
                """id_abonne = str(input('Quel est votre identifiant de compte ?'))"""

                cursor.execute(
                    f"SELECT * FROM bibliotheque WHERE id_abonne = '{account_details[0]}' and id_livre = '{identifiant}'"
                )
                if cursor.fetchone():
                    cursor.execute(
                        f"UPDATE bibliotheque SET etat = NULL WHERE id_livre = {identifiant}"
                    )
                    cursor.execute(
                        f"UPDATE bibliotheque SET id_abonne = NULL WHERE id_abonne = {account_details[0]}"
                    )
                    conn.commit()
                    print("Retour effectué avec succès")
                else:
                    print("Il y a une erreur dans votre demande. Veuillez recommencer.")
            else:
                print("Le livre n'est pas réservé")

        elif requete == 6:
            print("")
            livre_recherche_reservation = int(
                input("Quel est l'identifiant du livre ? ")
            )
            cursor.execute(
                f"SELECT titre_livre, auteur, id_livre, id_abonne FROM bibliotheque WHERE id_livre = '{livre_recherche_reservation}'"
            )
            resultat = cursor.fetchone()
            recherche_id = resultat[3]
            cursor.execute(
                f"SELECT nom, prenom FROM abonnes WHERE id_abonne = '{recherche_id}'"
            )
            id_prenom_nom = cursor.fetchone()
            if id_prenom_nom:
                print("")
                print(
                    f"{resultat[0]}, écrit par {resultat[1]}, réservé par {id_prenom_nom[1]} {id_prenom_nom[0]}"
                )
            else:
                print("")
                print(f"{resultat[0]}, écrit par {resultat[1]}, non réservé.")

        elif requete == 7:
            print("")
            livre_recherche_reservation = int(
                input("Quel est l'identifiant du livre ? ")
            )
            cursor.execute(
                f"SELECT titre_livre, auteur, id_livre, id_abonne FROM bibliotheque WHERE id_livre = '{livre_recherche_reservation}'"
            )
            resultat = cursor.fetchone()
            recherche_id = resultat[3]
            cursor.execute(
                f"SELECT courriel FROM abonnes WHERE id_abonne = '{recherche_id}'"
            )
            id_courriel = cursor.fetchone()
            if id_courriel:
                print("")
                print(
                    f"{resultat[0]}, écrit par {resultat[1]}, réservé par {id_courriel[0]}"
                )
            else:
                print("")
                print(f"{resultat[0]}, écrit par {resultat[1]}, non réservé.")

        elif requete == 8:
            print("")
            livre_recherche_reservation = int(
                input("Quel est l'identifiant du livre ? ")
            )
            cursor.execute(
                f"SELECT reservation FROM bibliotheque WHERE id_livre = '{livre_recherche_reservation}' AND etat = 'reserve'"
            )
            resultat = cursor.fetchone()
            if resultat:
                date_object = datetime.strptime(resultat[0], "%Y-%m-%d")
                date_string = date_object.strftime("%d %B %Y")
                print("")
                print(f"Le livre est réservé depuis le {date_string}")
            else:
                print("")
                print("Ce livre n'est pas réservé.")

        elif requete == 9:
            print("")
            liste_resultats = []
            cursor.execute(
                f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre, id_abonne FROM bibliotheque WHERE reservation = '{date_jour - timedelta(6)}'"
            )
            resultat = cursor.fetchall()
            try:
                if len(resultat) > 0:
                    for row in resultat:
                        livre_data = f"{row[0]}, écrit par {row[1]}"
                        if livre_data not in liste_resultats:
                            liste_resultats.append(livre_data)

                    print("")
                    print("Les livres qui doivent être rendus demain sont :")
                    for res in liste_resultats:
                        print("")
                        print(f" - {res}")
                    del resultat
                else:
                    print("")
                    print("Aucun livre ne doit être rendu demain.")
                    del resultat
            except:
                print("")
                print("Votre recherche n'a donné aucun résultat.")
                pass

        elif requete == 10:
            print("")
            liste_resultats = []
            cursor.execute(
                f"SELECT titre_livre, auteur, editeur, code_rayon, id_livre, id_abonne FROM bibliotheque WHERE reservation <= '{date_jour - timedelta(7)}'"
            )
            resultat = cursor.fetchall()
            try:
                if len(resultat) > 0:
                    for row in resultat:
                        livre_data = f"{row[0]}, écrit par {row[1]}"
                        if livre_data not in liste_resultats:
                            liste_resultats.append(livre_data)

                    print("")
                    print("Les livres en retard sont :")
                    for res in liste_resultats:
                        print("")
                        print(f" - {res}")
                    del resultat
                else:
                    print("")
                    print("Aucun livre n'est en retard.")
                    del resultat
            except:
                print("")
                print("Votre recherche n'a donné aucun résultat.")
                pass


conn.commit()
conn.close()
