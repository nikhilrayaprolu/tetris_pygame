__author__="Nikhil Rayaprolu"
__version__ = "1.0.0"
__maintainer__ = "Nikhil Rayaprolu"
__email__ = "nikhil.rayaprolu@students.iiit.ac.in"
__status__ = "Development"

import pygame,random
import time

class Block(object):
	"""block class for the tetris game"""
	def __init__(self):
		super(Block, self).__init__()
		
		self.MOVESIDEWAYSFREQ = 0.15
		self.MOVEDOWNFREQ = 0.1
		self.BlockShape()

	def moveLeft(self):
		 		self.fallingPiece['x'] -=1
		 		self.movingLeft = True
		 		self.movingRight = False
		 		self.lastMoveSidewaysTime = time.time()
		 		

	def moveRight(self):
		 		self.fallingPiece['x'] +=1
		 		self.movingRight=True
		 		self.movingLeft = False
		 		self.lastMoveSidewaysTime= time.time()
		 		

	def Rotate(self, r):
		 		self.fallingPiece['rotation']=(self.fallingPiece['rotation']+r)% len(self.PIECES[self.fallingPiece['shape']])

	def BlockShape(self):
		self.S_SHAPE_TEMPLATE = [['.....',
	                     '.....',
	                     '..OO.',
	                     '.OO..',
	                     '.....'],
	                    ['.....',
	                     '..O..',
	                     '..OO.',
	                     '...O.',
	                     '.....']]

		self.Z_SHAPE_TEMPLATE = [['.....',
		                     '.....',
		                     '.OO..',
		                     '..OO.',
		                     '.....'],
		                    ['.....',
		                     '..O..',
		                     '.OO..',
		                     '.O...',
		                     '.....']]

		self.I_SHAPE_TEMPLATE = [['..O..',
		                     '..O..',
		                     '..O..',
		                     '..O..',
		                     '.....'],
		                    ['.....',
		                     '.....',
		                     'OOOO.',
		                     '.....',
		                     '.....']]

		self.O_SHAPE_TEMPLATE = [['.....',
		                     '.....',
		                     '.OO..',
		                     '.OO..',
		                     '.....']]

		self.J_SHAPE_TEMPLATE = [['.....',
		                     '.O...',
		                     '.OOO.',
		                     '.....',
		                     '.....'],
		                    ['.....',
		                     '..OO.',
		                     '..O..',
		                     '..O..',
		                     '.....'],
		                    ['.....',
		                     '.....',
		                     '.OOO.',
		                     '...O.',
		                     '.....'],
		                    ['.....',
		                     '..O..',
		                     '..O..',
		                     '.OO..',
		                     '.....']]

		self.L_SHAPE_TEMPLATE = [['.....',
		                     '...O.',
		                     '.OOO.',
		                     '.....',
		                     '.....'],
		                    ['.....',
		                     '..O..',
		                     '..O..',
		                     '..OO.',
		                     '.....'],
		                    ['.....',
		                     '.....',
		                     '.OOO.',
		                     '.O...',
		                     '.....'],
		                    ['.....',
		                     '.OO..',
		                     '..O..',
		                     '..O..',
		                     '.....']]

		self.T_SHAPE_TEMPLATE = [['.....',
		                     '..O..',
		                     '.OOO.',
		                     '.....',
		                     '.....'],
		                    ['.....',
		                     '..O..',
		                     '..OO.',
		                     '..O..',
		                     '.....'],
		                    ['.....',
		                     '.....',
		                     '.OOO.',
		                     '..O..',
		                     '.....'],
		                    ['.....',
		                     '..O..',
		                     '.OO..',
		                     '..O..',
		                     '.....']]
		self.PIECES = {'S': self.S_SHAPE_TEMPLATE,
          'Z': self.Z_SHAPE_TEMPLATE,
          'J': self.J_SHAPE_TEMPLATE,
          'L': self.L_SHAPE_TEMPLATE,
          'I': self.I_SHAPE_TEMPLATE,
          'O': self.O_SHAPE_TEMPLATE,
          'T': self.T_SHAPE_TEMPLATE}
	def getNewPiece(self):
	    # return a random new piece in a random rotation and color
	    self.shape = random.choice(list(self.PIECES.keys()))
	    newPiece = {'shape': self.shape,
	                'rotation': random.randint(0, len(self.PIECES[self.shape]) - 1),
	                'x': int(self.BOARDWIDTH / 2) - int(self.TEMPLATEWIDTH / 2),
	                'y': -2, # start it above the board (i.e. less than 0)
	                'color': random.randint(0, len(self.COLORS)-1)}
	    return newPiece		                 
	def isOnBoard(self,x, y):
		return x >= 0 and x < self.BOARDWIDTH and y < self.BOARDHEIGHT
	def drawPiece(self,piece, pixelx=None, pixely=None,PIECES={}):
	    shapeToDraw = self.PIECES[piece['shape']][piece['rotation']]
	    if pixelx == None and pixely == None:
	        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
	        pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])

	    # draw each of the boxes that make up the piece
	    for x in range(self.TEMPLATEWIDTH):
	        for y in range(self.TEMPLATEHEIGHT):
	            if shapeToDraw[y][x] != self.BLANK:
	                self.drawBox(None, None, piece['color'], pixelx + (x * self.BOXSIZE), pixely + (y * self.BOXSIZE))
	def drawNextPiece(self,piece,PIECES):
	    # draw the "next" text
	    nextSurf = self.BASICFONT.render('Next:', True, self.TEXTCOLOR)
	    nextRect = nextSurf.get_rect()
	    nextRect.topleft = (self.WINDOWWIDTH - 120, 80)
	    self.DISPLAYSURF.blit(nextSurf, nextRect)
	    # draw the "next" piece
	    self.drawPiece(piece, pixelx=self.WINDOWWIDTH-120, pixely=100,PIECES={})


		