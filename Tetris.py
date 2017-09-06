import pygame,sys,time

from pygame.locals import* 

import random

#Canvas properties
BLOCK_SIZE = 15		# Pixel size of blocks 
TOP_BOTTOM_OFFSET=1	# Top and bottom blocks to render as "wall"
SIDE_OFFSET = 1		# "wall" width of gamezones
ZONE_HEIGHT = 30	# Total height of gamezone
ZONE_WIDTH =10		# Total width of gamezone
OFFSET = []
#Build bottom/top walls
for i in range(3*(2*SIDE_OFFSET + ZONE_WIDTH)):
	OFFSET.append(99)
#Color definitions
BLUE = [66,154,223]
RED = [205, 30, 16]
YELLOW =[241,171,0]
COLORS=[BLUE, RED, YELLOW]
#Pieces Definition
SHAPE_T = [[0,0,0,0,0], [0,1,1,1,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]
SHAPE_S = [[0,0,0,0,0], [0,0,1,1,0], [0,1,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]
SHAPE_Z = [[0,0,0,0,0], [0,1,1,0,0], [0,0,1,1,0], [0,0,0,0,0], [0,0,0,0,0]]
SHAPE_J = [[0,0,0,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,0,0], [0,0,0,0,0]]
SHAPE_L = [[0,0,0,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,1,0], [0,0,0,0,0]]
SHAPE_O = [[0,0,0,0,0], [0,1,1,0,0], [0,1,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]
SHAPE_I = [[0,0,0,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0]]

SHAPES = [SHAPE_T, SHAPE_S, SHAPE_Z, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_I]
NAMES = ['T', 'S', 'Z', 'J', 'L', 'O', 'I']

class falling_block(object):
	"""Falling Object Class"""
	def __init__(self):
		self.name = None
		self.shape = None
		self.x = None		# X coordinate is from top to bottom
		self.y = None		# Y Cordinate is from left to right
		self.color = None
		self.zone = None

	def rotate(self):
		"""Rotates block"""
		rotated = list(zip(*self.shape[::-1]))
		self.shape = rotated

	def move(self, dir):
		"""Moves block sideways"""
		pass

	def fall(self):
		"""Falls block 1 space"""
		self.x+=1

	def changeZone(self):
		"""Changes game zone"""
		self.zone = (zelf.zone+1)%3


def create_block():
	"""Creates a falling object object"""
	name = random.randint(0,len(NAMES)-1)	#Select randomly a piece
	block = falling_block()
	block.name = NAMES[name]
	block.shape = SHAPES[name]
	block.color = random.choice(COLORS)
	block.zone = 1
	block.x = -1
	block.y = 3
	return block



def createMatrix(n,m):
	"""Creates matrix to be used as container of blocks"""
	matrix = []
	for i in range(n):
		matrix.append([])
		for j in range(m):
			matrix[i].append(0)
	return matrix

def joinMatrix(matrix1, matrix2, matrix3):
	"""Appends gamezones, inserts separators between zones"""
	if (len(matrix1)!=len(matrix2) or len(matrix1)!=len(matrix3)):
		print ("joinMatrix: Matrices must be of same height!")
		return matrix1
	new_matrix=[]
	for i in range(len(matrix1)):
		new_row = matrix1[i].copy()		#Insert Zone1
		for j in range(SIDE_OFFSET):	#Add walls Zone 1
			new_row.insert(0,99)
			new_row.append(99)
		for j in range(SIDE_OFFSET):	#Add left walls of zone 2
			new_row.append(99)
		new_row.extend(matrix2[i])		#Add Zone 2
		for j in range(SIDE_OFFSET):	#Add double wall between zones
			new_row.append(99)
			new_row.append(99)
		new_row.extend(matrix3[i])		#Add zone 3
		for j in range(SIDE_OFFSET):	#Add remaining wall
			new_row.append(99)
		new_matrix.append(new_row)
	for i in range(TOP_BOTTOM_OFFSET):	#Add floor and ceil
		new_matrix.insert(0, OFFSET)
		new_matrix.append(OFFSET)
	return new_matrix

def drawMatrix(window, matrix, color):
	"""Renders gamescreen"""
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			#Render walls as gray
			if matrix[i][j] == 99:
				pygame.draw.rect(window, (128,128,128,0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
			#elif matrix[i][j]:
			#	pygam
		pass

def showMatrix(matrix): 
	"""Prints a matrix to console for debug"""
	for i in range(len(matrix)):
		print(matrix[i]) 

def blockStatus(block):
	"""Prints to console data about block object"""
	print(block.name)
	print(block.color)
	showMatrix(block.shape)
	print([block.x, block.y])

def mainWindow():
	window = pygame.display.set_mode((800,600))


	while True:
		window.fill((0,0,0))
		zone1 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		zone2 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		zone3 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		toRender = joinMatrix(zone1,zone2,zone3)
		drawMatrix(window, toRender, [128,128,128])
		#showMatrix(toRender)
		for events in pygame.event.get():
			if events.type == QUIT:
				pygame.quit()
				sys.exit()
			elif events.type == KEYDOWN:
				if events.key==K_UP:
					print ("^")
					falling.rotate()
					blockStatus(falling)
				if events.key==K_LEFT:
					print ("<")
					falling.move(-1)
					blockStatus(falling)
				if events.key==K_RIGHT:
					print (">")
					falling.move(1)
					blockStatus(falling)
				if events.key==K_RETURN:
					print ("ENTER")
					falling = create_block()
					blockStatus(falling)
				if events.key==K_DOWN:
					print ("v")
					falling.fall();
					blockStatus(falling)

		pygame.display.update()
		time.sleep(.04)



mainWindow()
