# -*- coding: utf-8 -*-	
# Algoritmo para realizar a recessão espacial com uma fotografia e quatro pontos de controle
# Utiliza-se como modelo funcional as equações de colinearidade
# Desenvolvido por Natália Carvalho - Universidade Federal do Paraná

import numpy as np
import cv2 as cv
from sympy import *
from numpy.linalg import inv


#Enter with de parameters of interior orientation

c = 50 #Focal lengh in milimeters

#coordinates of principal point im milimeters
x0 = -0.223
y0 = 0.051

#Radial Distortion coeficients

K1 = -1.5604645*10**-5
K2 = 4.0643961*10**-9
K3 = 0

#Decentering Distortion coeficients P1 and P2

P1 = 0
P2 = 0

def calculateRadialDist(x_obs, y_obs):

	#calculating r
	r = np.sqrt(x_obs**2 + y_obs**2)

	#calculating dx and dy
	dx = (K1*r**2 + K2*r^4 + K3*r^6)*x_obs
	dy = (K1*r**2 + K2*r^4 + K3*r^6)*y_obs

	radialDist = [dx, dy]

	return radialDist

def calculateDecentringDist(x_obs, y_obs):

	#calculating r
	r = np.sqrt(x_obs**2 + y_obs**2)

	#calculate dx and dy
	dx = P1*(r**2 + 2*x_obs**2) + 2*P2*x_obs*y_obs
	dy = 2*P1*x_obs*y_obs + P2(r**2 + 2*y_obs**2)

	decentringDist = [dx, dy]

	return decentringDist



def photogrametricCorrection(radialList, decentringList, x_obs, y_obs):

	x_corrected = x_obs + radialList[0] + decentringList[0]
	y_corrected = y_obs + radialList[1] + decentringList[1]

	correctedPhotocoordinates = [x_corrected, y_corrected]

	return correctedPhotocoordinates

def convertCoordinates(C, L):

	img = cv.imread('img1.tif'); #You must give the path of your image

	rows, columms, bands = img.shape #The method shape return the dimensions of the image, but here the bands are not interesting

	#print("The image size: ")
	#print(img.shape)

	pixel_size_x = 0.0046
	pixel_size_y = 0.0046

	x_mm = 0
	y_mm = 0

	x_mm = pixel_size_x * (C - ((columms-1)/2)) #calculate the x coordinate
	y_mm = -pixel_size_y * (L - ((rows-1)/2)) #calculate the y coordinate

	#print("The transformed coordinates: ")
	#print(x_mm, y_mm)

	return (x_mm,y_mm)

def readArqs(nomeArq):

	'''Esta função pode ser utilizada tanto para ler o arquivo com os pontos de controle, quanto para ler um arquivo com os valores
	iniciais dos parâmetros a serem calculados. Esta função armazena os valores lidos linha por linha em uma lista, ou seja, cada
	membro da lista é uma linha do arquivo lido. Para a correta manipulação dos valores, você deve saber em qual coluna os valores
	de interesse estão posicionados. O arquivo deve ter apenas números
	 '''

	print("\n\nAs coordenadas dos pontos de controle serão lidas no arquivo " + nomeArq)

	arq = open(nomeArq + '.txt', 'r')

	dados1 = arq.readlines() #Armazena o arquivo como um todo

	if dados1:
	   print("Leitura realizada com sucesso!")
	else:
	   print("Leitura falhou!")

	lista_pontos = [] #Lista que armazena cada linha do arquivo como float
	lista_linhas = []

	for i in dados1:
	    dados_separados = i.split(" ") #captura cada numero separado por espaço
	    for j in dados_separados:
	        lista_linhas.append(float(j)) #converte cada número de caractere para float
	        #print(j)
	    lista_pontos.append(lista_linhas) # esta é a lista que interessa
	    lista_linhas = []

	return lista_pontos


def getEquation():

	# Modelo Funcional: Equações de Colinearidade
	# Ordem de rotação: R(z) R(y) R(x)


	#Leirtura dos pontos de controle
	nomeArquivo = "controlpoints"
	pontos = readArqs(nomeArquivo)
	
	xp, yp, X, Y, Z, X0, Y0, Z0, om, fi, kapa, c  = symbols('xp yp X Y Z X0 Y0 Z0 om fi kapa c')

	m11 = cos(fi) * cos(kapa)
	m12 = cos(om) *sin(kapa) + sin(om)*sin(fi)*sin(kapa)
	m13 = sin(om) *sin(kapa) - cos(om)*sin(fi)*cos(kapa)

	m21 = -cos(fi)* sin(kapa)
	m22 = cos(om)*cos(kapa) - sin(om)*sin(fi)*sin(kapa)
	m23 = sin(om)*cos(kapa) + cos(om)*sin(fi)*sin(kapa)

	m31 = sin(om)
	m32 = sin(om)*cos(fi)
	m33 = cos(om)*cos(fi)


	x = xp - c * (m11*(X-X0) + m12*(Y-Y0) + m13*(Z-Z0)) / (m31*(X-X0) + m32*(Y-Y0) + m33*(Z-Z0))
	y = yp - c * (m21*(X-X0) + m22*(Y-Y0) + m23*(Z-Z0)) / (m31*(X-X0) + m32*(Y-Y0) + m33*(Z-Z0))

	parametros = []
	l_aux = []

	xf=0
	yf=0
	zf=0

	for h in pontos:
		xf = xf+h[2]
		yf = yf+h[3]
		zf = zf+h[4]
	


	'''for i in pontos:
		l_aux.append(xf/len(pontos)) #X0
		l_aux.append(yf/len(pontos)) #Y0
		l_aux.append(zf/len(pontos)) #Z0
		l_aux.append(i[2]) #X
		l_aux.append(i[3]) #Y
		l_aux.append(i[4]) #Z
		l_aux.append(0) #omega
		l_aux.append(0) #fi
		l_aux.append(0.174532925) #kapa
		parametros.append(l_aux)
		l_aux = []'''

	#Lendo os valores iniciais do arquivo ini.txt
	parametros = readArqs("ini")

	#print(parametros)

	

	#print(x)
	
	## As equações de colinearidade precisam ser linearizadas através do polinomio de taylor
	## Aparentemente, o modulo sympy não dispõe de algoritmo para linearização por serie de taylor, portanto:
	
	a1 = diff(x,X0)
	a2 = diff(x,Y0)
	a3 = diff(x,Z0)
	a4 = diff(x,om)
	a5 = diff(x,fi)
	a6 = diff(x,kapa)
	a7 = diff(y,X0)
	a8 = diff(y,Y0)
	a9 = diff(y,Z0)
	a10 = diff(y,om)
	a11 = diff(y,fi)
	a12 = diff(y,kapa)

	coef = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]

	A_linha = []

	for i in parametros:
		for j in coef:
			num_a = j.evalf(subs={c: 50, xp: -0.223, yp: 0.051, X0: i[0], Y0: i[1], Z0: i[2], X: i[3], Y: i[4], Z: i[5], om: i[6], fi: i[7], kapa: i[8]})
			A_linha.append(num_a)
			

	#expr.evalf(subs={x:2})

	A_sub = np.array(A_linha, dtype = 'float').reshape(8,6)
	#print(A_sub)

	L0 = []
	#a = np.vstack([a, b])
	for i in parametros:
		xl = x.evalf(subs={c: 50, xp: -0.223, yp: 0.051, X0: i[0], Y0: i[1], Z0: i[2], X: i[3], Y: i[4], Z: i[5], om: i[6], fi: i[7], kapa: i[8]})
		yl = y.evalf(subs={c: 50, xp: -0.223, yp: 0.051, X0: i[0], Y0: i[1], Z0: i[2], X: i[3], Y: i[4], Z: i[5], om: i[6], fi: i[7], kapa: i[8]})
		L0.append([xl, yl])

	return (A_sub, L0, parametros)



def calculateParameters():

	nameArq = "foto_observ"

	pontos_foto1 = readArqs(nameArq) #É uma lista com as coordenadas digital na qual cada linha tem coordenadas C,L (foto)

	#pontos_foto = np.array(pontos_foto1).reshape(8,1)


	#print(len(pontos_foto1))

	matriz_P = []
	cont_j = 0
	lin_aux = []
	var_p = 0.0046

	#Criando a matriz de pesos
	for i in range(len(pontos_foto1)*2):
		for j in range(len(pontos_foto1)*2):
			if i==j:
				lin_aux.append(var_p/2)
			else:
				lin_aux.append(0)
		matriz_P.append(lin_aux)
		lin_aux = []


	matriz_P = np.array(matriz_P) #reshape(len(pontos_foto1)*2, len(pontos_foto1)*2) #Este comando

	(A, Li, parametros_ini)= getEquation()

	#print("Li original")
	#print(Li)

	Li = np.array(Li, dtype = 'float').reshape(8,1)

	#print("Li modificado")
	#print(Li)

	Lob = []
	 

	for i in pontos_foto1:
		(x_f, y_f) = convertCoordinates(i[0], i[1])
		Lob.append(x_f)
		Lob.append(y_f)

	L = []

	for i in range(len(Lob)):
		L.append((Lob[i] - Li[i][0]))

	L = np.array(L).reshape(len(Lob), 1) #transforma L em um objeto numpy

	#Até o momento A é um array (numpy) L e matriz_P são listas. Deve-se transformar todos em objetos numpy para tornar possível
	#a multiplicação de matrizes

	#print(A.dtype)
	#print(L.dtype)
	#print(matriz_P.dtype)

	At = A.transpose()

	N = np.linalg.inv(np.dot(np.dot(At, matriz_P), A))
	
	U = np.dot(np.dot(At, matriz_P),L)
	
	X = np.dot(N, U)

	#print(X)

	arq_n = open('ini.txt', 'w')

	cont = 0

	for i in parametros_ini:
		for j in range(len(X)):
			if j < 3:
				i[j] = i[j] + X[j][0]
			else:
				i[j+3] = i[j+3] + X[j][0]

	#print(parametros_ini)

	cont = 0
	aux = 0

	for i in parametros_ini:
		for j in range(len(X)+3):
			if (cont == 3) and (j == 8):
				arq_n.write(str(i[j]))
			else:
				if aux == 8:
					arq_n.write(str(i[j]))
					arq_n.write("\n")
					aux = 0
				else:
					arq_n.write(str(i[j]))
					arq_n.write(" ")
					aux = aux + 1
		cont = cont + 1
			

	arq_n.close()

	return(X)

	
	#X = np.dot(A, matriz_P) 



'''def initialView():

	op =10

	while op != 0:

		op = int(input("Selecione um referencial: \n1. Referencial Digital (linha, coluna) \n2. Referencial Fotogramétrico (x, y em mm) \n0. Sair"))

		if op == 1:
			convertCoordinates()

		elif op==2:
			getEquation()#getPhotoCoordinates()
		else:
			print("\n\nSaindo...\n\n")

initialView()'''

loop = True
threshold = 2
cont = 1
contp = 0

#(A_sub, L0, parametros) = getEquation()

#print(L0)


for i in range(5):
	X_atual = calculateParameters()
	cont = cont + 1


print("\n\nO processamento terminou, o valores para cada parâmetro são: \n")
print(X_atual)
print("\nNúmero de iterações: ", cont)
print("\n---------------------Fim ------------------------------------------\n")