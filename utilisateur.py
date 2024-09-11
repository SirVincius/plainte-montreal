class Utilisateur:
    # Constructeur d'utilisateur
    def __init__(self, prenom, nom, adresse_courriel,
                 liste_etablissements, mot_de_passe):
        self.prenom = prenom
        self.nom = nom
        self.adresse_courriel = adresse_courriel
        self.liste_etablissements = liste_etablissements
        self.mot_de_passe = mot_de_passe
