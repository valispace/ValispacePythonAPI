from helpers import *

import requests
import json

class ValispaceAPI:
	def __init__(self, url=None, username=None, password=None):
		# performs the password based oAuth 2.0 login for resd/write access
		
		# if url is None:
		# 	url = raw_input('  url: ')
		# if username is None:
		# 	username = raw_input('  username: ')
		# if password is None:
		# 	password = raw_input('  password: ')

		if url      is None:
			url      = "https://demo.valispace.com"
		if username is None:
			username = "francisco.lgpc"
		if password is None:
			password = "password"

		### TBD - check for SSL connection, before sending the username and password ###

		oauth_url = url + "/o/token/"
		client_id = "docs.valispace.com/user-guide/addons/#matlab" # registered client-id in Valispace Deployment
		result = requests.post(oauth_url, data = {
			'grant_type': 'password',
	  	'username':   username,
	  	'password':   password,
	  	'client_id':  client_id
		})
		access = "Bearer " + result.json()['access_token']
		
		self.valispace_login = { 
			'url': url + '/rest/', 
			'options': {
				'Timeout': 200, 
				'Headers': { 'Authorization': access, 'Content-Type': 'application/json' }
		  }
	  }

		print "You have been successfully connected to the " + self.valispace_login['url'] + " API."

	def pull(self):
		# Returns a list of all Valis	

		url     = self.valispace_login['url'] + "vali/"
		headers = self.valispace_login['options']['Headers']

		valis = requests.get(url, headers=headers).json()	

		return_dictionary = {}
		for vali in valis:
			return_dictionary[str(vali["id"])] = vali

		return return_dictionary


	def pull_vali_names(self):
		# Returns a list of all Valis with only names and ids
		
		url     = self.valispace_login['url'] + "valinames/"
		headers = self.valispace_login['options']['Headers']

		result  = requests.get(url, headers=headers)

		return result.json()


	def get_vali(self, id=None, name=None):
		# Returns the correct Vali. Input can be id or name
		
		# Check if no argument was passed
		if id is None and name is None:
			print "VALISPACE-ERROR: 1 argument expected (name or id)"
			return

		# Check if name argument was passed
		if id is None:
			id = self.__name_to_id(name)
		
		# Access API
		url = self.valispace_login['url'] + "vali/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		return requests.get(url, headers=headers).json()

	def get_value(self, id=None, name=None):
		# Returns the value of a vali.

		if id is None:
			return self.get_vali(name=name)["value"]
		else:
			return self.get_vali(id=id)["value"]

	def get_matrix(self, id):
		# Returns the correct Matrix. Input id.

		url = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		
		matrix_data = requests.get(url, headers=headers).json()
		matrix = []

		for row in range(matrix_data['number_of_rows']):
			matrix.append([])
			for col in range(matrix_data['number_of_columns']):
				matrix[row].append(self.get_vali(matrix_data['cells'][row][col]))

		return matrix

	# Private methods

	def __name_to_id(self, name):
		valis = self.pull_vali_names()
		for vali in valis:
			if vali["name"] == name:
				return vali["id"]
