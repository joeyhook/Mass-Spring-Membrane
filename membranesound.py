'''
Vibrating Membrane Simulation
written by Jeremy Gonzales and Joey Hook
12/8/15

Updated 11/21/16
wav file write added, visuals removed
'''

from math import *
from visual.graph import *
import numpy 
import wave

class SoundFile:
   def  __init__(self, signal):
       self.file = wave.open('membrane.wav', 'wb')
       self.signal = signal
       self.sr = 44100
       self.bd = 16

   def write(self):
       self.file.setparams((1, 2, self.sr, iterations, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

#Constants
b  = 0.01       #drag coefficient
m  = 1          #mass of masses
k  = 1          #spring constant
N  = 51          #number of masses across one side
L0 = 1          #Relaxed length of spring                            
L  = (N-1)*L0   #Length of grid
A  = 1          #Amplitude
t = 0           #time
dt = 0.1       #Time interval
iterations = 0
Etotal = 1
maxdisplacement = 0

#init string to write wave to
signal = ''

def mag(vector):
    return (sqrt(vector[0]**2+vector[1]**2+vector[2]**2))

#acceleration function
def r_dd(rn_m, rnp1_m, rnm1_m, rn_mp1, rn_mm1):
    #return m,nth mass acceleration
    return (-k*(mag(rn_m-rnm1_m)-L0)*(rn_m-rnm1_m)/mag(rn_m-rnm1_m)
            +k*(mag(rnp1_m-rn_m)-L0)*(rnp1_m-rn_m)/mag(rnp1_m-rn_m)
            -k*(mag(rn_m-rn_mm1)-L0)*(rn_m-rn_mm1)/mag(rn_m-rn_mm1)
            +k*(mag(rn_mp1-rn_m)-L0)*(rn_mp1-rn_m)/mag(rn_mp1-rn_m))

#make masses
positions = [ [ 0 for n in range(N) ] for m in range(N) ]
for n in range(N):
    for m in range(N):
        positions[m][n] = vector(m*L0, n*L0, 0)
        
#initialize velocity and acceleration lists
velocities    = [ [ vector(0, 0, 0) for n in range(N) ] for m in range(N) ]     
accelerations = [ [ vector(0, 0, 0) for n in range(N) ] for m in range(N) ]

#pluck membrane
positions[int(L/2)  ][int(L/2)  ].z = A

positions[int(L/2)+1][int(L/2)+1].z = A/2
##positions[int(L/2)+1][int(L/2)-1].z = A/2
##positions[int(L/2)+1][int(L/2)  ].z = A/2
##positions[int(L/2)-1][int(L/2)+1].z = A/2
##positions[int(L/2)-1][int(L/2)-1].z = A/2
##positions[int(L/2)-1][int(L/2)  ].z = A/2
##positions[int(L/2)  ][int(L/2)+1].z = A/2
##positions[int(L/2)  ][int(L/2)-1].z = A/2

#main loop
print 'Working...'
while (Etotal > 0.00001) and (t < 25000):

    #calculate total energy
    Etotal = 0
    for n in range(N):
        for m in range(N):
            Etotal += 0.5*m*mag(velocities[m][n])**2
    for n in range(N-1):
        for m in range(N-1):
            Etotal += (0.5*k*(mag(positions[m+1][n]-positions[m][n])-L0)**2
                      +0.5*k*(mag(positions[m][n+1]-positions[m][n])-L0)**2)
    
    #update accelerations
    for n in range(N-2):
        for m in range(N-2):
            accelerations[m+1][n+1] = r_dd(positions[m+1][n+1], positions[m+2][n+1],
                                      positions[m][n+1], positions[m+1][n+2],
                                      positions[m+1][n] ) - b*velocities[m+1][n+1]
            
    #update velocities
    for n in range(N):
        for m in range(N):
            velocities[m][n] += accelerations[m][n]*dt
        
    #update positions
    for n in range(N):
        for m in range(N):
            positions[m][n] += velocities[m][n]*dt
            
    #writing z-position data to .wav file
    signal += wave.struct.pack('h',(2**16/2)*positions[int(L/2)][int(L/2)].z) # transform to binary     

    if (t%100 < dt):
       print 'Working...t =',t, 'Etotal =', Etotal
       print 'Max Amplitude =',maxdisplacement

    if (abs((2**16/2)*positions[int(L/2)][int(L/2)].z) > maxdisplacement):
        maxdisplacement = abs((2**16/2)*positions[int(L/2)][int(L/2)].z)
        
    iterations += 1
    t += dt
    
f = SoundFile(signal)
f.write()
print 'max displacement =', maxdisplacement
print 'file written'
