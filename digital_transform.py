# -*- coding: utf-8 -*-	
#  This is a simple code to transform coordinates vector on a digital image coordinates system on a milimetric coordinate system
#  with origin at the centre of the image.
#  The mathematical model is apresented by Daniel Rodrigues dos Santos on this material: https://docs.ufpr.br/~danielsantos/FotoII-capII_A5.pdf
#  Code written by Natália Carvalho de Amorim - Universidade Federal do Paraná

import cv2 as cv

img = cv.imread('img.png'); #You must give the path of your image

rows, columms, bands = img.shape #The method shape return the dimensions of the image, but here the bands are not interesting

print("The image size: ")
print(img.shape)

pixel_size_x = float(input("Inform the pixel size (mm) on x axis: ")) #Ask the user the pixel size in milimeters
pixel_size_y = float(input("Inform the pixel size (mm) on y axis: ")) #Ask the user the pixel size in milimeters

C = float(input("Inform the columm coordinate to transform: "))
L = float(input("Inform the row coordinate to transform: "))

x = pixel_size_x * (C - ((columms-1)/2)) #calculate the x coordinate
y = -pixel_size_y * (L - ((rows-1)/2)) #calculate the y coordinate

print("The transformed coordinates: ")
print(x, y)



