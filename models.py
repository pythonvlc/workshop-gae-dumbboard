from google.appengine.ext import ndb


class Post(ndb.Model):
    title = ndb.StringProperty()
    media_url = ndb.StringProperty()
    likes = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)



