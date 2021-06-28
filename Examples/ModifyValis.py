import valispace

deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")

# The ID of the Vali that you want to modify
vali_id = 

# New value you want to update the Vali with.
newValue = 

# Function to get Vali by the fullname
Vali = valispace.get_vali(vali_id)

print("The Vali found is named: "+ str(Vali["name"]))
print("The old value was "+ str(Vali["formula"])+" "+str(Vali["unit"])+". The new value of the Vali will be "+str(newValue)+" "+str(Vali["unit"]))

# This request function is sending a web request to the server to change the formula of the identified vali with the new value you determine
valispace.request("patch", "valis/"+str(Vali["id"])+"/", data={"formula":newValue})

