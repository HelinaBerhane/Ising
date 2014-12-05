#monte carlo simulation of the Ising model

#import libraries
from scipy import *	#used to make arrays
from pylab import *
import random  		#used to calculate random numbers
random.seed()  		#makes the random numbers different for every run

"""
import time
"""

#generates a random float between 0 and i
def Random_number(i): 
	r = i * random.random()
	return r

#calclates the energy of the lattice
def Energy(lattice):	
	energy = 0.
	for i in range(linear_dim):							#for every row
		for j in range(linear_dim):						#and every column
			spin = lattice[i, j]						#determine the spin of the dipole
			top_spin    = lattice[(i-1)%linear_dim, j]	#determine the spin of its neighbours
			bottom_spin = lattice[(i+1)%linear_dim, j]	# % calculates the remainder
			left_spin   = lattice[i, (j-1)%linear_dim]	#so if a dipole is at the edge
			right_spin  = lattice[i, (j+1)%linear_dim]	#it takes the spin of the dipole on the other side
			total_spin  = top_spin + bottom_spin + left_spin + right_spin
			energy += (-total_spin * spin)				#calculate the sum of the energy
	return energy/2										#and return half because each dipole is considered twice

#initialise the variables
linear_dim = 10		#linear dimensions of the lattice
iterations = 10000	#total number of monte carlo steps
warm_up    = 1000	#number of warm up steps
measure    = 100	#how often measurements are taken

#initialise the arrays
Temps = linspace(4, 0.5, 100)	#create an array of 100 equally spaced temperatures from 4 to 0.5
Mags = []						#create an array to store the magnetisation at each temperature
Energies = []					#create an array to store the energy at each temperature
Specific_heats = []				#create an array to store the specific heat at each temperature
Mag_suscepts = []				#create an array to store the magnetic susceptibility at each temperature

#initialise the lattice
lattice = zeros((linear_dim,linear_dim), dtype=int)	#make a matrix of 0s
for i in range(linear_dim):    						#for every row
	for j in range(linear_dim):						#and every column
		spin = int(Random_number(2)) - 1			#give it a random spin
		lattice[i, j] = spin

"""
checked up to this point

for T in Temps:						#for every temperature
	
    prob = zeros(9, dtype = float)	#create an array to store the possible probabilities
    prob[4 + 4] = exp(-4. * 2/T)	#calculate possible probabilities
    prob[4 + 2] = exp(-2. * 2/T)
    prob[  4  ] = exp( 0. * 2/T)
    prob[4 - 2] = exp( 2. * 2/T)
    
    prob[4 - 4] = exp( 4. * 2/T)
    energy = Energy(lattice)		#calculate the initial energy of the lattice
    magnetisation = sum(lattice)	#calculate the initial magnetisation of the lattice
    
    N = 0							#store the number of iterations after warm up
    sum_energy = 0.					#store the average energy
    sum_energy_2 = 0.				#store the average energy ^ 2
    sum_magnetisation = 0. 			#store the average magnetisation
    sum_magnetisation_2 = 0. 		#store the average magnetisation ^ 2
    area = linear_dim ** 2			#calculate the area of the lattice
    
    for itt in range(iterations):			#for every iteration
		i = int(Random_number(linear_dim))	#pick a random dipole in the lattice
		j = int(Random_number(linear_dim))
		N = 0
		spin = lattice[i, j]						#get its spin
		top_spin    = lattice[(i-1)%linear_dim, j]	#calculate the total surrounding spin
		bottom_spin = lattice[(i+1)%linear_dim, j]
		left_spin   = lattice[i, (j-1)%linear_dim]
		right_spin  = lattice[i, (j+1)%linear_dim]
		total_spin  = top_spin + bottom_spin + left_spin + right_spin

#		print lattice
#		time.sleep(0.01)
		
		energy_before = Energy(lattice)		#calculate the energy before the change
		energy = energy_before				
		lattice[i, j] = -spin				#change the spin
		energy_after  = Energy(lattice)		#compare it to the energy after the change
		
		if (energy_after - energy_before) >= 0:		#if the change in energy is positive
			probability = prob[4+spin*total_spin]	#calculate the probability of a spin change
			if probability > Random_number(1.):		#if the change is rejected
				
			
		if itt > warm_up:								#if the warm up period has passed
			energy = energy_after						#calculate the change in energy
			magnetisation = sum(lattice)				#calculate the change in magnetisation
			sum_energy += energy						#sum the energy
			sum_energy_2 += energy ** 2					#sum the energy ^ 2
			sum_magnetisation += magnetisation			#sum the magnetisations
			sum_magnetisation_2 += magnetisation ** 2	#sum the magnetisations ^ 2	
			N += 1										#count the number of iterations after warm
    
    ave_energy = sum_energy / N									#calculate the average energy
    ave_energy_2 = sum_energy_2 / N								#calculate the average energy ^ 2
    ave_magnetisation = sum_magnetisation / N					#calculate the average magnetisation
    ave_magnetisation_2 = sum_magnetisation_2 / N				#calculate the average magnetisation
    specific_heat = (ave_energy_2 - (ave_energy ** 2))/(T**2)	#calculete the specific hea
    mag_susceptibility = (ave_magnetisation_2 - (ave_magnetisation ** 2))/(T**2)
    
    Mags.append(ave_magnetisation/(N**2))			#add the average magnetisations to the array of magnetisations
    Energies.append(ave_energy/(N**2))				#add the average energy to the arrray of energies
    Specific_heats.append(specific_heat/(N**2))		#add the specific heat to the array
    Mag_suscepts.append(mag_susceptibility/(N**2))	#add the magnetic susceptibility to the array
    
    print T, ave_magnetisation/(N**2), ave_energy/(N**2), specific_heat/(N**2), mag_susceptibility/(N**2)
    
plot(Temps, Energies      , label='E(T)')	#plot the graphs
#plot(Temps, Specific_heats, label='cv(T)')
plot(Temps, Mags          , label='M(T)')
plot(Temps, Mag_suscepts, label='chi(T)')
xlabel('T')
legend(loc='best')
show()
