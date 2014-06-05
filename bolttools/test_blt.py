# coding=utf8
#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import blt
import yaml
import unittest
from errors import *

class TestLinks(unittest.TestCase):
	def test_limit(self):
		a = blt.Links(2)
		a.add_link("a",1)
		a.add_link("a",2)
		self.assertRaises(LimitExceededError,lambda: a.add_link("a",3))

	def test_errors(self):
		a = blt.Links()
		a.add_link("a",1)
		self.assertRaises(ValueError,lambda: a.add_link("b",1))

	def test_accessors(self):
		a = blt.Links()
		a.add_link("a",1)
		a.add_link("a",2)
		a.add_link("b",3)
		a.add_link("c",4)

		self.assertEqual(set(a.get_dsts("a")),set([1,2]))
		self.assertEqual(set(a.get_dsts("b")),set([3]))

		self.assertEqual(a.get_src(1),"a")
		self.assertEqual(a.get_src(2),"a")
		self.assertEqual(a.get_src(3),"b")
		self.assertEqual(a.get_src(4),"c")

class TestClass(unittest.TestCase):
	def setUp(self):
		self.cl = yaml.load("""
id: roundBattery
names:
  - name:
      safe: roundBattery 
      nice: Round Batteries
    labeling:
      nice: "%(T)s Battery"
    description: Most common round single cell battery sizes
  - name: Common Batteries
    labeling:
      safe: "%(T)s_Battery"
      nice: "%(T)s Battery"
    description: Most common round single cell battery sizes
standards:
  - body: IEC
    standard: IEC 60086
    suffix:
      safe: Cat1
      nice: Category 1
    labeling:
      nice: "IEC60086 Cat 1 Battery %(T)s"
    description: Cylindrical cells with protruding positive and recessed or flat negative terminals.
parameters:
  free: [T]
  defaults: {T: "AAA"}
  types:
    T: Table Index
    h: Length (mm)
    d: Length (mm)
  description:
    T: Type Code
    h: height
    d: diameter
  tables:
     index: T
     columns: [h,d]
     data:
       "AAA" : [44.5,10.5]
       "AA" : [50.5,14.5]
       "C" : [50,26.2]
       "D" : [61.5,34.2]
       "1/2AA" : [24,14.5]
       "AAAA" : [42.5,8.3]
       "A" : [50, 17]
       "N" : [30.2, 12]
       "Sub-C" : [42.9, 22.2]
source: http://en.wikipedia.org/wiki/List_of_battery_sizes
""")

	def test_class(self):
		res = blt.Class(self.cl)
		self.assertEqual(res.source,'http://en.wikipedia.org/wiki/List_of_battery_sizes')
		self.assertEqual(res.id,'roundBattery')

	def test_classname(self):
		res = []
		for cn in self.cl['names']:
			res.append(blt.ClassName(cn,self.cl['id']))

		self.assertEqual(len(res),2)

		#use noop substitution
		self.assertEqual(res[0].labeling.get_safe_name({'T' : '%(T)s'}),'%(T)s_Battery')
		self.assertEqual(res[1].labeling.get_safe_name({'T' : '%(T)s'}),'%(T)s_Battery')

	def test_standardname(self):
		res = []
		for sn in self.cl['standards']:
			res.append(blt.StandardName(sn,self.cl['id']))

		self.assertEqual(len(res),1)
		self.assertEqual(res[0].standard.get_safe_name(),'IEC60086')
		self.assertEqual(res[0].standard.get_nice_name(),'IEC 60086')
		self.assertEqual(res[0].suffix.get_safe_name(),'Cat1')
		self.assertEqual(res[0].suffix.get_nice_name(),'Category 1')

class MockDesignation(blt.DesignationMixin):
	def __init__(self,id,subids=[]):
		self.id = id
		self.subids = subids
	def get_id(self):
		return self.id
	def all_standards_single(self):
		for sid in self.subids:
			yield MockDesignation(sid)
	def all_names_single(self):
		for sid in self.subids:
			yield MockDesignation(sid)
	def contains_standard_single(self,id):
		return id in self.subids
	def contains_name_single(self,id):
		return id in self.subids
	def get_standard_single(self,id):
		if not id in self.subids:
			raise KeyError("Key not found")
		return MockDesignation(id)


class TestContainer(unittest.TestCase):
	def test_permissions(self):
		cnt = blt.ContainerMixin()
		cnt.add_standard_single(MockDesignation("id1"))
		cnt.add_standard_multi(MockDesignation("id2"))
		cnt.add_name_single(MockDesignation("id3"))
		cnt.add_name_group(MockDesignation("id4",["id5"]))

		cnt = blt.ContainerMixin([])
		self.assertRaises(ValueError,lambda: cnt.add_standard_single(MockDesignation("id1")))
		self.assertRaises(ValueError,lambda: cnt.add_standard_multi(MockDesignation("id2")))
		self.assertRaises(ValueError,lambda: cnt.add_name_single(MockDesignation("id3")))
		self.assertRaises(ValueError,lambda: cnt.add_name_group(MockDesignation("id3")))

	def setUp(self):
		self.cnt = blt.ContainerMixin()
		self.cnt.add_name_single(MockDesignation("id1"))
		self.cnt.add_standard_single(MockDesignation("id2"))
		self.cnt.add_name_single(MockDesignation("id3"))
		self.cnt.add_standard_multi(MockDesignation("id4",["id6","id8"]))
		self.cnt.add_name_group(MockDesignation("id7",["id9"]))

	def test_collisions(self):
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_name_single(MockDesignation("id1")))
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_name_group(MockDesignation("id1")))
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_name_group(MockDesignation("id5",["id1"])))
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_standard_single(MockDesignation("id1")))
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_standard_multi(MockDesignation("id1",[])))
		self.assertRaises(MalformedRepositoryError,
				lambda: self.cnt.add_standard_multi(MockDesignation("id5",["id1"])))

	def test_contains(self):
		self.assertTrue(self.cnt.contains_name_single('id3'))
		self.assertFalse(self.cnt.contains_name_single('id5'))

		self.assertTrue(self.cnt.contains_name_group('id7'))
		self.assertFalse(self.cnt.contains_name_group('id6'))
		self.assertFalse(self.cnt.contains_name_group('id5'))

		self.assertTrue(self.cnt.contains_name('id1'))
		self.assertTrue(self.cnt.contains_name('id9'))
		self.assertFalse(self.cnt.contains_name('id5'))
		self.assertFalse(self.cnt.contains_name('id7'))

		self.assertTrue(self.cnt.contains_standard_single('id2'))
		self.assertFalse(self.cnt.contains_standard_single('id3'))

		self.assertTrue(self.cnt.contains_standard_multi('id4'))
		self.assertFalse(self.cnt.contains_standard_multi('id3'))
		self.assertFalse(self.cnt.contains_standard_single('id6'))

		self.assertTrue(self.cnt.contains_standard('id2'))
		self.assertTrue(self.cnt.contains_standard('id6'))
		self.assertFalse(self.cnt.contains_standard('id1'))

		self.assertTrue(self.cnt.contains('id1'))
		self.assertTrue(self.cnt.contains('id2'))
		self.assertTrue(self.cnt.contains('id4'))
		self.assertTrue(self.cnt.contains('id6'))
		self.assertFalse(self.cnt.contains('id5'))

	def test_accessors(self):
		self.cnt.get_name_single('id3')
		self.assertRaises(KeyError, lambda: self.cnt.get_name_single('id5'))

		self.cnt.get_name_group('id7')
		self.assertRaises(KeyError, lambda: self.cnt.get_name_group('id4'))

		self.cnt.get_standard_single('id2')
		self.assertRaises(KeyError, lambda: self.cnt.get_standard_single('id3'))

		self.cnt.get_standard_multi('id4')
		self.assertRaises(KeyError, lambda: self.cnt.get_standard_multi('id3'))
		self.assertRaises(KeyError, lambda: self.cnt.get_standard_single('id6'))

		self.cnt.get_standard('id2')
		self.cnt.get_standard('id6')
		self.assertRaises(KeyError, lambda: self.cnt.get_standard('id1'))

		self.cnt.get('id1')
		self.cnt.get('id2')
		self.cnt.get('id4')
		self.cnt.get('id6')
		self.cnt.get('id7')
		self.cnt.get('id9')
		self.assertRaises(KeyError, lambda: self.cnt.get('id5'))

	def test_iterators(self):
		self.assertEqual(len([i for i in self.cnt.all_names_single()]),2)
		self.assertEqual(len([i for i in self.cnt.all_names_group()]),1)
		self.assertEqual(len([i for i in self.cnt.all_standards_single()]),1)
		self.assertEqual(len([i for i in self.cnt.all_standards_multi()]),1)
		self.assertEqual(len([i for i in self.cnt.all_standards()]),3)


#TODO: slow?
class TestRepository(unittest.TestCase):
	def setUp(self):
		self.repo = blt.Repository("test_blt")

	def test_repository(self):
		self.assertTrue("hexagonthinnut1" in self.repo.classes)
		self.assertTrue('nut' in self.repo.collections)
		self.assertEqual(len(self.repo.classes),11)
		self.assertEqual(len(self.repo.collections),2)

		self.assertEqual(self.repo.get_standard("DIN439_B").replacedby,"ISO4035")

	def test_accessors(self):
		self.assertEqual(len([n for n in self.repo.all_names_single()]),7)
		self.assertEqual(len([n for n in self.repo.all_names_group()]),0)
		self.assertEqual(len([n for n in self.repo.all_standards()]),14)
		self.assertEqual(len([n for n in self.repo.all_standards_multi()]),4)

		self.assertEqual(self.repo.get_class_by_id('hexagonnut2').id,'hexagonnut2')

	def test_ids(self):
		self.repo.contains('DIN933')
		self.repo.contains_standard_single('DIN933')
		self.repo.contains('IEC60086_Cat1')
		self.repo.contains('IEC60086')
		self.repo.contains_standard_multi('IEC60086')

		self.repo.contains('roundBatteries')
		self.repo.contains_name_single('roundBatteries')

	def test_bodies(self):
		self.assertEqual(len(self.repo.standard_bodies),5)
		self.assertTrue('DIN' in self.repo.standard_bodies)


if __name__ == '__main__':
	unittest.main()


