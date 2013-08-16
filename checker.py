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
				if rows[j][i] == "None":
					continue
				current_value = float(rows[j][i])

				if direction is None and not last_value is None:
					#positive if ascending, negative if descending
					direction = current_value - last_value

				elif (not direction is None) and direction*current_value < direction*last_value:
					self.error(msg % j,blt["collection"],part)

				last_value = float(rows[j][i])


files = listdir('blt')

checker = TableChecker()
for file in files:
	if file[-4:] == ".blt":
		coll = load_collection(file)
		checker.add_collection(coll)

checker.check()
