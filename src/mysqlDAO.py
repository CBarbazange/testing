# -*- coding: utf-8 -*-
import mysql.connector
import unicodedata
import datetime

class mysqlDAO():

	def __init__(self, cursor):
		self.cursor = cursor


	def getAllEntreprises(self):

		try:
			#sql_request = """SELECT nom FROM recolte_Entreprise WHERE nom = %s"""
			sql_request = """SELECT nom FROM recolte_Entreprise"""
			#input = (site_name,)
			#self.cursor.execute(sql_request, input)
			self.cursor.execute(sql_request)
			myresult = self.cursor.fetchall()

			ret = []

			for elem in myresult:
				ret.append(str(elem[0]))

			return ret
		except Exception as e:
			raise e


	def createClient(self, nom, prenom, email, telephone, societe):
	#def createClient(self, societe):

		_societe = str(unicodedata.normalize('NFKD', societe.decode('utf-8')).encode('ascii', 'ignore').decode('ascii'))

		_societe = societe.replace("-", "").replace(" ", "").split(".")[0].lower()

		print(_societe)

		sql_request = """ SELECT COUNT(*) from business_InfosClient WHERE societe = %s"""
		input = (_societe,)
		self.cursor.execute(sql_request, input)
		myresult = self.cursor.fetchone()

		if myresult[0] != 0:
			print("Un client possede deja ce nom")
			return "Un client possede deja ce nom"
		else:
			sql_request = """INSERT INTO business_InfosClient(nom, prenom, email, societe, telephone) VALUES(%s, %s, %s, %s, %s)"""
			input = (nom, prenom, email, societe, telephone)
			self.cursor.execute(sql_request, input)
			print("Ajout du client a la base de donnees")
			return "Ajout du client a la base de donnees"