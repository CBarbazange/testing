#-*- coding: utf-8 -*
from flask import Flask
from flask import request
import datetime
import re
import json


import mysql.connector
from mysqlDAO import mysqlDAO
from dbloader import dbloader


app = Flask(__name__)


dbl = dbloader()
db_infos = dbl.getDBInfos()
user_infos = dbl.getUserInfos("scrap_user")
host = db_infos["host"]
db = db_infos["db"]
user = user_infos["username"]
passwd = user_infos["password"]


bdd_data = {
		"_host" : host,
		"_user" : user,
		"_passwd" : passwd,
		"_db" : db
	}



def fct_createClient(nom, prenom, email, telephone, societe):

	transactionOK = False
	ret = None

	try:

		#Création de la connexion à la base de données
		mydb = mysql.connector.connect(
			host = bdd_data["_host"],
			user = bdd_data["_user"],
			passwd = bdd_data["_passwd"],
			db = bdd_data["_db"]
			)

		#mycursor = mydb.cursor()
		mycursor = mydb.cursor(prepared=True)

		#Data Access Object
		DAO = mysqlDAO(mycursor)

		ret = DAO.createClient(nom, prenom, email, telephone, societe)

		transactionOK = True

	except Exception as e:
		raise e
	else:

		if transactionOK:
			mydb.commit()
		else:
			mydb.rollback()

		#Fermeture de la connexion à la base de données
		mycursor.close()
		mydb.close()


	return str(ret)


@app.route("/")
def home():
	return "Home page"



@app.route("/register", methods=['POST'])
def register():

	nom		=	request.form['nom']
	prenom	=	request.form['prenom']
	email	=	request.form['email']
	tel		=	request.form['tel']
	societe	=	request.form['societe']

	sources	=	request.form.get('sources')

	string_sources = json.dumps(request.form)
	json_sources = json.loads(string_sources)

	checked_sources = []
	is_mail_valid = False

	for elem in json_sources:
		if json_sources[elem] == "source_checked":
			checked_sources.append(str(elem))

	if re.match(r"[^@]+@[^@]+\.[^@]+", email):
		is_mail_valid = True

	if nom == "" or prenom == "" or email == "" or tel == "" or societe == "" or len(checked_sources) == 0 or is_mail_valid == False:
		final_string = "Veuillez renseigner toutes les informations demandees"
	else:
		final_string = nom + " - " + prenom + " - " + email + " - " + tel + " - " + societe + " - " + str(checked_sources)

		add = fct_createClient(nom, prenom, email, tel, societe)

		print(add)

	return add


@app.route("/client/create")
def route_createClient():

	return "Client cree"




@app.route("/test")
def test():

	try:

		#Création de la connexion à la base de données
		mydb = mysql.connector.connect(
			host = bdd_data["_host"],
			user = bdd_data["_user"],
			passwd = bdd_data["_passwd"],
			db = bdd_data["_db"]
			)

		#mycursor = mydb.cursor()
		mycursor = mydb.cursor(prepared=True)

		#Data Access Object
		DAO = mysqlDAO(mycursor)

		ret = DAO.createClient("Tà Mèré En Sälôpette.com")
		ret = DAO.createClient("ioffer")

		return str(ret)

	except Exception as e:
		raise e
	else:

		#Fermeture de la connexion à la base de données
		mydb.commit()
		mycursor.close()
		mydb.close()

		return "Test"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8992)