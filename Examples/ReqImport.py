import valispace
import csv, json


deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")


## Add File path e.g. - Make sure you use /, not \, to divide folders
csvFilePath = ".../file.csv"
# Id of the specification the requirements should added to
specification_ID = 0


def import_req(csvFilePath, specification_ID):
        with open(csvFilePath, encoding="utf8") as csvFile:
                csvReader = csv.DictReader(csvFile)
                for rows in csvReader:
                        req = {
                                "specification": specification_ID,
                                "identifier" : rows['ID'],
                                "title" :  rows['Name'],
                                "text" : rows['Description']
                                }
                        requirementPosted = valispace.post('requirements/', req)



import_req(csvFilePath, specification_ID)