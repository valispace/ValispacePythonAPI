# This code generates a csv file with a System breakdown, with each level divided in columns, and the selected properties.
# This Script doesn't work with Matrices yet.

import valispace
import csv

deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")


# ID of the main component to start the BOM from.
# Obs.: It can be multiple IDs. E.g.: [100, 110]
MainComponents = []

# Name of the generated file containing the BOM
fileName = "BOM.csv"


# Headers
# You can rename levels by anythign else. For example: ["System", "Subsystem", "Element"]
# but the number of elements in this list, is the depth you go with the BOM.
Levels = ["Level 1", "Level 2", "Level 3", "Level 4"]
# Headers - Which Vali you want to be added to the BOM.
Valis = ["Mass", "Cost"]
Textvalis = ["Material", "Part_Number"]
fields = Levels + Valis + Textvalis


# Function that returns the current vali of a given Vali, return empty if the Vali doesn't exist in the current component
def writeField(componentValis, field, property):
	try:
		return [obj for obj in componentValis if obj['shortname']==field][0][property]
	except:
		return ""

# Function that writes each line of the BOM
def writeLine(component_id, currentLevel):
	component = valispace.get("components/"+str(component_id))
	componentValis = valispace.get("valis/?parent="+str(component_id))
	componentTextvalis = getTextValis(component_id)
	row = {}
	
	if currentLevel <= len(Levels):
		row[Levels[currentLevel-1]]= component["name"]

	for field in Valis:
		row[field] = writeField(componentValis, field, "value")
	
	for field in Textvalis:
		row[field] = writeField(componentTextvalis, field, "text")

	writer.writerow(row)
	currentLevel += 1

def getTextValis(component_id):
	textvalis = valispace.get('textvalis/?clean_text=text')
	componentTextvalis = []
	for textvali in textvalis:
		if textvali['parent'] == component_id:
			componentTextvalis.append(textvali)
	return componentTextvalis


# Recursive function the goes into every child element of the given component.
def getChildAndWriteLine(parent_id, currentLevel):
	currentLevel += 1
	children_list = valispace.get("components/?parent="+str(parent_id))
	
	for child in children_list:
		writeLine(child["id"], currentLevel)
		if child["children"] != []:
			getChildAndWriteLine(child["id"], currentLevel)



with open(fileName, mode='w', encoding='utf-8-sig') as file:
	currentLevel = 1
	writer = csv.DictWriter(file, fieldnames=fields, lineterminator = '\n')
	writer.writeheader()
	
	for component in MainComponents:
		writeLine(component, currentLevel)
		getChildAndWriteLine(component, currentLevel)
	
	print('Export Finished.')



