class Contravention:
    # Constructeur de contravention
    def __init__(self, id_poursuite, id_business, date_infraction,
                 description, adresse,
                 date_jugement, etablissement, montant, proprietaire, ville,
                 statut, date_statut, categorie):
        numero_civique, rue, ville, province = self.creer_adresse(adresse)
        self.id_poursuite = id_poursuite
        self.id_business = id_business
        self.date_infraction = date_infraction
        self.description = description
        self.numero_civique = numero_civique
        self.rue = rue
        self.province = province
        self.date_jugement = date_jugement
        self.etablissement = etablissement
        self.montant = montant
        self.proprietaire = proprietaire
        self.ville = ville
        self.statut = statut
        self.date_statut = date_statut
        self.categorie = categorie

    # Fractionne une adresse en ces différentes parties
    def creer_adresse(self, adresse):
        numero_rue, ville, province = adresse.rsplit(', ', 2)
        numero, rue = numero_rue.split(' ', 1)
        return numero, rue, ville, province

    # Retourne une contravention sous forme de json
    def to_json(self):
        contravention_json = {
            "id_poursuite": self.id_poursuite,
            "id_businnes": self.id_business,
            "date_infraction": self.date_infraction,
            "description": self.description,
            "numero_civique": self.numero_civique,
            "rue": self.rue,
            "ville": self.ville,
            "province": self.province,
            "date_jugement": self.date_jugement,
            "etablissement": self.etablissement,
            "montant": self.montant,
            "proprietaire": self.proprietaire,
            "statut": self.statut,
            "date_statut": self.date_statut,
            "categorie": self.categorie
        }
        return contravention_json
