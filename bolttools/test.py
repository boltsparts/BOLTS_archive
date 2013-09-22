import blt_parser
import openscad
import freecad
import unittest
from errors import *

class TestRepositoryLoad(unittest.TestCase):

	def test_nonexistant(self):
		self.assertRaises(MalformedRepositoryError, lambda:
			blt_parser.BOLTSRepository("test_repos/does_not_exist")
		)

	def test_empty(self):
		self.assertRaises(MalformedRepositoryError, lambda:
			blt_parser.BOLTSRepository("test_repos/empty")
		)

	def test_no_collections(self):
		repo = blt_parser.BOLTSRepository("test_repos/no_collections")
		self.assertEqual(repo.collections,[])

	def test_slash(self):
		repo = blt_parser.BOLTSRepository("test_repos/no_collections/")
		self.assertEqual(repo.collections,[])

	def test_no_drawings(self):
		self.assertRaises(MalformedRepositoryError, lambda:
				blt_parser.BOLTSRepository("test_repos/no_drawings/")
		)

	def test_small(self):
		repo = blt_parser.BOLTSRepository("test_repos/small")


class TestCollectionLoad(unittest.TestCase):

	def test_empty(self):
		self.assertRaises(MalformedCollectionError, lambda:
			blt_parser.BOLTSCollection("test_collections/empty.blt")
		)

	def test_wrong_version(self):
		self.assertRaises(VersionError, lambda:
			blt_parser.BOLTSCollection("test_collections/wrong_version.blt")
		)

	def test_no_classes(self):
		self.assertRaises(MissingFieldError, lambda:
			blt_parser.BOLTSCollection("test_collections/no_classes.blt")
		)

	def test_empty_classes(self):
		self.assertRaises(MalformedCollectionError, lambda:
			blt_parser.BOLTSCollection("test_collections/empty_classes.blt")
		)

	def test_minimal_class(self):
		coll = blt_parser.BOLTSCollection("test_collections/minimal_class.blt")
		self.assertEqual(coll.author_names,["Johannes Reinhardt"])
		self.assertEqual(coll.author_mails,["jreinhardt@ist-dein-freund.de"])
		self.assertEqual(coll.license_name,"CC-BY-SA")
		self.assertEqual(coll.license_url,"http://creativecommons.org/licenses/by-sa/3.0/")

		cl = coll.classes[0]
		self.assertEqual(cl.naming.template,"Partname")
		self.assertEqual(cl.source,"Invented for testpurposes")
		self.assertEqual(cl.parameters.free,[])

	def test_parameters(self):
		coll = blt_parser.BOLTSCollection("test_collections/parameters.blt")

		cl = coll.classes[0]
		self.assertEqual(cl.parameters.free,['key','l'])
		self.assertEqual(cl.parameters.free,['key','l'])
		self.assertEqual(type(cl.parameters.tables[0].data['M2.5'][2]),float)
		params = cl.parameters.collect({'key' : 'M2.5', 'l' : 37.4})
		self.assertEqual(params['s'],12.0)

	def test_naming_error(self):
		#wrong name for substitute field
		self.assertRaises(UnknownFieldError, lambda:
			blt_parser.BOLTSCollection("test_collections/naming.blt")
		)

	def test_type_error1(self):
		#additional parameter name in types
		self.assertRaises(ValueError, lambda:
			blt_parser.BOLTSCollection("test_collections/type_error1.blt")
		)
	def test_type_error2(self):
		#unknown type in types
		self.assertRaises(ValueError, lambda:
			blt_parser.BOLTSCollection("test_collections/type_error2.blt")
		)

	def test_table_error(self):
		#negative value for parameter of type length
		self.assertRaises(ValueError, lambda:
			blt_parser.BOLTSCollection("test_collections/table_error1.blt")
		)
		#negative value for parameter of type number
		blt_parser.BOLTSCollection("test_collections/table_error2.blt")

class TestOpenSCADGeneration(unittest.TestCase):
	def test_data_init(self):
		repo = blt_parser.BOLTSRepository("test_repos/small")
		self.assertEqual(len(repo.openscad.getbase),4)
		openscad.OpenSCADExporter().write_output(repo)

	def test_multi_table(self):
		repo = blt_parser.BOLTSRepository("test_repos/multi_table")
		self.assertEqual(len(repo.openscad.getbase),4)
		openscad.OpenSCADExporter().write_output(repo)

class TestFreeCADGeneration(unittest.TestCase):
	def test_data_init(self):
		scad = freecad.FreeCADData("test_repos/small")



if __name__ == '__main__':
	unittest.main()


