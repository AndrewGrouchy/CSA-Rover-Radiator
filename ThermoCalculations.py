import math
#contants
sigmaBoltz = 5.669E-8
pi = math.pi

#thermal conductivities
kPeek = 0.25
kAl = 205
kAero = 0.004

#emissivities
eAl = 0.77 #anodised ALuminium: 0.77    oxidized Aluminium : 0.4

    #dimensions
radiatorArea = 0.3**2 #+ 4*(0.05*0.3)

rodWidth = 0.2
rodArea = rodWidth**2
rodThickness = 0.035 #IMPORTANT NOTE: For anodised Aluminium, must be 0.035 m, for oxidized Aluminium must be 0.01 m (due to T1 values acquired in line 29)

marginArea = radiatorArea - rodArea

screwRadius = 0.01
screwArea = pi*screwRadius**2
lScrew = rodThickness

    #Thermo
Qmin = 15


def blackBodyTemp(epsilon,Q,A):
    T1 = ((Q/A)/(epsilon*sigmaBoltz))**(1/4)
    return T1

def FourierConductionT2(Q, k, A, T1, L):
    T2 = (Q*L)/(k*A/1000) + T1
    return T2

T_radiator = blackBodyTemp(eAl, Qmin, radiatorArea) #Anodised Aluminium: 248.57811584713096 K     Oxidized Aluminium: 292.79966488252586 K
T_rover = FourierConductionT2(Qmin, kAl, rodArea, T_radiator, rodThickness) #Anodised Aluminium: 312.6025060910334 K    Oxidized Aluminium: 311.09234780935515 K

def FourierConductionQ(k, A, T1, T2, L):
    Q = k*(A/1000)*(T2-T1)/L
    return Q

T_radiator_night = 0
T_rover_night = 253

print("DAY".center(30,'-'))

print("Radiator temperature: " + str(blackBodyTemp(eAl, Qmin, radiatorArea)) + " K")

print("Rover internal temperature T2: " + str(FourierConductionT2(Qmin, kAl, rodArea, T_radiator, rodThickness)) + " K")

print("Heat transfer rate Q (verification): " + str(FourierConductionQ(kAl, rodArea, T_radiator, T_rover, rodThickness)) + " W")

print("NIGHT".center(30,'-'))

print("Radiator temperature: 0 K (worst case scenario; most heat transfer)")

QNightAreo = FourierConductionQ(kAero, marginArea, T_radiator_night, T_rover_night, rodThickness )
QNightScrew = FourierConductionQ(kPeek, screwArea, T_radiator_night, T_rover_night, lScrew)
print ("Heat transfer rate: " + str(QNightAreo + 4*QNightScrew) + " W")

print("Rover internal temperature: " + str(T_rover_night) + " K")
