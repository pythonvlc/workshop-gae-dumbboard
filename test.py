import unittest

from google.appengine.ext import testbed

from models import Post


class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_post_create(self):
        url = 'http://3.bp.blogspot.com/-shlkF4-lOrI/UqEk25whCBI/AAAAAAAAAV4/vAwo6UN2Sis/s1600/appengine_final.png'
        post_key = Post(title='el viejo logo de GAE',
                        media_url = url).put()
        self.assertEqual(1, Post.query().count(), 'wrong post count')
        self.assertEqual(0, post_key.get().get_comments().count(), 'wrong comment count')
        self.assertEqual(1, 0, '1 is not 0? oh wait, wrong test')


if __name__ == '__main__':
    unittest.main()