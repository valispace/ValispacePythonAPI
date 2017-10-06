from lib import *
import json

def pull():
	# Returns a list of all Valis
	
	if globals.valispace_login is None:
		print 'VALISPACE-ERROR: You first have to run valispace.init()'
		return	

	url     = globals.valispace_login['url'] + "vali/"
	headers = globals.valispace_login['options']['Headers']

	result  = requests.get(url, headers=headers)

	valis = result.json()	

	return_dictionary = {}
	for vali in valis:
		return_dictionary[str(vali["id"])] = vali

	return return_dictionary
