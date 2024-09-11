# Système de contraventions

## À propos du projet

Auteur : Vincent Brunelle
Code permanent : BRUV28018509

## Fonctionnalités implémentées

### A1 10xp - Obtention et insertion des données dans la base de données

- La liste de données est obtenue et les données sont insérées automatiquement lors du lancement de l'application ou mises à jour lors de lancement subséquents.

### A2 10xp - Outil de recherche de contraventions

- La page d'accueil offre l'outil de recherche demandé, avec les critères demandés. Les résultats s'affichent sur une nouvelle page et toutes les données sont affichées. Il suffit d'entrer un mot-clé, de chosir un critère de recherche et de lancer la recherche
- Les résultats sont ajoutés en dessous des trois outils de recherche offerts sur la page principale.

### A3 5xp - Mises à jour programmées

- L'application met automatiquement à jour les données à minuit chaque jour par l'entremise d'un BackgroundScheduler.
- On peut tester en modifiant la ligne suivante `scheduler.add_job(update_database, 'cron', hour=00, minute=00)` dans app.py et entrer l'heure désirée.

### A4 10xp - Service REST entre deux dates

- Le service REST demandé est implémenté et et la documentation RAML complétée.
- La route de du service est `/api/contrevenants`.
- On peut texter le service avec le formulaire développé en A5.

### A5 10xp - Implémentation du formulaire de recherche par dates

- Le formulaire de recherche par dates est implémenté et retourne les deux colonnes demandées.
- La recherche est faîte à l'aide d'une requête AJAX.
- Les résultats sont ajoutés en dessous des trois outils de recherche offerts sur la page principale.

### A6 10xp- Implémentation du formulaire de recherche par nom de restaurant

- Le formulaire de recherche par nom de restaurant est implémenté.
- La liste des restaurants est prédeterminée.
- La recherche est faîte à l'aide d'une requête AJAX.
- Les résultats sont ajoutés en dessous des trois outils de recherche offerts sur la page principale.
- La route du service est `/api/restaurant/<restaurant>`.
- On peut tester en sélectionnant le restaurant dont on souhaite afficher les infractions.

### C1 10xp - Service REST liste établissement ayant au moins une infraction au format JSON

- Le nombre d'infraction est indiqué.
- La liste est classé par ordre décroissant d'infractions.
- Le service est documenté avec RAML.
- La route du service est `/api/count_infractions_restaurants/json`.
- On peut tester le service en entrant l'adresse suivante dans la barre de d'adresse `http://localhost:5000/api/count_infractions_restaurants/json`.

### C2 5xp - Service REST liste établissement ayant au moins une infraction au format XML

- Le nombre d'infraction est indiqué.
- La liste est classé par ordre décroissant d'infractions.
- Le service est documenté avec RAML.
- La route du service est `/api/count_infractions_restaurants/xml`.
- On peut tester le service en entrant l'adresse suivante dans la barre de d'adresse `http://localhost:5000/api/count_infractions_restaurants/xml`.

### C3 5xp - Service REST liste établissement ayant au moins une infraction au format CSV

- Le nombre d'infraction est indiqué.
- La liste est classé par ordre décroissant d'infractions.
- Le service est documenté avec RAML.
- La route du service est `/api/count_infractions_restaurants/csv`.
- On peut tester le service en entrant l'adresse suivante dans la barre de d'adresse `http://localhost:5000/api/count_infractions_restaurants/csv`.

### D1 15xp - Service REST permettant de faire une demande d’inspection à la ville

- Le document est validé avec un json-schema.
- Le service reçoit les données demandées.
- Le service est documenté avec RAML.
- Une page permet de déposer une plainte qui est ensuite enregistrée dans la base de données en invoquant le service REST.
- On peut accéder au formulaire de plainte dans la barre de navigation dans le haut de la page.
- La route su service est `/api/deposer_plainte`.
- On peut tester le service en complétant une plainte dans la page `Déposer une plainte`.

### E1 15xp - Service REST permettant à un utilisateur de se créer un profil d'utilisateur

- Le système reçoit un document JSON contenant les informations demandées.
- Le document est validé avec un json-schema.
- Les données sont enregistrées dans la base de données en invoquant le service REST.
- La route su service est `/api/nouvel_utilisateur`.
- Extra : Le point E2 n'a pas été implémenté, mais un petit espace nommé "Test\* Ajouter un nouvel utilisateur" a tout de même été ajouté sur la page principale afin de pouvoir tester l'ajout d'un utilisateur, puisque ceci fait partie du point E2 aucune vérification n'a été mise en place pour vérifier que toutes les données fournies.

### Total 105xp
