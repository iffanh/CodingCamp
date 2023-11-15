import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import apasii 
q = 2000
pwf = 1500
pr = 3000
pb = 2180
rw = 0.5
h = 20
d = 2.259
qg = 1000000 #cuft/d
rho = 49.9 #lbm/ft^3
g = 32.174 #m/s
ift = 30 #dynes/cm
miul = 2
d = 2.259
Z = 0.935
T = 175
P = 800
gammag = 0.709
R = 10.73
miug = 0.0131
roughness = 0.0006
totaldepth = 1500
incrementdepth = 150

qmax = float(q/(1 - ( 0.2 * pwf / pr) - 0.8 *(( pwf/ pr) **2)))
print("The Balue of qmax = ",qmax)
print()
print("Calculate VLP using Hagedorn Eq")
ipr_list=[]
qipr_list = []
for i in range (pr,0,-100):
    ipr = i
    delta_p = pr - i
    inshage = (1 - 0.2 * delta_p / (rw * h) - 0.8 * (delta_p / (rw * h))**2) * ((pwf - pb) / (pr - pb))
    qipr = qmax / inshage
    ipr_list.append(ipr)
    qipr_list.append(qipr)
    #print(i)
data_ipr = np.array(ipr_list)
data_qipr = np.array(qipr_list)
print(data_qipr,data_ipr)

fbhp_list, q1_list = apasii.vogel(q,pwf,pr)
table = pd.DataFrame({'q': q1_list, 'fbhp': fbhp_list})
print(table)
print()
plt.plot(q1_list,fbhp_list, label = "IPR", color = "Blue")
# plt.plot(data_qvlp,data_vlp, label = "TPR", color = "Red")


plt.xlabel("q")
plt.ylabel("fbhp")
plt.title ("q vs fbhp")
plt.legend()
plt.grid()
plt.show()
# Pressure drop calculation
musl = apasii.musl(q, d)
musg = apasii.musg(qg, d, Z, T, P)
mium = apasii.musg(qg, d, Z, T, P) + apasii.musl(q, d)
gasfrac = apasii.gasfrac(q, qg, d, T, P, Z)
LB = apasii.lb(q, qg, d, Z , T, P)
if LB >= 0.13 :
    LB = 0.13
else :
    LBtetep = LB
if gasfrac > LB :
    print("THe flow regime is not bubble flow")
else :
    print("The flow is bubble flow")
Nvl = apasii.nvl(q, d ,rho, g, ift)
Nvg = apasii.nvg(qg, d, Z, T, P, rho, g, ift)
ND = apasii.nd(d, rho, ift)
NL = apasii.nl(miul, rho, ift)
CN = apasii.cnl(miul, rho, ift)
H = apasii.h(miul, rho, ift, q, d, g, qg, Z, T, P, CN)
yltao = apasii.yltao(H)
B = apasii.B(Nvg, NL, ND)
tao = apasii.tao(B)
lholdup = apasii.lholdup(yltao, tao)  
rhog = apasii.rhog(gammag, P, Z, R, T)
massrate = apasii.massrate(d, musl, rho, musg, rhog)
reynold = apasii.reynold(d, miul, miug, lholdup, massrate)
ff = apasii.frictionfactor(roughness, reynold, d)
denavg = apasii.insituavg(lholdup, rho, rhog)
dpdz = apasii.dpdz(denavg, ff, massrate, d)
print("Value of dpdz is",dpdz)

# NYOBA UNTUK NEW PRESSURE
vlp_list = []
depth_list = []
dpdz_list = []
for depth in range (0, totaldepth, incrementdepth):
    depth_list.append(depth)
    deltpressure = incrementdepth * dpdz
    P = P - deltpressure 
    musg = apasii.musg(qg, d, Z, T, P)
    mium = apasii.musg(qg, d, Z, T, P) + apasii.musl(q, d)
    gasfrac = apasii.gasfrac(q, qg, d, T, P, Z)
    LB = apasii.lb(q, qg, d, Z, T, P)
    if LB >= 0.13:
        LB = 0.13
    else:
        LBtetep1 = LB
    if gasfrac > LB:
        print("The flow regime is not bubble flow")
    else:
        print("The flow is bubble flow")
    Nvl = apasii.nvl(q, d, rho, g, ift)
    Nvg = apasii.nvg(qg, d, Z, T, P, rho, g, ift)
    ND = apasii.nd(d, rho, ift)
    NL = apasii.nl(miul, rho, ift)
    CN = apasii.cnl(miul, rho, ift)
    H = apasii.h(miul, rho, ift, q, d, g, qg, Z, T, P, CN)
    yltao = apasii.yltao(H)
    B = apasii.B(Nvg, NL, ND)
    tao = apasii.tao(B)
    lholdup = apasii.lholdup(yltao, tao)
    rhog = apasii.rhog(gammag, P, Z, R, T)
    massrate = apasii.massrate(d, musl, rho, musg, rhog)
    reynold = apasii.reynold(d, miul, miug, lholdup, massrate)
    ff = apasii.frictionfactor(roughness, reynold, d)
    denavg = apasii.insituavg(lholdup, rho, rhog)
    dpdz = apasii.dpdz(denavg, ff, massrate, d)
    dpdz_list.append(dpdz)
    vlp_list.append(P)
    print("Value of dpdz is", dpdz)

data_dpdz = np.array(vlp_list)
data_depth = np.array(depth_list)

print(vlp_list, data_depth)
table_vlp = pd.DataFrame({'depth': depth_list, 'P': vlp_list})
print(table_vlp)

plt.plot(vlp_list,depth_list, label = "trial", color = "Blue")
# plt.plot(data_qvlp,data_vlp, label = "TPR", color = "Red")


plt.xlabel("vlp")
plt.ylabel("depth")
plt.title ("depth vs vlp")
plt.legend()
plt.grid()
plt.show()