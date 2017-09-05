import pygame,sys,time

from pygame.locals import* 

from random import randint 

BLOCK_SIZE = 15
TOP_BOTTOM_OFFSET=1
SIDE_OFFSET = 1
ZONE_HEIGHT = 30
ZONE_WIDTH =10
OFFSET = []
#Build bottom/top offset
for i in range(3*(2*SIDE_OFFSET + ZONE_WIDTH)):
	OFFSET.append(99)

def createMatrix(n,m):
	"""Creates matrix to be used as container of blocks"""
	matrix = []
	for i in range(n):
		matrix.append([])
		for j in range(m):
			matrix[i].append(0)
	return matrix

def joinMatrix(matrix1, matrix2):
	"""Appends colums of matrix 2 to matrix 1, inserts separators inside"""
	if len(matrix1)!=len(matrix2):
		print ("joinMatrix: Matrices must be of same height!")
		return matrix1
	new_matrix=[]
	last_index= len(new_matrix) +1
	for i in range(len(matrix1)):
		new_row = matrix1[i].copy()
		new_row.append(99)
		new_row.extend(matrix2[i])
		new_matrix.append(new_row)
	#for i in range(TOP_BOTTOM_OFFSET):
	#	new_matrix.insert(0, OFFSET)
	#	new_matrix.append(OFFSET)
	return new_matrix

def drawMatrix(window, matrix, color =[128,0,128]):
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			#Render walls as gray
			if matrix[i][j] == 99:
				pygame.draw.rect(window, (128, 128, 128,0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
				pass
			pass

def showMatrix(matrix): 
	"""Prints a matrix to console for debug"""
	for i in range(len(matrix)):
		print(matrix[i]) 


def mainWindow():
	window = pygame.display.set_mode((600,500))


	while True:
		window.fill((0,0,0))
		zone1 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		zone2 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		zone3 = createMatrix(ZONE_HEIGHT,ZONE_WIDTH)
		toRender = joinMatrix(joinMatrix(zone1,zone2),zone3)
		drawMatrix(window, toRender, [128,128,128])
		#showMatrix(toRender)
		for events in pygame.event.get():
			if events.type == QUIT:
				pygame.quit()
				sys.exit()
			elif events.type == KEYDOWN:
				if events.key==K_UP:
					print ("Up") 
				if events.key==K_LEFT:
					print ("Left") 
				if events.key==K_RIGHT:
					print ("Right") 
				if events.key==K_RETURN:
					print ("ENTER") 
				if events.key==K_DOWN:
					print ("Down") 




		pygame.display.update()
		time.sleep(.04)



mainWindow()