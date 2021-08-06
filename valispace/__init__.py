#!/usr/bin/env python
# -*- coding: utf-8 -*-


from logging import Logger
import typing
import httpx


"""
Valispace public python API, version 2
"""


class ValispaceException(Exception):
    pass


class Valispace:
    def __init__(
        self,
        options: typing.Optional[typing.Dict[str, typing.Union[str, typing.Any]]] = None,
        username: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        url: typing.Optional[str] = None
    ):
        self.total_requests: int = 0

        username = options.get("username", username) if options is not None else None
        if not username:
            raise ValispaceException("Username not provided")

        password = options.get("password", password) if options is not None else None
        if not password:
            raise ValispaceException("Password not provided")

        url = options.get("url", url) if options is not None else None
        if not url:
            raise ValispaceException("URL not provided")
        else:
            url = url.strip().rstrip("/")
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "https://" + url

        t = options.get("logger", None) if options is not None else None
        if t is None and not isinstance(t, Logger):
            import logging
            self.logger: Logger = logging.getLogger("console")
        else:
            self.logger: Logger = typing.cast(Logger, t)

        self.__url = url + "/rest/"
        self.__oauth_url = url + "/o/token/"

        self.logger.debug(f"URL: {self.__url}")

        self.client = httpx.AsyncClient()

        CLIENT_ID = "ValispaceREST"

        result = self.client.post(self.__oauth_url, data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": CLIENT_ID,
        })


class Project:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Component:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Vali:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Matrix:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class TextVali:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Specification:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Requirement:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


# vvv OLD STUFF vvv


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

    _writable_vali_fields = [
        'reference', 'margin_plus', 'margin_minus', 'unit',
        'formula', 'description', 'parent', 'tags', 'shortname',
        'minimum', 'maximum',
    ]


    def __init__(self, url=None, username=None, password=None, keep_credentials=False, warn_https=True):
        print("\nAuthenticating Valispace...\n")
        if url is None:
            url = six.moves.input('Your Valispace url: ')

        url = url.strip().rstrip("/")

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url

        # Check for SSL connection before sending the username and password.
        if warn_https and url[:5] != "https":
            sys.stdout.write("Are you sure you want to use a non-SSL connection? "
                "This will expose your password to the network and might be a significant security risk [y/n]: ")
            while True:
                choice = six.moves.input().lower()
                if choice == "y":
                    break
                if choice == "n":
                    return
                print("Please answer 'y' or 'n'")

        self._url = url + '/rest/'
        self._oauth_url = url + '/o/token/'
        self._session = requests.Session()
        self.username, self.password = None, None
        if self.login(username, password):
            if keep_credentials:
                self.username, self.password = username, password
            print("You have been successfully connected to the {} API.".format(self._url))


    def login(self, username=None, password=None):
        """
        Performs the password-based oAuth 2.0 login for read/write access.
        """
        # clear out old auth headers
        self._session.headers = {}
        if username is None:
            username = six.moves.input('Username: ').strip()
        if password is None:
            password = getpass.getpass('Password: ').strip()

        try:
            client_id = "ValispaceREST"  # registered client-id in Valispace Deployment
            response = self._session.post(self._oauth_url, data={
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

        response.raise_for_status()

        json = response.json()

        if 'error' in json and json['error'] != None:
            if 'error_description' in json:
                raise Exception("VALISPACE-ERROR: " + json['error_description'])
            else:
                raise Exception("VALISPACE-ERROR: " + json['error'])
            return

        access = "Bearer " + json['access_token']
        self._session.headers = {
            'Authorization': access,
            'Content-Type': 'application/json'
        }
        return True


    def get_all_data(self, type=None):
        """
        Returns a dict of all component/vali/textvali/tags with their properties.
        """
        # Check if valid argument was passed.
        if type not in ('component', 'vali', 'textvali', 'tag'):
            raise Exception("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags)")

        if type in ('component', 'vali', 'textvali'):
            url = type + 's/' # add an s to the end to get to the right endpoint
        else:
            url = type + '/'

        get_data = self.get(url)

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
        url = "valis/?"
        if workspace_id:
            url += "parent__project__workspace={}".format(workspace_id)
        if workspace_name:
            url = self.__increment_url(url) + "parent__project__workspace__name={}".format(workspace_name)
        if project_id:
            url = self.__increment_url(url) + "project={}".format(project_id)
        if project_name:
            project = self.get_project_by_name(project_name)
            url = self.__increment_url(url) + "project={}".format(project[0]['id'])
        if parent_id:
            url = self.__increment_url(url) + "parent={}".format(parent_id)
        if parent_name:
            url = self.__increment_url(url) + "parent__unique_name={}".format(parent_name)
        if tag_id:
            url = self.__increment_url(url) + "tags__id={}".format(tag_id)
        if tag_name:
            url = self.__increment_url(url) + "tags__name={}".format(tag_name)
        if vali_marked_as_impacted:
            url = self.__increment_url(url) + "valis_marked_as_impacted={}".format(vali_marked_as_impacted)

        try:
            return self.get(url)
        except Exception as e:
            print('Something went wrong with the request. Details: {}'.format(e))

        # if response.status_code != 200:
        #     print('Response:', response)
        #     print('Status code:', response.status_code)
        #     print('Text:', response.text)
        #     return None
        # else:
        #     return response.json()


    def get_vali_names(self, project_name=None):
        """
        Returns a list of all Valis with only names and IDs.
        :returns: JSON object.
        """
        if project_name:
            project = self.get_project_by_name(project_name)
            if project:
                project = project[0]
                return self.get("valis/?fields=id,name&_project={}".format(project["id"]))
            else:
                return None
        else:
            return self.get("valis/?fields=id,name")


    def get_vali(self, id):
        """
        Returns JSON of a unique Vali.
        :param id: ID of the Vali to fetch.
        :returns: JSON object.
        """
        if type(id) != int:
            raise Exception("VALISPACE-ERROR: The function requires an ID (int) as parameter.")
        return self.get("valis/{}/".format(id))


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
                return self.get("valis/{}/".format(entry["id"]))

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

        url = "fuzzysearch/Vali/name/{}/".format(searchterm)
        result = self.get(url, allow_redirects=True)

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
    #         margin_minus=None, minimum=None, maximum=None, reference=None, tags=None, data={}):
    #     """
    #     Creates a new Vali.
    #     """
    #     # TBD...


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
        url = "valis/{}/".format(id)
        return self.request('PATCH', url, data=data)


    def impact_analysis(self, id, target_vali_id, range_from, range_to, range_step_size):
        data = {}

        if not id:
            raise Exception("VALISPACE-ERROR: You need to pass an ID.")

        url = "valis/{}/impact-analysis-graph-for/{}/?range_min={}&range_max={}&range_step_size={}".format(id, target_vali_id, range_from, range_to, range_step_size)
        # FIXME: (patrickyeon) I special-cased this because there's some
        #        printing of returned values on error, but I suspect
        #        that is really better handled by the normal error-
        #        handling path and getting rid of these print()s
        print(url)
        result = self._session.get(self._url + url, data=data)
        if result.status_code != 200:
            print(result.text)
            raise Exception("Invalid Request.")
        return json.loads(result.text)


    def what_if(self, vali_name, target_name, value):
        if not id or not target_name or not value:
            raise Exception("VALISPACE-ERROR: You need to pass an ID.")

        url = "alexa_what_if/{}/{}/{}/".format(vali_name, target_name, value)
        # FIXME: (patrickyeon) same comment as on impact_analysis()
        print(url)
        result = self._session.get(self._url + url)
        if result.status_code != 200:
            print(result.text)
            raise Exception("Invalid Request.")
        return json.loads(result.text)


    def get_component_list(
        self,
        workspace_id=None,
        workspace_name=None,
        project_id=None,
        project_name=None,
        parent_id=None,
        parent_name=None,
        tag_id=None,
        tag_name=None,
    ):
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
        url = "components/?"
        if workspace_id:
            url += "project__workspace={}".format(workspace_id)
        elif workspace_name:
            url = self.__increment_url(url) + "workspace__name={}".format(workspace_name)
        elif project_id:
            url = self.__increment_url(url) + "project={}".format(project_id)
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

        return self.get(url)


    def get_component(self, id):
        """
        Returns JSON of a unique Component.
        :param id: ID of the component to fetch.
        :returns: JSON object.
        """
        if type(id) != int:
            raise Exception("VALISPACE-ERROR: The function requires an id (int) as argument.")

        return self.get("components/{}/".format(id))


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

        project = self.get_project_by_name(name=project_name)
        results = []
        component_list = self.get_component_list(project_name=project_name)
        for entry in component_list:
            if entry['unique_name'] == unique_name:
                results.append(entry)
                #return self.get("valis/{}/".format(entry["id"]))
        num_results = len(results)

        if num_results == 1:
            return results[0]
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
        url = "project/?"
        if workspace_id:
            if type(workspace_id) != int:
                raise Exception("VALISPACE-ERROR: workspace_id must be an integer.")
            url += "workspace={}".format(workspace_id)
        elif workspace_name:
            if type(workspace_name) != str:
                raise Exception("VALISPACE-ERROR: workspace_name must be a string.")
            url = self.__increment_url(url) + "workspace__name={}".format(workspace_name)
        return self.get(url)


    def get_project(self, id):
        """
        Retrieve a Project via ID.
        :param id: ID of the project.
        :returns: JSON object.
        """
        if type(id) != int:
            raise Exception("VALISPACE-ERROR: The function requires an id (int) as argument.")
        return self.get("project/{}/".format(id))


    def get_project_by_name(self, name):
        """
        Retrieve a Project via name.
        :param name: name of the project (unique).
        :returns: JSON object.
        """
        if type(name) != str:
            raise Exception("VALISPACE-ERROR: The function requires a valid project name (str) as argument.")

        # Construct URL.
        url = "project/?name={}".format(name)
        response = self.get(url)
        if len(response) == 0:
            raise Exception("VALISPACE-ERROR: A Project with this name does not exist. Please check for typos.")
        else:
            return response


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
        if type not in ('component', 'vali', 'textvali', 'tag'):
            raise Exception("VALISPACE-ERROR: Type argument expected (component/vali/textvali/tags).")

        if type in ('component', 'vali', 'textvali'):
            url = type + 's/' # Add an s to the end of the type for component, vali and textvali to get to the correct endpoint
        else:
            url = type + '/'

        # FIXME: (patrickyeon) special-casing this, but maybe this whole
        #        method is not required now that post() exists?
        result = self._session.post(self._url + url, data=data)

        if result.status_code == 201:
            print("Successfully updated Vali:\n" + str(data) + "\n")
        elif result.status_code == 204:
            raise Exception(
                "The server successfully processed the request, but is not "
                "returning any content (status code: 204)\n"
            )
        elif result.status_code == 500:
            raise Exception(
                "The server encountered an unexpected condition which "
                "prevented it from fulfilling the request (status code: 500)\n"
            )
        else:
            raise Exception("Invalid Request (status code: {}): {}\n".format(result.status_code, result.content))

        return result.json()


    def post(self, url, data=None, **kwargs):
        """
        Posts data
        :param url: the relative url
        :param data: the data
        :param **kwargs: additional args passed to the request call
        :returns: JSON object.
        """

        return self.request('POST', url, data, **kwargs)


    def get(self, url, data=None, **kwargs):
        """
        Posts data
        :param url: the relative url
        :param data: the data
        :param **kwargs: additional args passed to the request call
        :returns: JSON object.
        """

        return self.request('GET', url, data, **kwargs)


    def request(self, method, url, data=None, **kwargs):
        """
        Generic request data
        :param method: the method
        :param url: the relative url
        :param data: the data
        :param **kwargs: additional args passed to the request call
        :returns: JSON object.
        """

        url = self._url + url
        result = self._session.request(method, url, json=data, **kwargs)

        if result.status_code == 401:
            # authentication expired
            if self.username is None:
                print("Authentication expired, please re-login")
                # otherwise, we've got it saved and this is transparent
            self.login(self.username, self.password)
            # try the request one more time
            result = self._session.request(method, url, json=data, **kwargs)

        result.raise_for_status()
        return result.json()


    def get_matrix(self, id):
        """
        Returns the correct Matrix.
        :param id: ID of Matrix.
        :returns: list of lists.
        """
        url = "matrices/{}/".format(id)
        matrix_data = self.get(url)
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
        url = "matrices/{}/".format(id)
        matrix_data = self.get(url)
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
        url = "matrices/{}/".format(id)
        matrix_data = self.get(url)

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
        url = 'rest/valis/' + vali_id + '/convert-to-dataset/'

        data = {}
        return self.post(url, data)


    def create_dataset_and_set_values(self, vali_id, input_data):
        """
        Sets a dataset.
        :param vali_id: Id of the vali where we want to create the dataset.
        :param data: Data, in the format of [[x0, y0...], [x1, y1...], ...]
        """
        if type(input_data) != list:
            raise Exception('input_data must be an array')

        url = 'datasets/'
        data = {
            "vali": vali_id
        }
        try:
            response = self.post(url, data)
        except:
            raise Exception("VALISPACE ERROR: Is the vali_id valid?")

        dataset_id = response['id']
        variable_id = response['points'][0]['variables'][0]['id']
        point_id = response['points'][0]['id']

        s = 0

        for d in input_data:
            if s != 0:
                if len(d) != s:
                    raise Exception("Data members with inconsistent length. Found {}, expected {}.".format(len(d), s))
                url = 'vali/functions/datasets/points/'
                data = {
                    "dataset": dataset_id
                }
                response = self.post(url, data)
                point_id = response['id']
                variable_id = response['variables'][0]['id']
            else:
                s = len(d)

            url = 'vali/functions/datasets/points/{}/'.format(point_id)
            data = {
                "value": d[0]
            }
            self.request('PATCH', url, json=data)

            for v in d[1:]:
                url = 'vali/functions/datasets/points/variables/{}/'.format(variable_id)
                data = {
                    "value_number": v
                }
                self.request('PATCH', url, json=data)

        return dataset_id


    def vali_import_dataset(self, vali_id, data, headers=None):
        if headers is None:
            headers = []
            for i in range(len(data[0])):
                headers.append(chr(ord('a') + i))
        self.request('POST', 'valis/' + str(vali_id) + '/import-dataset/', data={'headers': headers, 'data': data})
