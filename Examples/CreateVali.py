import valispace

deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")


# The ID of the Component where the Vali will be created
component_id = 

# Object with the new Vali Properties
vali = {
	"shortname": "Force",
	"formula": 10,
	"unit": "N",
	"parent": component_id
}

# Function to get Vali by the fullname
Vali = valispace.post("valis/", vali)

