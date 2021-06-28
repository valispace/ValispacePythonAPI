import valispace

deployment = input("Deployment Name:")
valispace = valispace.API(url="https://"+deployment+".valispace.com/")


Matrix = {
	"name": "MatrixName5",
	"number_of_columns": 2,
	"number_of_rows": 2,
	"parent": , # ID of Parent Component
	"unit": "kg" # Change the base unit for the matrix
}
posted_matrix = valispace.post("matrices/", Matrix)
matrix_id = posted_matrix["id"]

MatrixValues = [[1, 2], [3, 4]]
for row in posted_matrix["cells"]:
	for cell in row:

		Vali = {
		"shortname": "vali_"+str(cell),
		"formula": MatrixValues[posted_matrix["cells"].index(row)][row.index(cell)],
		"parent": matrix_id
		}

		patched_vali = valispace.request("patch", "valis/"+str(cell)+"/", Vali)
