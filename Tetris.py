import pygame,sys,time,copy,math

from pygame.locals import* 

import random

pygame.font.init()		# Load font module and font to use
myfont = pygame.font.SysFont("Arial", 15)
scorefont = pygame.font.SysFont("Arial", 45)
gameOverfont = pygame.font.SysFont("Comic Sans MS", 15)


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
gameOver_surface = gameOverfont.render("GAME OVER", 1, (0,0,255))
#Build bottom/top walls
for i in range(3*(2*SIDE_OFFSET + ZONE_WIDTH)):
	OFFSET.append(99)
#Build empty line
for i in range(ZONE_WIDTH):
	EMPTY_LINE.append(0)
#Color definitions
BLUE = [0,191,255]
RED = [205, 30, 16]
YELLOW =[255,255,0]
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
FALLING_CPU = False
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
	
	def updateExternals(self):
		"""Updates external indexes"""
		color = self.color
		if color == None:					# If no assigned color, all are outliers
			self.externals = copy.deepcopy(self.filled_spaces)
			return
		if color == BLUE: match = 10			#Use a different match acording to zone color
		elif color == RED: match = 20
		elif color == YELLOW: match = 30
		outliers=[]						# Iterate across filled space detecting outliers
		for filled in self.filled_spaces:
			if self.space[filled[0]][filled[1]] != match:
				outliers.append(filled)
		if len(outliers)<1:
			return
		else:
			self.externals = copy.deepcopy(outliers)

	def rotate(self):
		"""Rotates space slicing"""
		rotated = list(zip(*self.filled_spaces[::-1]))
		self.filled_rotated = rotated

	def fallAfterDelete(self, coordinate):
		"""Falls column after deleting element at coordinate"""
		for i in range(coordinate[0],0,-1):		#Iterate backwards from removed item
			upper=self.space[i-1][coordinate[1]]
			if upper !=0:						#If upper block exist
				self.space[i][coordinate[1]] = upper
			else:
				if CONSOLE_DEBUG: print("fallAfterDelete: Interrupting at row: ", i)
				self.space[i][coordinate[1]] = upper
				break
				
		self.getIndexes()
		self.rotate()
		self.updateExternals()
		if CONSOLE_DEBUG: print("fallAfterDelete: Rolled down!")

	def deleteExternal(self):
		"""Delete an external from space"""
		element = random.randint(0, len(self.externals)-1)
		outlier = self.externals[element]
		print("deleting: ", outlier)
		self.space[outlier[0]][outlier[1]]=0
		self.fallAfterDelete(outlier)

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
		if CONSOLE_DEBUG: print ("joinMatrix: Matrices must be of same height!")
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
		if CONSOLE_DEBUG: print("Not correct zone! Penalty!")
		i=0							# Add 2 squares to this zone, one to each other zone
		for index in reversed(falling_block.indexes):
			i+=1
			x = x_init + index[0]
			y = y_init + index[1]
			game_space[x][y]=filler
			zone.getIndexes()
			zone.updateExternals()
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
	else:
		toAppended = True
		lower=29
		while(toAppended):
			if find_element_in_list([lower,col], zone.filled_spaces) == None:
				game_space[lower][col] = filler
				if CONSOLE_DEBUG: print("addPenalty: Appending to:", [lower,col])
				toAppended = False
			else:
				lower-=1
				if CONSOLE_DEBUG: print("addPenalty: Non empty space, trying again")
				toAppended= True
				
	zone.getIndexes()				# Update indexes and outliers in zone
	zone.updateExternals()
	zone.rotate()
	
def removePenalty(zones, seed):
	"""Removes a penalty from zone (if exist), attemps 2 times"""
	index=seed%3							#Check if zone has outliers, if not, try again
	if zoneHasExternals(zones[index]):
		zone=zones[index]					#Delete external
		zone.deleteExternal()
	else:
		"""
		if zoneHasExternals(zones[(index+1)]%3):
			#Delete external, second attempt
			pass
		else: return						#If second attempt didn´t work, do nothing
		"""
		return

def cancelPenalty(zone, position):
	"""Cancels a penalty and converts it to right color in zone"""
	if zone.color == None: return 	#If zone has no color yet, do nothing
	work_space = zone.space 			#Read current space
	outlier_list = zone.externals
	if find_element_in_list(position, outlier_list) == None:
		if CONSOLE_DEBUG: print("No outlier here!")	#If no outlier, do nothing
		return
	else:						#If outlier there, replace
		color = zone.color 			#Get correct color
		if color == BLUE: filler = 10
		elif color == RED: filler = 20
		elif color == YELLOW: filler = 30
		work_space[position[0]][position[1]]=filler
		zone.getIndexes()
		zone.rotate()
		zone.updateExternals()
		return



def zoneHasExternals(zone):
	"""Test if zone has outliers on it"""
	if len(zone.externals)>0:
		#print("Zone has externals!")
		return True
	return False

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
					if CONSOLE_DEBUG: print("isValidMove: Collision!")
					if (x_init == 0):
						gameOver()
					return False
			else: return False
		else: return False
	return True

def isValidChange(zones, falling_block, number):
	"""Check if change between zones is valid"""
	zone = zones[(falling_block.zone+number)%3]
	return isValidMove(falling_block.indexes, falling_block.x, falling_block.y, zone.space) 
	
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

def checkForOutliers(lines, outliers_list):
	valid_lines=[]
	outlier_line=[]				# Get lines of outliners
	if CONSOLE_DEBUG: print("Checking for outliers")
	for outlier in outliers_list:
		outlier_line.append(outlier[0])
	if lines == None:				#If no lines yet, do nothing
		return None
	for line in lines:
		if find_element_in_list(line, outlier_line) == None:
			valid_lines.append(line)
		else:
			if CONSOLE_DEBUG: print("checkForOutliers: Line has outlier! Not removing")
	if len(valid_lines)<1:
		return None
	else:
		return valid_lines

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
					if CONSOLE_DEBUG: print("Possible line in ROW %i"%row)
			if len(zone.externals)>0:			# Check and discard lines of outliers
				valid_lines = checkForOutliers(completed_lines, zone.externals)
			else: valid_lines = completed_lines			
			if valid_lines != None:
				for line in valid_lines:			# Remove valid lines, replace with empty ones at top
					del zone.space[line]
					zone.space.insert(0, copy.deepcopy(EMPTY_LINE))
					print("Deleting line in ROW %i"%line)
					global SCORE
					global score_surface
					SCORE += 1
					removePenalty(zones, SCORE)	# Remove an outlier
					score_surface = scorefont.render("{0}".format(SCORE), 1, (255,255,255))
				zone.getIndexes()
				zone.updateExternals()
				zone.rotate()
	global FALLING_CPU
	if FALLING_CPU == False:			#Start CPU player after first row
		if SCORE > 1:
			FALLING_CPU = True
			print("Starting CPU")

def fallingSpeed():
	"""Returns interval between blocks as function of score"""
	global SCORE
	if SCORE <=10: return 0.3
	else: return 0.3*(1 - math.exp(-5/(SCORE-5)))

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
	print("Game Over!!")
	GAME_ALIVE = False

def renderText(window, text, x=0, y=0):
	"""Render text"""
	text_render = myfont.render(text, 1, (255,255,255))
	window.blit(text_render,(x,y))
	window.blit(score_surface,(625,150))
	window.blit(gameOver_surface,(200,600))

def clearRedraw(window, falling, zones, next_block):
	"""Clears screen and draws game"""
	window.fill((0,0,0))		
	toRender = evaluateGame(falling, zones)
	if FALLING_OBJECT: drawMatrix(window, toRender, falling.color)
	else: drawMatrix(window, toRender, RED)
	drawNext(window, next_block)
	renderText(window, "Next Block", 600, 0)
	renderText(window, "Controls:", 540,250)
	renderText(window, "- Use Arrows to move", 550,270)
	renderText(window, "- Left CTRL and Left ALT", 550,290)
	renderText(window, "  changes zones Try it!", 550,310)
	renderText(window, "Tips:", 540,350)
	renderText(window, "- Keep the same color per zone", 550,370)
	renderText(window, "  (Penalties doesn´t count)", 550,390)
	renderText(window, "- Penalties are removed on scoring", 550,410)
	renderText(window, "Try to score above 35   :)", 560,450)

def mapMousePos(pos):
	"""Maps Mouse position to relevant game zone, returns area an coords"""
	x_block = int(pos[0]/BLOCK_SIZE)
	y_block = int(pos[1]/BLOCK_SIZE)
	#print("Evaluating:", [y_block,x_block])
	if y_block<SIDE_OFFSET or y_block>ZONE_HEIGHT:	# Trim outside of bounds
		#print("No valid Zone!, Out of Y")
		return None, None
	if x_block<TOP_BOTTOM_OFFSET or x_block>(5*(SIDE_OFFSET) + 3*(ZONE_WIDTH)):
		#print("No valid Zone! Out of X")
		return None, None
	#Area 0
	if x_block>=SIDE_OFFSET and x_block < ZONE_WIDTH + SIDE_OFFSET:
		x = y_block- TOP_BOTTOM_OFFSET
		y = x_block - SIDE_OFFSET
		return 0, [x,y]
	#Area 1
	if x_block>=(3*(SIDE_OFFSET) + ZONE_WIDTH) and x_block<(3*(SIDE_OFFSET) + 2*ZONE_WIDTH):
		x = y_block - TOP_BOTTOM_OFFSET
		y = x_block-(3*(SIDE_OFFSET) + ZONE_WIDTH)
		return 1, [x,y]
	#Area 2
	if x_block>=(5*(SIDE_OFFSET) + 2*ZONE_WIDTH) and x_block<(5*(SIDE_OFFSET) + 3*ZONE_WIDTH):
		x = y_block - TOP_BOTTOM_OFFSET
		y = x_block-(5*(SIDE_OFFSET) + 2*ZONE_WIDTH)
		return 2, [x,y]
	#No other area
	else:
		#print("No valid area!")
		return None, None

def zoneCost(zones, block):
	"""Cost of being in zone"""
	cost = 100						# Maximum cost of bad zone
	color = block.color 				# Current block color
	currentZone=block.zone 				# Current location
	if zones[currentZone].color == None:	# If no color assigned to Zone, zone is Ok
		#print("Entering empty color zone")
		return 0
	if zones[currentZone].color != color:	# If zone color is not block color, return cost
		return cost
	else:
		#print("Maching color zone and block")
		return 0 # If color matches, no cost of being here

def calculateCosts(zones, future_block):
	"""Calculates cost of possible action"""
	cumulative = int(0)
	cumulative += zoneCost(zones, future_block)

	return cumulative

def CPUMove(zones, block):
	"""Makes a move for the CPU block"""
	ultimate_cost = int(1e10)
	policy = []						# Holder for costs at each move
									#Cost of staying
	stay_block = copy.deepcopy(block)
	print("CPUMove: Stay")
	cost = calculateCosts(zones, stay_block)
	policy.append(cost)
									#Cost of rotate
	rot_block = copy.deepcopy(block)		#Check if rotation is posible
	print("CPUMove: Rotate")
	rot_block.rotate()					
	if isValidMove(rot_block.indexes, rot_block.x, rot_block.y, zones[rot_block.zone].space):
		cost = calculateCosts(zones, stay_block)
		policy.append(cost)
	else:							#If rotation not possible, append max cost
		policy.append(ultimate_cost)
									#Cost of left
	left_block = copy.deepcopy(block)		# If move is valid, do and check for cost
	print("CPUMove: Move Left")
	if isValidMove(left_block.indexes, left_block.x, left_block.y-1, zones[left_block.zone].space):
		left_block.move(-1)
		cost = calculateCosts(zones, left_block)
		policy.append(cost)
	else:
		policy.append(ultimate_cost)		# If left not possible, append max cost
									# Cost of moving right
	right_block = copy.deepcopy(block)		# If move is valid, do and check for cost
	print("CPUMove: Move Right")
	if isValidMove(right_block.indexes, right_block.x, right_block.y+1, zones[right_block.zone].space):
		right_block.move(+1)
		cost = calculateCosts(zones, right_block)
		policy.append(cost)
	else:
		policy.append(ultimate_cost) 		# If left not possible, append max cost
									# Cost of changing zone left
	l_sh_block = copy.deepcopy(block)		# If change is valid, do and return cost
	print("CPUMove: Shift Left")
	if isValidChange(zones, l_sh_block, 2):
		l_sh_block.changeZone()
		l_sh_block.changeZone()
		cost = calculateCosts(zones, l_sh_block)
		policy.append(cost)
	else:							# If left shift not possible, append max cost
		policy.append(ultimate_cost)
									#Cost of shifting right
	r_sh_block = copy.deepcopy(block)		# If change is valid, do and return cost
	print("CPUMove: Shift Right")
	if isValidChange(zones, r_sh_block, 1):
		r_sh_block.changeZone()
		cost = calculateCosts(zones, r_sh_block)
		policy.append(cost)
	else:
		policy.append(ultimate_cost)

	
	print(policy)	
	return





def mainWindow():
	global FALLING_OBJECT
	window = pygame.display.set_mode((750,485))
	pygame.display.set_caption("Tri-Tetris")
	zones=createZones();	#Create Board to play in
	falling = None
	
	next_block = create_block()				#Create new block: Game Start
	falling, next_block = rollNext(next_block)	# Get next block
	next_cpu_block = create_block()			# Create new CPU block
	cpu_block, next_cpu_block = rollNext(next_cpu_block)			# Get CPU next block 
	cpu_block.zone=0
	FALLING_OBJECT = True

	if CONSOLE_DEBUG: blockStatus(falling)

	while GAME_ALIVE:
		clearRedraw(window, falling, zones, next_block)
		for events in pygame.event.get():
			if events.type == QUIT:
				pygame.quit()
				sys.exit()
			elif events.type == KEYDOWN:
				if events.key==K_UP:
					#print ("^")
					future_block=copy.deepcopy(falling)	#Create a copy of block
					future_block.rotate()
					if isValidMove(future_block.indexes, future_block.x, future_block.y, zones[future_block.zone].space):
						falling.rotate()
						if CONSOLE_DEBUG: blockStatus(falling)
					
					clearRedraw(window, falling, zones, next_block)
					#else: print("No change! Interference")
					del future_block
						
				if events.key==K_LEFT:
					#print ("<")
					if isValidMove(falling.indexes, falling.x, falling.y-1, zones[falling.zone].space):
						falling.move(-1)
						if CONSOLE_DEBUG: blockStatus(falling)
					clearRedraw(window, falling, zones, next_block)
				if events.key==K_RIGHT:
					#print (">")
					if isValidMove(falling.indexes, falling.x, falling.y+1, zones[falling.zone].space):
						falling.move(1)	
						if CONSOLE_DEBUG: blockStatus(falling)
					clearRedraw(window, falling, zones, next_block)
				if events.key==K_RETURN:
					#print ("ENTER")
					CPUMove(zones, falling)
				if events.key==K_DOWN:
					#print ("v")
					falling, next_block = checkColission(falling, zones, next_block)
					#checkForScore(zones)
					clearRedraw(window, falling, zones, next_block)
				if events.key==K_LCTRL:
					#print("Left CTRL")
					if isValidChange(zones, falling, 2):
						falling.changeZone()
						falling.changeZone()
					clearRedraw(window, falling, zones, next_block)
				if events.key==K_LALT:
					#print("Left Alt")
					if isValidChange(zones, falling, 1):
						falling.changeZone()
					clearRedraw(window, falling, zones, next_block)
				if events.key == K_s:
					global SCORE
					SCORE += 1
			elif events.type == pygame.MOUSEBUTTONUP:
				raw_pos = pygame.mouse.get_pos()	#Read mouse posiion and map to game zone
				delete_from_zone, sup_outlier = mapMousePos(raw_pos)
				if delete_from_zone != None:		#Delete penalty if exists
					cancelPenalty(zones[delete_from_zone], sup_outlier)
					clearRedraw(window, falling, zones, next_block)
					checkForScore(zones)
		pygame.display.update()
		time.sleep(fallingSpeed())
		falling, next_block = checkColission(falling, zones, next_block);	#Fall piece
		checkForScore(zones)
	time.sleep(2)

mainWindow()