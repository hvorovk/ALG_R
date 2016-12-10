from PIL import Image
import pickle
import random
# import time
from math import sqrt
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

    def set_images(self, images: dict):
        """set_images - method for set source pic for mattrix"""
        self.images = images.copy

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
        # make to save matrix of mid color levels
        matrix_colors = list()
        # first cycle column of table
        for i in range(img_pos[0]):
            # temp list for save row
            row = list()
            # second cycle row of table
            for j in range(img_pos[1]):
                # temp for save mid color level
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

class GausianBlur():

    def __init__(self):
        pass

    def boxes_for_gauss(self, sigma, n):  # standard deviation, number of boxes
        wIdeal = sqrt((12*sigma*sigma/n)+1)  # Ideal averaging filter width
        wl = int(wIdeal)
        if not wl % 2:
            wl -= 1
        wu = wl + 2

        mIdeal = (12 * (sigma ** 2) - n * (wl ** 2) - 4 * n * wl - 3 * n)/(-4 * wl - 4)
        m = int(mIdeal+0.5)
        return [(lambda x: wl if x < m else wu)(i) for i in range(n)]

    def gauss_blur(self, img, sigma):
        if isinstance(img, str):
            img = Image.open(img)
        elif isinstance(img, Image):
            pass
        else:
            return -1

        x, y = img.size
        imgL = img.load()

        imgFlat = []
        for i in range(x):
            for j in range(y):
                imgFlat.append(imgL[i, j])

        r = self.gauss_blur_on_chanel([i[0]for i in imgFlat], y, x, sigma)
        g = self.gauss_blur_on_chanel([i[1]for i in imgFlat], y, x, sigma)
        b = self.gauss_blur_on_chanel([i[2]for i in imgFlat], y, x, sigma)

        out = Image.new("RGB", (x, y))
        
        for i in range(x):
            for j in range(y):
                out.putpixel((i, j), (r[i*y+j], g[i*y+j], b[i*y+j]))
        return out

    def gauss_blur_on_chanel(self, scl, w, h, r):
        bxs = self.boxes_for_gauss(r, 3)
        tcl = self.__box_blur(scl, w, h, (bxs[0]-1)//2)
        scl = self.__box_blur(tcl, w, h, (bxs[1]-1)//2)
        return self.__box_blur(scl, w, h, (bxs[2]-1)//2)

    def __box_blur(self, scl, w, h, r):
        tcl = scl.copy()
        scl = self.__box_blur_h(tcl, scl, w, h, r)
        return self.__box_blur_t(scl, tcl, w, h, r)

    def __box_blur_h(self, scl, tcl, w, h, r):
        iarr = 1 / (r + r + 1)
        for i in range(h):
            ti = i * w
            li = ti
            ri = ti + r
            fv = scl[ti]
            lv = scl[ti + w-1]
            val = (r + 1)*fv
            for j in range(r):
                val += scl[ti + j]
            for j in range(r + 1):
                val += scl[ri] - fv
                ri += 1
                tcl[ti] = int(0.5 + val * iarr)
                ti += 1
            for j in range(r+1, w-r):
                val += scl[ri] - scl[li]
                tcl[ti] = int(0.5 + val * iarr)
                ri += 1
                li += 1
                ti += 1
            for j in range(w-r, w):
                val += lv - scl[li]
                tcl[ti] = int(0.5 + val * iarr)
                li += 1
                ti += 1
        return tcl

    def __box_blur_t(self, scl, tcl, w, h, r):
        iarr = 1 / (r + r + 1)
        for i in range(w):
            ti = i
            li = ti
            ri = ti + r * w
            fv = scl[ti]
            lv = scl[ti + w * (h - 1)]
            val = (r + 1) * fv
            for j in range(r):
                val += scl[ti + j * w]
            for j in range(r+1):
                val += scl[ri] - fv
                tcl[ti] = int(0.5 + val * iarr)
                ri += w
                ti += w
            for j in range(r+1, h-r):
                val += scl[ri] - scl[li]
                tcl[ti] = int(0.5 + val * iarr)
                li += w
                ri += w
                ti += w
            for j in range(h-r, h):
                val += lv - scl[li]
                tcl[ti] = int(0.5 + val * iarr)
                li += w
                ti += w
        return tcl

class Operators():
    def __init__(self):
        pass

    def make_sobel(self, img):
        operators = ([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]],
                    [[1, 2, 1],
                     [0, 0, 0],
                     [-1, -2, -1]])
        return self.__apply(img, operators)

    def make_scharr(self, img):
        operators = ([[3, 10, 3],
                     [0, 0, 0],
                     [-3, -10, -3]],
                    [[3, 0, -3],
                     [10, 0, -10],
                     [3, 0, -3]])
        return self.__apply(img, operators)

    def make_prewitt(self, img):
        operators = ([[-1, 0, 1],
                     [-1, 0, 1],
                     [-1, 0, 1]],
                    [[1, 1, 1],
                     [0, 0, 0],
                     [-1, -1, -1]])
        return self.__apply(img, operators)

    def __apply(self, img, operators):
        if isinstance(img, str):
            img = Image.open(img)
        imgP = img.load()
        size = img.size
        output = Image.new("RGB", size)
        for x in range(size[0]):
            for y in range(size[1]):
                if x == 0 or y == 0 or x == size[0]-1 or y == size[1]-1:
                    aver = 0
                else:
                    sumX, sumY = 0, 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            pix = imgP[x+i,y+j]
                            sr = sum(pix) // 3
                            sumX += sr * operators[0][i+1][j+1]
                            sumY += sr * operators[1][i+1][j+1]
                    aver = int(sqrt(sum((sumX ** 2, sumY ** 2))))
                if aver > 255:
                    aver = 255
                elif aver < 0:
                    aver = 0
                output.putpixel((x,y), (aver, aver , aver))
        return output


class ContrastAdjustment():
    """Class for contrast adjustments of a given picture"""

    def __init__(self, initial_image):
        if isinstance(initial_image, str):
            initial_image = Image.open(initial_image)
        self.x, self.y = initial_image.size
        imgL = initial_image.load()
        self.red = []
        self.green = []
        self.blue = []
        # Set colour channels
        for i in range(self.x):
            for j in range(self.y):
                self.red.append(imgL[i, j][0])
                self.green.append(imgL[i, j][1])
                self.blue.append(imgL[i, j][2])

    
    def __update(self):
        """Update initail image using new colours"""
        final_image = Image.new("RGB", (self.x, self.y))

        for i in range(self.x):
            for j in range(self.y):
                final_image.putpixel(
                    (i, j), 
                    (self.red[i*self.y+j], self.green[i*self.y+j], self.blue[i*self.y+j])
                    )
        return final_image

    def performAdjustment(self, contrast = 0.0):
        """Perform contrast adjustments.

        Arguments: 
        contrast -- the desired level of contrast (default 100.0)
        """
        # Calculate a contrast correction factor
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))

        # Calculate new colours
        for i in range(len(self.red)):
            self.red[i] = self.truncate(factor * (self.red[i] - 128) + 128)
            self.green[i] = self.truncate(factor * (self.green[i] - 128) + 128)
            self.blue[i] = self.truncate(factor * (self.blue[i] - 128) + 128)

        # Return updated image
        return self.__update()

    def truncate(self, value):
        """Truncate a given value"""
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        return int(value)

class BrightnessAdjustment():
    """Class for brightness adjustment of a given picture"""

    def __init__(self, initial_image):
        if isinstance(initial_image, str):
            initial_image = Image.open(initial_image)
        self.x, self.y = initial_image.size
        imgL = initial_image.load()
        self.red = []
        self.green = []
        self.blue = []
        # Set colour channels
        for i in range(self.x):
            for j in range(self.y):
                self.red.append(imgL[i, j][0])
                self.green.append(imgL[i, j][1])
                self.blue.append(imgL[i, j][2])

    
    def __update(self):
        """Update initail image using new colours"""
        final_image = Image.new("RGB", (self.x, self.y))

        for i in range(self.x):
            for j in range(self.y):
                final_image.putpixel(
                    (i, j), 
                    (self.red[i*self.y+j], self.green[i*self.y+j], self.blue[i*self.y+j])
                    )
        return final_image

    def performAdjustment(self, brightness = 0.0):
        """Perform brightness adjustments.

        Arguments: 
        brightness -- the desired level of brightness (default 0.0)
        """

        # Calculate new colours
        for i in range(len(self.red)):
            self.red[i] = self.truncate(self.red[i] + brightness)
            self.green[i] = self.truncate(self.green[i] + brightness)
            self.blue[i] = self.truncate(self.blue[i] + brightness)

        # Return updated image
        return self.__update()

    def truncate(self, value):
        """Truncate a given value"""
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        return int(value)

class GammaCorrection():
    """Class for gamma correction of a given picture"""

    def __init__(self, initial_image):
        if isinstance(initial_image, str):
            initial_image = Image.open(initial_image)
        self.x, self.y = initial_image.size
        imgL = initial_image.load()
        self.red = []
        self.green = []
        self.blue = []
        # Set colour channels
        for i in range(self.x):
            for j in range(self.y):
                self.red.append(imgL[i, j][0])
                self.green.append(imgL[i, j][1])
                self.blue.append(imgL[i, j][2])

    
    def __update(self):
        """Update initail image using new colours"""
        final_image = Image.new("RGB", (self.x, self.y))

        for i in range(self.x):
            for j in range(self.y):
                final_image.putpixel(
                    (i, j), 
                    (self.red[i*self.y+j], self.green[i*self.y+j], self.blue[i*self.y+j])
                    )
        return final_image

    def performAdjustment(self, gamma = 2.0):
        """Perform gamma correction.

        Arguments: 
        gamma -- the desired level of correction (default 2.0)
        """

        gammaCorrection = 1 / gamma

        # Calculate new colours
        for i in range(len(self.red)):
            self.red[i] = int(255 * ((self.red[i] / 255) ** gammaCorrection))
            self.green[i] = int(255 * ((self.green[i] / 255) ** gammaCorrection))
            self.blue[i] = int(255 * ((self.blue[i] / 255) ** gammaCorrection))

        # Return updated image
        return self.__update()

class Solarisation():
    """Class for solarisation of a given picture"""

    def __init__(self, initial_image):
        if isinstance(initial_image, str):
            initial_image = Image.open(initial_image)
        self.x, self.y = initial_image.size
        imgL = initial_image.load()
        self.red = []
        self.green = []
        self.blue = []
        # Set colour channels
        for i in range(self.x):
            for j in range(self.y):
                self.red.append(imgL[i, j][0])
                self.green.append(imgL[i, j][1])
                self.blue.append(imgL[i, j][2])

    
    def __update(self):
        """Update initail image using new colours"""
        final_image = Image.new("RGB", (self.x, self.y))

        for i in range(self.x):
            for j in range(self.y):
                final_image.putpixel(
                    (i, j), 
                    (self.red[i*self.y+j], self.green[i*self.y+j], self.blue[i*self.y+j])
                    )
        return final_image

    def solarise(self, threshold = None):
        """Perform solarisation.

        Arguments: 
        threshold -- the intensity value which signals the filter to inverse the colour
        (if not given, then filter performs the colour inversion for all intensity values)
        """
        if threshold is None:
            for i in range(len(self.red)):
                self.red[i] = 255 - self.red[i]
                self.green[i] = 255 - self.green[i]
                self.blue[i] = 255 - self.blue[i]
        else:
            for i in range(len(self.red)):
                self.red[i] = 255 - self.red[i] if self.red[i] < threshold else self.red[i]
                self.green[i] = 255 - self.green[i] if self.green[i] < threshold else self.green[i]
                self.blue[i] = 255 - self.blue[i] if self.blue[i] < threshold else self.blue[i]

        # Return updated image
        return self.__update()
