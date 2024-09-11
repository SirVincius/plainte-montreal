import sqlite3
from datetime import datetime
from date_tools import Date_Tools


class Database():
    # Initie la connexion
    def __init__(self):
        self.connection = None

    # Ouvre la connexion
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    # Ferme la connexion
    def deconnection(self):
        if self.connection is not None:
            self.connection.close()

    # Insère une contravention dans la base de données
    def inserer_contraventions(self, contraventions):
        connection = self.get_connection()
        for c in contraventions:
            date_infraction = Date_Tools.string_to_date(c.date_infraction)
            date_jugement = Date_Tools.string_to_date(c.date_jugement)
            date_statut = Date_Tools.string_to_date(c.date_statut)
            connection.execute(
                    """INSERT OR REPLACE INTO contravention
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (int(c.id_poursuite), int(c.id_business),
                     date_infraction, c.description,
                     c.numero_civique, c.rue, c.ville,
                     c.province, date_jugement,
                     c.etablissement, int(c.montant),
                     c.proprietaire, c.statut,
                     date_statut, c.categorie)
                 )
        connection.commit()

    # Met à jour la base de données de contraventions
    def update_contravention(self, c):
        connection = self.get_connection()
        date_infraction = Date_Tools.string_to_date(c.date_infraction)
        date_jugement = Date_Tools.string_to_date(c.date_jugement)
        date_statut = Date_Tools.string_to_date(c.date_statut)
        connection.execute(
            """UPDATE contravention
               SET id_business = ?, date_infraction = ?, description = ?,
                   numero_civique = ?, rue = ?, ville = ?, province = ?,
                   date_jugement = ?, etablissement = ?, montant = ?,
                   proprietaire = ?, statut = ?, date_statut = ?, categorie = ?
               WHERE id_poursuite = ?""",
            (int(c.id_business), date_infraction, c.description,
             c.numero_civique, c.rue, c.ville, c.province, date_jugement,
             c.etablissement, int(c.montant), c.proprietaire, c.statut,
             date_statut, c.categorie, int(c.id_poursuite))
        )
        connection.commit()

    # Effectue une recherche à l'aide d'un critère et d'un mot-clé
    def rechercher_par_critere(self, critere, mot_cle):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM contravention WHERE {critere} LIKE ?"
        cursor.execute(query, (f'%{mot_cle}%',))
        resultats = cursor.fetchall()
        connection.commit()
        cursor.close()
        return resultats

    # Recherche les contraventions émises entre deux dates
    def rechercher_par_dates(self, date_minimum, date_maximum):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """SELECT * FROM contravention
            WHERE date_infraction BETWEEN ? AND ? ORDER BY etablissement""",
            (date_minimum, date_maximum)
        )
        resultats = cursor.fetchall()
        cursor.close()
        return resultats

    # Rechrche les infractions émises pour un restaurant
    def rechercher_infractions_par_restaurant(self, etablissement):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """SELECT etablissement, description, date_infraction, montant
            FROM contravention WHERE etablissement like ?""", (etablissement,)
        )
        resultats = cursor.fetchall()
        cursor.close()
        return resultats

    # Retourne la liste de tous les établissements
    def obtenir_liste_etablissement(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """SELECT DISTINCT etablissement FROM
            contravention ORDER BY etablissement"""
        )
        resultats = cursor.fetchall()
        cursor.close()
        return resultats

    # Retourne les étalissements et le nombre d'infractions pour chacun
    def obtenir_nombre_infractions(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """SELECT etablissement, COUNT(*) FROM contravention
            GROUP BY etablissement ORDER BY COUNT(*) DESC"""
        )
        count = cursor.fetchall()
        cursor.close()
        return count

    # Insère un utilisateur la base de données
    def inserer_utilisateur(self, prenom, nom, adresse_courriel,
                            liste_etablissements, mot_de_passe):
        connection = self.get_connection()
        connection.execute("""INSERT INTO utilisateur VALUES
                           (?, ?, ?, ?, ?)""",
                           (prenom, nom, adresse_courriel,
                            liste_etablissements, mot_de_passe))
        connection.commit()

    # Insère une plainte dans la base de données
    def deposer_plainte(self, prenom, nom, etablissement, adresse,
                        ville, date_visite, description):
        connection = self.get_connection()
        formatted_date = datetime.strptime(date_visite, '%Y-%m-%d')
        connection.execute("""INSERT INTO plainte VALUES
                           (?, ?, ?, ?, ?, ?, ?)""",
                           (prenom, nom, etablissement,
                            adresse, ville, formatted_date,
                            description))
        connection.commit()
