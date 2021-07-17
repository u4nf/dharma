# dharma

aiart.sh
  Loops over getart.sh and dharma.py creating a single mandala each iteration.
  
 getart.sh
  Downloads image from www.thisartworkdoesnotexist.com and renames it to 1.jpg
  
dharma.py
  Creates a mandala.
  
  Select 45, 22.5 or 11.25 degrees at random for wedge angle.
  Select random point inside source image.
  Verify wedge entirely within xy coords.
  Cut a wedge from source image.
  Paste wedge to blank image.
  Rotate and flip copy of wedge.
  Repeat until 360 degrees have been accounted for.
  Check if saturation / contrast values set, apply at random strength.
  Check if filename exists, if yes, increment.
  Save as png.
