class Plainte:
    # Constructeur de plainte
    def __init__(self, prenom_client, nom_client, etablissement,
                 adresse, ville, date_visite_client, description):
        self.prenom_client = prenom_client
        self.nom_client = nom_client
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite_client = date_visite_client
        self.description = description
