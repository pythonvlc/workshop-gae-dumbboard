#!/usr/bin/python
import optparse
import sys
import unittest
from StringIO import StringIO

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def run_from_gae():
    suite = unittest.loader.TestLoader().discover('.')
    s = StringIO()
    unittest.TextTestRunner(verbosity=2, stream=s).run(suite)
    s.seek(0)
    result = s.read()
    s.close()
    return result


def run_from_shell(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print 'Error: Exactly 2 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    run_from_shell(SDK_PATH, TEST_PATH)