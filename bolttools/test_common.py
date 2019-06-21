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

import common
import yaml
import unittest
from errors import *

class TestLinks(unittest.TestCase):
    def test_limit(self):
        a = common.Links(2)
        a.add_link("a",1)
        a.add_link("a",2)
        self.assertRaises(LimitExceededError,lambda: a.add_link("a",3))

    def test_errors(self):
        a = common.Links()
        a.add_link("a",1)
        self.assertRaises(ValueError,lambda: a.add_link("b",1))

    def test_accessors(self):
        a = common.Links()
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

class TestBipartiteLinks(unittest.TestCase):
    def test_errors(self):
        a = common.BipartiteLinks()
        a.add_link("a",1)

        self.assertRaises(ValueError,lambda: a.add_link(1,2))
        self.assertRaises(ValueError,lambda: a.add_link(2,"a"))

    def test_accessors(self):
        a = common.BipartiteLinks()
        a.add_link("a",1)
        a.add_link("a",2)
        a.add_link("b",1)
        a.add_link("c",2)

        self.assertEqual(set(a.get_dsts("a")),set([1,2]))
        self.assertEqual(set(a.get_dsts("b")),set([1]))

        self.assertEqual(set(a.get_srcs(1)),set(["a","b"]))
        self.assertEqual(set(a.get_srcs(2)),set(["a","c"]))

class TestBijectiveLinks(unittest.TestCase):
    def test_errors(self):
        a = common.BijectiveLinks()
        a.add_link("a",1)

        self.assertRaises(ValueError,lambda: a.add_link(1,2))
        self.assertRaises(ValueError,lambda: a.add_link(2,"a"))
        self.assertRaises(ValueError,lambda: a.add_link("a",3))
        self.assertRaises(ValueError,lambda: a.add_link(4,1))

    def test_accessors(self):
        a = common.BijectiveLinks()
        a.add_link("a",1)
        a.add_link("b",2)
        a.add_link("c",3)

        self.assertEqual(a.get_dst("a"),1)

        self.assertEqual(a.get_src(2),"b")


class TestParseAngled(unittest.TestCase):
    def test_wellformed(self):
        res = common.parse_angled("Johannes Reinhardt <jreinhardt@ist-dein-freund.de>")
        self.assertEqual(res[0],"Johannes Reinhardt")
        self.assertEqual(res[1],"jreinhardt@ist-dein-freund.de")

    def test_garbage(self):
        res = common.parse_angled("Johannes Reinhardt <jreinhardt@ist-dein-freund.de> Garbage")
        self.assertEqual(res[0],"Johannes Reinhardt")
        self.assertEqual(res[1],"jreinhardt@ist-dein-freund.de")

    def test_empty(self):
        res = common.parse_angled("<jreinhardt@ist-dein-freund.de> Garbage")
        self.assertEqual(res[0],"")
        self.assertEqual(res[1],"jreinhardt@ist-dein-freund.de")

class TestCheckSchema(unittest.TestCase):
    def test_wellformed(self):
        res = yaml.load("""
a: 100
b: Eimer
c: 3.4
""")
        common.check_schema(res,"Tests",["a","b"],["c","d"])

    def test_unknown_field(self):
        res = yaml.load("""
a: 100
b: Eimer
c: 3.4
e: foo
""")
        self.assertRaises(UnknownFieldError,lambda: common.check_schema(res,"Tests",["a","b"],["c","d"]))

    def test_missing_field(self):
        res = yaml.load("""
a: 100
c: 3.4
""")
        self.assertRaises(MissingFieldError,lambda: common.check_schema(res,"Tests",["a","b"],["c","d"]))


class TestConvertRawParameters(unittest.TestCase):
    def test_unknown_type(self):
        self.assertRaises(UnknownTypeError, lambda: common.convert_raw_parameter_value("p","Length (km)","4"))

    def test_none(self):
        self.assertIs(common.convert_raw_parameter_value("p","Length (mm)","None"),None)
        self.assertIs(common.convert_raw_parameter_value("p","Number","None"),None)
        self.assertIs(common.convert_raw_parameter_value("p","String","None"),None)
        self.assertIs(common.convert_raw_parameter_value("p","Bool","None"),None)

    def test_number(self):
        self.assertIsInstance(common.convert_raw_parameter_value("p","Number","-0.8"),float)

    def test_length(self):
        self.assertIsInstance(common.convert_raw_parameter_value("p","Length (mm)","3"),float)
        self.assertIsInstance(common.convert_raw_parameter_value("p","Length (in)","0.3"),float)
        self.assertRaises(ValueError, lambda: common.convert_raw_parameter_value("p","Length (mm)","-0.5"))
        self.assertRaises(ValueError, lambda: common.convert_raw_parameter_value("p","Length (in)","-1"))

    def test_angle(self):
        self.assertIsInstance(common.convert_raw_parameter_value("p","Angle (deg)","-240"),float)
        self.assertRaises(ValueError, lambda: common.convert_raw_parameter_value("p","Angle (deg)","-400"))

    def test_bool(self):
        self.assertTrue(common.convert_raw_parameter_value("p","Bool","true"))
        self.assertFalse(common.convert_raw_parameter_value("p","Bool","false"))
        self.assertRaises(ValueError, lambda: common.convert_raw_parameter_value("p","Bool","True"))

class TestSorting(unittest.TestCase):
    def test_numerical(self):
        num = common.Numerical()
        self.assertTrue(num.is_applicable(["M2.4","M9","M4"]))
        self.assertFalse(num.is_applicable(["M2.4","M4","Foo"]))
        self.assertEqual(num.sort(["M2.4","M9","M4"]),["M2.4","M4","M9"])

    def test_Alphabetical(self):
        num = common.Numerical()
        self.assertTrue(num.is_applicable(["M2.4","M9","M4"]))
        self.assertFalse(num.is_applicable(["M2.4","M4","Foo"]))
        self.assertEqual(num.sort(["M2.4","M9","M4"]),["M2.4","M4","M9"])

class TestParameter(unittest.TestCase):

    def test_type(self):
        self.assertRaises(UnknownTypeError,lambda: common.Parameters(yaml.load("""
literal:
  test: 125
types:
  test: Length (nm)
description:
  test: Length for testing
""")))

    def test_missing_type(self):
        self.assertRaises(MissingTypeError,lambda: common.Parameters(yaml.load("""
literal:
  test: 125
free: [inp]
types:
  test: Length (mm)
description:
  test: Length for testing
""")))

    def test_unknown_parameter(self):
        self.assertRaises(UnknownParameterError,lambda: common.Parameters(yaml.load("""
types:
  test: Length (mm)
""")))
        self.assertRaises(UnknownParameterError,lambda: common.Parameters(yaml.load("""
free: [test2]
description:
  test: Test length
types:
  test2: Length (mm)
""")))

    def setUp(self):
        self.params = common.Parameters(yaml.load("""
literal:
  lit: 21
free: [ind,ind2]
tables:
  - index: ind
    columns: [col1]
    data:
      "row1" : [1]
      "row3" : [3]
  - index: ind
    columns: [col2]
    data:
      "row1" : [4]
      "row3" : [2]
      "row2" : [1]
tables2d:
  colindex: ind
  rowindex: ind2
  result: tab
  columns: ["row1","row3","row2"]
  data:
    "foo" : [2.4, 2.5, 2.6]
    "bar" : [1.2, 3.5, 9.9]
types:
  lit: Number
  ind: Table Index
  ind2: Table Index
  col1: Length (mm)
  col2: Length (in)
  tab: Length (mm)
defaults:
  ind: row1
  ind2: foo
description:
  ind: Index 1
  ind2: Index 2
  col1: Column 1
  col2: Column 2
  tab: Table data
"""))

    def test_init(self):
        for p in ['ind','col1','col2','ind2','tab','lit']:
            self.assertIn(p,self.params.parameters)

        for c in ['row1','row3']:
            self.assertIn(c,self.params.choices['ind'])
        self.assertNotIn('row2',self.params.choices['ind'])

        self.assertEqual(self.params.defaults['ind'],'row1')
        self.assertEqual(self.params.defaults['ind2'],'foo')

        self.assertEqual(len(self.params.common),4)

    def test_collect(self):
        res = self.params.collect({'ind' : 'row1', 'ind2' : 'bar'})
        self.assertEqual(res['lit'],21)
        self.assertEqual(res['tab'],1.2)
        self.assertEqual(res['ind'],'row1')
        self.assertEqual(res['ind2'],'bar')
        self.assertEqual(res['col1'],1)
        self.assertEqual(res['col2'],4)

    def test_union(self):
        params2 = common.Parameters(yaml.load("""
literal:
  lit2: 23
free: [barbar]
types:
  lit2: Number
  barbar: String
defaults:
  barbar: Foofoo
"""))
        res = params2.union(self.params)
        self.assertIn('lit', res.parameters)
        self.assertIn('lit2', res.parameters)
        self.assertIn('barbar', res.free)
        self.assertIn('ind', res.free)
        self.assertEqual(len(res.common),1)

class TestTable(unittest.TestCase):
    def test_init(self):
        res = common.Table(yaml.load("""
index: ind
columns: [col1]
data:
  "row1" : [1]
  "row3" : [3]
"""))
        res._normalize_and_check_types({'col1' : 'Number', 'ind' : 'Table Index'})
        self.assertEqual(len(res.data),2)
        self.assertEqual(res.get_values('row1'),{'col1' : 1})

    def test_rows(self):
        res = common.Table(yaml.load("""
index: ind
columns: [col1]
data:
  "row1" : [1]
  "row3" : [3,eimer]
"""))
        self.assertRaises(ValueError,
            lambda: res._normalize_and_check_types({'col1' : 'Number', 'ind' : 'Table Index'}))

class TestTable2D(unittest.TestCase):
    def test_init(self):
        res = common.Table2D(yaml.load("""
colindex: ind
rowindex: ind2
result: tab
columns: ["row1","row3","row2"]
data:
  "foo" : [2.4, 2.5, 2.6]
  "bar" : [1.2, 3.5, 9.9]
"""))
        res._normalize_and_check_types({'tab' : 'Length (mm)', 'ind' : 'Table Index', 'ind2' : 'Table Index'})
        self.assertEqual(res.get_value('bar','row1'),{'tab' : 1.2})

    def test_rows(self):
        res = common.Table2D(yaml.load("""
colindex: ind
rowindex: ind2
result: tab
columns: ["row1","row3","row2"]
data:
  "foo" : [2.4, 2.5, 2.6, 3.9]
  "bar" : [1.2, 3.5, 9.9]
"""))
        self.assertRaises(ValueError,
            lambda: res._normalize_and_check_types({'tab' : 'Length (mm)', 'ind' : 'Table Index', 'ind2' : 'Table Index'}))

class TestIdentifier(unittest.TestCase):
    def test_init(self):
        res = common.Identifier(yaml.load("""
nice: Test Part
"""))
        self.assertEqual(res.nice,'Test Part')
        self.assertEqual(res.safe,'TestPart')

    def test_sanitize(self):
        res = common.Identifier(yaml.load(u"""
nice: Test Part with/Garba%;üe
"""))
        self.assertEqual(res.safe,'TestPartWithgarbae')

    def test_check(self):
        self.assertRaises(ValueError,lambda: common.Identifier(yaml.load(u"""
nice: Test Part with/Garba%;üe
safe: Test Part with/Garba%;üe
""")))
    def test_equality(self):
        res = [common.Identifier(yaml.load("""
nice: Test Part
"""))]
        res.append(common.Identifier({'nice' : 'Test Part', 'safe' : 'Test_Part'}))
        self.assertTrue(res[0] == res[0])
        self.assertFalse(res[0] == res[1])
        self.assertTrue(res[0] != res[1])
        self.assertFalse(res[0] != res[0])

class TestSubstitution(unittest.TestCase):
    def test_init(self):
        res = common.Substitution(yaml.load("""
nice: Test Part %(name)s
"""))
        self.assertEqual(res.get_nice({'name' : 'Foo'}),'Test Part Foo')
        self.assertEqual(res.get_safe({'name' : 'Foo'}),'Test_Part_Foo')

    def test_check(self):
        self.assertRaises(ValueError,lambda: common.Substitution(yaml.load(u"""
nice: Test Part with/Garba%;üe
safe: Test Part with/Garba%;üe
""")))


if __name__ == '__main__':
    unittest.main()
