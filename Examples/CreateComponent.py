import valispace

deployment = input("Deployment Name:")
valispace = valispace.API(deployment=deployment)

# The ID of the Parent Component; If it is at the highest level, parent is null, but project need to be specified.
parent_component = 

# Object with the new Component Property
component = {
	"name": "NewCompentName",
	"parent": parent_component
}

# Function to get Vali by the fullname
componentPosted = valispace.post("components/", component)

