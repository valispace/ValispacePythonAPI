from valispace_sdk import ValispaceAPI

api = ValispaceAPI()

# valis = api.pull()
# print valis["2112"]
# print api.get_vali(2112)
# print api.get_vali(id=2112)
# print api.get_vali(name="Frontend.Cost.HIGH_PRECISION")
# print api.get_value(id=2112)
# print api.get_value(name="Frontend.Cost.HIGH_PRECISION")

# matrix = api.get_matrix(443)
# for row in matrix:
# 	print "**************************************************"
# 	for cell in row:
# 		print "--------------------------------------------------"
# 		print cell["value"]
# 		print "--------------------------------------------------"
# 	print "**************************************************"

# api.update_vali(id=2112, formula="1.2")
# api.update_vali(id=2112, formula="3.1")
# api.update_vali(id=2112, fields={"name": "4"})
# api.update_vali(id=2112, fields={"blabla": "4"})
# api.update_vali(id=2112, fields={"formula": "1.1"})
# api.update_vali(id=2112, fields={"name": "test name"})

# matrix_orig = [[2.1], [0.0], [0.0]]
# matrix_new  = [[3.3], [1.1], [0.6]]
# api.update_matrix_formulas(443, matrix_orig)

