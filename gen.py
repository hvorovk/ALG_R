import json
import requests
import os
import pickle
from PIL import Image
import shutil
import time

import flickrapi


class UploaderImage():
    """
    This class download & resize and dumped in pickle
    format more image
    use:
    some = UploaderImage(path, count, path_to_key, size)
    path - the path to your directory
    count - count of output image
    path_to_key - the path to your api key and secret
                  (it dont save in program)
    size - the size of each out image
    some.upload(tag) - make pickle file which contain dict:
    {tuple(RGB): image_pil...}
    """

    def __init__(self, path="images", count=1000, path_to_key="acces.json", size=50):
        with open(path_to_key) as conf:
            config = json.load(conf)
        self.path = path
        self.api = flickrapi.FlickrAPI(config["api"]["key"], config["api"]["secret"])
        self.size = size
        self.temp = False
        self.count = count

    def change_count(self, count):
        self.count = count

    def change_path(self, path):
        self.path = path

    def change_size(self, size):
        self.size = size

    def upload_img(self, url, title):
        time.sleep(0.06)
        temp = requests.get(url)
        if not self.temp:
            try:
                os.mkdir("temp")
            except OSError:
                self.temp = True
        path = os.path.join("temp/" + title + ".jpg")
        with open(path, "wb") as out:
            out.write(temp.content)
        temp = Image.open(path)
        if temp.mode != "RGB":
            os.remove(path)
            return False
        else:
            return True

    def upload_imgs(self, tag, count=None):
        if count is None:
            count = self.count
        id = 0
        walker = self.api.walk(tag_mode="any", tags=tag)
        for photo in walker:
            if int(photo.get("ispublic")) != 1:
                continue
            if id == count:
                break
            if self.upload_img("https://farm" + str(photo.get("farm")) + ".staticflickr.com/" +
                               str(photo.get("server")) + "/" + str(photo.get("id")) + "_" +
                               str(photo.get("secret")) + ".jpg", str(photo.get("id"))):
                print(str(photo.get("id")))
                id += 1
            else:
                print("Grayscale...remove")

    def dump(self, custom_name=None):
        if custom_name is None:
            custom_name = self.path
        self.data = dict()
        for name in os.listdir(self.path):
            print(os.path.join(self.path, name))
            image = Image.open(os.path.join(self.path, name))
            pixel_map = image.load()
            a = (0, 0, 0)
            for it in range(image.size[0]):
                for jt in range(image.size[0]):
                    a = tuple(map(lambda x, y: x + y, a, pixel_map[it, jt]))
            a = tuple(map(lambda x: int(x / (self.size ** 2)), a))
            self.data[a] = image
        with open(custom_name + '.pickle', 'wb') as f:
            pickle.dump(self.data, f)
        shutil.rmtree(os.path.join(self.path))

    def resize(self, remove=False, size=None):
        if size is not None:
            self.size = size
        image_dir = "temp"
        out_dir = self.path
        try:
            os.mkdir(out_dir)
        except OSError:
            print("Folder exist!")
            raise
        for name in os.listdir(image_dir):
            path = os.path.join(image_dir, name)
            image = Image.open(path)

            # crop image to square (anchor at centre)
            w, h = image.size
            if w != h:
                if w > h:
                    d = float(w - h) / 2
                    box = (d, 0, w - d, h)
                elif h > w:
                    d = float(h - w) / 2
                    box = (0, d, w, h - d)

                box = map(lambda x: int(x), box)
                image = image.crop(box=box)
            # resize
            image = image.resize(size=(self.size, self.size))
            # write image
            image.save(os.path.join(out_dir, name))
        if remove:
            shutil.rmtree(os.path.join(image_dir))

    def upload(self, tag):
        print("Start generating...")
        print("Download...")
        t = time.clock
        self.upload_imgs(tag)
        print("Ends: " + str(int(time.clock - t)))
        print("Resize...")
        t = time.clock
        self.resize()
        print("Ends: " + str(int(time.clock - t)))
        print("Dump...")
        t = time.clock
        self.dump()
        print("Ends: " + str(int(time.clock - t)))

if __name__ == "__main__":
    alpha = UploaderImage()
    alpha.change_size(15)
    alpha.resize()
    alpha.dump("new")
    # alpha.upload(input("Please enter tag for search:"))
