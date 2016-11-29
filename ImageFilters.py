from PIL import Image
import pickle
import random
# import sys


class MosaicPy():
    def __init__(self, size, images="base.pickle"):
        """Init: size - size of blocks, images - path to your source img"""
        self.size_block = size
        self.images = None
        self.load_images(images)

    def distance(self, a, b):
        """Calculate Manhatten distance from a to b"""
        dist = 0
        for i in range(0, len(a)):
            dist += abs(a[i] - b[i])
        return dist

    def change_size(self, size_new):
        """Change size of block"""
        self.size = size_new

    def load_images(self, file="base.pickle"):
        """load_images - method for load source pic for mattrix"""
        with open(file, "rb") as file:
            self.images = pickle.load(file)

    def __load_image(self, img):
        """
        private method for load and calc color level for each block
        img - input image is PIL format or str
        func return - list[i][j] i,j - column and row of color level image contain
        mid value of each block
        """
        if isinstance(img, str):
            img = Image.open(img)
        # calc amount of row and column of table mid color level
        img_pos = tuple(map(lambda x: x // self.size_block, img.size))
        # load image in format which provide pixel access
        pixel_map = img.load()
        # make var to save matrix of mid color levels
        matrix_colors = list()
        # first cycle column of table
        for i in range(img_pos[0]):
            # temp list for save row
            row = list()
            # second cycle row of table
            for j in range(img_pos[1]):
                # temp var for save mid color level
                mid_color = (0, 0, 0)
                # third cycle column of block
                for it in range(self.size_block):
                    # fourth cycle row of block
                    for jt in range(self.size_block):
                        # sum all color levels termwise
                        mid_color = tuple(map(lambda x, y: x + y,
                                              mid_color,
                                              pixel_map[i * self.size_block + it, j * self.size_block + jt]))
                # calc mid value of color levels
                mid_color = tuple(map(lambda x: x // (self.size_block ** 2), mid_color))
                # add block in row
                row.append(mid_color)
            # add row in mattrix
            matrix_colors.append(row)
        # return mattrix
        return matrix_colors

    def make_mosaic(self, input_image):
        """
        public function for make mosaic from input_image
        input_image is str or PIL.Image
        return - PIL.Image
        """
        # load matrix
        matrix_colors = self.__load_image(input_image)
        # count on vertical and horizontal blocks
        x, y = len(matrix_colors), len(matrix_colors[0])
        # new image for output
        new_image = Image.new("RGB", (x * self.size_block, y * self.size_block))
        # traversal on horizontal
        for i in range(x):
            # traversal on vertical
            for j in range(y):
                # search dist to that block
                find = {self.distance(matrix_colors[i][j], x): x for x in self.images.keys()}
                # sort on dist
                a = sorted(find)
                # paste random pic in block
                new_image.paste(self.images[find[random.choice(a[0:20])]],
                                (i * self.size_block, j * self.size_block,
                                i * self.size_block + self.size_block,
                                j * self.size_block + self.size_block))
        # return this pic
        return new_image
