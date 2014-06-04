import logging

from google.appengine.ext.webapp import RequestHandler, WSGIApplication, template
from os.path import join, dirname
from models import Post


class MainHandler(RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class HomeHandler(RequestHandler):
    def get(self):
        posts = Post.query().order(-Post.date).fetch(10)
        logging.info("HomeHandler - sirviendo {} posts".format(len(posts)))
        html = render('home.html', {'posts': posts})
        self.response.write(html)


class PostCreate(RequestHandler):
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


app = WSGIApplication([
    ('/hello', MainHandler),
    ('/', HomeHandler),
    ('/post/create', PostCreate)
], debug=True)


def render(tmpl_file, values={}):
    path = join(dirname(__file__), 'templates', tmpl_file)
    return template.render(path, values)

