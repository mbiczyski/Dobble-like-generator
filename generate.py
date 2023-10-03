import os
from random import shuffle
from re import match

pathname = 'images\\'
shuffleSymbolsOnCard = True

# prepare a list of icons in directory
symbols = []
for filename in os.listdir(pathname):
  if filename.endswith(".bmp") or filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".gif"):
    symbols.append(filename)

# check how many symbols can be on card with available files
for testNum in range(1, 20):
  if len(symbols) < (testNum**2 + testNum + 1):
    numberOfSymbolsOnCard = testNum - 1
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
      
#Output all cards  
i = 0
for card in cards:
  i+=1
  line = str(i) + " - ["
  for number in card:
    line = line + symbols[number-1] + ", "
  line = line[:-2] + "]"  
  print(line)

### Borrowed code END