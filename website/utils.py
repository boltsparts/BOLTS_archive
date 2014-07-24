from bolttools.common import UNITS

def tables2d_as_dicts(params):
	"""
	Convert the 2D tables of a Parameters instance into a form suitable for the html_table Jinja Filter

	Returns a list of dicts
	"""
	res = []
	for table in params.tables2d:
		result = None
		if params.types[table.result] in UNITS:
			result = "%s (%s)" % (table.result,UNITS[params.types[table.result]])
		else:
			result = table.result
		res.append({
			"data" : [table.data[i] for i in params.choices[table.rowindex]],
			"corner" : result,
			"col_header" : table.columns,
			"row_header" : params.choices[table.rowindex]
		})
	return res


def tables_as_dicts(params):
	"""
	Convert the tables of a Parameters instanceinto a form suitable for the html_table Jinja Filter

	Returns a list of dicts
	"""
	res = []
	for table in params.tables:
		header = [str(table.index)]
		for p in table.columns:
			if params.types[p] in UNITS:
				header.append("%s (%s)" % (str(p), UNITS[params.types[p]]))
			else:
				header.append("%s" % str(p))
		res.append({
			"data" : [[idx] + table.data[idx] for idx in params.choices[table.index]],
			"header" : header,
		})
	return res

