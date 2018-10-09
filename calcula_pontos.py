# Código simples para cálculo de coordenadas de pontos de uma nuvem levantada através de laser scanner
# Pode conter pequenos erros, uma vez que não foi validado
# Desenvolvido por Natália Carvalho de Amorim - Universidade Federal do Paraná

import numpy as np
import math as mt

#--------------- Inicializando o laver arm e o body sight -------------------------------------------

leaver_arm = np.array([-0.091, -0.014, -0.099]).reshape(3,1)
body_sight = np.array([0.0, 0.0, 0.0]).reshape(3,1)

#----------------------------------------------------------------------------------------------------

#--------------- Leitura do Arquivo e armazenamento em uma lista ------------------------------------

arq = open('faixa_1.txt', 'r') #abre o arquivo
arq2 = open('coords_v.pcd','w')

dados1 = arq.readlines() #Armazena o arquivo como um todo

if dados1:
   print("Leitura realizada com sucesso!")
else:
   print("Leitura falhou!")

lista = [] #Lista que armazena cada linha do arquivo como float
lista_linhas = []

for i in dados1:
    dados_separados = i.split(" ") #captura cada numero separado por espaço
    for j in dados_separados:
        lista_linhas.append(float(j)) #converte cada número de caractere para float
        #print(j)
    lista.append(lista_linhas) # esta é a lista que interessa
    lista_linhas = []
#-------------------------------------------------------------------------------------

#--------------- Calculando as coordenadas -------------------------------------------

coords_corrigidas = [] # Esta lista vai receber as coordenadas calculadas segundo os angulos de atitude

for i in lista:
	roll = (i[10]*(mt.pi))/180
	pitch =  (i[11]*(mt.pi))/180
	yaw = (i[12]*(mt.pi))/180 #cria a lista com roll, pitch e yaw

	m11 = mt.cos(yaw)*mt.cos(pitch) #cos fi cos kappa
	m21 = mt.sin(yaw)*mt.cos(pitch)
	m31 = -mt.sin(pitch)

	m12 = (mt.cos(yaw)*mt.sin(pitch)*mt.sin(roll)) - (mt.sin(yaw) * mt.cos(roll))
	m22 = (mt.sin(yaw)*mt.sin(pitch)*mt.sin(roll)) + (mt.cos(yaw) * mt.cos(roll))
	m32 = mt.cos(pitch) * mt.sin(roll)

	m13 = (mt.cos(yaw)*mt.sin(pitch)*mt.cos(roll)) + (mt.sin(yaw)*mt.sin(roll))
	m23 = (mt.sin(yaw)*mt.sin(pitch)*mt.cos(roll)) - (mt.cos(yaw)*mt.sin(roll))
	m33 = mt.cos(pitch)*mt.cos(roll)

	#---------------------- Matriz em relação rotação em kappa---------------------------
	roll = 0
	pitch = 0

	m11_ = mt.cos((mt.pi/2))*mt.cos(pitch) #conferir
	m21_ = mt.sin((mt.pi/2))*mt.cos(pitch)
	m31_ = -mt.sin(pitch)

	m12_ = (mt.cos((mt.pi/2))*mt.sin(pitch)*mt.sin(roll)) - (mt.sin((mt.pi/2)) * mt.cos(roll))
	m22_ = (mt.sin((mt.pi/2))*mt.sin(pitch)*mt.sin(roll)) + (mt.cos((mt.pi/2)) * mt.cos(roll))
	m32_ = mt.cos(pitch) * mt.sin(roll)

	m13_ = (mt.cos((mt.pi/2))*mt.sin(pitch)*mt.cos(roll)) + (mt.sin((mt.pi/2))*mt.sin(roll))
	m23_ = (mt.sin((mt.pi/2))*mt.sin(pitch)*mt.cos(roll)) - (mt.cos((mt.pi/2))*mt.sin(roll))
	m33_ = mt.cos(pitch)*mt.cos(roll)



	#--------------------------------------------------------------------------------


	matriz_rot = np.array([m11,m12,m13,m21,m22,m23,m31,m32,m33]).reshape(3,3)

	mat_90 = np.array([m11_,m12_,m13_,m21_,m22_,m23_,m31_,m32_,m33_]).reshape(3,3) #matriz rotacional para variação de angulos de atitude igual a zero

	vetor_xyz = np.array([i[0],i[1],i[2]]).reshape(3,1)

	V = np.array([i[7],i[8],i[9]]).reshape(3,1)

	#X = V + (matriz_rot * leaver_arm) + ((matriz_rot * body_sight) * (mat_90 * vetor_xyz))

	X = V + np.dot(mat_90, (np.dot(matriz_rot,vetor_xyz))) + np.dot(matriz_rot,leaver_arm)

#--------------- Gravando as coordenadas em um arquivo-------------------------------------------
	cont = 0
	for j in X:
		arq2.write(str(j[0]))
		arq2.write(" ")
		cont = cont + 1
		if cont == 3:
			arq2.write("\n")
			cont = 0
	
#print(lista[20][1])
#print(lista[20][2])

#print(lista[20][1] + lista[20][2])

print("\n\nCálculo de coordenadas concluído com sucesso (será??)\n\n")

print(X[0])

arq.close()
arq2.close()