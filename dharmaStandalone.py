#!/usr/bin/python3

import sys
import argparse
import shutil
import PIL as p
import math
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
from random import randint, uniform, choice

parser = argparse.ArgumentParser(description='A commandline tool to generate mandalas utilising random numbers.  It has the capacity to use multiple input source images, and output multiple mandalas to a specified width in pixels.')
parser.add_argument('-d', type=str, default='./', help='The directory that contains source images. (Defaults to current directory)')
parser.add_argument('-q', type=int, default=5, help='The quantity of mandalas requested for each source image. (Defaults to 5)')
parser.add_argument('-s', type=int, default=2000, help='The horizontal size in pixels requested for each mandala.  (Defaults to 2000)')
args=parser.parse_args()

#set variables
direct = './' + args.d
quantity = args.q
origOutputwidth = args.s

regularImage = False
saturateImage = False
contrastImage = False
satcontImage = True

if not os.path.isdir(direct):
	print(direct + ' does not exist')
	exit()

#create list of .jpg in specified directory
listOfImages = []
for file in os.listdir(direct):
	if file.endswith('.jpg'):
		listOfImages.append(file)


def buildMandalas(img, currentDir):


	def generateCoords(img, quantity):
		#im - image to be processed
		#outputwidth - minimum width in pixels of finished mandala
		#quantity - how many tuples to be created
		#returns - list of x,y coords that will be within the bounds of the source image

		coordsList = []

		for i in range(0, quantity):

			stx = 0
			sty = 0
			enx = 9999
			eny = 9999
			
			while enx > img.size[0] or eny > img.size[1]:

				stx = randint(0, img.size[0] - (math.floor(outputWidth / 2)))
				sty = stx
				enx = stx + (math.floor(outputWidth / 2))
				eny = enx


			#if there is remainder the cropping algorithm will be out by a few pixels, this just ensures it returns an integer
			if ((enx + stx) % 2 == 1):
				stx = stx + 1
				print('Decrimented end point of xy axis')

			coordsList.append((stx, sty, enx, eny))

		return(coordsList)


	def createWedge(angle, stx, sty, enx, eny):
		#creates a fragment using the verified x/y coordinates
		#returns a cropped image containing the fragment

		mask = Image.new("L", img.size, 0)

		draw = ImageDraw.Draw(mask)

		draw.pieslice([stx, sty, enx, eny], 270, 270 + angle, fill='white')

	    #create wedge fragment
		frag = img.copy()

		frag.putalpha(mask)
		frag = frag.crop(((enx + stx) / 2, sty, enx, (eny + stx) / 2))
		print('frag x' + str(frag.size[0]))
		return frag


	def construct(frag, angle):
		#build the mandala using supplied angle of the fragment

		def deg225ToDeg45(frag):
		#take 22.5 deg wedge, mirror it to make it 45 degrees
		#returns 45 deg frag

			output = Image.new('RGBA', (frag.size[1] - 1, frag.size[1] - 1))
			xpaste = 0
			ypaste = 0

			#paste 25.5 deg frag to output canvas
			output.paste(frag, (xpaste, ypaste), frag)

			#flip and rotate frag to create a 45 deg frag 
			frag = frag.transpose(method=Image.FLIP_TOP_BOTTOM).rotate(90)
			frag = frag.rotate(45, center=(0, frag.size[1]))
			output.paste(frag, (xpaste, ypaste), frag)

			return output


		def deg1125ToDeg225(frag):
		#take 11.25 deg wedge, mirror it to make it 22.5 degrees
		#returns 22.5 deg frag

			output = Image.new('RGBA', (frag.size[1] - 1, frag.size[1] - 1))
			xpaste = 0
			ypaste = 0

			#paste 11.25 deg frag to output canvas
			output.paste(frag, (xpaste, ypaste), frag)

			#flip and rotate frag to create a 22.5 deg frag 
			frag = frag.transpose(method=Image.FLIP_TOP_BOTTOM).rotate(90)
			frag = frag.rotate(67.5, center=(0, frag.size[1]))
			output.paste(frag, (xpaste, ypaste), frag)

			return output


		#modify supplied fragment to make it 45 deg
		if angle == 22.5:
			frag = deg225ToDeg45(frag)
			angle = 45

		elif angle == 11.25:
			frag = deg225ToDeg45(deg1125ToDeg225(frag))
			angle = 45


		#create blank square canvas for output and determine the centre (added 10 pixels to create dead space)
		output = Image.new('RGBA', (frag.size[0] * 2 + (10), frag.size[0] * 2 + (10)))
		offset = math.floor(frag.size[1])

		#paste the first fragment against the 12 oclock position
		degreesLeft = 360
		originalAngle = angle
		angleMultiplier = 2

		#set y pos for pasting based on how many degrees have been pasted
		while degreesLeft > 0:
		
			def getXY(degreesLeft):
				if degreesLeft > 270:
					xpaste = offset + 5
					ypaste = 5

				elif degreesLeft > 180:
					xpaste = offset + 5
					ypaste = offset + 5

				elif degreesLeft > 90:
					xpaste = 5
					ypaste = offset + 5

				else:
					xpaste = 5
					ypaste = 5

				return(xpaste, ypaste)

		
			output.paste(frag, (getXY(degreesLeft)[0], getXY(degreesLeft)[1]), frag)

			degreesLeft = degreesLeft - originalAngle
			

			if degreesLeft == 270:
				angleMultiplier = 0

			if degreesLeft < 270:
				angle = 360 - (originalAngle * angleMultiplier)

			else:
				angle = originalAngle * angleMultiplier


			frag = frag.transpose(method=Image.FLIP_TOP_BOTTOM).rotate(angle)
			angleMultiplier = angleMultiplier + 2

		return output


	print('source x = ' +str(img.size[0]))
	print('source y = ' +str(img.size[1]))

	coordsList = generateCoords(img, quantity)


	for i in range(0, len(coordsList)):
		#iterate over each item in the coords list and produce mandala for each

		#randomly choose fragment angle
		angle = choice([11.25, 22.5, 45])
		print('angle = ' + str(angle))

		#randomly choose rotation
		img = p.Image.open(currentImage)
		flip = choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM])
		img = img.transpose(flip)

		frag = createWedge(angle, coordsList[i][0], coordsList[i][1], coordsList[i][2], coordsList[i][3])
		output = construct(frag, angle)
		
		#set file name for saving to ensure nothing gets overwritten
		outname = i

		#set suffix based on saturation / contrast flags
		if regularImage:
			fileSuffix = ''
		elif saturateImage:
			fileSuffix = 's'
		elif contrastImage:
			fileSuffix = 'c'
		else:
			fileSuffix = 'sc'
	       
	    #check to see if file name exists and increment to avoid overwriting old images
		while os.path.isfile(currentDir + str(outname) + fileSuffix + '.png'):
			outname = outname + 1
		
		#saves the raw mandala without applying any filters
		if regularImage:
			print('Saving ' + str(outname) + '.png\n')
			output.save(currentDir + str(outname) + '.png')


		if saturateImage or satcontImage:
			#generate random float for saturation severity
			saturateInt = uniform(1.2, 2.1)
			print('Saturation set to ' + str(saturateInt))

			satFilter = ImageEnhance.Color(output)
			outputSaturate = satFilter.enhance(saturateInt)

			#only save here if saturation flag set (eliminates excessive files if satcontImage is set)
			if saturateImage:
				print('Saving saturated image as ' + str(outname) + 's.png\n')
				outputSaturate.save(currentDir + str(outname) + 's.png')


		if contrastImage or satcontImage:
			#generate random float for contrast severity
			contrastInt = uniform(1.2, 2.1)
			print('Contrast set to ' + str(contrastInt))

	        #check if the saturate flag is true, if so the apply contrast to the saturated image
	        #if not apply contrast to the unmodified output image
			if satcontImage:
				contrastFilter = ImageEnhance.Contrast(outputSaturate)
				outputContrast = contrastFilter.enhance(contrastInt)
				print('Saving contrasted / saturated image as ' + str(outname) + 'sc.png\n')
				outputContrast.save(currentDir + str(outname) + 'sc.png')

			else:
				contrastFilter = ImageEnhance.Contrast(output)
				outputContrast = contrastFilter.enhance(contrastInt)
				print('Saving contrasted image as ' + str(currentDir + outname) + 'c.png\n')
				outputContrast.save(currentDir + str(outname) + 'c.png')

		print('***\n')



#iterate over all source images
for imageName in listOfImages:

	currentImage = direct + '/' + imageName
	currentDir = './output/' + imageName[:-4] + '/'
	outputWidth = origOutputwidth

	#check if directories exist create if needed
	if not os.path.isdir('./output'):
		os.mkdir('./output')
	if not os.path.isdir(currentDir):
		os.mkdir(currentDir)

	#copy source image
	shutil.copy(currentImage, currentDir)
	os.rename(currentDir + imageName, currentDir + '0.jpg')

	img = Image.open(currentImage)
	print('******************************************************')
	print('Source image: ' + currentDir)


	print('x ' + str(img.size[0]) + ' y ' + str(img.size[1]))
	#ensure image is in landscape mode
	if img.size[0] < img.size[1]:
		img = img.transpose(Image.ROTATE_90)
		print('Rotated source image')

	#ensure image is of sufficient size
	smallestAxis = min(img.size[0], img.size[1])

	if (smallestAxis - (outputWidth / 2) < 1):
		print('Source image is too small (' + str(img.size[0]) + 'px wide, / ' + str(img.size[1]) + 'px high)')
		print('Requested output width is ' + str(outputWidth) + 'px')
		print('Output size will be set to ' + str(math.floor((smallestAxis * 0.9) * 2)) + 'px')
		outputWidth = math.floor((smallestAxis * 0.9) * 2)

	buildMandalas(img, currentDir)