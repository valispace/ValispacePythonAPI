from lib import *

def init(url=None, username=None, password=None):
	# performs the password based oAuth 2.0 login for resd/write access

	
	# if url      is None:
	# url      = raw_input('url: ')
	# if username is None:
	# username = raw_input('username: ')
	# if password is None:
	# password = raw_input('password: ')

	if url      is None:
		url      = "https://demo.valispace.com"
	if username is None:
		username = "francisco.lgpc"
	if password is None:
		password = "password"


	### TBD - check for SSL connection, before sending the username and password ###

	# define global variables
	globals.init()

	oauth_url = url + "/o/token/"
	client_id = "docs.valispace.com/user-guide/addons/#matlab" # registered client-id in Valispace Deployment
	result = requests.post(oauth_url, data = {
		'grant_type': 'password',
  	'username':   username,
  	'password':   password,
  	'client_id':  client_id
	})
	access = "Bearer " + result.json()['access_token']
  
	
	globals.valispace_login = { 
		'url': url + '/rest/', 
		'options': {
			'Timeout': 200, 
			'Headers': { 'Authorization': access, 'Content-Type': 'application/json' }
	  }
  }

	print "You have been successfully connected to the " + globals.valispace_login['url'] + " API."

# Test
# init("https://demo.valispace.com","francisco.lgpc","")