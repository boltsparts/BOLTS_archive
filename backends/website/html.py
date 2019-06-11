from jinja2 import Markup
import sys
if sys.version_info.major >= 3:
	unicode = str

def table(value):
	"""
	processes a dictionary into a html table, similar to the functionality in html.py

	the dictionary can contain the following keys

	data - a list of lists with the content of the table
	class - a string to be used as html class attribute for the table
	header - a list of column headers (optional)
	row_classes - a list of html class attributes for the rows of the table (optional)
	"""
	table_data = value["data"]
	header = None
	if "header" in value:
		header = value["header"]
	cl = ""
	if "class" in value:
		cl = value["class"]

	row_classes = [None]*len(table_data)
	if "row_classes" in value:
		row_classes = value["row_classes"]

	res = []
	if not cl == "":
		res.append('<table class="%s">' % cl)
	else:
		res.append('<table>')

	if header is not None:
		row = " ".join([u"<th>%s</th>" % unicode(head) for head in header])
		res.append(u"<tr>%s<tr>" % row)

	for row_data,row_class in zip(table_data,row_classes):
		row = " ".join([u"<td>%s</td>" % unicode(datum) for datum in row_data])
		if row_class is None:
			res.append(u"<tr>%s</tr>" % row)
		else:
			res.append(u"<tr class='%s'>%s</tr>" % (row_class,row))
	res.append("</table>")
	return Markup(u"\n".join(res))

def table2d(value):
	"""
	processes a dictionary into a html table, similar to the functionality in html.py

	the dictionary can contain the following keys

	data - a list of lists with the content of the table
	class - a string to be used as html class attribute for the table
	corner - string for the corner cell
	col_header - a list of column headers
	row_header - a list of row headers
	"""
	table_data = value["data"]
	corner = value["corner"]
	col_header = value["col_header"]
	row_header = value["row_header"]

	res = ['<table class="%s">' % value["class"]]
	row = " ".join([u"<th>%s</th>" % unicode(head) for head in col_header])
	res.append(u"<tr><td>%s</td>%s<tr>" % (corner,row))
	for row_data,header in zip(table_data,row_header):
		row = " ".join([u"<td>%s</td>" % unicode(datum) for datum in row_data])
		res.append(u"<tr><th>%s</th>%s</tr>" % (header,row))
	res.append("</table>")
	return Markup(u"\n".join(res))

def properties(value):
	"""
	processes a list of tuples into a html table
	"""
	res = ['<table class="table">']
	for prop,val in value:
		res.append("<tr><th><strong>%s:</strong></th><td>%s</td></tr>" % (prop,val))
	res.append("</table>")
	return Markup(u"\n".join(res))

def a(content,**kwargs):
	return u"<a %s>%s</a>" % (" ".join('%s="%s"' % kv for kv in kwargs.items()),content)

def img(**kwargs):
	return u"<img %s>" % (" ".join('%s="%s"' % kv for kv in kwargs.items()))
