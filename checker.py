from os import listdir
from blt_parser import load_collection
import numpy as np

class TableChecker:
	def __init__(self):
		self.blts = []
		self.errors = 0

	def error(self,msg,coll,part):
		print "%s coll: %s standard: %s" % (msg,coll["name"],str(part["standard"])) 

	def add_collection(self,blt):
		self.blts.append(blt)

	def check(self):
		for blt in self.blts:
			for part in blt["parts"]:
				if not "table" in part.keys():
					continue
				table = part["table"]
				self._check_row_length(blt,part,table)
				self._check_monotonicity(blt,part,table)
				self._check_order_of_magnitude(blt,part,table)
				self._check_positivity(blt,part,table)

	def _check_row_length(self,blt,part,table):
		msg = "Inconsistent row sizes in row: %s"
		row_length = len(table["columns"])
		for key in table["data"].keys():
			if len(table["data"][key]) != row_length:
				error(msg % key,blt["collection"],part)

	def _check_monotonicity(self,blt,part,table):
		msg = "Non-monotonuous entries in row: %s"
		rows = [list(row[1]) for row in sorted(table["data"].iteritems(),key=lambda x: float(x[0][1:]))]
		n = len(rows)
		m = len(rows[0])

		for i in range(1,m):
			direction = None
			last_value = None
			for j in range(1,n):
				if rows[j][i] is None:
					continue
				current_value = rows[j][i]

				if direction is None and not last_value is None:
					#positive if ascending, negative if descending
					direction = current_value - last_value

				elif (not direction is None) and direction*current_value < direction*last_value:
					self.error(msg % j,blt["collection"],part)

				last_value = rows[j][i]

	def _check_order_of_magnitude(self,blt,part,table):
		msg = "Unusually magnitude for entry in row: %s"
		rows = [list(row[1]) for row in sorted(table["data"].iteritems(),key=lambda x: float(x[0][1:]))]
		n = len(rows)
		m = len(rows[0])

		for i in range(1,m):
			last_value = None
			for j in range(1,n):
				if rows[j][i] is None:
					last_value = None
					continue
				elif not last_value is None:
					ratio = rows[j][i]/last_value
					#threshholds are arbitrary, but small enough to catch shifted decimal points
					if ratio > 7.5 or 40*ratio < 3.:
						self.error(msg % j, blt["collection"],part)
				last_value = rows[j][i]

	def _check_positivity(self,blt,part,table):
		msg = "Negative entry in row: %s"
		rows = [list(row[1]) for row in sorted(table["data"].iteritems(),key=lambda x: float(x[0][1:]))]
		n = len(rows)
		m = len(rows[0])

		for i in range(1,m):
			for j in range(1,n):
				if rows[j][i] is None:
					continue
				if rows[j][i] < 0:
					self.error(msg % j, blt["collection"],part)

class CollectionChecker:
	#List of accepted licenses
	licenses = {
		"CC-BY-NC-SA" : "http://creativecommons.org/licenses/by-nc-sa/3.0/",
		"CC-BY-SA" : "http://creativecommons.org/licenses/by-sa/3.0/"
	}
	def __init__(self):
		self.blts = []
		self.errors = 0

	def error(self,msg,coll):
		print "%s coll: %s" % (msg,coll["name"])

	def add_collection(self,blt):
		self.blts.append(blt)

	def check(self):
		for blt in self.blts:
			self._check_license(blt)
			self._check_author(blt)

	def _check_license(self,blt):
		license = blt["collection"]["license"]
		name, url = (part.strip("> ") for part in license.split("<"))
		if not name in self.licenses.keys():
			self.error("Unknown license: %s" % name,blt["collection"])
		elif self.licenses[name] != url:
			self.error("Wrong url for license %s: %s" % (name,url),blt["collection"])

	def _check_author(self,blt):
		author = blt["collection"]["author"]
		name, email = (part.strip("> ") for part in author.split("<"))
		#very rough check
		if not "@" in email:
			self.error("Invalid mail address in author: %s" % author, blt["collection"])


files = listdir('blt')

checkers = [TableChecker(),CollectionChecker()]

for file in files:
	if file[-4:] == ".blt":
		coll = load_collection(file)
		for checker in checkers:
			checker.add_collection(coll)

for checker in checkers:
	checker.check()
