# function [ Matrix, MatrixNames, MatrixValiIDs ] = ValispaceGetMatrix(id)
# % ValispaceGetMatrix() returns a Matlab Matrix with the values, one with
# % the names and one with the ValiIDs
#     global ValispaceLogin
#     global ValiList
    
#     if (length(ValispaceLogin)==0) 
#         error('VALISPACE-ERROR: You first have to run ValispaceInit()');
#     end
    
  

#     url = ValispaceLogin.url + "matrix/" + id + "/";
#     MatrixData = webread(url, ValispaceLogin.options);
  
#     Matrix = [];
#     MatrixNames = string([]); % create empty string array
    
#     for column = 1:MatrixData.number_of_columns
#        for row = 1:MatrixData.number_of_rows
#            Vali = ValispaceGetVali(MatrixData.cells(row,column));
#            Matrix(row,column) = Vali.value;
#            MatrixNames(row,column) = Vali.name;
#            MatrixValiIDs(row,column) = Vali.id;
#        end
#     end
    
# end

from lib import *
from helpers import name_to_id
from get_vali import get_vali

def get_matrix(id):
	# Checks Authentication
	if not hasattr(globals, 'valispace_login'):
		print 'VALISPACE-ERROR: You first have to run valispace.init()'
		return
		
	url = globals.valispace_login['url'] + "matrix/" + str(id) + "/"
	headers = globals.valispace_login['options']['Headers']
	
	matrix_data = requests.get(url, headers=headers).json()
	matrix = []

	for row in range(matrix_data['number_of_rows']):
		matrix.append([])
		for col in range(matrix_data['number_of_columns']):
			matrix[row].append(get_vali(matrix_data['cells'][row][col]))

	return matrix