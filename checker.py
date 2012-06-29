from os import listdir
from blt_parser import load_collection

class TableChecker:
	def __init__(self):
		self.blts = []
		self.errors = 0

	def error(self,msg,coll,part):
		print "%s coll %s stand %s" % (msg,coll["name"],str(part["standard"])) 

	def add_collection(self,blt):
		self.blts.append(blt)

	def check(self):
		for blt in self.blts:
			for part in blt["parts"]:
				if not "table" in part.keys():
					continue
				table = part["table"]

				#Check row length
				msg = "Inconsistent row sizes in row: %s"
				row_length = len(table["columns"])
				for key in table["data"].keys():
					if len(table["data"][key]) != row_length:
						error(msg % key,blt["collection"]["name"],part)


files = listdir('blt')

checker = TableChecker()
for file in files:
	if file[-4:] == ".blt":
		coll = load_collection(file)
		checker.add_collection(coll)

checker.check()
