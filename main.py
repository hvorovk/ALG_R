# import sys
# import os
# import time
import random
# from multiprocessing import Pool
from PIL import Image
from ImageFilters import GausianBlur
from ImageFilters import ContrastAdjustment


# def doit(inp):
#     return magic.make_mosaic("noelsematters", magic.load_image(inp))


# def split4(inp):
#     a = Image.open(inp)
#     x, y = a.size
#     block = 10
#     x, y = x-(x % block**2), y-(y % block**2)
#     images = []
#     boxes = [(0, 0, int(x/2), int(y/2)), (int(x/2), 0, x, int(y/2)),
#              (0, int(y/2), int(x/2), y), (int(x/2), int(y/2), x, y)]
#     for i in boxes:
#         temp = Image.new("RGB", (int(x/2), int(y/2)))
#         temp.paste(a.crop(i), boxes[0])
#         images.append(temp)
#     return images


# def merge4(mass):
#     x, y = (i*2 for i in mass[0].size)
#     boxes = [(0, 0, int(x/2), int(y/2)), (int(x/2), 0, x, int(y/2)),
#              (0, int(y/2), int(x/2), y), (int(x/2), int(y/2), x, y)]
#     out = Image.new("RGB", (x, y))
#     for i in range(4):
#         out.paste(mass[i], boxes[i])
#     return out


if __name__ == "__main__":
    gausian = GausianBlur()
    img = Image.open("temp.jpg")
    img.show()
    x, y = img.size
    imgL = img.load()
    imgFlat = []
    for i in range(x):
        for j in range(y):
            imgFlat.append(imgL[i, j])
    r = [i[0]for i in imgFlat]
    g = [i[1]for i in imgFlat]
    b = [i[2]for i in imgFlat]
    r = gausian.gaussBlur_4(r, x, y, 3)
    g = gausian.gaussBlur_4(g, x, y, 3)
    b = gausian.gaussBlur_4(b, x, y, 3)
    out = Image.new("RGB", img.size)
    for i in range(x):
        for j in range(y):
            out.putpixel((i, j), (r[i*x+j], g[i*x+j], b[i*x+j]))
    out.show()



    # KIRILL KIRILL KIRILL KIRILL KIRILL

    # Open an image using PIL
    image_to_process = Image.open("batman.jpg")

    contrast = ContrastAdjustment(image_to_process)

    # Perform contrast correction, 
    # argument - the desired level of contrast (0 by default)
    corrected_img = contrast.performAdjustment(150)
    corrected_img.show()


    # lenght = len(sys.argv)
    # magic = MosaicPy.ImageMatrix(10)
    # multi = False
    # if lenght >= 4 and sys.argv[3] == 'm':
    #     pool = Pool(4)
    #     multi = True
    # if lenght == 1:
    #     pass
    # elif lenght >= 2:
    #     try:
    #         if not os.path.exists(sys.argv[1]):
    #             raise OSError
    #     except OSError:
    #         print(sys.argv[1] + " not found!")
    #     out_image = sys.argv[2] if lenght >= 3 else input("Please enter out image name:")
    #     if lenght == 5:
    #         try:
    #             if not os.path.exists(sys.argv[4]):
    #                 raise OSError
    #         except OSError:
    #             print(sys.argv[4] + " not found!")
    #         magic.load_images(sys.argv[4])
    #     else:
    #         magic.load_images()
    #     print("Start processing:")
    #     t = time.time()
    #     if multi:
    #         img = pool.map(doit, split4(sys.argv[1]))
    #         merge4(img).save(out_image)
    #     else:
    #         img = Image.open(sys.argv[1])
    #         doit(img).save(out_image)
    #     print("successfully completed in: " + str(int(time.time()-t)))
