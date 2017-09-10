import pygame,sys,time, copy

from pygame.locals import* 

import random

pygame.font.init()		# Load font module and font to use
myfont = pygame.font.SysFont("Comic Sans MS", 15)
scorefont = pygame.font.SysFont("Comic Sans MS", 45)


#Canvas properties
BLOCK_SIZE = 15		# Pixel size of blocks 
TOP_BOTTOM_OFFSET=1	# Top and bottom blocks to render as "wall"
SIDE_OFFSET = 1		# "wall" width of gamezones
ZONE_HEIGHT = 30	# Total height of gamezone
ZONE_WIDTH =10		# Total width of gamezone
OFFSET = []
EMPTY_LINE = []

SCORE =0
score_surface = scorefont.render("{0}".format(SCORE), 1, (255,255,255))
#Build bottom/top walls
for i in range(3*(2*SIDE_OFFSET + ZONE_WIDTH)):
	OFFSET.append(99)
#Build empty line
for i in range(ZONE_WIDTH):
	EMPTY_LINE.append(0)
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
GAME_ALIVE = True
CONSOLE_DEBUG = False

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
		self.filled_spaces = None
		self.filled_rotated = None
		self.color = None
		self.externals = []

	def getIndexes(self):
		"""Returns touples of non zero contents in game space"""
		indexes=[]
		for j in range(len(self.space)):
			subindex = [i for i, e in enumerate(self.space[j]) if e != 0]
			if subindex!=[]:
				for k in subindex:
					indexes.append([j,k])
		self.filled_spaces=indexes

	def rotate(self):
		"""Rotates space slicing"""
		rotated = list(zip(*self.filled_spaces[::-1]))
		self.filled_rotated = rotated

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

def rollNext(next_block):
	"""Changes next block to falling block, generates new next"""
	falling=copy.deepcopy(next_block)	#Copy next to falling
	next_block = create_block()		#Generate next Block
	falling.getIndexes()
	return falling, next_block

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
				pygame.draw.rect(window, (YELLOW[0],YELLOW[1],YELLOW[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
			elif matrix[i][j] == 1:		#Render falling block in specified color
				pygame.draw.rect(window, (color[0],color[1],color[2],0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)

def drawNext(window, next_block):
	"""Renders next block"""
	color=next_block.color
	x_render=2
	y_render=40
	for i in range(len(next_block.shape)):
		x = x_render + i
		for j in range(len(next_block.shape[i])):
			y = y_render + j
			if next_block.shape[i][j] == 1:
				pygame.draw.rect(window, (color[0],color[1],color[2],0),(y*BLOCK_SIZE, x*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)

def overlayBlock(falling_block, zones):
	"""Overlays current falling block to appropiate zone"""
	zone=[]
	overlay_zone=falling_block.zone 		
	zone=copy.deepcopy(zones[overlay_zone].space)
	x_init=falling_block.x
	y_init=falling_block.y
	shape = falling_block.shape
	falling_block.getIndexes()
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

def addBlockToZone(falling_block, zones):
	"""Adds a colliding or bottom falling block to fixed space"""
	zone = zones[falling_block.zone]
	game_space = zone.space
	x_init = falling_block.x 		#Get block coordinates
	y_init = falling_block.y
	color = falling_block.color 		#Acording to block color, chose fillercolor
	if color == BLUE: filler = 10
	elif color == RED: filler = 20
	elif color == YELLOW: filler = 30
	else: 						# If such color doesn´t exist, ignore
		print("addBlockToZone: Invalid color of falling block!")
		filler = 1
	if zone.color == None:			# If zone is not yet defined, define a color
		zone.color = copy.deepcopy(falling_block.color)
	if zone.color == falling_block.color:	# If correct color zone, add all to zone
		for index in falling_block.indexes:
			x = x_init + index[0]
			y = y_init + index[1]
			game_space[x][y]=filler 		#Fill space with previous block
	else: 
		print("Not correct zone! Penalty!")
		i=0							# Add 2 squares to this zone, one to each other zone
		for index in reversed(falling_block.indexes):
			i+=1
			x = x_init + index[0]
			y = y_init + index[1]
			zone.externals.append([x,y])
			game_space[x][y]=filler
			if i == 2: break
		addPenalty(zones, falling_block,1)
		addPenalty(zones, falling_block,2)

	if CONSOLE_DEBUG: print("Deleting block and creating new one")
	return create_block()			#Create new block

def addPenalty(zones, falling_block, number):
	"""Adds penalty to other zones"""
	color = zones[falling_block.zone].color
	if color == BLUE: filler = 10
	elif color == RED: filler = 20
	elif color == YELLOW: filler = 30
	else: 						# If such color doesn´t exist, ignore
		print("addPenalty: Invalid color of zone space!")
		filler = 1
	zone = zones[(falling_block.zone + number)%3]
	game_space = zone.space
	col = random.randint(0,9)
	if zone.filled_spaces == None:	# If empty zone, add at bottom at random
		game_space[29][col] = filler
		zone.externals.append([29,col])
	else:
		toAppended = True
		lower=29
		while(toAppended):
			if find_element_in_list([lower,col], zone.filled_spaces) == None:
				game_space[lower][col] = filler
				zone.externals.append([lower,col])
				if CONSOLE_DEBUG: print("addPenalty: Appending to:", [lower,col])
				toAppended = False
			else:
				lower-=1
				if CONSOLE_DEBUG: print("addPenalty: Non empty space, trying again")
				toAppended= True
				
	zone.getIndexes()				# Update indexes and outliers in zone
	zone.rotate()
	print(zone.filled_spaces)
	
def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None

def isValidMove(indexes, x_init, y_init, space):
	"""Check if movement is valid"""
	for index in indexes:				#Iterate over known filled in shape
		x = x_init + index[0]
		y = y_init + index[1]
		if(x< ZONE_HEIGHT and x>=0):		#Operate if in valid space X
			if(y < ZONE_WIDTH and y>=0):	#Operate if in valid y space
				if(space[x][y]==0):		#If space is empty
					pass
				else:
					if CONSOLE_DEBUG: print("Collision!")
					if (x_init == 0):
						gameOver()
					return False
			else: return False
		else: return False
	return True

def checkColission(falling_block, zones, next_block):
	"""Check for collition, append to zone if true, fall if not"""
	zone = falling_block.zone 		# Get space zone to operate
	game_space = zones[zone].space 	# Check if falling is valid 
	if isValidMove(falling_block.indexes, falling_block.x+1, falling_block.y, game_space):
		falling_block.fall()		# Fall if is valid
		if CONSOLE_DEBUG: blockStatus(falling_block)
	else:						#If not valid, append to zone as filled space
		if CONSOLE_DEBUG: print("Appending to zone.space")
		falling_block=addBlockToZone(falling_block, zones)
		zones[zone].getIndexes() 	# Refresh filled spaces
		zones[zone].rotate()
		return rollNext(next_block)	# Roll to next block
	return falling_block, next_block

def checkForScore(zones):
	"""Evaluates zones for completed lines"""
	for zone in zones:							#Iterate over non empty zones
		completed_lines=[]
		valid_lines = None
		if zone.filled_rotated != None and len(zone.filled_rotated)>0:
			rows = zone.filled_rotated[0]			# Rename fo clarity
			cols = zone.filled_rotated[0]
			last_row = 99						# If 10 times a row appears, is
			counter = 0						# a completed line
			for row in rows:
				if row == last_row :
					counter += 1
				else:
					counter = 0
					last_row = row
				if counter == ZONE_WIDTH -1:
					completed_lines.append(row)
					print("Completed line in ROW %i"%row)
			#checkForOutliers					# Check and discard lines of outliers
			valid_lines = completed_lines
			if valid_lines != None:
				for line in completed_lines:			# Remove valid lines, replace with empty ones at top
					del zone.space[line]
					zone.space.insert(0, copy.deepcopy(EMPTY_LINE))
					if CONSOLE_DEBUG: print("Deleting line in ROW %i"%line)
					global SCORE
					global score_surface
					SCORE += 1
					score_surface = scorefont.render("{0}".format(SCORE), 1, (255,255,255))
				zone.getIndexes()
				zone.rotate()


def evaluateGame(falling_block, zones):
	"""Appends all zones and overlays falling block before rendering"""
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

def gameOver():
	global GAME_ALIVE
	GAME_ALIVE = False
	print("Game Over!!")

def renderText(window, text, x=0, y=0):
	"""Render text"""
	text_render = myfont.render(text, 1, (255,255,255))
	window.blit(text_render,(x,y))
	window.blit(score_surface,(625,150))

def mainWindow():
	global FALLING_OBJECT
	window = pygame.display.set_mode((800,600))
	zones=createZones();	#Create Board to play in
	falling = None
#	pygame.font.init()
#	myfont = pygame.font.SysFont("Comic Sans MS", 15)
	#Next_piece_surface = myfont.render('Next piece', 1, (255,255,255))
	#Create new block: Game Start
	next_block = create_block()
	falling, next_block = rollNext(next_block)	# Get next block
	FALLING_OBJECT = True
	if CONSOLE_DEBUG: blockStatus(falling)

	while GAME_ALIVE:
		window.fill((0,0,0))		
		toRender = evaluateGame(falling, zones)
		if FALLING_OBJECT: drawMatrix(window, toRender, falling.color)
		else: drawMatrix(window, toRender, RED)
		drawNext(window, next_block)
		renderText(window, "Next Block", 600, 0)
		
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
						if CONSOLE_DEBUG: blockStatus(falling)
					#else: print("No change! Interference")
					del future_block
						
				if events.key==K_LEFT:
					print ("<")
					if isValidMove(falling.indexes, falling.x, falling.y-1, zones[falling.zone].space):
						falling.move(-1)
						if CONSOLE_DEBUG: blockStatus(falling)
				if events.key==K_RIGHT:
					print (">")
					if isValidMove(falling.indexes, falling.x, falling.y+1, zones[falling.zone].space):
						falling.move(1)	
						if CONSOLE_DEBUG: blockStatus(falling)
				if events.key==K_RETURN:
					print ("ENTER")
					falling.changeZone()
				if events.key==K_DOWN:
					print ("v")
					falling, next_block = checkColission(falling, zones, next_block)
					#checkForScore(zones)

		pygame.display.update()
		time.sleep(.2)
		falling, next_block = checkColission(falling, zones, next_block);	#Fall piece
		checkForScore(zones)
		print(SCORE)

mainWindow()