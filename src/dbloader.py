#-*- coding: utf-8 -*
import ast


class dbloader():

	config_file = "./volume/config/db_users.json"

	def getDBInfos(self):
		f = open(self.config_file, "r")
		data = f.read()
		dbInfos = ast.literal_eval(data)["mysql_bdd"]
		f.close()
		return dbInfos

	def getUserInfos(self, user):
		try:
			f = open(self.config_file, "r")
			data = f.read()
			userInfos = ast.literal_eval(data)[user]
			f.close()

			return(userInfos)

		except KeyError as err:
			return(0)
