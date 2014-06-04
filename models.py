from google.appengine.ext import ndb
from google.appengine.api.memcache import Client
import logging

dumbmemcache = Client()


class Post(ndb.Model):
    title = ndb.StringProperty()
    media_url = ndb.StringProperty()
    likes = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_comments(self):
        return Comment.query(Comment.post == self.key)

    def comment_count(self):
        count = dumbmemcache.get('{}_comment_count'.format(self.key.id()))
        if not count:
            count = self.get_comments().count()
            dumbmemcache.set('{}_comment_count', count)
        return count

    def get_absolute_url(self):
        return "/post/" + str(self.key.id())

    @classmethod
    def _post_delete_hook(cls, key, future):
        comment_keys = Comment.query(Comment.post == key).fetch(keys_only=True)
        ndb.delete_multi_async(comment_keys)
        logging.info("deleted {} comments for post {}".format(len(comment_keys), key.id()))


class Comment(ndb.Model):
    post = ndb.KeyProperty(required=True)
    text = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def _pre_put_hook(self):
        dumbmemcache.delete('{}_comment_count'.format(self.post.id()))


