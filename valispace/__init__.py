#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import json
import requests
import sys


class API:
	"""
	Defines REST API endpoints for Valispace.
	"""

	_read_only_vali_fields = [
		'id', 'url', 'name', 'formatted_formula', 'value', 'uses_default_formula', 'totalmargin_plus',
		'totalmargin_minus', 'wc_plus', 'wc_minus', 'calculated_valis', 'subscription_text', 'baseunit',
		'subscribed', 'value_baseunit', 'type', 'type_name', 'old_value',
	]

	_writable_vali_fields = [
		'reference', 'margin_plus', 'margin_minus', 'unit',
		'formula', 'description', 'parent', 'tags', 'shortname',
		'minimum', 'maximum',
	]

	def get_request_headers(self):
		return self.valispace_login['options']['Headers']

	def __init__(self, url=None, username=None, password=None):
		"""
		Performs the password-based oAuth 2.0 login for read/write access.
		"""
		print("\nAuthenticating Valispace...\n")
		if url is None:
			url = raw_input('Your Valispace url: ').rstrip("/")
		if username is None:
			username = raw_input('Username: ')
		if password is None:
			password = getpass.getpass('Password: ')

		# Check for SSL connection before sending the username and password.
		if url[:4] != "https":
			sys.stdout.write(
				"Are you sure you want to use a non-SSL connection? "
				"This will expose your password to the network [y/n]: "
			)
			while True:
				choice = raw_input().lower()
				if choice == "y":
					break
				if choice == "n":
					return

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
			print("VALISPACE-ERROR: Invalid credentials or url.")

	# def get_all_data(self, type=None):
	# 	""" Returns a dict of all component/vali/textvali/tags with their properties """
	# 	# Check if no argument was passed
	# 	if type is None:
	# 		print("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags)")
	# 		return
    #
	# 	# URL
	# 	if type is 'component':
	# 		url = self.valispace_login['url'] + "component/"
	# 	elif type is 'vali':
	# 		url = self.valispace_login['url'] + "vali/"
	# 	elif type is 'textvali':
	# 		url = self.valispace_login['url'] + "textvali/"
	# 	elif type is 'tag':
	# 		url = self.valispace_login['url'] + "tag/"
    #
	# 	headers = self.valispace_login['options']['Headers']
	# 	get_data = requests.get(url, headers=headers).json()
    #
	# 	return_dictionary = {}
	# 	for data in get_data:
	# 		return_dictionary[str(data["id"])] = data
    #
	# 	return return_dictionary

	def get_vali_list(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None, parent_id=None,
			parent_name=None, tag_id=None, tag_name=None, vali_marked_as_impacted=None):
		"""
		Returns JSON with all the Valis that mach the input arguments.
		Inputs are integers for IDs or vali_marked_as_impacted strings, and strings for names.
		Use the component 'unique_name' (not the 'name') in the parent_name argument.
		"""
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

		# Construct URL.
		url = self.valispace_login['url'] + "vali/?"
		if workspace_id:
			url += "parent__project__workspace={}".format(workspace_id)
		elif workspace_name:
			url = self.__increment_url(url) + "parent__project__workspace__name={}".format(workspace_name)
		elif project_id:
			url = self.__increment_url(url) + "parent__project__id={}".format(project_id)
		elif project_name:
			url = self.__increment_url(url) + "parent__project__name={}".format(project_name)
		elif parent_id:
			url = self.__increment_url(url) + "parent__id={}".format(parent_id)
		elif parent_name:
			url = self.__increment_url(url) + "parent__unique_name={}".format(parent_name)
		elif tag_id:
			url = self.__increment_url(url) + "tags__id={}".format(tag_id)
		elif tag_name:
			url = self.__increment_url(url) + "tags__name={}".format(tag_name)
		elif vali_marked_as_impacted:
			url = self.__increment_url(url) + "valis_marked_as_impacted={}".format(vali_marked_as_impacted)

		response = requests.get(url, headers=get_request_headers())
		return response.json()

	def get_vali_names(self):
		"""
		Returns a list of all Valis with only names and IDs.
		:returns: JSON.
		"""
		url = self.valispace_login['url'] + "valinames/"
		valinames = requests.get(url, headers=get_request_headers())
		return valinames.json()

	def get_vali(self, id):
		"""
		Returns JSON of a unique Vali.
		:param id: ID of the Vali to fetch.
		:returns: JSON object.
		"""
		if type(id) != int:
			print("VALISPACE-ERROR: The function requires an ID (int) as parameter.")
		url = self.valispace_login['url'] + "vali/{}/".format(id)
		return requests.get(url, headers=self.get_request_headers()).json()

	def get_vali_by_name(self, name):
		"""
		Returns JSON of a unique Vali.
		:param name: unique name of the vali.
		:returns: JSON object.
		"""
		if type(name) != str:
			print("VALISPACE-ERROR: The function requires a valid Vali name (str) as parameter.")

		url = self.valispace_login['url'] + "vali/?name={}".format(name)
		json_response = requests.get(url, headers=self.get_request_headers()).json()
		num_results = len(json_response)
		if num_results == 1:
			return json_response
		if num_results == 0:
			print("VALISPACE-ERROR: A Vali with this name does not exist. Please check for typos.")
		else:
			print("VALISPACE-ERROR: The name you admitted is ambiguous, are you sure you used the Vali's full name?")

	def get_vali_value(self, id):
		"""
		Returns the value of a vali.
		:param id: ID of Vali.
		:returns: int.
		"""
		try:
			vali = self.get_vali(id)
			return vali["value"]
		except:
			print("VALISPACE-ERROR: Could not retrieve Vali value.")

	# def create_vali(parent=None, type=None, shortname=None, description=None, formula=None, margin_plus=None,
	# 		margin_minus=None, minimum=None, maximum=None, reference=None, tags=None, data={}):
	# 	"""
	# 	Creates a new Vali.
	# 	"""
	# 	# TBD...

	def update_vali(self, id, shortname=None, formula=None, data={}):
		"""
		Finds the Vali that corresponds to the input id
		and updates it with the input shortname, formula and/or data.
		"""
		if not id:
			print("VALISPACE-ERROR: You need to pass an ID.")
			return

		if not shortname and not formula and not data:
			print("VALISPACE-ERROR: You have to pass data to update.")

		# Write Vali.
		if shortname:
			data["shortname"] = shortname
		if formula:
			data["formula"] = formula
		if not data:
			print(
				"You have not entered any valid fields. Here is a list of all fields that can be updated:\n{}."
				.format(", ".join(self._writable_vali_fields))
			)
		url = self.valispace_login['url'] + "vali/{}/".format(id)
		result = requests.patch(url, headers=self.get_request_headers(), data=data)
		if result.status_code == 200:
			print(
				"Successfully updated Vali {} with the following fields:\n{}"
				.format(vali["name"], stringified_new_vali_data)
			)
		else:
			print("Invalid Request.")
		return result

	def get_component_list(self, workspace_id=None, workspace_name=None, project_id=None, project_name=None,
			parent_id=None, parent_name=None, tag_id=None, tag_name=None):
		"""
		Returns JSON with all the Components that match the input arguments.
		Inputs are integers for IDs and strings for names.
		Use the component 'unique_name' (not the 'name') in the parent_name argument.

		:returns: JSON object.
		"""

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

		# Construct URL.
		"url = self.valispace_login['url'] + "component/?"
		if workspace_id:
			url += "project__workspace={}".format(workspace_id)
		elif workspace_name:
			url = self.__increment_url(url) + "workspace__name={}".format(workspace_name)
		elif project_id:
			url = self.__increment_url(url) + "project__id={}".format(project_id)
		elif project_name:
			url = self.__increment_url(url) + "project__name={}".format(project_name)
		elif parent_id:
			url = self.__increment_url(url) + "parent={}".format(parent_id)
		elif parent_name:
			url = self.__increment_url(url) + "parent__unique_name={}".format(parent_name)
		elif tag_id:
			url = self.__increment_url(url) + "tags__id={}".format(tag_id)
		elif tag_name:
			url = self.__increment_url(url) + "tags__name={}".format(tag_name)

		response = requests.get(url, headers=get_request_headers())
		return response.json()

	def get_component(self, id):
		"""
		Returns JSON of a unique Component.
		:param id: ID of the component to fetch.
		:returns: JSON object.
		"""
		if type(id) != int:
			print("VALISPACE-ERROR: The function requires an id (int) as argument.")
			return

		url = self.valispace_login['url'] + "component/{}/".format(id)
		response = requests.get(url, headers=get_request_headers())
		return response.json()

	def get_component_by_name(self, name):
		"""
		Returns JSON of a unique Component.
		:param name: unique name of the component to fetch.
		:returns: JSON object.
		"""
		if type(name) != str:
			print("VALISPACE-ERROR: The function requires a component unique name (str) as argument.")
			return

		url = self.valispace_login['url'] + "component/?unique_name={}".format(name)
		json_response = requests.get(url, headers=get_request_headers()).json()
		num_results = len(json_response)
		if num_results == 1:
			return json_response
		if num_results == 0:
			print("VALISPACE-ERROR: A Component with this name does not exist. Please check for typos.")
		else:
			print("VALISPACE-ERROR: The name you admitted is ambiguous, are you sure you used the Component's full name?")

	def get_project_list(self, workspace_id=None, workspace_name=None):
		"""
		Returns JSON with all the Projects that mach the input arguments.
		Inputs are integers for IDs and strings for names.
		:returns: JSON object.
		"""
		if type(workspace_id) != int:
			print("VALISPACE-ERROR: workspace_id must be an integer.")
			return

		# Construct URL.
		url = self.valispace_login['url'] + "project/?"
		if workspace_id:
			url += "workspace={}".format(workspace_id)
		elif workspace_name:
			url = self.__increment_url(url) + "workspace__name={}".format(workspace_name)
		response = requests.get(url, headers=get_request_headers())
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

	def post_data(self, type=None, data={}):
		"""
		Post new component/vali/textvali/tags with the input data
		Data is expected to be a JSON string with some required fields like name.
		:param type: type of object to create/update.
		:param data: dict with key value pairs for the object attributes.
		:returns: JSON object.
		"""

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

		result = requests.post(url, headers=self.get_request_headers(), data=data)

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
		"""
		Returns the correct Matrix.
		:param id: ID of Matrix.
		:returns: list of lists.
		"""
		url = self.valispace_login['url'] + "matrix/" + str(id) + "/"
		matrix_data = requests.get(url, headers=self.get_request_headers()).json()
		try:
			# TODO:
			# T: there is probably a faster and more efficient way...
			matrix = []
			for row in range(matrix_data['number_of_rows']):
				matrix.append([])
				for col in range(matrix_data['number_of_columns']):
					matrix[row].append(self.get_vali(matrix_data['cells'][row][col]))
			return matrix
		except KeyError:
			print("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
		except:
			print("VALISPACE-ERROR: Unknown error.")

	def get_matrix_str(self, id):
		"""
		Returns the correct Matrix.
		:param id: ID of Matrix.
		:returns: list of lists.
		"""
		url = self.valispace_login['url'] + "matrix/{}/".format(id)
		matrix_data = requests.get(url, headers=self.get_request_headers()).json()
		try:
			matrix = []
			for row in range(matrix_data['number_of_rows']):
				matrix.append([])
				for col in range(matrix_data['number_of_columns']):
					matrix[row].append({
						"vali": matrix_data['cells'][row][col],
						"value": self.get_vali(matrix_data['cells'][row][col])["value"],
					})
			return matrix
		except KeyError:
			print("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
		except:
			print("VALISPACE-ERROR: Unknown error.")

	def update_matrix_formulas(self, id, matrix):
		"""
		Finds the Matrix that corresponds to the input id,
		Finds each of the Valis that correspond to the vali id (contained in each cell of the matrix)
		Updates the formula of each of the Valis with the formulas contained in each cell of the input matrix.
		"""
		# Read Matrix.
		url = self.valispace_login['url'] + "matrix/{}/".format(id)
		matrix_data = requests.get(url, headers=self.get_request_headers).json()

		# Check matrix dimensions.
		if not len(matrix) == matrix_data["number_of_rows"] and len(matrix[0]) == matrix_data["number_of_columns"]:
			print('VALISPACE-ERROR: The dimensions of the local and the remote matrix do not match.')

		# Update referenced valis in each matrix cell
		for row in range(matrix_data['number_of_rows']):
			for col in range(matrix_data['number_of_columns']):
				self.update_vali(id=matrix_data['cells'][row][col], formula=matrix[row][col])

	# Increment function to add multiple fields to url
	def __increment_url(self, url):
		# TODO:
		# T: Replace this with a proper query param function...
		if not url.endswith('?'):
			url += "&"
		return url
