from numpy.random import randint
from random import random
from numpy import copy,zeros,array,newaxis,exp,dot,sqrt,reshape,loadtxt,ones
from pylab import imshow,show,subplots,pcolor

#Parametros
T = 0.1 #Temperatura
steps = 10000 #numero de pasos de Monte Carlo
memory_txt = 'memory.txt' #nombre del archivo con los estados de memoria
num_sim = 7 #numero de simulaciones
#Parametros

def E(S,J): #Funcion que toma la configuracion de spines y las constantes de acoplo y devuelve la energia
	return(-0.5*float(dot(S,dot(J,S.T))))

axes_files = int(num_sim/2)
f, axes = subplots(axes_files, num_sim-axes_files, sharey=True)

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

S_in = 2*randint(0,2,[1,N]) - 1 #configuracion inicial aleatoria
S_mat = reshape(S_in,(L,L))

axes[0,0].pcolor(S_mat)
inicial_txt = 'Configuración inicial : T = %.2f ; Steps = %i' %(T,steps)
axes[0,0].set_title(inicial_txt)

#Iteraciones Monte Carlo
fil = 0
sim = 0
for fil in range(axes_files):
	for cols in range(num_sim-axes_files):
		if fil+cols == 0:
			continue
		S = copy(S_in)
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
		sim += 1

		S_mat = reshape(S,(L,L))
		axes[fil,cols].pcolor(S_mat)
		title_txt = 'Sim. %i : T = %.2f ; Steps = %i' %(sim,T,steps)
		axes[fil,cols].set_title(title_txt)

show()	
