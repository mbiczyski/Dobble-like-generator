import img2pdf
from PIL import Image
import os

outpathname = 'output\\'
dpi = 300 # px/in
cardDiam = 10.16 # cm

cards = []
for filename in os.listdir(outpathname):
  if filename.endswith('.png'):
    cards.append(filename)

layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpi, dpi))
for card in cards:
	### Borrowed code START
	#Source: How to Convert Image to PDF in Python? - https://www.geeksforgeeks.org/python-convert-image-to-pdf-using-img2pdf-module/
	image = Image.open(outpathname + card)
	# Modification to use fixed dpi - 06/10/23 MB
	pdf_bytes = img2pdf.convert(image.filename, layout_fun=layout_fun)
	namelen = len(card)
	file = open(outpathname + card[0:namelen-4] + '.pdf', "wb")
	file.write(pdf_bytes)
	image.close()
	file.close()
	### Borrowed code END

print("Converted " + str(len(cards)) + " files to .pdf")