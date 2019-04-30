from numpy.random import randint
from random import random
from numpy import copy,zeros,array,newaxis,exp,dot,sqrt,reshape,loadtxt
from pylab import imshow,show,subplots,pcolor

#Parametros
T = 0.2 #Temperatura
steps = 2000 #numero de pasos de Monte Carlo
memory_txt = 'faces.txt' #nombre del archivo con los estados de memoria
#Parametros

def E(S,J): #Funcion que toma la configuracion de spines y las constantes de acoplo y devuelve la energia
	return(-0.5*float(dot(S,dot(J,S.T))))


f, (ax1, ax2) = subplots(1, 2, sharey=True)

#Cargamos los datos de memoria
memory = loadtxt(memory_txt)#[newaxis] OJO! utilizar [newaxis] solo si vais a introducir un solo estado de memoria, en caso contrario borradlo
K = memory.shape[0] #numero de estamos de memoria
N = memory.shape[1] #numero de spines de la red (debe tener raiz entera)
L = int(sqrt(N)) #tamaño de la red cuadrada de spines
J = zeros([N,N],float)
for k in range(K):
	xi = memory[k,:][newaxis]
	J += N**(-1)*(dot(xi.T,xi)) #Calculamos las constantes de acoplo (Eq 1.5 del paper de Amit et al.)
for k in range(N):
	J[k,k] = 0.0 #Eliminamos los terminos diagonales

S = 2*randint(0,2,[1,N]) - 1 #configuracion inicial aleatoria
S_mat = reshape(S,(L,L))

ax1.imshow(S_mat)

#Iteraciones Monte Carlo
for k in range(steps):
	i = randint(0,N)
	S_moved = copy(S)
	if S_moved[0,i] < 0:
		S_moved[0,i] = 1
	else:
		S_moved[0,i] = -1
	
	dE = E(S_moved,J) - E(S,J)
	
	if random() < exp(-dE/T):
		S = copy(S_moved)

S_mat = reshape(S,(L,L))
ax2.imshow(S_mat)
inicial_txt = 'Configuración inicial : T = %.2f ; Steps = %i' %(T,steps)
final_txt = 'Configuración final : T = %.2f ; Steps = %i' %(T,steps)
ax1.set_title(inicial_txt)
ax2.set_title(final_txt)

show()	
