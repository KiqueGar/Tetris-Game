import pygame,sys,time

from pygame.locals import* 

from random import randint 


def createMatrix(n,m):
	"""Creates matrix to be used as container of blocks"""
	matrix = []
	for i in range(n):
		matrix.append([])
		for j in range(m):
			matrix[i].append(0)
	return matrix

def joinMatrix(matrix1, matrix2):
	"""Appends colums of matrix 2 to matrix 1"""
	if len(matrix1)!=len(matrix2):
		print ("joinMatrix: Matrices must be of same height!")
		return matrix1
	new_matrix=[]
	"""
	for i in range(len(matrix1)):
		new_col = matrix1[i]
		new_col.append(99)
		new_col.extend(matrix2[i])
		new_matrix.append(new_col)
	"""
	for i in range(len(matrix1)):
		new_row = matrix1[i].copy()
		new_row.append(99)
		new_row.extend(matrix2[i])
		new_matrix.append(new_row)
	return new_matrix

def showMatrix(matrix): 
	"""Prints a matrix to console for debug"""
	for i in range(len(matrix)):
		print(matrix[i]) 


def window():
	window = pygame.display.set_mode((600,700))


	while True:
		window.fill((0,0,0))
		canvas1 = createMatrix(20,10)
		canvas2 = createMatrix(20,10)
		canvas3 = createMatrix(20,10)

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



window()