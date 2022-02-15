# Readme

The Dharma project is a script that will take a jpg file, and transform it into a series of mandalas in png format using pythons random.randint function.  This allows for a very large number of unique mandalas to be generated from a single source image as many aspects are randomised such as:

- the angle of the wedge, either 45, 22.5 or 11.25 degrees
- The position of the wedge in the image
- The orientation of the source image
- The brightness / contrast of the output image 

# Usage

**dharmaStandalone.py \[-h\] \[-d D\] \[-q Q\] \[-s S\]**

optional arguments:
  -h, --help  show this help message and exit
  -d D        The directory that contains source images. (Defaults to current directory)
  -q Q        The quantity of mandalas requested for each source image. (Defaults to 5)
  -s S        The horizontal size in pixels requested for each mandala. (Defaults to 2000)
<br>
example:

**dharmaStandalone.py -d myDir -q 20 -s 2000**

- creates 20 mandalas of 2000 pixels width from each jpg file within the myDir directory

# Note
1. The script will filter out any files that do not end in ".jpg" it does not matter what else iis in the source directory.
1. If the specified output width is not possible due to the source image being of insufficient resolution, the output size will be optimised for the largest size possible.  This will likely result in reduced diversity amongst the final mandalas, as the wedge used to create them will have less varience than it otherwise would.
1. If the directory "output" does not exist, it will be created and all mandalas will be saved there, each series will be in their own folder with a copy of the source image
1. For best results use source images in sharp focus

# Known issues
- Smaller images may not render correctly when using a 45 degree wedge 

# Examples

Original | Examples | |
![](https://github.com/u4nf/dharma/blob/master/examples/a.jpg =250x250) | https://github.com/u4nf/dharma/blob/master/examples/a1.png | https://github.com/u4nf/dharma/blob/master/examples/a2.png | https://github.com/u4nf/dharma/blob/master/examples/a3.png
<p float="left">
  <img src="https://github.com/u4nf/dharma/blob/master/examples/a.jpg" width="250" />
  <img src="https://github.com/u4nf/dharma/blob/master/examples/a1.jpg" width="250" />
  <img src="https://github.com/u4nf/dharma/blob/master/examples/a2.jpg" width="250" />
  <img src="https://github.com/u4nf/dharma/blob/master/examples/a3.jpg" width="250" />
</p>
