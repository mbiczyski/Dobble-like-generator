import os
from random import shuffle, uniform
from re import match
import cv2 as cv
import numpy as np
import math

pathname = 'input\\'
outpathname = 'output\\'
shuffleSymbolsOnCard = True
dpi = 300 # px/in
cardDiam = 10.16 # cm

# prepare a list of icons in directory
symbols = []
for filename in os.listdir(pathname):
  if filename.endswith(".bmp") or filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".gif"):
    symbols.append(filename)
print(symbols)

# check how many symbols can be on card with available files
for testNum in range(1, 20):
  if len(symbols) < (testNum**2 + testNum + 1):
    numberOfSymbolsOnCard = testNum
    break
print(len(symbols), (testNum**2 + testNum + 1))

### Borrowed code START
#Source: The Dobble Algorithm - www.101computing.net/the-dobble-algorithm/
cards = []

#Work out the prime number
n = numberOfSymbolsOnCard - 1

#Total number of cards that can be generated following the Dobble rules
numberOfCards = n**2 + n + 1  #e.g. 7^2 + 7 + 1 = 57


#Add first set of n+1 cards (e.g. 8 cards)
for i in range(n+1):  
  #Add new card with first symbol
  cards.append([1])
  #Add n+1 symbols on the card (e.g. 8 symbols)
  for j in range(n):
    cards[i].append((j+1)+(i*n)+1)

#Add n sets of n cards 
for i in range(0,n):
  for j in range(0,n):
    #Append a new card with 1 symbol
    cards.append([i+2])
     #Add n symbols on the card (e.g. 7 symbols)
    for k in range(0,n):
      val  = (n+1 + n*k + (i*k+j)%n)+1
      cards[len(cards)-1].append(val)

#Shuffle symbols on each card
if shuffleSymbolsOnCard :
  for card in cards:
    shuffle(card)


      
# #Output all cards  
# i = 0
# for card in cards:
#   i+=1
#   line = str(i) + " - ["
#   for number in card:
#     line = line + symbols[number-1] + ", "
#   line = line[:-2] + "]"  
#   print(line)

### Borrowed code END

INTOCM = 2.54
cardSizePx = int(cardDiam / INTOCM * dpi)
cardSizePxMid = int(cardDiam / INTOCM * dpi / 2)

blanka = np.zeros((cardSizePx,cardSizePx,4), np.uint8)
cv.circle(blanka, (cardSizePxMid,cardSizePxMid), cardSizePxMid, (255,255,255,255), -1)
cv.circle(blanka, (cardSizePxMid,cardSizePxMid), cardSizePxMid, (0,0,0,255), 2)

cardNum = 1
for card in cards:
  ang = 0
  blankaCard = blanka.copy()

  for number in card:
    icon = cv.imread(pathname+symbols[number],cv.IMREAD_UNCHANGED)
    iconRow, iconCol, iconCha = icon.shape

    # scale the icon
    destSize = int(cardSizePxMid/3)
    scale = uniform(0.75, 1.25)*destSize/max(iconRow,iconCol)
    # icon = cv.resize(icon, None, fx=scale, fy=scale, interpolation = cv.INTER_AREA)
    # iconRow, iconCol, iconCha = icon.shape

    # rotate icon
    rotang = uniform(0,360)
    rotMatrix = cv.getRotationMatrix2D((int(iconCol/2),int(iconRow/2)), rotang, scale)
    icon = cv.warpAffine(icon, rotMatrix, (iconCol,iconRow))
    iconRow, iconCol, iconCha = icon.shape

    # calculate position of the icon
    r = uniform(cardSizePxMid*0.2, cardSizePxMid*0.8)
    angvar = uniform(-360/numberOfSymbolsOnCard/2*0.5, 360/numberOfSymbolsOnCard/2*0.5)
    posX = int(r*math.cos(math.radians(ang+angvar))+cardSizePxMid)
    posY = int(r*math.sin(math.radians(ang+angvar))+cardSizePxMid)
    # print(ang+angvar, math.radians(ang+angvar), r*math.cos(math.radians(ang+angvar)), posX, r*math.sin(math.radians(ang+angvar)), posY)

    # ensure the icon stays within base image
    iconX = int(posX-iconRow/2)
    if posX-iconRow/2 < 0:
      iconX = int(0)
    if posX+iconRow/2 > cardSizePx:
      iconX = int(cardSizePx-iconRow)

    iconY = int(posY-iconCol/2)
    if posY-iconCol/2 < 0:
      iconY = int(0)
    if posY+iconCol/2 > cardSizePx:
      iconY = int(cardSizePx-iconCol)

    roi = blankaCard[iconX:iconX+iconRow,iconY:iconY+iconCol,0:4]

    # cut out the icon and card background
    iconMask = icon[:,:,3]
    iconMaskInv = cv.bitwise_not(iconMask)
    iconFG = cv.bitwise_and(icon,icon,mask = iconMask)
    cardBG = cv.bitwise_and(roi,roi,mask = iconMaskInv)

    # add icon to the card
    blankaCard[iconX:iconX+iconRow,iconY:iconY+iconCol,0:4] = cv.add(iconFG,cardBG)

    # print(ang, r, angvar, scale, icon.shape)
    ang += 360/numberOfSymbolsOnCard

  cv.imshow('card',blankaCard)
  cv.waitKey(0)
  cv.destroyAllWindows()

  cv.imwrite(outpathname+'card'+str(cardNum)+'.png', blankaCard)
  cardNum += 1
  
cv.imwrite('testblank.png', blanka)
