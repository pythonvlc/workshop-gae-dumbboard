import logging

from google.appengine.ext.webapp import RequestHandler, WSGIApplication, template
from google.appengine.api import taskqueue

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
            post_key = Post(title=title, media_url=media_url).put()
            taskqueue.add(url='/backburner/download_post_media',
                          params={'post': post_key.urlsafe()})
        self.redirect('/')


class PostHandler(RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        html = render('post.html', {'post': post, 'comments': post.get_comments()})
        self.response.out.write(html)

    def post(self, post_id):
        text = self.request.get('text', '')
        if len(text):
            Comment(text=text, post=ndb.Key(Post, int(post_id))).put()
        self.redirect('/post/' + post_id)


class PostDeleteHandler(RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if post:
            post.key.delete()
            logging.info("Post {} deleted".format(post_id))
        self.redirect('/')


class LikePostHandler(RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if post:
            post.likes += 1
            post.put()
        self.redirect(self.request.referer)


class CommentDeleteHandler(RequestHandler):
    def get(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            post_id = comment.post.id()
            comment.key.delete()
            logging.info("Comment {} deleted".format(comment_id))
            self.redirect('/post/' + str(post_id))
        else:
            self.redirect('/')


app = WSGIApplication([
    ('/hello', MainHandler),
    ('/', HomeHandler),
    ('/post/create', PostCreateHandler),
    ('/post/(?P<post_id>\d+)/delete', PostDeleteHandler),
    (r'/post/(?P<post_id>\d+)', PostHandler),
    (r'/post/(?P<post_id>\d+)/like', LikePostHandler),
    (r'/comment/(?P<comment_id>\d+)/delete', CommentDeleteHandler),
], debug=True)


def render(tmpl_file, values={}):
    path = join(dirname(__file__), 'templates', tmpl_file)
    return template.render(path, values)

