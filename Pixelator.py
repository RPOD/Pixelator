# -*- coding: utf-8 -*-
"""
Pixelator tool, main module:

This program is a simple tool to make any picture look pixelated.
You will be asked 4 prompts upon start:
    - image name (must be the same folder or total path must be given)
    - the pixel size, this declares how pixelated the picture will look in the end
    - it calculates the mean color of a cluster the size of the pixelsize²
    - the output name of the file (keep in mind every picture will be saved in PNG)
    - scale (if you do not wish an up or downscale just type in 100)

Author: R.P.O.D.

Version: 0.3
"""

from PIL import Image
import math


class Pixelator:

    def __init__(self, filename, pixelSize, outputName, scale):
        self.filename = filename
        self.pixelSize = pixelSize
        self.outputName = outputName
        self.scale = scale

    def readImage(self):
        image = Image.open(self.filename)
        return image

    def meanPixel(self, tile):
        rt = 0
        gt = 0
        bt = 0
        for pixel in tile:
            r, g, b = pixel
            rt = rt + r
            gt = gt + g
            bt = bt + b
        mean = [math.floor(rt / len(tile)), math.floor(gt / len(tile)), math.floor(bt / len(tile))]
        return mean

    def pixelate(self, image):
        width, height = image.size
        image = image.convert('RGB')
        hr = math.ceil(height / int(self.pixelSize))
        wr = math.ceil(width / int(self.pixelSize))
        tiles = [[[]for i in range(hr)]for j in range(wr)]
        for x in range(width):
            for y in range(height):
                tiles[math.floor(x / self.pixelSize)][math.floor(y / self.pixelSize)].append(image.getpixel((x, y)))
        meanArray = [([0] * hr)for k in range(wr)]
        for metaX in range(wr):
            for metaY in range(hr):
                meanArray[metaX][metaY] = self.meanPixel(tiles[metaX][metaY])
        pixelData = image.load()
        for x in range(width):
            for y in range(height):
                r = meanArray[math.floor(x / self.pixelSize)][math.floor(y / self.pixelSize)][0]
                g = meanArray[math.floor(x / self.pixelSize)][math.floor(y / self.pixelSize)][1]
                b = meanArray[math.floor(x / self.pixelSize)][math.floor(y / self.pixelSize)][2]
                pixelData[x, y] = (r, g, b)
        if (not self.scale == 100):
            image = image.resize((int(width * self.scale / 100), int(height * self.scale / 100)), Image.ANTIALIAS)
        image.save(self.outputName, 'PNG')


def main():
    px = Pixelator(input('Insert the filename: '), int(input('Set the Pixelsize: ')), input('Insert the output name: '), int(input('Set scale (in percent): ')))
    px.pixelate(px.readImage())

if __name__ == '__main__':                # call if module is called as main
    main()