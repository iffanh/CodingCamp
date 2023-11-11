import math as mt
import numpy as np

def calc(pop,lop,ipo): #try math
    qwer = mt.pi*pop*lop*ipo
    return qwer

def darcy(k, DeltaP, miu, B, L): #Darcy
    q = k*(DeltaP)/(miu*B*L)
    return q

def J(DeltaP, q): #Productivity Index calculated by measured q and delta P
    piai=q/DeltaP
    return piai

#def pic(k,h,miu,B,re,rw,S): #Productivity Index calculation #argumen kebanyakan, lebih disederhanakan (kayak heat eq)
   
def vogel(q,pwf,pr): #IPR calculation with Vogel (not all the FBHP)
    fbhp_list= []
    q1_list = []
    qmax = float(q/(1 - ( 0.2 * pwf / pr) - 0.8 *(( pwf/ pr) **2)))
    for k in range(pr,0,-100):
        fbhp = k
        insvog = (1-0.2*(fbhp/pr)-0.8*(fbhp/pr)**2)
        q1 = qmax*insvog
        fbhp_list.append(fbhp)
        q1_list.append(q1)
    return fbhp_list, q1_list

def musl(q : int, d : float) : #Superficial Velocity for Liquid #->> AMANNN
    # q in bbl/d, d in inch
    musl = float(q * 5.615 /(86400 * 1/4 * np.pi * ((d/12)**2) )) #Result in ft/s
    return musl  # result in ft/s
      
def musg (qg : int,d : float, Z : float, T : float, P : float): #Superficial Velocity of gas, rate in cuft/d #->> AMANNNN
    # qg in scf/d, d in inch, Z as 0.935, T as Fahrenheit, P as psia
    musg = float((4/(np.pi * ((d/12) ** 2)) * qg * Z * ((460 + T) / 520) * (14.7 / P) ))
    return musg / 86400 # -> result in ft/s

def nvl (q : int, d : float ,rho : float, g : float, ift : float): #->> AMANN 
    # q in bbl/d , d in inch, rho in lbm/ft^3, g in ft/s^2 , ift in dynes/cm
    nvl = 1.938 * musl(q,d) * ((rho/ift) ** 0.25)
    return nvl # -> result in fraction

def nvg (qg : int, d : float, Z : float , T : float, P : float, rho : float, g : float, ift : int): #->> AMANNN
    # qg in scf/d, d in inch, Z equal 0.935, T in fahrenheit, P in psia, rho in lbm/ft^3, g in ft/s^2, ift in dynes/cm
    nvg = 1.938 * musg(qg, d, Z, T, P) * ((rho/ift)**0.25)
    return nvg

def nd (d : float, rho : float, ift : float): #_>> AMANNN 
    # d in inch, rho in lbm/ft^3, ift in dyne/cm
    nd = 120.872 * (d/12) * ((rho/ift)**(0.5))
    return nd

def nl (miul : int, rho : float, ift : int): #->>> AMANNN
    # miul in cP, rho in lbm/ft^3 , ift in dyne/cm
    nl = 0.15726 * miul * ((1 / (rho * ift**3))**0.25)
    return nl

def gasfrac (q : float ,qg : float ,d : float ,T : float ,P : float ,Z : float) : #_>AMANNN
    # q in bbl/d, qg in scf/d, d in inch, T in fahrenheit, P in psia, Z equal to 0.935
    musg = float((4/(np.pi * ((d/12) ** 2)) * qg * Z * ((460 + T) / 520) * (14.7 / P) )) / 86400
    musl = float(q * 5.615 /(86400 * 1/4 * np.pi * ((d/12)**2) )) 
    mum = musg + musl
    gasfrac = musg / mum
    return gasfrac

def lb (q : int, qg : int,d : float, Z : float, T : float, P : float): #to identify flow regime #->> AMANNN
    # q in bbl/d , qg in scf/d, d in inch, Z equal to 0.935, T in fahrenheit, P in psia
    lb = 1.071 - 0.2218*(((musg(qg, d ,Z, T, P) + musl(q, d))**2)/(d/12))
    if lb < 13 :
        lb = 0.13       
    return lb #can be improved for identifying flow regime by if function

def cnl (miul : int, rho : float, ift : int): #->> AMANN
    # miul in cP, rho in lbm/ft^3, ift in dynes/cm
    cnl1 = 0.0019 + 0.0322 * nl(miul, rho, ift) - 0.6642 * nl(miul, rho, ift)**2 + 4.9951 * nl(miul, rho, ift)**3 
    cnl2 = 1 - 10.0147 * nl(miul, rho, ift) + 33.8696 * nl(miul, rho, ift)**2 + 277.2817 * nl(miul, rho, ift)**3
    cnltot = cnl1 / cnl2 
    cnl = cnltot
    return cnl

def h (miul : int, rho : float, ift : int, q : int, d : float , g : float, qg : int, Z : float , T : float, P : float, cnl): #->> AMANNN
    # miul in cP, rho in lbm/ft^3, q in bbl/d, d in inch, g in ft/s^2, qg in scf/d, Z equal to 0.935, T in Fahrenheit, P in psia
    h1 = nvl(q, d, rho, g, ift)  * cnl * ((P/14.7)**0.1)
    h2 = (nvg(qg, d, Z, T, P, rho, g, ift)**0.575 )* nd(d, rho, ift)
    htot = h1/h2
    return htot

def yltao(h : float): #->> AMANNNN
    yltao1 = 0.0047 + 1123.32 * h + 729789.64 * (h**2)
    yltao2 = 1 + 1097.1566 * h + 722153.97 * (h**2)
    yltaotot = (yltao1 / yltao2)**0.5
    return yltaotot

def B (nvg : float, nl : float, nd: float): #->> AMANNN
    B1 = nvg * (nl**0.38)
    B2 = nd**2.14
    btot = B1 / B2
    return btot

def tao (B : float) : #->> AMANNN
    tao1 = 1.0886 - 69.9473 * B + 2334.3497 * (B**2) - 12896.683 * (B**3)
    tao2 = 1 - 53.4401 * B + 1517.9369 * (B**2) - 8419.8115 * (B**3)
    taotot = tao1 / tao2
    return taotot

def lholdup (yltao : float, tao :float): #->> AMANNN
    lholdup = (yltao/tao)*tao
    #tulis differnce between lholdup and gasfraction
    return lholdup

def rhog(gammag: float, P : float, Z : float, R : float, T: float): #->> AMANNNN
    # gammag equal to 0.709, P in psia, Z equal to 0.935, R equal to 10.73 psi/ft^3/lbmol R, T in fahrenheit
    rhog1 = 28.97 * gammag * P
    rhog2 = Z * R * (T + 459.67)
    rhogtot = rhog1 / rhog2 
    return rhogtot

def massrate(d : float, musl : float, rhol : float, musg : float, rhog : float): # ->> AMANNNN
    # d in inch, musl in ft/s, rhol in lbm/ft^3, musg in ft/s, rhog in lbm/ft^3
    massrate = (0.25 * np.pi * ((d/12) **2)) * ((musl * rhol) + (musg * rhog))
    return massrate * 86400 #convert to d
    
def reynold (d : float,  miul : float, miug : float, lholdup : float, massflow : float): #->> AMANN
    # d in inch, rhoavg in lbm/ft^3, miul in cP, miug equal to 0.0131, lholdup in fraction, massflow in lbm/d
    reynold1 = 2.2 * (10**-2) * massflow
    reynold2 = (d/12) * (miul ** lholdup) * (miug ** (1- lholdup ))
    reynoldnum = reynold1 / reynold2 
    return reynoldnum

def frictionfactor(roughness : float, reynold : float, d : float): 
    # roughness in fraction, reynold in fraction
    inside_log1 = roughness / (3.7065 * (d/12))
    inside_log2 = 5.0452 / reynold
    inside_logcore = ((((roughness / d) ** 1.1098) / 2.8257) + ((5.8506 / reynold) ** 0.8981))
    inside_tot = inside_log1 - inside_log2 * np.log(inside_logcore)
    complete = -2 * np.log(inside_tot)
    ff = (1 / (complete)) ** 2          
    return ff 
    
def insituavg(lholdup : float, rho : float, rhog : float): #-> AMANNN
    # lholdup in fraction, rho in lbm/ft^3, rhog in lbm/ft^3
    insituavg = lholdup * rho + (1 - lholdup) * rhog
    return insituavg

def dpdz(insituavg : float, ff : float, massrate : float, d :float): # -> AMANNNN
    # insituavf in lbm / ft^3, ff in fractoin, massrate in lbm/d, d in inch
    dpdz1 = 1/144
    dpdz_inside = (insituavg + ((ff * (massrate **2)/((7.413 * (10**10) * (d/12)**5 * (insituavg))))))
    dpdz_tot = dpdz1 * dpdz_inside
    return dpdz_tot

