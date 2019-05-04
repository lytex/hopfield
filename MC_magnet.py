from numpy.random import randint
from random import random
from numpy import copy,zeros,array,newaxis,exp,dot,sqrt,reshape,loadtxt,empty,ones
from pylab import imshow,show,subplots,plot,ylim,title

#Parametros
T = 0.1 #Temperatura
steps = 10000 #numero de pasos de Monte Carlo
memory_txt = 'memory.txt' #nombre del archivo con los estados de memoria
#Parametros

def E(S,J): #Funcion que toma la configuracion de spines y las constantes de acoplo y devuelve la energia
	return(-0.5*float(dot(S,dot(J,S.T))))

#Cargamos los datos de memoria
memory = loadtxt(memory_txt)#[newaxis] OJO! utilizar [newaxis] solo si vais a introducir un solo estado de memoria, en caso contrario borradlo
K = memory.shape[0] #numero de estamos de memoria
N = memory.shape[1] #numero de spines de la red (debe tener raiz entera)
L = int(sqrt(N)) #tamaño de la red cuadrada de spines
J = zeros([N,N],float)
m_memory = empty(K,float)
for k in range(K):
	xi = memory[k,:][newaxis]
	m_memory[k] = abs(float(sum(xi[0,:])))/N
	m_vec = m_memory[k]*ones(steps,float)
	plot(m_vec,'k--')
	J += N**(-1)*(dot(xi.T,xi)) #Calculamos las constantes de acoplo (Eq 1.5 del paper de Amit et al.)
for k in range(N):
	J[k,k] = 0.0 #Eliminamos los terminos diagonales

S_in = 2*randint(0,2,[1,N]) - 1 #configuracion inicial aleatoria

#Iteraciones Monte Carlo

S = copy(S_in)
M = empty(steps,float)
for k in range(steps):
	i = randint(0,N)
	S_moved = copy(S)
	if S_moved[0,i] < 0:
		S_moved[0,i] = 1
	else:
		S_moved[0,i] = -1
	
	dE = E(S_moved,J) - E(S,J)
	
	if random() < exp(-dE/T):
	#if dE < 0: #This is for T=0
		S = copy(S_moved)
	M[k] = abs(float(sum(S[0,:])/N))


plot(M,'b-')
title('Magnetizacion')
ylim(0.0,1.0)

show()	
