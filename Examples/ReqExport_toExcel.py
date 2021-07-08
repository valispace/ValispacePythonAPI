import valispace
import xlsxwriter


username = ""
password = ""
deployment_name = ""

valispace = valispace.API(deployment="demo" username=username, password=password)


workbook = xlsxwriter.Workbook('OutputFilename.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format()
cell_format.set_text_wrap()


# Project ID
project_ID = 
# Specification ID
# If you want to export all Specifications on that project, use 0 as the ID
specification_ID = 0

# Get Complete List of Requirements with VM - The specification will be filtered in the for loop
requirementList = valispace.get("requirements/complete/?project="+str(project_ID)+"&clean_text=text,comment")
# Get Complete List of Files
filesList = valispace.get("files/?project="+str(project_ID))

# Generate Req Mapping - id to identifier
reqMapping = {}
for req in requirementList:
	reqMapping[req["id"]] = req["identifier"]

# Generate Req Mapping - id to identifier
filesMapping = {}
for file in filesList:
	# Object Id of a File represents the parent to which the file is attached to
	if file["file_type"] == 1 or file["file_type"] == 2:
		if file["object_id"] not in filesMapping:
			filesMapping[file["object_id"]] = [file["download_url"]]
		else:
			filesMapping[file["object_id"]].append(file["download_url"])
	# Reference Link to another file
	if file["file_type"] == 3:
		download_url = [obj for obj in filesList if obj['id']==file["reference_file"]][0]['download_url']
		if file["object_id"] not in filesMapping:
			filesMapping[file["object_id"]] = [download_url]
		else:
			filesMapping[file["object_id"]].append(download_url)

states = valispace.get('requirements/states')

# Target File
fields = ["identifier", "title", "text", "specification", "rationale", "state", "parent", "children", "verification method", "components", "status", "attachments"]

col = 0
for field in fields:
	worksheet.write(0, col, field, cell_format)
	col += 1


row_num = 1


for req in requirementList:
	row = dict.fromkeys(fields, "")

	if req["specification"] == specification_ID or specification_ID==0 :
		row["title"] = req["title"]
		row["identifier"] = req["identifier"]
		row["text"] = req["text"]
		row["specification"] = valispace.get("requirements/specifications/"+str(req["specification"]))["name"]
		row["state"] = next((state['name'] for state in states if state['id'] == req["state"]), "")

		if req["comment"] != None:
			row["rationale"] = req["comment"]

		# Add File URL if there is any file attached to this requirement
		if req["id"] in filesMapping:
			for file in filesMapping[req["id"]]:
				if row["attachments"] != "" : row["attachments"] += "\n"
				row["attachments"] += file

		for child in req["children"]:
			try:
				if row["children"] != "" : row["children"] += "\n"
				row["children"] += "" + reqMapping[child]
			except:
				print("Error finding child with id: ", child)
		for parent in req["parents"]:
			try:
				if row["parent"] != "" : row["parent"] += "\n"
				row["parent"] += "" + reqMapping[parent]
			except:
				print("Error finding parent with id: ", parent)

		for verification in req["verification_methods"]:
			for componentVM in verification["component_vms"]:				

				if verification["method"] == None:
					if row["verification method"] != "" : row["verification method"] += "\n"
					row["verification method"] +=  "Method Not Defined"
				else:
					if row["verification method"] != "" : row["verification method"] += "\n"
					row["verification method"] +=  verification["method"]["name"]

				if row["components"] != "" : row["components"] += "\n"
				row["components"] +=  valispace.get("components/"+str(componentVM["component"]))["name"]

				if row["status"] != "" : row["status"] += "\n"
				if componentVM["status"] != None:
					row["status"] += componentVM["status"]
				else:
					row["status"] += "No Status"

		col = 0
		for field in fields:	
			worksheet.write(row_num, col, row[field], cell_format)
			col += 1
		
		row_num += 1
			
workbook.close()