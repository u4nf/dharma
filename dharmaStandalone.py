#!/usr/bin/python3

import sys
import shutil
import PIL as p
import math
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
from random import randint, uniform

# usage dharma {dir} {qty} {size}
#{dir}  - directory containing source images in .jpg format
#{qty}  - quantity of mandalas per source image (default 20)
#{size} - size of final mandala in pixels (default 2000)


#randomly choose fragment angle
angles = [11.25, 22.5, 45]
angle = angles[randint(0, 1)]

regularImage = False
saturateImage = False
contrastImage = False
satcontImage = True

def setEnv():
	#set environment variables
	if (len(sys.argv) == 4):
		direct = './' + sys.argv[1]
		quantity = int(sys.argv[2])
		outputWidth = int(sys.argv[3])
	else:
		print('Incorrect number of arguments, defaults have been set')
		print('Usage  - dharma \{dir\} \{qty\} \{size\}\{dir\}\n')
		print('\{dir}  - directory containing source images in .jpg format')
		print('\{qty\}  - quantity of mandalas per source image (default 20)')
		print('\{size\} - size of final mandala in pixels (default 2000)\n')
		print('eg: dharma zoesimages 5 1000')
		print('will give 5 mandalas at 1000 pixels wide for each image in the directory "zoesimages"')
		direct = './'
		quantity = 20
		outputWidth = 2000

	listOfImages = []
	for file in os.listdir(direct):
		if file.endswith('.jpg'):
			listOfImages.append(file)

	return direct, quantity, outputWidth, listOfImages
	

def buildMandalas(img, currentDir):

	print('source x = ' +str(img.size[0]))
	print('source y = ' +str(img.size[1]))


	def generateCoords(img, outputWidth, quantity):
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

				stx = randint(0, img.size[0] - (outputWidth / 2))
				sty = stx
				enx = stx + (outputWidth / 2)
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

		def verify(img, stx, sty, enx, eny):
			#ensure start and end points within appropriate range so wedge will be complete

			print('user defined coordinates =  start (x/y) ' + str(stx) + '/' + str(sty) + ' - end (x/y) ' + str(enx) + '/' + str(eny))
			#verify angle will not give blank space or overlap on output image
			if (360 % angle != 0):
				print('inappropriate angle. suggest - 90, 45')
				print('You entered ' + str(angle))
				quit()

			#check that start coords are before end coords
			if (stx >= enx):
				print('start point must be less than end point, you entered: start (x, y) ' + str(stx) + '/' + str(sty) + ', end (x, y) ' + str(enx) + '/' + str(eny))
				quit()



		img = p.Image.open(currentImage)
		
		verify(img, stx, sty, enx, eny)

		mask = Image.new("L", img.size, 0)

		draw = ImageDraw.Draw(mask)

		draw.pieslice([stx, sty, enx, eny], 270, 270 + angle, fill='white')

	    #create wedge fragment
		frag = img.copy()
		frag.putalpha(mask)
		frag = frag.crop(((enx + stx) / 2, sty, enx, (eny + stx) / 2))
		
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


	coordsList = generateCoords(img, outputWidth, quantity)


	for i in range(0, len(coordsList)):
		#iterate over each item in the coords list and produce mandala for each
		#if quantity variable set to one, it will only run once

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
				outputSaturate.save(currentDir +str(outname) + 's.png')


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
				outputContrast.save(currentDir +str(outname) + 'sc.png')

			else:
				contrastFilter = ImageEnhance.Contrast(output)
				outputContrast = contrastFilter.enhance(contrastInt)
				print('Saving contrasted image as ' + str(outname) + 'c.png\n')
				outputContrast.save(currentDir +str(outname) + 'c.png')

		print('***************************\n')


direct, quantity, outputWidth, listOfImages = setEnv()

for img in listOfImages:

	currentImage = direct + '/' + img
	currentDir = './output/' + img[:-4] + '/'

	img = Image.open(currentImage)

	if img.size[0] - (outputWidth / 2) < 1:
		print('Source image is too small (' + str(img.size[0]) + ')')
		print('Requested output width is ' + str(outputWidth))
		print('Not processing ' + currentImage + '\n')
		continue

	os.mkdir(currentDir)
	shutil.copy(currentImage, currentDir)

	buildMandalas(img, currentDir)