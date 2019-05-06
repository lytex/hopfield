from numpy.random import randint
from random import random
from numpy import copy,zeros,array,newaxis,exp,dot,sqrt,loadtxt,empty,ceil,log2,squeeze,linspace,savetxt,fill_diagonal
from scipy.linalg import hadamard
from pylab import imshow,show,subplots,plot,ylabel,xlabel,title,legend

#Parametros
T_vec = linspace(0.6,1.2,30)
steps = 10000 #numero de pasos de Monte Carlo
N_vec = [16,32,64,128,256]
K = 1
#Parametros

#funciones
def E(S,J): #Funcion que toma la configuracion de spines y las constantes de acoplo y devuelve la energia
	return(-0.5*float(dot(S,dot(J,S.T))))

def get_stationary(N, K):
    had_size = 2**ceil(log2(N))
    # had_size has to be a power of two
    H = squeeze(hadamard(had_size)) # Orthogonal patterns
    L = int(sqrt(N))
    if K == 1:
        H = H[0:N, L:L+1] 
    else:
        H = H[0:N, 0:K]
    return H
    
def m_fun(xi,S_in,steps,T):
	S = copy(S_in)
	M = empty(steps,float)
	for k in range(steps): #termalización
		i = randint(0,N)
		S_moved = copy(S)
		if S_moved[0,i] < 0:
			S_moved[0,i] = 1
		else:
			S_moved[0,i] = -1
		
		dE = E(S_moved,J) - E(S,J)
		
		if random() < exp(-dE/T):
			S = copy(S_moved)
	S_av = zeros([1,S.shape[1]],float)
	for k in range(steps): #magnetizacion
		i = randint(0,N)
		S_moved = copy(S)
		if S_moved[0,i] < 0:
			S_moved[0,i] = 1
		else:
			S_moved[0,i] = -1
		
		dE = E(S_moved,J) - E(S,J)
		
		if random() < exp(-dE/T):
			S = copy(S_moved)
		S_av += S/steps
	M = abs(float(dot(xi,S_av.T)/N))
	return M
#funciones
legend_vec = []
for N in N_vec:
	print(N)
	xi = get_stationary(N,K)
	xi = xi.T
	m_memory = abs(float(sum(xi[0,:])))/N
	J = N**(-1)*(dot(xi.T,xi))
	fill_diagonal(J,0.0)

	S_in = 2*randint(0,2,[1,N]) - 1 #configuracion inicial aleatoria
	M_vec = empty(len(T_vec),float)
	q = 0
	for T in T_vec:
		M_vec[q] = m_fun(xi,S_in,steps,T)
		q += 1
	#M_txt = 'M_%i.txt' %(N) #Quitar las almohadillas para guardar los resultados
	#savetxt(M_txt,M_vec)
	legend_txt = 'N = %i' %(N)
	legend_vec.append(legend_txt)
	plot(T_vec,M_vec,'o')
legend(legend_vec)
ylabel('Overlap')
xlabel('T')
show()
		
		
