__author__="Nikhil Rayaprolu"
__version__ = "1.0.0"
__maintainer__ = "Nikhil Rayaprolu"
__email__ = "nikhil.rayaprolu@students.iiit.ac.in"
__status__ = "Development"

from Board import Board
from Block import Block
from scores import Score
import pygame,sys
import time
from pygame.locals import *
class GamePlay(Board,Block,object):
	"""game play class for the game"""
	def __init__(self):
		super(GamePlay, self).__init__()		
		self.scoreboard=Score()
		self.FPSCLOCK = pygame.time.Clock()
		self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
		print self.TEXTSHADOWCOLOR
    	
    	pygame.display.set_caption('Tetromino')

	def start(self):
		pygame.init()
		self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
		self.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)

		pygame.display.set_caption('My Game')
		#Some variables used in the game loop
		clock=pygame.time.Clock()
		GameEnd=False
		display=pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
		self.showTextScreen('Tetromino')
		while True: # game loop
			self.runGame()
			self.showTextScreen('Game Over')
	def runGame(self):
		self.board=self.InitialBoard()
		self.lastDownTime=time.time()
		self.lastSideWaysTime=time.time()
		self.lastFallTime = time.time()
		self.movingDown = False # note: there is no movingUp variable
		self.movingLeft = False
		self.movingRight = False
		self.score = 0
		self.level, self.fallFreq = self.scoreboard.calculateLevelAndFallFreq(self.score)
		self.fallingPiece = self.getNewPiece()
		self.fallingPiece=self.fallingPiece
		self.nextPiece = self.getNewPiece()
		self.nextPiece=self.nextPiece
		while True: # game loop
			if self.fallingPiece == None:
				# No falling piece in play, so start a new piece at the top
				self.fallingPiece = self.nextPiece
				self.fallingPiece=self.fallingPiece
				self.nextPiece = self.getNewPiece()
				self.lastFallTime = time.time() # reset lastFallTime

				if not self.isValidPosition(self.board, self.fallingPiece):
					return # can't fit a new piece on the board, so game over

			self.checkForQuit()
			for event in pygame.event.get(): # event handling loop
				if event.type == KEYUP:
					if (event.key == K_p):
						# Pausing the game
						DISPLAYSURF.fill(BGCOLOR)
						showTextScreen('Paused') # pause until a key press
						self.lastFallTime = time.time()
						self.lastMoveDownTime = time.time()
						self.lastMoveSidewaysTime = time.time()
					elif (event.key == K_LEFT or event.key == K_a):
						self.movingLeft = False
					elif (event.key == K_RIGHT or event.key == K_d):
						self.movingRight = False
					elif (event.key == K_DOWN or event.key == K_s):
						self.movingDown = False

				elif event.type == KEYDOWN:
					# moving the piece sideways
					if (event.key == K_LEFT or event.key == K_a) and self.isValidPosition(self.board, self.fallingPiece, adjX=-1):
						self.moveLeft()
					elif (event.key == K_RIGHT or event.key == K_d) and self.isValidPosition(self.board, self.fallingPiece, adjX=1):
						self.moveRight()
					# rotating the piece (if there is room to rotate)
					elif (event.key == K_UP or event.key == K_w):
						self.Rotate(1)
						if not self.isValidPosition(self.board, self.fallingPiece):
							self.Rotate(-1)
					elif (event.key == K_q): # rotate the other direction
						self.Rotate(-1)
						if not self.isValidPosition(self.board, self.fallingPiece):
							self.Rotate(1)

					# making the piece fall faster with the down key
					elif (event.key == K_DOWN or event.key == K_s):
						self.movingDown = True
						if self.isValidPosition(self.board, self.fallingPiece, adjY=1):
							self.fallingPiece['y'] += 1
						self.lastMoveDownTime = time.time()

					# move the current piece all the way down
					elif event.key == K_SPACE:
						self.movingDown = False
						self.movingLeft = False
						self.movingRight = False
						for i in range(1, self.BOARDHEIGHT):
							if not self.isValidPosition(self.board, self.fallingPiece, adjY=i):
								break
						self.fallingPiece['y'] += i - 1

			# handle moving the piece because of user input
			if (self.movingLeft or self.movingRight) and time.time() - self.lastMoveSidewaysTime > self.MOVESIDEWAYSFREQ:
				if self.movingLeft and self.isValidPosition(self.board, self.fallingPiece, adjX=-1):
					self.fallingPiece['x'] -= 1
				elif self.movingRight and self.isValidPosition(self.board, self.fallingPiece, adjX=1):
					self.fallingPiece['x'] += 1
				self.lastMoveSidewaysTime = time.time()

			if self.movingDown and time.time() - self.lastMoveDownTime > self.MOVEDOWNFREQ and self.isValidPosition(self.board, self.fallingPiece, adjY=1):
				self.fallingPiece['y'] += 1
				self.lastMoveDownTime = time.time()

			# let the piece fall if it is time to fall
			if time.time() - self.lastFallTime > self.fallFreq:
				# see if the piece has landed
				if not self.isValidPosition(self.board, self.fallingPiece, adjY=1):
					# falling piece has landed, set it on the board
					self.addToBoard(self.board, self.fallingPiece,self.PIECES)
					self.score += self.removeCompleteLines(self.board)
					self.level, self.fallFreq = self.scoreboard.calculateLevelAndFallFreq(self.score)
					self.fallingPiece = None
				else:
					# piece did not land, just move the piece down
					self.fallingPiece['y'] += 1
					self.lastFallTime = time.time()

			# drawing everything on the screen
			self.DISPLAYSURF.fill(self.BGCOLOR)
			self.drawBoard(self.board)
			self.drawStatus(self.score, self.level)
			self.drawNextPiece(self.nextPiece,self.PIECES)
			if self.fallingPiece != None:
				self.drawPiece(self.fallingPiece)

			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)
	def terminate(self):
		pygame.quit()
		sys.exit()
	def checkForKeyPress(self):
		# Go through event queue looking for a KEYUP event.
		# Grab KEYDOWN events to remove them from the event queue.
		self.checkForQuit()

		for event in pygame.event.get([KEYDOWN, KEYUP]):
			if event.type == KEYDOWN:
				continue
			return event.key
		return None
	def showTextScreen(self,text):
		# This function displays large text in the
		# center of the screen until a key is pressed.
		# Draw the text drop shadow
		titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTSHADOWCOLOR)
		titleRect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2))
		self.DISPLAYSURF.blit(titleSurf, titleRect)

		# Draw the text
		titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTCOLOR)
		titleRect.center = (int(self.WINDOWWIDTH / 2) - 3, int(self.WINDOWHEIGHT / 2) - 3)
		self.DISPLAYSURF.blit(titleSurf, titleRect)

		# Draw the additional "Press a key to play." text.
		pressKeySurf, pressKeyRect = self.makeTextObjs('Press a key to play.', self.BASICFONT, self.TEXTCOLOR)
		pressKeyRect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2) + 100)
		self.DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

		while self.checkForKeyPress() == None:
			pygame.display.update()
			self.FPSCLOCK.tick()

	def checkForQuit(self):
		for event in pygame.event.get(QUIT): # get all the QUIT events
			self.terminate() # terminate if any QUIT events are present
		for event in pygame.event.get(KEYUP): # get all the KEYUP events
			if event.key == K_ESCAPE:
				self.terminate() # terminate if the KEYUP event was for the Esc key
			pygame.event.post(event) # put the other KEYUP event objects back

	def convertToPixelCoords(self,boxx, boxy):
		# Convert the given xy coordinates of the board to xy
		# coordinates of the location on the screen.
		return (self.XMARGIN + (boxx * self.BOXSIZE)), (self.TOPMARGIN + (boxy * self.BOXSIZE))


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
	def makeTextObjs(self,text, font, color):
	    surf = font.render(text, True, color)
	    return surf, surf.get_rect()


	
	
