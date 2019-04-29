from numpy.random import randint
from random import random
from numpy import copy,empty,array,newaxis,exp,dot,sqrt

#Parametros
N = 9 #importante poner el cuadrado de un entero
T = 0.5
steps = 100
#Parametros

def E(S,J):
	return(-0.5*float(dot(S,dot(J,S.T))))
	
def matrix_convert(A):
	M = A.shape[1]
	L = int(sqrt(M))
	S_matrix = empty([L,L],int)
	n = 0
	for q in range(L):
		for k in range(L):
			S_matrix[q,k] = S[0,n]
			n += 1
	return S_matrix

#Prueba Xi
xi_1 = array([1,1,1,1,-1,1,1,1,1],int)[newaxis]
#xi_2 = array([1,1,1,-1,-1,-1,1,1,1],int)[newaxis]
J = N**(-1)*(dot(xi_1.T,xi_1))
for k in range(N):
	J[k,k] = 0.0
#J = np.empty([N,N],float)

S = 2*randint(0,2,[1,N]) - 1 #configuracion inicial aleatoria
S_mat = matrix_convert(S)
print(S_mat)

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

S_mat = matrix_convert(S)
print(S_mat)
	
