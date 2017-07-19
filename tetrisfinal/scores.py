__author__="Nikhil Rayaprolu"
__version__ = "1.0.0"
__maintainer__ = "Nikhil Rayaprolu"
__email__ = "nikhil.rayaprolu@students.iiit.ac.in"
__status__ = "Development"


import pygame

class Score():

	def __init__(self):
		
		pass
	
	def calculateLevelAndFallFreq(self,score):
	    level = int(score / 10) + 1
	    fallFreq = 0.27 - (level * 0.02)
	    return level, fallFreq
