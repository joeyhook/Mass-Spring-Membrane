'''
Vibrating Membrane Simulation
written by Jeremy Gonzales and Joey Hook
12/8/15
'''

from __future__ import division

from visual import *
from visual.graph import *
from visual.controls import *


scene.width=640
scene.height=685

print('''This program is meant to simulate a vibrating membrane with
masses and springs. While the program is running some attributes can
be changed by sliders on the right. The value selected by a slider
will be printed in the shell.
''')

#Constants
b  = 0.1        #drag coefficient
d  = 0.1        #Diameter of masses
N  = 15
##N  = input('''How many masses would you like along each side of the grid?
##Picking an odd number makes for better symmetry, and we all know that
##physicists love symmetry. You can make the grid as big as you like, but
##more than 15 might not run so well. 
##Input:''')
L0 = 1          #Relaxed length of spring                            
L  = (N-1)*L0   #Length of grid
A  = 2          #Amplitude
t = 0
dt = 0.01    #Time interval
choice = 1
choice = input('''You have a few options now:
1.) You can flick a single mass in the center and see what happens.
2.) Pull back the center mass and the rest along with it, then let go.
3.) Apply a sinusoidal driving force to the center mass.
Input 1, 2, or 3:''')
if choice != 1 and choice != 2 and choice != 3:
    print('Hey! Good for you, smart guy. Now nothing is going to happen.')


#center camera on middle of grid
scene.center=vector(L/2, L/2, 0)

#reset initial positions
def change(): 
    for n in range(N):
        for m in range(N):
            masses[m][n].pos = vector(m*L0, n*L0, 0)
    for n in range(N-2):
        for m in range(N-2):
            accelerations[m+1][n+1] = vector(0,0,0)
    for n in range(N-2):
        for m in range(N-2):
            velocities[m+1][n+1] = vector(0,0,0)            
    print('reset')   
#print slider values
def changek():
    print('All spring constants changed to:', k.value)    
def changew():
    if choice != 3:
        print('''This won't do you much good right now.''')
    else:
        print('Frequency of driven mass changed to:', w.value)
def changeA():
    if choice != 3:
        print('''This won't do you much good right now.''')
    else:    
        print('Amplitude of driven mass changed to:', A.value)
def changeR():
    print('Speed of animation changed to:', R.value)
# Create controls window
C = controls( title = 'Sliders for k(cyan), w(magenta), A(yellow), and rate(green)',
              x = 640, y = 0, height = 600, width = 640, ) 
# Create a button in the controls window:
reset = button( pos=(-70, -60), length=15, height=15, text='RESET',
                action=lambda: change(), color=color.red )
k = slider( pos=(-30, 60), min =   5, max = 50, length=60, width=30, height=30, 
            text='spring constant', action=lambda: changek(), value = 20, color=color.cyan ) 
w = slider( pos=(-30, 20), min =   10, max = 100, length=60, width=30, height=30, 
            text='frequency', action=lambda: changew(), value = 5, color=color.magenta )
A = slider( pos=(-30,-20), min =0.01, max =  2, length=60, width=30, height=30, 
            text='amplitude', action=lambda: changeA(), value = 1, color=color.yellow)
R = slider( pos=(-30,-60), min =1, max =  1000, length=60, width=30, height=30, 
            text='rate', action=lambda: changeR(), value = 1000, color=color.green) 

#acceleration function
def r_dd(rn_m, rnp1_m, rnm1_m, rn_mp1, rn_mm1):
    #return m,nth mass acceleration
    return (-k.value*(mag(rn_m-rnm1_m)-L0)*(rn_m-rnm1_m)/mag(rn_m-rnm1_m)
            +k.value*(mag(rnp1_m-rn_m)-L0)*(rnp1_m-rn_m)/mag(rnp1_m-rn_m)
            -k.value*(mag(rn_m-rn_mm1)-L0)*(rn_m-rn_mm1)/mag(rn_m-rn_mm1)
            +k.value*(mag(rn_mp1-rn_m)-L0)*(rn_mp1-rn_m)/mag(rn_mp1-rn_m))
  
#Objects
f = frame()

##Lwall = box(pos=vector(0, L/2, 0),
##        length=d, width=d, height=L+d, material=materials.wood,frame=f)
##Rwall = box(pos=vector(L, L/2, 0),
##        length=d, width=d, height=L+d, material=materials.wood,frame=f)
##Ceiling = box(pos=vector(L/2, L, 0),
##        length=L+d, width=d, height=d, material=materials.wood,frame=f)
##Floor = box(pos=vector(L/2, 0, 0),
##        length=L+d, width=d, height=d, material=materials.wood,frame=f)


#make masses
masses = [ [ 0 for n in range(N) ] for m in range(N) ]
for n in range(N):
    for m in range(N):
        masses[m][n] = sphere(pos=vector(m*L0, n*L0, 0), radius=d/2,
                              material=materials.emissive,frame=f)

#initialize velocity and acceleration lists
velocities    = [ [ vector(0, 0, 0) for n in range(N) ] for m in range(N) ]     
accelerations = [ [ vector(0, 0, 0) for n in range(N) ] for m in range(N) ]

#pull middle back in z-direction

if choice == 1:
    masses[int(L/2)][int(L/2)].pos.z = A.value

if choice == 2:
    for n in range(N):
        for m in range(N):
            if n+m <= L and m >= n:
                masses[n][m].pos.z = 2*n*A.value/L
            if n+m <= L and m < n:
                masses[n][m].pos.z = 2*m*A.value/L
            elif n+m > L and n >= m:    
                masses[n][m].pos.z = 2*(L-n)*A.value/L
            elif n+m > L and n < m:    
                masses[n][m].pos.z = 2*(L-m)*A.value/L
    f.rotate(angle=-pi/6,axis=vector(1,0,0))
    scene.range=L/2

#init graph
gd1 = gdisplay (x=640, y=0, width=640, height=250,
                title='Z displacement of center mass',
                xtitle='Time', ytitle='Displacement',
                foreground=color.blue, background=color.black)
f1 = gcurve(color=color.red)
gd2 = gdisplay (x=640, y=250, width=640, height=250,
               title='Total energy',
               xtitle='Time', ytitle='Energy',
               foreground=color.blue, background=color.black,
               xmin = 0, xmax = 50)
f2 = gcurve(color=color.green)

Etotal = 1
#animate
while True:  #(Etotal > 0.001) and (t < 25000):
    rate(R.value)
    
    #calculate total energy
    Etotal = 0
    for n in range(N):
        for m in range(N):
            Etotal += 0.5*mag(velocities[m][n])**2
    for n in range(N-1):
        for m in range(N-1):
            Etotal += (0.5*k.value*(mag(masses[m+1][n].pos-masses[m][n].pos)-L0)**2
                      +0.5*k.value*(mag(masses[m][n+1].pos-masses[m][n].pos)-L0)**2)
    
    #update accelerations
    for n in range(N-2):
        for m in range(N-2):
            accelerations[m+1][n+1] = r_dd(masses[m+1][n+1].pos, masses[m+2][n+1].pos,
                                      masses[m][n+1].pos, masses[m+1][n+2].pos,
                                      masses[m+1][n].pos ) - b*velocities[m+1][n+1]
    if choice == 3:
        accelerations[int(L/2)][int(L/2)]=vector(0,0,0) #center mass is driven => not pulled by springs

    #update velocities
    for n in range(N):
        for m in range(N):
            velocities[m][n] += accelerations[m][n]*dt

    #update positions   
    if choice == 3:
        masses[int(L/2)][int(L/2)].pos.z = A.value*cos(w.value*t) #center mass is driven
    for n in range(N):
        for m in range(N):
            masses[m][n].pos += velocities[m][n]*dt

    #update color depending on z displacement
    for n in range(N):
        for m in range(N):
            c = (masses[m][n].pos.z+A.max)/(2*A.max) #0 < c < 1
            masses[m][n].color = color.gray(c)
            #print masses[1][1].pos    

    #plot graphs
    f1.plot(pos=(t,masses[int(L/2)][int(L/2)].pos.z))
    f2.plot(pos=(t,Etotal)) 

    t += dt

    #print Etotal

