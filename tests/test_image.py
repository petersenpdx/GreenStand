from lib.image import TreeImage
from PIL import Image
import hashlib
import PIL
import imagehash


def test_check_image_exist():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert myimage.check_if_new() == False

    print(myimage.image_path())

    non_existent  = TreeImage('https://nothing.com/nothing')

    assert non_existent.check_if_new() == True

def test_ckeck_path_type():

    pathtype = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert pathtype.check_path_type() == False

    jpeg = TreeImage('2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert jpeg.check_if_new() == False

def test_check_image_corrupt():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert myimage.check_file_path() == None


def test_url_content():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert myimage.url_content() == None

def test_hash_image():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert myimage.hash_image() != None

def test_dhash_image():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    assert myimage.dhash_image() != None

def test_resize_image():

    myimage = TreeImage('https://treetracker-dev.nyc3.digitaloceanspaces.com/2018.06.14.19.40.59_1d3caa37-f8fa-49ee-a7bd-41f3cbe450c7_IMG_20180614_121404_811444820.jpg')

    mywidth = 483

    img = Image.open(myimage.image_path())
    wpercent = (mywidth/float(img.size[0]))
    hsize = int(float(img.size[1])*float(wpercent))
    img = img.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
    img.save('resized-test-image.jpeg')


    BLOCKSIZE = 65536
    m = hashlib.sha1()
    with open('resized-test-image.jpeg', 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            m.update(buf)
            buf = afile.read(BLOCKSIZE)
            hash_result = m.hexdigest()

    assert hash_result != myimage.hash_image()

    e = Image.open('resized-test-image.jpeg')
    dhash_result = str(imagehash.average_hash(e))

    assert dhash_result == myimage.dhash_image()