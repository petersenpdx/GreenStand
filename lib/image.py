import requests
import hashlib
from pprint import pprint
import imagehash
from PIL import Image
import os



class TreeImage:

    IMAGE_DIR = "images"

    def __init__(self, url):
        self.url = url

    def image_path(self):

        fname = self.url.split('/')[-1]

        result = os.path.join(self.IMAGE_DIR, fname)
        return result

    def check_if_new(self):

        fname = self.url.split('/')[-1]

        result = True
        for root, dirs, files in os.walk("./images"):
            if fname in files:
                result = False
        return result



    # Check if url or file in local directory
    def check_path_type(self):

        pathtype = self.url

        result = False
        for root, dirs, files in os.walk("."):
            if pathtype in files:
                pathtype.startswith('http://' or 'https://')
                result = True
            # elif url in files:
            #     url.endswith('.jpg')
            #     result = 'fname'
        return result

    # Check if local file is corrupt
    def check_file_path(self):

        fname = self.url.split('/')[-1]

        result = None
        for root, dirs, files in os.walk("./images"):
            if fname in files:
                try:
                    img = Image.open('./images/' + fname)
                    img.verify()
                except (IOError, SyntaxError) as e:
                    print('Bad Files:', files)
        return result

    def url_content(self):
        result = None
        try:
            result = requests.get(self, allow_redirects=True)
        except Exception as e:
            print("{}".format(e))
        return result


    def hash_image(self):


        BLOCKSIZE = 65536
        m = hashlib.sha1()
        with open(self.image_path(), 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                m.update(buf)
                buf = afile.read(BLOCKSIZE)

        result = None
        try:
            result = m.hexdigest()
        except Exception as e:
            print("{}".format(e))
        return result


    def dhash_image(self):

        result = None
        e = Image.open(self.image_path())
        try:
            result = str(imagehash.average_hash(e))
        except Exception as e:
            print("{}".format(e))
        return result



    def export(self):
        result = {}
        result["hash"] = self.hash_image()
        result["dash"] = self.dhash_image()
        result["new"] = self.check_if_new()
        return result





