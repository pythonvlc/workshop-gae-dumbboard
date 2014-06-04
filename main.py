import logging

from google.appengine.ext.webapp import RequestHandler, WSGIApplication, template
from os.path import join, dirname
from models import Post, ndb, Comment


class MainHandler(RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class HomeHandler(RequestHandler):
    def get(self):
        posts = Post.query().order(-Post.date).fetch()
        logging.info("HomeHandler - sirviendo {} posts".format(len(posts)))
        html = render('home.html', {'posts': posts})
        self.response.write(html)


class PostCreateHandler(RequestHandler):
    def get(self):
        html = render('post_create.html')
        self.response.write(html)

    def post(self):
        # manualmente? pues si
        title = self.request.get('title')
        media_url = self.request.get('media_url')
        if title and media_url:
            Post(title=title, media_url=media_url).put()
        self.redirect('/')


class PostHandler(RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        html = render('post.html', {'post': post})
        self.response.out.write(html)

    def post(self, post_id):
        text = self.request.get('text', '')
        if len(text):
            Comment(text=text, post=ndb.Key(Post, int(post_id))).put()
        self.redirect('/post/' + post_id)


class LikePostHandler(RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if post:
            post.likes += 1
            post.put()
        self.redirect(self.request.referer)


app = WSGIApplication([
    ('/hello', MainHandler),
    ('/', HomeHandler),
    ('/post/create', PostCreateHandler),
    (r'/post/(?P<post_id>\d+)', PostHandler),
    (r'/post/(?P<post_id>\d+)/like', LikePostHandler),
], debug=True)


def render(tmpl_file, values={}):
    path = join(dirname(__file__), 'templates', tmpl_file)
    return template.render(path, values)

