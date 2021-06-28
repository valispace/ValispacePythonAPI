# This code returns all child components (ids and names) from a given component in a flat list (no hierarchy)
import valispace

deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")

components_ids = {}
component_id = 

def get_child(parent_id):
	children_list = valispace.get("components/?parent="+str(parent_id))
	for child in children_list:
		components_ids[child["id"]] = child["name"]
		if child["children"] != []:
			get_child(child["id"])


get_child(component_id)
print(components_ids)