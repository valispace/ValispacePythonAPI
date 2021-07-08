# This script allows you to import all your requirements from an csv file including all the Parent/Child relationship
# To import it to valispace, you just need one end of the relationship, either the Parents pointing to the Children, or the Children pointing to the Parents
# The csv file must have headers and you need to adtapt the code to the respective headers it has.

import valispace
import csv, json


deployment = input("Deployment Name:")
valispace = valispace.API(deployment=deployment)


## Add File path e.g. - Make sure you use /, not \, to divide folders
csvFilePath = ".../RequirementsFile.csv"

# Id of the specification the requirements will be added to
specification_ID = 33933

# How are the Parent/Children are separated in the csv. E.g.: Children: "Req-005, Req-006"; the separator is ","
separator = ","

# Variable that holds a mapping from the Requirement Identifier to the object ID in Valispace.
ReqMapping = {}

def import_req(csvFilePath, specification_ID):
        
        # First run populates Valispace with all requirements, withouth relationship
        with open(csvFilePath, encoding="utf8") as csvFile:
                csvReader = csv.DictReader(csvFile)
                for rows in csvReader:
                        req = {
                                "specification": specification_ID,
                                "identifier" : rows['IDENTIFIER'], # Replace 'IDENTIFIER' with the header title you have on the file where you have the Identifiers
                                "title" :  rows['TITLE'], # Optional: Replace 'TITLE' with the header title you have on the file where you have the Req. Title
                                "text" : rows['TEXT'] # Replace 'TEXT' with the header title you have on the file where you have the Req. Text
                                }
                        requirementPosted = valispace.post('requirements/', req)
                        ReqMapping[req["identifier"]] = requirementPosted["id"]

        # Second run populates all the relationship - Populating from the Parents to the child
        
        # If you would like to use a column that defines the parents only, change the child filds
        # ToDo: Write a Function for either Parents or Child.

        with open(csvFilePath, encoding="utf8") as csvFile:
                csvReader = csv.DictReader(csvFile)
                for rows in csvReader:
                        currentReqId = ReqMapping[rows['IDENTIFIER']]
                        if rows['CHILDREN'] != "":
                                children = rows['CHILDREN'].split(separator)  # Replace 'CHILDREN' with the header title you have on the file where you have the children of the requirement
                                for child in children:
                                        childId = ReqMapping[child.lstrip()]
                                        valispace.request('PUT', 'requirements/'+str(currentReqId)+'/add-child/', {"child": childId})




import_req(csvFilePath, specification_ID)