from get_vali import get_vali

def get_value(id=None, name=None):
	# Returns the value of a vali.

	if id is None:
		return get_vali(name=name)["value"]
	else:
		return get_vali(id=id)["value"]