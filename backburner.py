import logging

from google.appengine.api import urlfetch, files
from google.appengine.api.images import Image, JPEG, get_serving_url
from google.appengine.ext.webapp import RequestHandler, WSGIApplication
from google.appengine.ext.ndb import Key


class MediaDownloader(RequestHandler):
    def get(self):
        self.response.out.write("No, yo no sirvo para peticiones get")

    def post(self):
        # Upload as a blob
        post_safekey = self.request.get('post')
        logging.info("Downloading media from post url")
        post = Key(urlsafe=post_safekey).get()
        if post:
            result = urlfetch.fetch(post.media_url)
            if result.status_code == 200:

                post.media_url = store_picture_from_content(result.content, result.headers['content-type'])
                post.put()
                logging.info("Post media uploaded to url {}".format(post.media_url))
            else:
                logging.error("Error downloading {} - {}".format(post.media_url, result.status_code))

        else:
            logging.info("Post not found: {}".format(post_safekey))


def store_picture_from_content(content, mime_type='application/octet-stream'):
    img = Image(content)
    img.resize(width=800, height=800)
    img.im_feeling_lucky()
    img = img.execute_transforms(output_encoding=JPEG)

    # create file
    file_name = files.blobstore.create(mime_type=mime_type)
    with files.open(file_name, 'a') as f:
        f.write(img)

    # Finalize the file
    files.finalize(file_name)

    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(file_name)
    return get_serving_url(blob_key)


app = WSGIApplication([
        ('/backburner/download_post_media', MediaDownloader),
], debug=True)