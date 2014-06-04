from google.appengine.ext import ndb


class Post(ndb.Model):
    title = ndb.StringProperty()
    media_url = ndb.StringProperty()
    likes = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_comments(self):
        return Comment.query(Comment.post == self.key)

    def comment_count(self):
        return self.get_comments().count()

    def get_absolute_url(self):
        return "/post/" + str(self.key.id())


class Comment(ndb.Model):
    post = ndb.KeyProperty()
    text = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
