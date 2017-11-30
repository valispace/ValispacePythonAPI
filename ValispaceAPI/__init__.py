import requests
import json


class ValispaceAPI:
	global _read_only_vali_fields
	_read_only_vali_fields = [
		'id', 'url', 'name', 'formatted_formula', 'value', 'uses_default_formula', 'totalmargin_plus',
		'totalmargin_minus', 'wc_plus', 'wc_minus', 'calculated_valis', 'subscription_text', 'baseunit',
		'subscribed', 'value_baseunit', 'type', 'type_name', 'old_value',
	]

	global _writeable_vali_fields
	_writeable_vali_fields = [
		'reference', 'margin_plus', 'margin_minus', 'unit',
		'formula', 'description', 'parent', 'tags', 'shortname', 
		'minimum', 'maximum',
	]

	def __init__(self, url=None, username=None, password=None):
		# performs the password based oAuth 2.0 login for resd/write access

		if url is None:
			url = raw_input('  url: ').rstrip("/")
		if username is None:
			username = raw_input('  username: ')
		if password is None:
			password = raw_input('  password: ')

		# if url      is None:
		# 	url      = "https://demo.valispace.com"
		# if username is None:
		# 	username = "francisco.lgpc"
		# if password is None:
		# 	password = "password"

		# TODO - check for SSL connection, before sending the username and password ###

		try:
			oauth_url = url + "/o/token/"
			client_id = "docs.valispace.com/user-guide/addons/#matlab"  # registered client-id in Valispace Deployment
			result = requests.post(oauth_url, data={
				'grant_type': 'password',
				'username': username,
				'password': password,
				'client_id': client_id,
			})
			print result
			access = "Bearer " + result.json()['access_token']

			self.valispace_login = {
				'url': url + '/rest/',
				'options': {
					'Timeout': 200,
					'Headers': {'Authorization': access, 'Content-Type': 'application/json'}
				}
			}

			print "You have been successfully connected to the " + self.valispace_login['url'] + " API."
		except:
			print "VALISPACE-ERROR: Invalid credentials or url"

	def pull(self):
		# Returns a list of all Valis	

		url     = self.valispace_login['url'] + "vali/"
		headers = self.valispace_login['options']['Headers']
		valis   = requests.get(url, headers=headers).json()	

		return_dictionary = {}
		for vali in valis:
			return_dictionary[str(vali["id"])] = vali

		return return_dictionary

	def pull_vali_names(self):
		# Returns a list of all Valis with only names and ids
		
		url       = self.valispace_login['url'] + "valinames/"
		headers   = self.valispace_login['options']['Headers']
		valinames = requests.get(url, headers=headers)

		return valinames.json()

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

	def update_vali(self, name=None, id=None, formula=None, fields={}):
		# Finds the Vali that corresponds to the input id (or name) and
		# Updates it with the input formula (or fields)

		# Check if no argument was passed
		if id is None and name is None:
			print "VALISPACE-ERROR: 1 argument expected (name or id)"
			return

		# Check if name argument was passed
		if id is None:
			id = self.__name_to_id(name)
		
		# Read Vali
		url     = self.valispace_login['url'] + "vali/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		vali    = requests.get(url, headers=headers).json() 

		# Write Vali
		new_vali_data = {}
		stringified_new_vali_data = ""
		if not formula is None:
			fields["formula"] = str(formula)
		for k, v in fields.items():
			if k in _writeable_vali_fields:
				new_vali_data[k] = v
				stringified_new_vali_data += "  --> " + str(k) + " = " + str(v) + "\n"
		result = requests.patch(url, headers=headers, json=new_vali_data)

		if new_vali_data == {}:
			print( 
				'You have not entered any valid fields. Here is a list of updateable fields:\n' + 
				self.__list_to_bullets(_writeable_vali_fields)
			)
		elif result.status_code == 200:
			print(
				"Successfully updated Vali " + vali["name"] + " with the following fields:\n" + 
				stringified_new_vali_data
			)
		else:
			print "Invalid Request"
			
		return result

	def update_matrix_formulas(self, id, matrix):
		# Finds the Matrix that corresponds to the input id,
		# Finds each of the Valis that correspond to the vali id (contained in each cell of the matrix)
		# Updates the formula of each of the Valis with the formulas contained in each cell of the input matrix		

		# Read Matrix
		url     = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		matrix_data = requests.get(url, headers=headers).json()

		# Check matrix dimensions
		if not(
			len(matrix)    == matrix_data["number_of_rows"]    and 
			len(matrix[0]) == matrix_data["number_of_columns"]
		):
			print 'VALISPACE-ERROR: The dimensions of the local and the remote matrix do not match.'

		# Update referenced valis in each matrix cell
		for row in range(matrix_data['number_of_rows']):
			for col in range(matrix_data['number_of_columns']):
				self.update_vali(id=matrix_data['cells'][row][col], formula=matrix[row][col])

	# Private methods

	def __name_to_id(self, name):
		valis = self.pull_vali_names()
		for vali in valis:
			if vali["name"] == name:
				return vali["id"]

	def __list_to_bullets(self, list):
		return "  --> " + "\n  --> ".join(list) if list else ""