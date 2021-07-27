import valispace
import xlsxwriter

# TODO: Option to make verification methods muli-line?

# START OF CONFIG -------------------------------------
deployment_name = ""

fileName = "" 

# Project ID
project_ID = 
# Specification ID
# If you want to export all Specifications on that project, use 0 as the ID
specification_ID = 

# Target File - Add or remove any field you want to get exported.
fields = ['identifier', "title", "text", "specification", "rationale", "state", "type", "parents", "children", 'verification method', 'components','closeout reference', 'status','verification comment', 'verified on', 'verified by']


standardSeparator = ', '
verificationMethodSeparator = "\n"
componentsSeparator = ', '

orderReqsBy = 'identifier'

# END OF CONFIG -------------------------------------

# Connect to Valispace
valispace = valispace.API(url='https://'+deployment_name+'.valispace.com')

# Set up Excel Config
workbook = xlsxwriter.Workbook(fileName+'.xlsx')
worksheet = workbook.add_worksheet()
cell_format = workbook.add_format()
cell_format.set_text_wrap()


# Get Complete List of Requirements with VM - The specification will be filtered in the for loop
requirementList = valispace.get("requirements/complete/?project="+str(project_ID)+"&clean_text=text,comment")
requirementList = sorted(requirementList, key = lambda i: i[orderReqsBy])

idMappingName = {}
fileList = None

if 'attachments' in fields:
	# Get Complete List of Files
	fileList = valispace.get('files/?project='+str(project_ID))
	idMappingName['attachments'] = fileList
if 'state' in fields:
	# Get States
	stateList = valispace.get('requirements/states/?project='+str(project_ID))
	idMappingName['state'] = stateList
if 'tags' in fields:
	# Get States
	tagsList = valispace.get('tags/?project='+str(project_ID))
	idMappingName['tags'] = tagsList
if 'type' in fields:	
	# Get Types
	typeList = valispace.get('requirements/types/?project='+str(project_ID))
	idMappingName['type'] = typeList
if 'specification' in fields:	
	# Get Types
	specificationList = valispace.get('requirements/specifications/?project='+str(project_ID))
	idMappingName['specification'] = specificationList
if 'section' in fields:	
	# Get Types
	sectionList = valispace.get('requirements/groups/?project='+str(project_ID))
	idMappingName['group'] = sectionList
if 'compliance' or 'custom compliance' in fields:	
	# Get Types
	complianceList = valispace.get('requirements/compliance-statements/?project='+str(project_ID))
	idMappingName['compliance'] = complianceList
if 'components' in fields:
	# Get Types
	componentsList = valispace.get('components/?project='+str(project_ID))
	idMappingName['components'] = componentsList
if 'closeout reference' in fields:
	if fileList is None: fileList = valispace.get('files/?project='+str(project_ID))
	analysisList = valispace.get('analyses/?project='+str(project_ID))
	testList = valispace.get('testing/test-procedures/?project='+str(project_ID))
	testStepsList = valispace.get('testing/test-procedure-steps/?project='+str(project_ID))
if 'owner' in fields or 'verified by' in fields:
	userList = valispace.get('user')
	idMappingName['users'] = userList
# Generate Req Mapping - id to identifier
# reqMapping = {}
# for req in requirementList:
# 	reqMapping[req["id"]] = req["identifier"]

# Generate Req Mapping - id to identifier
# filesMapping = {}
# for file in filesList:
# 	# Object Id of a File represents the parent to which the file is attached to
# 	if file["file_type"] == 1 or file["file_type"] == 2:
# 		if file["object_id"] not in filesMapping:
# 			filesMapping[file["object_id"]] = [file["download_url"]]
# 		else:
# 			filesMapping[file["object_id"]].append(file["download_url"])
# 	# Reference Link to another file
# 	if file["file_type"] == 3:
# 		download_url = [obj for obj in filesList if obj['id']==file["reference_file"]][0]['download_url']
# 		if file["object_id"] not in filesMapping:
# 			filesMapping[file["object_id"]] = [download_url]
# 		else:
# 			filesMapping[file["object_id"]].append(download_url)

col = 0
for field in fields:
	worksheet.write(0, col, field, cell_format)
	col += 1


if 'rationale' in fields:
	fields[fields.index('rationale')] = 'comment'
if 'section' in fields:
	fields[fields.index('section')] = 'group'
if 'compliance' in fields:
	fields[fields.index('compliance')] = 'compliance_statement'
if 'compliance comment' in fields:
	fields[fields.index('compliance comment')] = 'compliance_comment'
if 'verified on' in fields:
	fields[fields.index('verified on')] = 'verified_on'





directMappingFields = ['id','identifier', 'title', 'text', 'comment', 'position', 'created', 'updated', 'compliance_statement','compliance_comment']
directMultipleMappingFields = ['tags']
idMappingFields = ['specification', 'group', 'type', 'state', ]
idMultipleMappingFields = ['parents', 'children']

def main():
	col = 0
	row_num = 1
	for req in requirementList:
		row = dict.fromkeys(fields, "")
		
		if req["specification"] == specification_ID or specification_ID==0 :

			for field in fields:
				if field in directMappingFields: 
					row[field] = req[field]
					
				elif field in idMappingFields and req[field] != None: 
					row[field] = next((object_['name'] for object_ in idMappingName[field] if object_['id'] == req[field]), "")
				elif field in idMultipleMappingFields:
					output = ""
					itemList = req[field]
					for item in itemList:
						if output != "" : output += standardSeparator
						if field in ['parents', 'children']:
							output += next((object_['identifier'] for object_ in requirementList if object_['id'] == item), "") 
					row[field] = output

				elif field in directMultipleMappingFields:
					output = ""
					itemList = req[field]
					for item in itemList:
						if output != "" : output += standardSeparator
						output += item
					row[field] = output
					
				elif field == 'owner' and req['owner'] != None:
					user= next((object_ for object_ in idMappingName['users'] if object_['id'] == req['owner']['id']), "")
					if user != '':
						if user['first_name'] == '':
							row['owner'] += user['username']
						else:
							row['owner'] += user['first_name'] + ' ' + user['last_name']
					
				elif field == '#verified methods':
					row['#verified methods'] = "{:s}/{:s}".format(str(req['verified_items']),str(req['total_items']))
				elif field == '#verified children':
					row['#verified children'] = "{:s}/{:s}".format(str(req['verified_children']),str(req['total_children']))

				elif field == "verification method":
					for verification in req["verification_methods"]:
						if verification["method"] == None:
							if row["verification method"] != "" : row["verification method"] += verificationMethodSeparator
							row["verification method"] +=  "Method Not Defined"
						else:
							if row["verification method"] != "" : row["verification method"] += verificationMethodSeparator
							row["verification method"] +=  verification["method"]["name"]
						
						if 'components' in fields:
							if row["components"] != "": row["components"] += verificationMethodSeparator
							if 'closeout reference' in fields and row["closeout reference"] != "" : row["closeout reference"] += verificationMethodSeparator
							if 'verified by' in fields and row["verified by"] != "" : row["verified by"] += verificationMethodSeparator

							for componentVM in verification["component_vms"]:
								if row["components"] != "" and not row["components"].endswith('\n'): row["components"] += componentsSeparator
								row["components"] +=  next((object_['name'] for object_ in componentsList if object_['id'] == componentVM["component"]), "") 

								if 'closeout reference' in fields:
									if verification["method"] != None and verification["method"]["name"] == "Rules":
										if row["closeout reference"] != "" and not row["closeout reference"].endswith('\n'): row["closeout reference"] += componentsSeparator
										row["closeout reference"] += "Rules"	
									else:							
										contentType = componentVM['content_type']
										if row["closeout reference"] != "" and not row["closeout reference"].endswith('\n'): row["closeout reference"] += componentsSeparator
										
										if componentVM['content_type'] == 171: # File
											row["closeout reference"] += next((object_['name'] for object_ in fileList if object_['id'] == componentVM['object_id']), "") 
										elif componentVM['content_type'] == 248: # Test
											testStep = next((testStep for testStep in testStepsList if testStep['id'] == componentVM['object_id']), "") 
											testProcedure = next((testProcedure for testProcedure in testList if testProcedure['id'] == testStep['test_procedure']), "") 
											row["closeout reference"] += "{:s}: {:s}".format(testStep['title'], testProcedure['name'])
										elif componentVM['content_type'] == 82: # Analysis
											row["closeout reference"] += next((object_['name'] for object_ in analysisList if object_['id'] == componentVM['object_id']), "") 

										
										# row["closeout reference"] = componentVM['object_id']
								if 'verified by' in fields:
									user = next((object_ for object_ in userList if object_['id'] == componentVM["verified_by"]), "") 
									if row["verified by"] != "" and not row["verified by"].endswith('\n'): row["verified by"] += componentsSeparator
									if user != '':
										if user['first_name'] == '':
											row['verified by'] += user['username']
										else:
											row['verified by'] += user['first_name'] + ' ' + user['last_name']


							if 'status' in fields:
								row["status"] = VMComponentPropertiesDirect(componentVM, row['status'], 'status', "-")
						
							if 'verification comment' in fields:
								row["verification comment"] = VMComponentPropertiesDirect(componentVM, row['verification comment'], 'comment', "")
							
							if 'custom compliance' in fields:
								row["custom compliance"] = VMComponentPropertiesID(componentVM, row['custom compliance'], 'custom_compliance_statement', complianceList, "")
							if 'custom compliance comment' in fields:
								row["custom compliance comment"] = VMComponentPropertiesDirect(componentVM, row['custom compliance comment'], 'custom_compliance_comment', "")
							if 'verification tags' in fields:
								if row["verification tags"] != "": row["verification tags"] += verificationMethodSeparator
								output = ""
								tagsList = componentVM['tags']
								for item in tagsList:
									if output != "" : output += standardSeparator
									output += item
								row["verification tags"] += output


				
			for field in fields:
				worksheet.write(row_num, fields.index(field), row[field], cell_format)

			# # Add File URL if there is any file attached to this requirement
			# if req["id"] in filesMapping:
			# 	for file in filesMapping[req["id"]]:
			# 		if row["attachments"] != "" : row["attachments"] += "\n"
			# 		row["attachments"] += file



			# col = 0
			# for field in fields:	
			# worksheet.write(row_num, col, row[field], cell_format)
			# 	col += 1
			
			row_num += 1

	workbook.close()

def VMComponentPropertiesDirect(componentVM, row, field, empty):
	if row != "": row += verificationMethodSeparator
	if componentVM[field] != None:
		row += componentVM[field]
	else:
		row += empty
	return row

def VMComponentPropertiesID(componentVM, row, field, list, empty):
	if row != "": row += verificationMethodSeparator
	if componentVM[field] != None:
		object_ = next((object_ for object_ in list if object_['id'] == componentVM[field]), "") 
		row += object_['name']
	else:
		row += empty
	return row


main()
