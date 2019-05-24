"""This script will run all tests in order.
   Run the following command:
      python .\run_all_tests.py
"""

import unittest

from test_batch_call import TestStringMethods as BatchMethods
from test_create_sandbox import TestStringMethods as SandboxMethods
from test_read_attributes import TestStringMethods as ReadMethods
from test_write_attributes import TestStringMethods as WriteMethods

suite = unittest.TestSuite()
suite.addTest(SandboxMethods('test_createdatabase'))
suite.addTest(SandboxMethods('test_createcategory'))
suite.addTest(SandboxMethods('test_createtemplate'))
suite.addTest(SandboxMethods('test_createelement'))

suite.addTest(WriteMethods('test_writesinglevalue'))
suite.addTest(WriteMethods('test_writedataset'))
suite.addTest(WriteMethods('test_updateattributevalue'))

suite.addTest(ReadMethods('test_readattributesnapshot'))
suite.addTest(ReadMethods('test_readattributestream'))
suite.addTest(ReadMethods('test_readattributeselectedfields'))

suite.addTest(BatchMethods('test_dobatchcall'))

suite.addTest(SandboxMethods('test_deleteelement'))
suite.addTest(SandboxMethods('test_deletetemplate'))
suite.addTest(SandboxMethods('test_deletecategory'))
suite.addTest(SandboxMethods('test_deletedatabase'))

unittest.TextTestRunner(verbosity=2).run(suite)
