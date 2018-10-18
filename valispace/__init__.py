#!/usr/bin/env python
# -*- coding: utf-8 -*-


import getpass
import json
import requests
import sys
import six
import re


class API:
	"""
	Defines REST API endpoints for Valispace.
	"""

	_read_only_vali_fields = [
		'id', 'url', 'name', 'formatted_formula', 'value', 'uses_default_formula', 'totalmargin_plus',
		'totalmargin_minus', 'wc_plus', 'wc_minus', 'calculated_valis', 'subscription_text', 'baseunit',
		'subscribed', 'value_baseunit', 'type', 'type_name', 'old_value', "data_type", "function_data",
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
			url = six.moves.input('Your Valispace url: ')
		if username is None:
			username = six.moves.input('Username: ').strip()
		if password is None:
			password = getpass.getpass('Password: ').strip()

		url = url.strip().rstrip("/")

		if not (url.startswith('http://') or url.startswith('https://')):
			url = 'http://' + url	# default to http... should be https

		# Check for SSL connection before sending the username and password.
		'''
		if url[:5] != "https":
			sys.stdout.write("Are you sure you want to use a non-SSL connection? "
				"This will expose your password to the network and might be a significant security risk [y/n]: ")
			while True:
				choice = six.moves.input().lower()
				if choice == "y":
					break
				if choice == "n":
					return
		'''

		try:
			oauth_url = url + '/o/token/'
			client_id = "ValispaceREST"  # registered client-id in Valispace Deployment
			response = requests.post(oauth_url, data={
				'grant_type': 'password',
				'username': username,
				'password': password,
				'client_id': client_id,
			})
		except requests.exceptions.RequestException as e:
			raise Exception("VALISPACE-ERROR: " + str(e))
		except:
			# TODO:
			# T: Capture specific exceptions, bc it is also possible that
			# the endpoint does not work or something like that...
			raise Exception("VALISPACE-ERROR: Invalid credentials or url.")

		if response.status_code != 200:
			raise Exception("VALISPACE-ERROR: Unknown.")

		json = response.json()

		if 'error' in json and json['error'] != None:
			if 'error_description' in json:
				raise Exception("VALISPACE-ERROR: " + json['error_description'])
			else:
				raise Exception("VALISPACE-ERROR: " + json['error'])
			return

		access = "Bearer " + json['access_token']
		self.valispace_login = {
			'url': url + '/rest/',
			'options': {
				'Timeout': 200,
				'Headers': {
					'Authorization': access,
					'Content-Type': 'application/json',
					#'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
				}
			}
		}
		print("You have been successfully connected to the {} API.".format(self.valispace_login['url']))


	def get_all_data(self, type=None):
		"""
		Returns a dict of all component/vali/textvali/tags with their properties.
		"""
		# Check if no argument was passed.
		if type is None:
			raise Exception("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags)")

		# URL
		if type is 'component':
			url = self.valispace_login['url'] + "component/"
		elif type is 'vali':
			url = self.valispace_login['url'] + "vali/"
		elif type is 'textvali':
			url = self.valispace_login['url'] + "textvali/"
		elif type is 'tag':
			url = self.valispace_login['url'] + "tag/"

		get_data = requests.get(url, headers=self.get_request_headers()).json()

		return_dictionary = {}
		for data in get_data:
			return_dictionary[str(data["id"])] = data

		return return_dictionary


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
				raise Exception("VALISPACE-ERROR: Workspace id must be an integer.")

		if project_id:
			try:
				project_id = int(project_id)
			except:
				raise Exception("VALISPACE-ERROR: Project id must be an integer")

		if parent_id:
			try:
				parent_id = int(parent_id)
			except:
				raise Exception("VALISPACE-ERROR: Parent id must be an integer")

		if tag_id:
			try:
				tag_id = int(tag_id)
			except:
				raise Exception("VALISPACE-ERROR: Tag id must be an integer")

		if vali_marked_as_impacted:
			try:
				vali_marked_as_impacted = int(vali_marked_as_impacted)
			except:
				raise Exception("VALISPACE-ERROR: Vali_marked_as_impacted must be an integer")

		# Construct URL.
		url = self.valispace_login['url'] + "vali/?"
		if workspace_id:
			url += "parent__project__workspace={}".format(workspace_id)
		if workspace_name:
			url = self.__increment_url(url) + "parent__project__workspace__name={}".format(workspace_name)
		if project_id:
			url = self.__increment_url(url) + "parent__project__id={}".format(project_id)
		if project_name:
			url = self.__increment_url(url) + "parent__project__name={}".format(project_name)
		if parent_id:
			url = self.__increment_url(url) + "parent__id={}".format(parent_id)
		if parent_name:
			url = self.__increment_url(url) + "parent__unique_name={}".format(parent_name)
		if tag_id:
			url = self.__increment_url(url) + "tags__id={}".format(tag_id)
		if tag_name:
			url = self.__increment_url(url) + "tags__name={}".format(tag_name)
		if vali_marked_as_impacted:
			url = self.__increment_url(url) + "valis_marked_as_impacted={}".format(vali_marked_as_impacted)
		response = requests.get(url, headers=self.get_request_headers())

		if response.status_code != 200:
			print('Response:', response)
			print('Status code:', response.status_code)
			print('Text:', response.text)
			return None
		else:
			return response.json()

	def get_vali_names(self, project_name=None):
		"""
		Returns a list of all Valis with only names and IDs.
		:returns: JSON object.
		"""
		url = self.valispace_login['url']
		if project_name:
			project = get_project_by_name(project_name)
			url += "project/{}/valinames/".format(project["id"])
		else:
		 	url += "valinames/"
		valinames = requests.get(url, headers=self.get_request_headers())
		return valinames.json()


	def get_vali(self, id):
		"""
		Returns JSON of a unique Vali.
		:param id: ID of the Vali to fetch.
		:returns: JSON object.
		"""
		if type(id) != int:
			raise Exception("VALISPACE-ERROR: The function requires an ID (int) as parameter.")
		url = self.valispace_login['url'] + "vali/{}/".format(id)
		return requests.get(url, headers=self.get_request_headers()).json()


	def get_vali_by_name(self, vali_name, project_name):
		"""
		Returns JSON of a unique Vali.
		:param vali_name: unique name of the vali.
		:returns: JSON object.
		"""
		if type(vali_name) != str:
			raise Exception("VALISPACE-ERROR: The function requires a valid Vali name (str) as parameter.")

		if type(project_name) != str:
			raise Exception("VALISPACE-ERROR: The function requires a valid Project name (str) as parameter.")

		valinames = self.get_vali_names()
		for entry in valinames:
			if entry['name'] == vali_name:
				url = self.valispace_login['url'] + "vali/{}/".format(entry["id"])
				response = requests.get(url, headers=self.get_request_headers())
				return response.json()

		raise Exception("VALISPACE-ERROR: There is no Vali with this name and project, make sure you admit a "
			"valid full name for the vali (e.g. ComponentX.TestVali) and a valid project name.")


	def fuzzysearch_vali(self, searchterm):
		"""
		Returns JSON of a unique Vali given a similar name
		:param searchterm: (not necessarily exact) name of vali
		:returns: JSON object.
		"""
		if type(searchterm) != str:
			raise Exception("VALISPACE-ERROR: The function requires a string as parameter.")

		url = self.valispace_login['url'] + "fuzzysearch/Vali/name/{}/".format(searchterm)
		result = requests.get(url, headers=self.get_request_headers(), allow_redirects=True).json()

		if result == {}:
			raise Exception("VALISPACE-ERROR: Could not find a matching vali for {}".format(searchterm))
		else:
			return result


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
			raise Exception("VALISPACE-ERROR: Could not retrieve Vali value.")

	# def create_vali(parent=None, type=None, shortname=None, description=None, formula=None, margin_plus=None,
	# 		margin_minus=None, minimum=None, maximum=None, reference=None, tags=None, data={}):
	# 	"""
	# 	Creates a new Vali.
	# 	"""
	# 	# TBD...


	def update_vali(self, id, shortname=None, formula=None, data=None):
		"""
		Finds the Vali that corresponds to the input id
		and updates it with the input shortname, formula and/or data.
		"""
		if data == None :
			data = {}
		elif type(data) != dict:
			raise Exception('VALISPACE-ERROR: data needs to be a dictionary. To update formula / value use "formula"')

		if not id:
			raise Exception("VALISPACE-ERROR: You need to pass an ID.")

		if not shortname and not formula and not data:
			raise Exception("VALISPACE-ERROR: You have to pass data to update.")

		# Write Vali.
		if shortname:
			data["shortname"] = shortname
		if formula:
			data["formula"] = formula
		if not data:
			raise Exception("You have not entered any valid fields. Here is a list of all fields \
				that can be updated:\n{}.".format(", ".join(self._writable_vali_fields)))
		url = self.valispace_login['url'] + "vali/{}/".format(id)
		result = requests.patch(url, headers=self.get_request_headers(), data=json.dumps(data))
		if result.status_code != 200:
			raise Exception("Invalid Request.")
		return json.loads(result.text)


	def impact_analysis(self, id, target_vali_id, range_from, range_to, range_step_size):
		data = {}

		if not id:
			raise Exception("VALISPACE-ERROR: You need to pass an ID.")

		url = self.valispace_login['url'] + "vali/{}/impact-analysis-graph-for/{}/?range_min={}&range_max={}&range_step_size={}".format(id, target_vali_id, range_from, range_to, range_step_size)
		print(url)
		result = requests.get(url, headers=self.get_request_headers(), data=data)
		if result.status_code != 200:
			print(result.text)
			raise Exception("Invalid Request.")
		return json.loads(result.text)


	def what_if(self, vali_name, target_name, value):
		if not id or not target_name or not value:
			raise Exception("VALISPACE-ERROR: You need to pass an ID.")

		url = self.valispace_login['url'] + "alexa_what_if/{}/{}/{}/".format(vali_name, target_name, value)
		print(url)
		result = requests.get(url, headers=self.get_request_headers())
		if result.status_code != 200:
			print(result.text)
			raise Exception("Invalid Request.")
		return json.loads(result.text)


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
				raise Exception("VALISPACE-ERROR: Workspace id must be an integer.")
		if project_id:
			try:
				project_id = int(project_id)
			except:
				raise Exception("VALISPACE-ERROR: Project id must be an integer.")
		if parent_id:
			try:
				parent_id = int(parent_id)
			except:
				raise Exception("VALISPACE-ERROR: Parent id must be an integer.")
		if tag_id:
			try:
				tag_id = int(tag_id)
			except:
				raise Exception("VALISPACE-ERROR: Tag id must be an integer.")

		# Construct URL.
		url = self.valispace_login['url'] + "component/?"
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

		response = requests.get(url, headers=self.get_request_headers())

		if response.status_code != 200:
			#print('Response:', response)
			print('Status code:', response.status_code)
			#print('Text:', response.text)
			return None
		else:
			return response.json()


	def get_component(self, id):
		"""
		Returns JSON of a unique Component.
		:param id: ID of the component to fetch.
		:returns: JSON object.
		"""
		if type(id) != int:
			raise Exception("VALISPACE-ERROR: The function requires an id (int) as argument.")

		url = self.valispace_login['url'] + "component/{}/".format(id)
		return requests.get(url, headers=self.get_request_headers()).json()


	def get_component_by_name(self, unique_name, project_name):
		"""
		Returns JSON of a unique Component.
		:param name: unique name of the component to fetch.
		:returns: JSON object.
		"""
		if type(unique_name) != str:
			raise Exception("VALISPACE-ERROR: The function requires a component unique name (str) as argument.")

		if type(project_name) != str:
			raise Exception("VALISPACE-ERROR: The function requires a valid Project name (str) as argument.")

		url = self.valispace_login['url'] + "component/?unique_name={}&project__name={}".format(unique_name, project_name)
		json_response = requests.get(url, headers=self.get_request_headers()).json()
		num_results = len(json_response)

		print("num_results: ", num_results)

		if num_results == 1:
			return json_response
		if num_results == 0:
			raise Exception("VALISPACE-ERROR: A Component with this name does not exist. Please check for typos.")
		else:
			raise Exception("VALISPACE-ERROR: The name you admitted is ambiguous, are you sure you used the Component's full name?")


	def get_project_list(self, workspace_id=None, workspace_name=None):
		"""
		Returns JSON with all the Projects that mach the input arguments.
		Inputs are integers for IDs and strings for names.
		:returns: JSON object.
		"""
		# Construct URL.
		url = self.valispace_login['url'] + "project/?"
		if workspace_id:
			if type(workspace_id) != int:
				raise Exception("VALISPACE-ERROR: workspace_id must be an integer.")
			url += "workspace={}".format(workspace_id)
		elif workspace_name:
			if type(workspace_name) != str:
				raise Exception("VALISPACE-ERROR: workspace_name must be a string.")
			url = self.__increment_url(url) + "workspace__name={}".format(workspace_name)
		response = requests.get(url, headers=self.get_request_headers())
		return response.json()


	def get_project(self, id):
		"""
		Retrieve a Project via ID.
		:param id: ID of the project.
		:returns: JSON object.
		"""
		if type(id) != int:
			raise Exception("VALISPACE-ERROR: The function requires an id (int) as argument.")
		url = self.valispace_login['url'] + "project/{}/".format(id)
		return requests.get(url, headers=self.get_request_headers()).json()


	def get_project_by_name(self, name):
		"""
		Retrieve a Project via name.
		:param name: name of the project (unique).
		:returns: JSON object.
		"""
		if type(name) != str:
			raise Exception("VALISPACE-ERROR: The function requires a valid project name (str) as argument.")

		# Construct URL.
		url = self.valispace_login['url'] + "project/?name={}".format(name)
		json_response = requests.get(url, headers=self.get_request_headers()).json()
		num_results = len(json_response)
		if num_results == 0:
			raise Exception("VALISPACE-ERROR: A Project with this name does not exist. Please check for typos.")
		else:
			return json_response


	def post_data(self, type=None, data=None):
		"""
		Post new component/vali/textvali/tags with the input data
		Data is expected to be a JSON string with some required fields like name.
		:param type: type of object to create/update.
		:param data: dict with key value pairs for the object attributes.
		:returns: JSON object.
		"""
		# Check if no argument was passed
		if data is None:
			data = {}
		elif type is None:
			raise Exception("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags).")

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
			raise Exception("The server successfully processed the request, but is not returning any content (status code: 204)\n")
		elif result.status_code == 500:
			raise Exception("The server encountered an unexpected condition which prevented it from fulfilling the request (status code: 500)\n")
		else:
			raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

		return result.json()


	def post(self, url, data=None):
		"""
		Posts data
		:param url: the relative url
		:param data: the data
		:returns: JSON object.
		"""

		self.request('POST', url, data)


	def get(self, url, data=None):
		"""
		Posts data
		:param url: the relative url
		:param data: the data
		:returns: JSON object.
		"""

		self.request('GET', url, data)


	def request(self, method, url, data=None):
		"""
		Generic request data
		:param method: the method
		:param url: the relative url
		:param data: the data
		:returns: JSON object.
		"""

		url = self.valispace_login['url'] + url
		result = requests.request(method, url, headers=self.get_request_headers(), json=data)

		if result.status_code >= 200 and result.status_code < 300:
			return result.json()
		else:
			raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))


	def get_matrix(self, id):
		"""
		Returns the correct Matrix.
		:param id: ID of Matrix.
		:returns: list of lists.
		"""
		url = self.valispace_login['url'] + "matrix/{}/".format(id)
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
			raise Exception("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
		except:
			raise Exception("VALISPACE-ERROR: Unknown error.")


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
			raise Exception("VALISPACE-ERROR: Matrix with id {} not found.".format(id))
		except:
			raise Exception("VALISPACE-ERROR: Unknown error.")

	def update_matrix_formulas(self, id, matrix_formula):
		"""
		Finds the Matrix that corresponds to the input id,
		Finds each of the Valis that correspond to the vali id (contained in each cell of the matrix)
		Updates the formula of each of the Valis with the formulas contained in each cell of the input matrix.
		"""
		# Read Matrix.
		url = self.valispace_login['url'] + "matrix/{}/".format(id)
		matrix_data = requests.get(url, headers=self.get_request_headers).json()

		# Check matrix dimensions.
		if not len(matrix_formula) == matrix_data["number_of_rows"] and len(matrix_formula[0]) == matrix_data["number_of_columns"]:
			raise Exception('VALISPACE-ERROR: The dimensions of the local and the remote matrix do not match.')

		# Update referenced valis in each matrix cell
		for row in range(matrix_data['number_of_rows']):
			for col in range(matrix_data['number_of_columns']):
				self.update_vali(id=matrix_data['cells'][row][col], formula=matrix_formula[row][col])

	# Increment function to add multiple fields to url
	def __increment_url(self, url):
		# TODO:
		# T: Replace this with a proper query param function...
		if not url.endswith('?'):
			url += "&"
		return url


	def vali_create_dataset(self, vali_id):
		"""
		Creates a new dataset in vali.
		:param vali_id: Id of the vali where we want to create the dataset.
		:returns: New datset id.
		"""
		url = self.valispace_login['url'] + 'vali/functions/datasets/'

		data = {
			"vali": int(vali_id)
		}

		result = requests.post(url, headers=self.get_request_headers(), json=data)

		if result.status_code != 201:
			raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

		return result.json()['id']


	'''def vali_dataset_set_values(self, vali_id, dataset_id, input_data, *name):
		"""
		Sets a dataset data.
		:param dataset_id: Id of the dataset that we want to change.
		:param data: Data, in the format of [[x0, y0...], [x1, y1...], ...]
		:param name: Name of each column, optional.
		"""
		url = self.valispace_login['url'] + 'vali/functions/datasets/'

		#if len(input_data) > 0:
		#	input_data.insert(0, name)

		s = 0

		points = []

		for d in input_data:
			if s != 0:
				if len(d) != s:
					raise Exception("Data members with inconsistent length. Found {}, expected {}.".format(len(d), s))
			else:
				s = len(d)

			point = {
				#'dataset': dataset_id,
				'position': d[0],
				'variables': [],
			}

			for v in d[1:]:
				point['variables'].append({
					'value': str(v),
					'value_string': str(v),
					'value_number': float(v),
				})

			points.append(point)

		data = {
			#'id': dataset_id,
			'vali': vali_id,
			'dimensions': s - 1,
			'points': points,
		}

		print(json.dumps(data))

		result = requests.post(url, headers=self.get_request_headers(), json=data)

		print(result.status_code, result.content)'''


	def create_dataset_and_set_values(self, vali_id, input_data):
		"""
		Sets a dataset.
		:param vali_id: Id of the vali where we want to create the dataset.
		:param data: Data, in the format of [[x0, y0...], [x1, y1...], ...]
		"""
		if type(input_data) != list:
			raise Exception('input_data must be an array')

		url = self.valispace_login['url'] + 'vali/functions/datasets/'
		data = {
			"vali": vali_id
		}
		try:
			response = requests.post(url, headers=self.get_request_headers(), json=data)
		except:
			raise Exception("VALISPACE ERROR: Is the vali_id valid?")

		if response.status_code >= 300:
			raise Exception("Invalid Request (status code: {}): {}\n".format(response.status_code, response.content))

		response = response.json()
		dataset_id = response['id']
		variable_id = response['points'][0]['variables'][0]['id']
		point_id = response['points'][0]['id']

		s = 0

		for d in input_data:
			if s != 0:
				if len(d) != s:
					raise Exception("Data members with inconsistent length. Found {}, expected {}.".format(len(d), s))
				url = self.valispace_login['url'] + 'vali/functions/datasets/points/'
				data = {
					"dataset": dataset_id
				}
				response = requests.post(url, headers=self.get_request_headers(), json=data)
				if response.status_code >= 300:
					raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

				response = response.json()
				point_id = response['id']
				variable_id = response['variables'][0]['id']
			else:
				s = len(d)

			url = self.valispace_login['url'] + 'vali/functions/datasets/points/' + str(point_id) + '/'
			data = {
				"value": d[0]
			}
			response = requests.patch(url, headers=self.get_request_headers(), json=data)
			if response.status_code >= 300:
				raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

			for v in d[1:]:
				url = self.valispace_login['url'] + 'vali/functions/datasets/points/variables/' + str(variable_id) + '/'
				data = {
					"value_number": v
				}
				response = requests.patch(url, headers=self.get_request_headers(), json=data)
				if response.status_code >= 300:
					raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

		return dataset_id
