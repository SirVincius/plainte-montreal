from flask_json_schema import JsonSchema
from schema import (valider_nouvelle_plainte_schema,
                    valider_nouvel_utilisateur_schema)
from flask import Flask, jsonify, render_template, g, request
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import csv
from io import StringIO

from database import Database
from contravention import Contravention
from datetime import datetime
import xml.etree.cElementTree as ET
import io
import requests

app = Flask(__name__)
schema = JsonSchema(app)


# Obtenir la base de données
def get_db():
    with app.app_context():
        database = getattr(g, "_database", None)
        if database is None:
            g._database = Database()
        return g._database


# Se déconnecter de la base de données
def deconnection():
    with app.app_context():
        database = getattr(g, "_database", None)
        if database is not None:
            database.deconnection()


# Met à jour la base de données
def update_database():
    with app.app_context():
        url = ("https://data.montreal.ca/dataset/0"
               "5a9e718-6810-4e73-8bb9-5955efeb91a0"
               "/resource/7f939a08-be8a-45e1-b208-d"
               "8744dca8fc6/download/violations.csv")
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            cr = csv.reader(StringIO(content))
            contraventions = []
            first_row_skipped = False
            for row in cr:
                if not first_row_skipped:
                    first_row_skipped = True
                    continue
                contravention = Contravention(row[0], row[1],
                                              row[2], row[3],
                                              row[4], row[5],
                                              row[6], row[7],
                                              row[8], row[9],
                                              row[10], row[11],
                                              row[12])
                contraventions.append(contravention)
            get_db().inserer_contraventions(contraventions)
            return "Database updated successfully"
        else:
            return "Failed to fetch data"


update_database()


scheduler = BackgroundScheduler()
scheduler.add_job(update_database, 'cron', hour=00, minute=00)
scheduler.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/plainte")
def plainte():
    return render_template("plainte.html")


@app.route("/confirmation_utilisateur")
def confirmation_utilisateur():
    return render_template("confirmation_utilisateur.html",)


@app.route("/confirmation_plainte")
def confirmation_plainte():
    return render_template("confirmation_plainte.html",)


@app.route("/recherche_par_critere", methods=['POST'])
def recherche_par_critere():
    mot_cle = request.form['mot-cle']
    critere = request.form['critere']
    resultats = get_db().rechercher_par_critere(critere, mot_cle)
    return render_template("resultats_recherche_par_critere.html",
                           resultats=resultats)


@app.route("/api/contrevenants", methods=['GET'])
def obtenir_contrevenants():
    date_minimum = request.args.get('du')
    date_maximum = request.args.get("au")

    formatted_date_minimum = datetime.strptime(date_minimum, '%Y-%m-%d')
    formatted_date_maximum = datetime.strptime(date_maximum, '%Y-%m-%d')

    data = get_db().rechercher_par_dates(formatted_date_minimum,
                                         formatted_date_maximum)
    data_rdy = []
    for row in data:
        adress = str(row[4]) + " " + row[5] + ", " + row[6] + ", " + row[7]
        contravention = Contravention(row[0], row[1], row[2], row[3],
                                      adress, row[8], row[9],
                                      row[10], row[11], row[6],
                                      row[12], row[13], row[14])
        contravention_json = contravention.to_json()

        contravention_json = contravention.to_json()
        data_rdy.append(
            contravention_json
        )
    return jsonify(data_rdy)


@app.route("/api/restaurant/<restaurant>", methods=['GET'])
def obtenir_infraction_par_restaurant(restaurant):
    data = get_db().rechercher_infractions_par_restaurant(restaurant)
    data_rdy = []
    for row in data:
        data_rdy.append({"etablissement": row[0],
                         "description": row[1],
                         "date_infraction": row[2],
                         "montant": row[3]})
    return jsonify(data_rdy)


@app.route("/api/etablissements")
def obtenir_etablissement():
    data = get_db().obtenir_liste_etablissement()
    data_rdy = []
    for row in data:
        data_rdy.append({"etablissement": row[0]})
    return jsonify(data_rdy)


@app.route("/api/count_infractions_restaurants/json")
def obtenir_count_infractions_restaurants_json():
    data = get_db().obtenir_nombre_infractions()
    data_rdy = []
    for row in data:
        data_rdy.append({"etablissement": row[0],
                         "nombre_d'infractions": row[1]})
    return jsonify(data_rdy)


@app.route("/api/count_infractions_restaurants/xml")
def obtenir_count_infractions_restaurants_xml():
    data = get_db().obtenir_nombre_infractions()
    root = ET.Element("infractions")
    for row in data:
        etablissement = ET.SubElement(root, "etablissement")
        nom_etablissement = ET.SubElement(etablissement, "nom_etablissement")
        nom_etablissement.text = str(row[0])
        nombre_infractions = ET.SubElement(etablissement, "nombre_infractions")
        nombre_infractions.text = str(row[1])
    return ET.tostring(root).decode()


@app.route("/api/count_infractions_restaurants/csv")
def obtenir_count_infractions_restaurants_csv():
    data = get_db().obtenir_nombre_infractions()
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['nom_etablissement', 'nombre_infractions'])
    for row in data:
        csv_writer.writerow(row)
    contenu = output.getvalue()
    output.close()
    return contenu


@app.route("/api/nouvel_utilisateur", methods=['POST'])
@schema.validate(valider_nouvel_utilisateur_schema)
def nouvel_utilisateur():
    try:
        data = request.get_json()
        get_db().inserer_utilisateur(data['prenom'], data['nom'],
                                     data['adresse_courriel'],
                                     data['liste_etablissements'],
                                     data['mot_de_passe'])
        return ("Utilisateur '" + data['prenom'] + " " +
                data['nom'] + "' ajouté avec succès!")
    except Exception as e:
        return jsonify("Erreur lors de l'ajout de l'utilisateur")


@app.route("/api/deposer_plainte", methods=['POST'])
@schema.validate(valider_nouvelle_plainte_schema)
def deposer_plainte():
    try:
        data = request.get_json()
        get_db().deposer_plainte(data['prenom'], data['nom'],
                                 data['etablissement'], data['adresse'],
                                 data['ville'], data['date_visite'],
                                 data['description'])

        return jsonify("Plainte de '" + data['prenom'] + " " +
                       data['nom'] + "' ajoutée avec succès!")
    except Exception as e:
        return jsonify("Erreur lors de l'ajout de l'utilisateur")


if __name__ == "__main__":
    app.run(debug=True)
