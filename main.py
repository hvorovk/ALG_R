#!/usr/bin/python3
import random
from PIL import Image
import argparse
from time import time
from ImageFilters import GausianBlur
from ImageFilters import ContrastAdjustment
from ImageFilters import Operators
from ImageFilters import MosaicPy
from ImageFilters import GammaCorrection
from ImageFilters import ContrastAdjustment
from ImageFilters import BrightnessAdjustment
from ImageFilters import Solarisation


def main():
    parser = argparse.ArgumentParser(description='-m=[gauss|gamma|mosaic|solar|contrast|sobel|prewitt|scharr|bright]\n' +
                                                 '-if=[inputfile] is required,-of=[outputfile], -show for show image')
    
    parser.add_argument('-m', '-method', action='store', dest='method', default='mosaic')
    parser.add_argument('-if', '-inputfile', action='store', dest='input_file')
    parser.add_argument('-of', '-outputfile', action='store', dest='output_file')
    parser.add_argument('-s', '-show', action='store_true', dest='show')
    
    parsed = parser.parse_args()
    method = parsed.method
    if not (parsed.input_file is None):
        if method == 'mosaic':
            mosaic = MosaicPy(15)
            t = time()
            output = mosaic.make_mosaic(parsed.input_file)
            print("Time: " + str(time()-t))
        elif method == 'gauss':
            gauss = GausianBlur()
            temp = int(input("Input sigma: "))
            t = time()
            output = gauss.gauss_blur(parsed.input_file, temp)
            print("Time: " + str(time()-t))
        elif method == 'gamma':
            gamma = GammaCorrection(parsed.input_file)
            temp = float(input("Input gamma: "))
            t = time()
            output = gamma.performAdjustment(temp)
            print("Time: " + str(time()-t))
        elif method == 'solar':
            solar = Solarisation(parsed.input_file)
            temp = int(input("Input intensity: "))
            t = time()
            output = solar.solarise(temp)
            print("Time: " + str(time()-t))
        elif method == 'contrast':
            contrast = ContrastAdjustment(parsed.input_file)
            temp = float(input("Input contrast: "))
            t = time()
            output = contrast.performAdjustment(temp)
            print("Time: " + str(time()-t))
        elif method == 'sobel':
            operator = Operators()
            t = time()
            output = operator.make_sobel(parsed.input_file)
            print("Time: " + str(time()-t))
        elif method == 'prewitt':
            operator = Operators()
            t = time()
            output = operator.make_prewitt(parsed.input_file)
            print("Time: " + str(time()-t))
        elif method == 'scharr':
            operator = Operators()
            t = time()
            output = operator.make_scharr(parsed.input_file)
            print("Time: " + str(time()-t))
        elif method == 'bright':
            bright = BrightnessAdjustment(parsed.input_file)
            temp = float(input("Input brightness: "))
            t = time()
            output = bright.performAdjustment(temp)
            print("Time: " + str(time()-t))
        else:
            print("-h for help.")
            return
    else:
        print("-h for help.")
        return
    
    if not (parsed.output_file is None):
        output.save(parsed.output_file)
    
    if parsed.show:
        output.show()


if __name__ == "__main__":
    main()
