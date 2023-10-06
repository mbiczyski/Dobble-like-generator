import os
from random import shuffle, uniform
from re import match
import cv2 as cv
import numpy as np
import math

regenerate = []

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

# check how many symbols can be on card with available files
for testNum in range(1, 20):
  if len(symbols) < (testNum**2 + testNum + 1):
    numberOfSymbolsOnCard = testNum
    break

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

### Borrowed code END

# generate blank card
INTOCM = 2.54
cardSizePx = int(cardDiam / INTOCM * dpi)
cardSizePxMid = int(cardDiam / INTOCM * dpi / 2)

blanka = np.zeros((cardSizePx,cardSizePx,4), np.uint8)
cv.circle(blanka, (cardSizePxMid,cardSizePxMid), cardSizePxMid, (255,255,255,255), -1)
cv.circle(blanka, (cardSizePxMid,cardSizePxMid), cardSizePxMid, (0,0,0,255), 2)

cardNum = 1

# select cards to generate
toGenerate = []
if regenerate:
  for cd in regenerate:
    toGenerate.append(cards[cd-1])
else:
  toGenerate = cards

for card in toGenerate:
  ang = 0
  blankaCard = blanka.copy()

  middle = True
  for number in card:
    icon = cv.imread(pathname+symbols[number-1],cv.IMREAD_UNCHANGED)
    iconRow, iconCol, iconCha = icon.shape

    # scale the icon
    destSize = int(cardSizePxMid/1.7)
    scale = uniform(0.75, 1.25)*destSize/max(iconRow,iconCol)

    # rotate icon
    rotang = uniform(0,360)
    rotMatrix = cv.getRotationMatrix2D((int(iconCol/2),int(iconRow/2)), rotang, scale)
    icon = cv.warpAffine(icon, rotMatrix, (iconCol,iconRow))
    iconRow, iconCol, iconCha = icon.shape

    # calculate position of the icon
    if middle:
      r = 0
      angvar = 0
      middle = False
    else:
      r = uniform(cardSizePxMid*0.5, cardSizePxMid*0.65)
      angvar = uniform(-360/(numberOfSymbolsOnCard-1)/2*0.5, 360/(numberOfSymbolsOnCard-1)/2*0.5)
    angvar = 0
    posX = int(r*math.cos(math.radians(ang+angvar))+cardSizePxMid)
    posY = int(r*math.sin(math.radians(ang+angvar))+cardSizePxMid)

    # resize matrix to object
    if iconCha == 4:
      iconSizeMask = icon[:,:,3]
    else:
      iconSizeGray = cv.cvtColor(icon,cv.COLOR_BGR2GRAY)
      retSize, iconSizeMask = cv.threshold(iconSizeGray, 10, 255, cv.THRESH_BINARY)

    flag = False
    for rowStart in range(0, iconRow):
      for pixel in range(0, iconCol):
        if iconSizeMask[rowStart,pixel] != 0:
          flag = True
          break
      if flag:
        break
    flag = False
    for rowEnd in range(iconRow-1, -1, -1):
      for pixel in range(iconCol-1, -1, -1):
        if iconSizeMask[rowEnd,pixel] != 0:
          flag = True
          break
      if flag:
        break
    flag = False
    for colStart in range(0, iconCol):
      for pixel in range(0, iconRow):
        if iconSizeMask[pixel,colStart] != 0:
          flag = True
          break
      if flag:
        break
    flag = False
    for colEnd in range(iconCol-1, -1, -1):
      for pixel in range(iconRow-1, -1, -1):
        if iconSizeMask[pixel,colEnd] != 0:
          flag = True
          break
      if flag:
        break

    icon = icon[rowStart:rowEnd,colStart:colEnd,:]
    iconRow, iconCol, iconCha = icon.shape

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

    roi = blankaCard[iconX:iconX+iconRow,iconY:iconY+iconCol,0:iconCha]

    # cut out the icon and card background
    if iconCha == 4:
      iconMask = icon[:,:,3]
    else:
      iconGray = cv.cvtColor(icon,cv.COLOR_BGR2GRAY)
      ret, iconMask = cv.threshold(iconGray, 10, 255, cv.THRESH_BINARY)
    iconMaskInv = cv.bitwise_not(iconMask)
    iconFG = cv.bitwise_and(icon,icon,mask = iconMask)
    cardBG = cv.bitwise_and(roi,roi,mask = iconMaskInv)

    # add icon to the card
    blankaCard[iconX:iconX+iconRow,iconY:iconY+iconCol,0:iconCha] = cv.add(iconFG,cardBG)

    if not middle:
      ang += 360/(numberOfSymbolsOnCard-1)

  # cv.imshow('card',blankaCard)
  # cv.waitKey(0)
  # cv.destroyAllWindows()

  if regenerate:
    cv.imwrite(outpathname+'card'+str(regenerate[cardNum-1])+'.png', blankaCard)
    print('card ' + str(regenerate[cardNum-1]) + ' generated -', card)
  else:
    cv.imwrite(outpathname+'card'+str(cardNum)+'.png', blankaCard)
    print('card ' + str(cardNum) + ' generated -', card)
  cardNum += 1
  
cv.imwrite(outpathname+'testblank.png', blanka)
