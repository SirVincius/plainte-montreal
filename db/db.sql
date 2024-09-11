create table contravention (
    id_poursuite integer primary key,
    id_business integer,
    date_infraction date,
    description text,
    numero_civique integer,
    rue text,
    ville text,
    province text,
    date_jugement date,
    etablissement text,
    montant integer,
    proprietaire text,
    statut text,
    date_statut date,
    categorie text
);

create table plainte (
    prenom_client text,
    nom_client text,
    etablissement text,
    adresse text,
    ville text,
    date_visite_client date,
    description text
);

create table utilisateur (
    prenom text,
    nom text,
    adresse_courriel text,
    liste_etablissements text,
    mot_de_passe text
);

