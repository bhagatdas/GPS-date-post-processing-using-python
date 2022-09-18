import pandas as pd
import math as mt
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, 'Rinex_files/log_24h.15n')
DATA_PATH = DATA_PATH.replace(os.sep, '/')

sow=373526
GM = 3.986008e+14   #Gravitational Constant m^3/s^2
OmegaE= 7.2921151467e-5 # Earth rotation rate, rad/s

def checkTime(t):  
    half_week = 302400
    tt = t
    if t >  half_week:
        tt = t-2*half_week
    if t < -half_week:
        tt = t+2*half_week
    return t

def Users_coordinates():
    fid=open(DATA_PATH, "rt")
    while True:   #to find END OF HEADER s
        line=fid.readline()
        if "END OF HEADER" in line:
            break
            
    while True:
        line=fid.readline()
        line=fid.readline()
        crs=line[24:42]
        crs=float(crs.replace('D', 'E'))
        deltan=line[43:61]
        deltan=float(deltan.replace('D', 'E'))
        M0=line[62:80]
        M0=float(M0.replace('D', 'E'))

        line=fid.readline()
        cuc=line[5:23]
        cuc=float(cuc.replace('D', 'E'))
        ecc=line[24:42]
        ecc=float(ecc.replace('D', 'E'))
        cus=line[43:61]
        cus=float(cus.replace('D', 'E'))
        roota=line[62:80]
        roota=float(roota.replace('D', 'E'))

        line=fid.readline()
        toe=line[5:23]
        toe=float(toe.replace('D', 'E'))
        cic=line[24:42]
        cic=float(cic.replace('D', 'E'))
        Omega0=line[43:61]
        Omega0=float(Omega0.replace('D', 'E'))
        cis=line[62:80]
        cis=float(cis.replace('D', 'E'))
        
        line=fid.readline()
        i0=line[5:23]
        i0=float(i0.replace('D', 'E'))
        crc=line[24:42]
        crc=float(crc.replace('D', 'E'))
        Omega=line[43:61]
        Omega=float(Omega.replace('D', 'E'))
        Omegadot=line[62:80]
        Omegadot=float(Omegadot.replace('D', 'E'))

        line=fid.readline()
        idot=line[62:80]
        idot=float(idot.replace('D', 'E')) 
        break
    
    #Procedure for coordinate calculation

    A = roota*roota;  #semimajor axis
    tk = checkTime(sow-toe)
    n0 = mt.sqrt(GM/pow(A,3))
    n = n0+deltan
    M = M0+n*tk

    E = M
    for i in range(4):
        E = M+ecc*mt.sin(E)
        
    v = mt.atan((mt.sin(E)*mt.sqrt(1-pow(ecc,2)))/(mt.cos(E)-ecc))

    phi = v+Omega
    u = phi + cuc*mt.cos(2*phi)+cus*mt.sin(2*phi)

    r = A*(1-ecc*mt.cos(E)) + crc*mt.cos(2*phi)+crs*mt.sin(2*phi)

    i = i0+idot*tk + cic*mt.cos(2*phi)+cis*mt.sin(2*phi)

    Omega = Omega0+(Omegadot-OmegaE)*tk-OmegaE*toe

    x1 = mt.cos(u)*r
    y1 = mt.sin(u)*r

    X = x1*mt.cos(Omega)-y1*mt.cos(i)*mt.sin(Omega)
    Y = x1*mt.sin(Omega)+y1*mt.cos(i)*mt.cos(Omega)
    Z = y1*mt.sin(i)

    print("ECEF Coordinates:")
    print("X axis value:",X)
    print("Y axis value:",Y)
    print("Z axis value:",Z)

    fid.close()
    return [X,Y,Z]

def main():
    pos = Users_coordinates()

if __name__ == "__main__":
    main()
