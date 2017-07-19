__author__="Nikhil Rayaprolu"
__version__ = "1.0.0"
__maintainer__ = "Nikhil Rayaprolu"
__email__ = "nikhil.rayaprolu@students.iiit.ac.in"
__status__ = "Development"

from random import randint
import numpy
from pygame.locals import *
import pygame

class Board(object):
	"""board for the tetris game"""
	def __init__(self):
		super(Board, self).__init__()
		
		self.initialboardcreator()
		self.pygameColors()
	def checkPiecePos(self):
		pass
	def fillPiecePos(self):
		pass
	def initialboardcreator(self):
		self.FPS = 25
		self.WINDOWWIDTH = 640
		self.WINDOWHEIGHT = 480
		self.BOXSIZE = 20
		self.BOARDWIDTH = 10
		self.BOARDHEIGHT = 20
		self.BLANK = '.'
		self.XMARGIN = int((self.WINDOWWIDTH - self.BOARDWIDTH * self.BOXSIZE) / 2)
		self.TOPMARGIN = self.WINDOWHEIGHT - (self.BOARDHEIGHT * self.BOXSIZE) - 5
		self.TEMPLATEWIDTH = 5
		self.TEMPLATEHEIGHT = 5

	def pygameColors(self):
		self.WHITE       = (255, 255, 255)
		self.GRAY        = (185, 185, 185)
		self.BLACK       = (  0,   0,   0)
		self.RED         = (155,   0,   0)
		self.LIGHTRED    = (175,  20,  20)
		self.GREEN       = (  0, 155,   0)
		self.LIGHTGREEN  = ( 20, 175,  20)
		self.BLUE        = (  0,   0, 155)
		self.LIGHTBLUE   = ( 20,  20, 175)
		self.YELLOW      = (155, 155,   0)
		self.LIGHTYELLOW = (175, 175,  20)
		self.BORDERCOLOR = self.BLUE
		self.BGCOLOR = self.BLACK
		self.TEXTCOLOR = self.WHITE
		self.TEXTSHADOWCOLOR = self.GRAY
		self.COLORS      = (     self.BLUE,      self.GREEN,      self.RED,      self.YELLOW)
		self.LIGHTCOLORS = (self.LIGHTBLUE, self.LIGHTGREEN, self.LIGHTRED, self.LIGHTYELLOW)
		assert len(self.COLORS) == len(self.LIGHTCOLORS) # each color must have light color
	def InitialBoard(self):
		self.board = []
		for i in range(self.BOARDWIDTH):
		    self.board.append([self.BLANK] * self.BOARDHEIGHT)
		return self.board

	def isValidPosition(self,board, piece, adjX=0, adjY=0):
	    # Return True if the piece is within the board and not colliding
	    for x in range(self.TEMPLATEWIDTH):
	        for y in range(self.TEMPLATEHEIGHT):
				print y
				print piece
				isAboveBoard = y + piece['y'] + adjY < 0
				if isAboveBoard or self.PIECES[piece['shape']][piece['rotation']][y][x] == self.BLANK:
					continue
				if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
					return False
				if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != self.BLANK:
					return False
	    return True
	def removeCompleteLines(self,board):
	    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
	    numLinesRemoved = 0
	    y = self.BOARDHEIGHT - 1 # start y at the bottom of the board
	    while y >= 0:
	        if self.isCompleteLine(board, y):
	            # Remove the line and pull boxes down by one line.
	            for pullDownY in range(y, 0, -1):
	                for x in range(self.BOARDWIDTH):
	                    board[x][pullDownY] = board[x][pullDownY-1]
	            # Set very top line to blank.
	            for x in range(self.BOARDWIDTH):
	                board[x][0] = self.BLANK
	            numLinesRemoved += 1
	            # Note on the next iteration of the loop, y is the same.
	            # This is so that if the line that was pulled down is also
	            # complete, it will be removed.
	        else:
	            y -= 1 # move on to check next row up
	    return numLinesRemoved
	def isCompleteLine(self,board, y):
	    # Return True if the line filled with boxes with no gaps.
	    for x in range(self.BOARDWIDTH):
	        if board[x][y] == self.BLANK:
	            return False
	    return True
	def addToBoard(self,board, piece,PIECES):
	    # fill in the board based on piece's location, shape, and rotation
	    for x in range(self.TEMPLATEWIDTH):
	        for y in range(self.TEMPLATEHEIGHT):
	            if PIECES[piece['shape']][piece['rotation']][y][x] != self.BLANK:
	                board[x + piece['x']][y + piece['y']] = piece['color']
	def drawBoard(self,board):
	    # draw the border around the board
	    pygame.draw.rect(self.DISPLAYSURF, self.BORDERCOLOR, (self.XMARGIN - 3, self.TOPMARGIN - 7, (self.BOARDWIDTH * self.BOXSIZE) + 8, (self.BOARDHEIGHT * self.BOXSIZE) + 8), 5)

	    # fill the background of the board
	    pygame.draw.rect(self.DISPLAYSURF, self.BGCOLOR, (self.XMARGIN, self.TOPMARGIN, self.BOXSIZE * self.BOARDWIDTH, self.BOXSIZE * self.BOARDHEIGHT))
	    # draw the individual boxes on the board
	    for x in range(self.BOARDWIDTH):
	        for y in range(self.BOARDHEIGHT):
	            self.drawBox(x, y, board[x][y])
	def drawStatus(self,score, level):
	    # draw the score text
	    scoreSurf = self.BASICFONT.render('Score: %s' % score, True, self.TEXTCOLOR)
	    LevelSurf = self.BASICFONT.render('Level: %s' % level, True, self.TEXTCOLOR)
	    scoreRect = scoreSurf.get_rect()
	    LevelRect = LevelSurf.get_rect()
	    scoreRect.topleft = (self.WINDOWWIDTH - 150, 20)
	    LevelRect.topleft=(self.WINDOWWIDTH-150,50)
	    self.DISPLAYSURF.blit(scoreSurf, scoreRect)
	    self.DISPLAYSURF.blit(LevelSurf, LevelRect)
	
	def drawBox(self,boxx, boxy, color, pixelx=None, pixely=None):
		# draw a single box (each tetromino piece has four boxes)
		# at xy coordinates on the board. Or, if pixelx & pixely
		# are specified, draw to the pixel coordinates stored in
		# pixelx & pixely (this is used for the "Next" piece).
		if color == self.BLANK:
		    return
		if pixelx == None and pixely == None:
		    pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
		pygame.draw.rect(self.DISPLAYSURF, self.COLORS[color], (pixelx + 1, pixely + 1, self.BOXSIZE - 1, self.BOXSIZE - 1))
		pygame.draw.rect(self.DISPLAYSURF, self.LIGHTCOLORS[color], (pixelx + 1, pixely + 1, self.BOXSIZE - 4, self.BOXSIZE - 4))

	

