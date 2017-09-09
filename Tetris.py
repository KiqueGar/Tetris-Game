import pygame,sys,time, copy

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

FALLING_OBJECT=False

class falling_block(object):
	"""Falling Object Class"""
	def __init__(self):
		self.name = None
		self.shape = None
		self.x = None		# X coordinate is from top to bottom
		self.y = None		# Y Cordinate is from left to right
		self.color = None
		self.zone = None
		self.indexes =None

	def rotate(self):
		"""Rotates block"""
		if self.name== 'O': return
		rotated = list(zip(*self.shape[::-1]))
		self.shape = rotated
		self.getIndexes()

	def move(self, dir):
		"""Moves block sideways"""
		self.y+=dir

	def fall(self):
		"""Falls block 1 space"""
		self.x+=1

	def changeZone(self):
		"""Changes game zone"""
		self.zone = (self.zone+1)%3

	def getIndexes(self):
		"""Returns touples of non zero coordinates in shape"""
		indexes=[]
		for j in range(len(self.shape)):
			subindex = [i for i, e in enumerate(self.shape[j]) if e != 0]
			if subindex!=[]:
				for k in subindex:
					indexes.append([j,k])
		self.indexes=indexes

class gameZone(object):
	"""Game Zone object"""
	def __init__(self):
		self.height = ZONE_HEIGHT
		self.width = ZONE_HEIGHT
		self.space = None

def createZones():
	"""Creates 3 gameZone objects, return them in array"""
	zone1 = gameZone()
	zone1.space = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
	zone2 = gameZone()
	zone2.space = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
	zone3 = gameZone()
	zone3.space = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)

	return [zone1, zone2, zone3]

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
	block.getIndexes()
	return block

def addBlockToZone(falling_block, game_space):
	"""Adds a colliding or bottom falling block to fixed space"""
	
	print("Deleting block and creating new one")
	return create_block()

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
		new_row.extend(matrix2[i].copy())		#Add Zone 2
		for j in range(SIDE_OFFSET):	#Add double wall between zones
			new_row.append(99)
			new_row.append(99)
		new_row.extend(matrix3[i].copy())		#Add zone 3
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
			elif matrix[i][j] == 10:	#Render as blue
				pygame.draw.rect(window, (BLUE[0],BLUE[1],BLUE[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
			elif matrix[i][j] == 20:	#Render as red
				pygame.draw.rect(window, (RED[0],RED[1],RED[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
			elif matrix[i][j] == 30:	#Render as yellow
				pygame.draw.rect(window, (RED[0],RED[1],RED[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
			elif matrix[i][j] == 1:		#Render falling block in specified color
				pygame.draw.rect(window, (color[0],color[1],color[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
		pass
def overlayBlock(falling_block, zones):
	"""Overlays current falling block to appropiate zone"""
	overlay_zone=falling_block.zone
	zone=copy.deepcopy(zones[overlay_zone].space)

	#TODO detect collision here
	x_init=falling_block.x
	y_init=falling_block.y
	shape = falling_block.shape

	for index in falling_block.indexes:
		x = x_init + index[0]
		y = y_init + index[1]
		if(x< ZONE_HEIGHT and x>=0):		#Operate if in valid space X
			if(y < ZONE_WIDTH and y>=0):	#Operate if in valid y space
				zone[x][y]=1
			else: print("Out of bounds in Y!")
		else: print("Out of bound in X!!")
	#Modify relevant matrix and return
	if overlay_zone ==0: return [zone, zones[1].space, zones[2].space]
	elif overlay_zone ==1: return [zones[0].space, zone, zones[2].space]
	elif overlay_zone ==2: return [zones[0].space, zones[1].space, zone]

def isValidMove(indexes, x_init, y_init, space):
	"""Check if movement is valid"""
	for index in indexes:
		x = x_init + index[0]
		y = y_init + index[1]
		if(x< ZONE_HEIGHT and x>=0):		#Operate if in valid space X
			if(y < ZONE_WIDTH and y>=0):	#Operate if in valid y space
				if(space[x][y]==0):		#If space is empty
					pass
				else:
					print("Collision!")
					return False
			else: return False
		else: return False
	return True

def checkColission(falling_block, game_space):
	"""Check for collition, append to zone if true, fall if not"""
	if isValidMove(falling_block.indexes, falling_block.x+1, falling_block.y, game_space):
		falling_block.fall()
		blockStatus(falling_block)
	else:
		print("Appending to zone.space")
		falling_block=addBlockToZone(falling_block, game_space)
	return falling_block

def evaluateGame(falling_block, zones):
	if FALLING_OBJECT:
		overlay = overlayBlock(falling_block, zones)
		#return joinMatrix(zones[0].space,zones[1].space,zones[2].space)
		return joinMatrix(overlay[0],overlay[1],overlay[2])
	else:
		return joinMatrix(zones[0].space,zones[1].space,zones[2].space)

def showMatrix(matrix): 
	"""Prints a matrix to console for debug"""
	for i in range(len(matrix)):
		print(matrix[i]) 

def blockStatus(block):
	"""Prints to console data about block object"""
	print(block.name, [block.x, block.y])
	print(block.indexes)
	print(block.color)
	showMatrix(block.shape)

def mainWindow():
	global FALLING_OBJECT
	window = pygame.display.set_mode((800,600))
	zones=createZones();	#Create Board to play in
	falling = None

	#Create new block: Game Start
	falling = create_block()
	FALLING_OBJECT = True
	blockStatus(falling)

	while True:
		window.fill((0,0,0))		
		toRender = evaluateGame(falling, zones)
		if FALLING_OBJECT: drawMatrix(window, toRender, falling.color)
		else: drawMatrix(window, toRender, RED)
		for events in pygame.event.get():
			if events.type == QUIT:
				pygame.quit()
				sys.exit()
			elif events.type == KEYDOWN:
				if events.key==K_UP:
					print ("^")
					future_block=copy.deepcopy(falling)	#Create a copy of block
					future_block.rotate()
					if isValidMove(future_block.indexes, future_block.x, future_block.y, zones[future_block.zone].space):
						falling.rotate()
						blockStatus(falling)
					#else: print("No change! Interference")
					del future_block
						
				if events.key==K_LEFT:
					print ("<")
					if isValidMove(falling.indexes, falling.x, falling.y-1, zones[falling.zone].space):
						falling.move(-1)
						blockStatus(falling)
				if events.key==K_RIGHT:
					print (">")
					if isValidMove(falling.indexes, falling.x, falling.y+1, zones[falling.zone].space):
						falling.move(1)	
						blockStatus(falling)
				if events.key==K_RETURN:
					print ("ENTER")
					falling.changeZone()
				if events.key==K_DOWN:
					print ("v")
					falling = checkColission(falling, zones[falling.zone].space)

		pygame.display.update()
		time.sleep(.1)
		falling = checkColission(falling, zones[falling.zone].space);		#Fall piece



mainWindow()