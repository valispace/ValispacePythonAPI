#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import json
import requests


class API:
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
		""" Performs the password based oAuth 2.0 login for resd/write access """

		print("--- Authenticating Valispace ---")

		if url is None:
			url = raw_input('Your Valispace url: ').rstrip("/")
		if username is None:
			username = raw_input('Username: ')
		if password is None:
			password = getpass.getpass('Password: ')

		# if url is None:
		# 	url = ""
		# if username is None:
		# 	username = ""
		# if password is None:
		# 	password = ""

		# TODO - check for SSL connection, before sending the username and password ###

		try:
			oauth_url = url + "/o/token/"
			client_id = "ValispaceREST"  # registered client-id in Valispace Deployment
			result = requests.post(oauth_url, data={
				'grant_type': 'password',
				'username': username,
				'password': password,
				'client_id': client_id,
			})
			access = "Bearer " + result.json()['access_token']

			self.valispace_login = {
				'url': url + '/rest/',
				'options': {
					'Timeout': 200,
					'Headers': {'Authorization': access, 'Content-Type': 'application/json'}
				}
			}

			print("You have been successfully connected to the " + self.valispace_login['url'] + " API.")
		except:
			print("VALISPACE-ERROR: Invalid credentials or url")

	def all_data(self, type=None):
		""" Returns a dict of all component/vali/textvali/tags with their properties """
		# Check if no argument was passed
		if type is None:
			print("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags)")
			return

		# URL
		if type is 'component':
			url = self.valispace_login['url'] + "component/"
		elif type is 'vali':
			url = self.valispace_login['url'] + "vali/"
		elif type is 'textvali':
			url = self.valispace_login['url'] + "textvali/"
		elif type is 'tag':
			url = self.valispace_login['url'] + "tag/"

		headers = self.valispace_login['options']['Headers']
		get_data = requests.get(url, headers=headers).json()	

		return_dictionary = {}
		for data in get_data:
			return_dictionary[str(data["id"])] = data

		return return_dictionary

	def all_vali_names(self):
		""" Returns a list of all Valis with only names and ids """

		url = self.valispace_login['url'] + "valinames/"
		headers = self.valispace_login['options']['Headers']
		valinames = requests.get(url, headers=headers)

		return valinames.json()

	def get_vali(self, id=None, name=None):
		""" Returns JSON of a unique Vali. Input can be id (int) or name (string).
		Valis name need to have the full tree path in order the names to be unique """

		if id:
			try:
				id = int(id)
			except:
				print("VALISPACE-ERROR: Vali id must be an integer")
				return

		# Check if no argument was passed
		if id is None and name is None:
			print("VALISPACE-ERROR: 1 argument expected (name or id)")
			return

		url = self.valispace_login['url'] + "vali/?"
		if id:
			url += "id=" + str(id)
		elif name:
			url += "name=" + str(name)

		# Access API
		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)

		return response.json()

	def filter_vali(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None, parent_id=None,
																	parent_name=None, tag_id=None, tag_name=None, vali_marked_as_impacted=None):
		""" Returns JSON with all the Valis that mach the input arguments.
		Inputs are integers for IDs or vali_marked_as_impacted, and strings for names.
		Use the component 'unique_name' (not the 'name') in the parent_name argument."""

		if workspace_id:
			try:
				workspace_id = int(workspace_id)
			except:
				print("VALISPACE-ERROR: Workspace id must be an integer")
				return

		if project_id:
			try:
				project_id = int(project_id)
			except:
				print("VALISPACE-ERROR: Project id must be an integer")
				return

		if parent_id:
			try:
				parent_id = int(parent_id)
			except:
				print("VALISPACE-ERROR: Parent id must be an integer")
				return

		if tag_id:
			try:
				tag_id = int(tag_id)
			except:
				print("VALISPACE-ERROR: Tag id must be an integer")
				return

		if vali_marked_as_impacted:
			try:
				vali_marked_as_impacted = int(vali_marked_as_impacted)
			except:
				print("VALISPACE-ERROR: Vali_marked_as_impacted must be an integer")
				return

		# Check if no argument was passed
		if workspace_id is None and workspace_name is None and project_id is None and project_name is None \
			and parent_id is None and parent_name is None and tag_id is None and tag_name is None \
			and vali_marked_as_impacted is None:

			print("VALISPACE-ERROR: at least 1 argument expected")
			return

		# URL
		url = self.valispace_login['url'] + "vali/?"
		if workspace_id:
			url += "parent__project__workspace=" + str(workspace_id)
		if workspace_name:
			url = self.__increment_url(url) + "parent__project__workspace__name=" + str(workspace_name)
		if project_id:
			url = self.__increment_url(url) + "parent__project__id=" + str(project_id)
		if project_name:
			url = self.__increment_url(url) + "parent__project__name=" + str(project_name)
		if parent_id:
			url = self.__increment_url(url) + "parent__id=" + str(parent_id)
		if parent_name:
			url = self.__increment_url(url) + "parent__unique_name=" + str(parent_name)
		if tag_id:
			url = self.__increment_url(url) + "tags__id=" + str(tag_id)
		if tag_name:
			url = self.__increment_url(url) + "tags__name=" + str(tag_name)
		if vali_marked_as_impacted:
			url = self.__increment_url(url) + "valis_marked_as_impacted=" + str(vali_marked_as_impacted)

		print url
		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)

		return response.json()

	def get_component(self, id=None, unique_name=None):
		""" Returns JSON of a unique Component. Input can be id (int) or name (string)."""

		if id:
			try:
				id = int(id)
			except:
				print("VALISPACE-ERROR: Component id must be an integer")
				return

		# Check if no argument was passed
		if id is None and unique_name is None:
			print("VALISPACE-ERROR: 1 argument expected (name or id)")
			return

		url = self.valispace_login['url'] + "component/?"
		if id:
			url += "id=" + str(id)
		elif unique_name:
			url += "unique_name=" + str(unique_name)

		# Access API
		headers = self.valispace_login['options']['Headers']

		response = requests.get(url, headers=headers)

		return response.json()

	def filter_component(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None, parent_id=None,
																						parent_name=None, tag_id=None, tag_name=None):
		""" Returns JSON with all the Components that mach the input arguments.
		Inputs are integers for IDs and strings for names.
		Use the component 'unique_name' (not the 'name') in the parent_name argument."""

		if workspace_id:
			try:
				workspace_id = int(workspace_id)
			except:
				print("VALISPACE-ERROR: Workspace id must be an integer")
				return
			
		if project_id:
			try:
				project_id = int(project_id)
			except:
				print("VALISPACE-ERROR: Project id must be an integer")
				return

		if parent_id:
			try:
				parent_id = int(parent_id)
			except:
				print("VALISPACE-ERROR: Parent id must be an integer")
				return

		if tag_id:
			try:
				tag_id = int(tag_id)
			except:
				print("VALISPACE-ERROR: Tag id must be an integer")
				return

		# Check if no argument was passed
		if workspace_id is None and workspace_name is None and project_id is None and project_name is None \
			and parent_id is None and parent_name is None and tag_id is None and tag_name is None:

			print("VALISPACE-ERROR: at least 1 argument expected")
			return

		# URL
		url = self.valispace_login['url'] + "component/?"
		if workspace_id:
			url += "project__workspace=" + str(workspace_id)
		if workspace_name:
			url = self.__increment_url(url) + "workspace__name=" + str(workspace_name)
		if project_id:
			url = self.__increment_url(url) + "project__id=" + str(project_id)
		if project_name:
			url = self.__increment_url(url) + "project__name=" + str(project_name)
		if parent_id:
			url = self.__increment_url(url) + "parent=" + str(parent_id)
		if parent_name:
			url = self.__increment_url(url) + "parent__unique_name=" + str(parent_name)
		if tag_id:
			url = self.__increment_url(url) + "tags__id=" + str(tag_id)
		if tag_name:
			url = self.__increment_url(url) + "tags__name=" + str(tag_name)

		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)

		return response.json()

	def get_project(self, id=None, name=None, workspace_id=None):
		""" Returns JSON of a unique Project. Input can be id (int) or name (string) """

		if id:
			try:
				id = int(id)
			except:
				print("VALISPACE-ERROR: Vali id must be an integer")
				return

		# Check if no argument was passed
		if id is None and name is None:
			print("VALISPACE-ERROR: 1 argument expected (name or id)")
			return

		# Access API
		# URL
		url = self.valispace_login['url'] + "project/?"
		if id:
			url += "id=" + str(id)
		elif name:
			url += "name=" + str(name)

		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)

		return response.json()

	def filter_project(self, workspace_id=None, workspace_name=None):
		""" Returns JSON with all the Projects that mach the input arguments.
		Inputs are integers for IDs and strings for names."""
		if workspace_id:
			try:
				workspace_id = int(workspace_id)
			except:
				print("VALISPACE-ERROR: Workspace id must be an integer")
				return

		# Check if no argument was passed
		if workspace_id is None and workspace_name is None:

			print("VALISPACE-ERROR: at least 1 argument expected")
			return

		# URL
		url = self.valispace_login['url'] + "project/?"
		if workspace_id:
			url += "workspace=" + str(workspace_id)
		if workspace_name:
			url = self.__increment_url(url) + "workspace__name=" + str(workspace_name)

		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)

		return response.json()	

	def get_value(self, id=None, name=None):
		""" Returns the value of a vali. """

		try:
			if id is None:
				return self.get_vali(name=name)["value"]
			else:
				return self.get_vali(id=id)["value"]
		except:
			print("VALISPACE-ERROR: could not get value of Vali")
			return

	def update_vali(self, name=None, id=None, formula=None, data={}):
		""" Finds the Vali that corresponds to the input id (or name) and updates it with the input formula (or data) """

		# Check if no argument was passed
		if id is None and name is None:
			print("VALISPACE-ERROR: 1 argument expected (name or id)")
			return

		# Check if name argument was passed
		if id is None:
			id = self.__name_to_id(name)

		# Read Vali
		url = self.valispace_login['url'] + "vali/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		vali = requests.get(url, headers=headers).json()

		# Write Vali
		new_vali_data = {}
		stringified_new_vali_data = ""
		if not formula is None:
			data["formula"] = str(formula)
		for k, v in data.items():
			if k in _writeable_vali_fields:
				new_vali_data[k] = v
				stringified_new_vali_data += "  --> " + str(k) + " = " + str(v) + "\n"
		result = requests.patch(url, headers=headers, data=new_vali_data)

		print("STATUS CODE: ", result.status_code)
		
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
			print("Invalid Request")

		return result

	def post_data(self, type=None, data={}):
		""" Post new component/vali/textvali/tags with the input data
		Data is expected to be a JSON string with some required fields like name"""

		# Check if no argument was passed
		if data is None:
			print("VALISPACE-ERROR: Data argument expected")
			return
		elif type is None:
			print("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags)")
			return

		# URL
		if type is 'component':
			url = self.valispace_login['url'] + "component/"
		elif type is 'vali':
			url = self.valispace_login['url'] + "vali/"
		elif type is 'textvali':
			url = self.valispace_login['url'] + "textvali/"
		elif type is 'tag':
			url = self.valispace_login['url'] + "tag/"
		
		headers = self.valispace_login['options']['Headers']
		result = requests.post(url, headers=headers, data=data)

		if result.status_code == 201:
			print("Successfully updated Vali:\n" + str(data) + "\n")
		elif result.status_code == 204:
			print("The server successfully processed the request, but is not returning any content (status code: 204)\n")
		elif result.status_code == 500:
			print("The server encountered an unexpected condition which prevented it from fulfilling the request (status code: 500)\n")
		else:
			print("Invalid Request (status code: ", result.status_code, "): ", result.content, "\n")

		return result.json()

	def get_matrix(self, id):
		""" Returns the correct Matrix. Input id. """

		url = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		matrix_data = requests.get(url, headers=headers).json()

		try:
			matrix = []
			for row in range(matrix_data['number_of_rows']):
				matrix.append([])
				for col in range(matrix_data['number_of_columns']):
					matrix[row].append(self.get_vali(matrix_data['cells'][row][col]))

			return matrix
		except KeyError:
			print("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
			return
		except:
			print("VALISPACE-ERROR: Unknown error.")

	def get_matrix_str(self, id):
		""" Returns the correct Matrix. Input id. """

		url = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		matrix_data = requests.get(url, headers=headers).json()

		try:
			matrix = []
			for row in range(matrix_data['number_of_rows']):
				matrix.append([])
				for col in range(matrix_data['number_of_columns']):
					matrix[row].append({"vali": matrix_data['cells'][row][col], "value": self.get_vali(matrix_data['cells'][row][col])["value"]})

			return matrix
		except KeyError:
			print("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
			return
		except:
			print("VALISPACE-ERROR: Unknown error.")

	def update_matrix_formulas(self, id, matrix):
		""" Finds the Matrix that corresponds to the input id,
		Finds each of the Valis that correspond to the vali id (contained in each cell of the matrix)
		Updates the formula of each of the Valis with the formulas contained in each cell of the input matrix	"""

		# Read Matrix
		url = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		headers = self.valispace_login['options']['Headers']
		matrix_data = requests.get(url, headers=headers).json()

		# Check matrix dimensions
		if not(
			len(matrix) == matrix_data["number_of_rows"] and
			len(matrix[0]) == matrix_data["number_of_columns"]
		):
			print('VALISPACE-ERROR: The dimensions of the local and the remote matrix do not match.')

		# Update referenced valis in each matrix cell
		for row in range(matrix_data['number_of_rows']):
			for col in range(matrix_data['number_of_columns']):
				self.update_vali(id=matrix_data['cells'][row][col], formula=matrix[row][col])

	# Private methods
	def __name_to_id(self, name):
		url = self.valispace_login['url'] + "vali/?name=" + str(name)
		headers = self.valispace_login['options']['Headers']
		response = requests.get(url, headers=headers)
		for vali in response.json():
			return vali['id']

	def __list_to_bullets(self, list):
		return "  --> " + "\n  --> ".join(list) if list else ""

	# Increment function to add multiple fields to url
	def __increment_url(self, url):
		if not url.endswith('?'):
				url += "&"
		return url
