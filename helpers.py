from lib import * 

def pull_vali_names():
	# Returns a list of all Valis with only names and ids
	
	url     = globals.valispace_login['url'] + "valinames/"
	headers = globals.valispace_login['options']['Headers']

	result  = requests.get(url, headers=headers)

	return result.json()

def name_to_id(name):
	valis = pull_vali_names()
	for vali in valis:
		if vali["name"] == name:
			return vali["id"]
