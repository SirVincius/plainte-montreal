valider_nouvelle_plainte_schema = {
    "type": "object",
    "properties": {
        "prenom": {"type": "string"},
        "nom": {"type": "string"},
        "etablissement": {"type": "string"},
        "adresse": {"type": "string"},
        "ville": {"type": "string"},
        "date_visite": {"type": "string", "format": "date"},
        "description": {"type": "string"}
    },
    "required": ["prenom", "nom", "etablissement", "adresse",
                 "ville", "date_visite", "description"],
    "additionalProperties": False
}

valider_nouvel_utilisateur_schema = {
    "type": "object",
    "properties": {
        "prenom": {"type": "string"},
        "nom": {"type": "string"},
        "adresse_courriel": {"type": "string"},
        "liste_etablissements": {"type": "string"},
        "mot_de_passe": {"type": "string"}
    },
    "required": ["prenom", "nom", "adresse_courriel",
                 "liste_etablissements", "mot_de_passe"],
    "additionalProperties": False
}
