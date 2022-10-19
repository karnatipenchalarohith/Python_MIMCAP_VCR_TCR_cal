
import pandas as pd
import matplotlib.pyplot as mp

import numpy as np
import statistics

from scipy.stats import linregress
from sklearn import linear_model

from  average_list import Average as Average


path_point_meas= r"C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\\"

Device_name="cmim2"

filename= Device_name + '_p025.txt'

with open(path_point_meas + filename) as f:
    df = pd.read_csv(f, sep="\t", header=None)

df.columns = ["SN", "M", "W", "L", "TEMP", "V", "C"]



temperature=25

#Mult=[16,100,16,100,16,100,16,100,16,100,16,100,10,10,10,10,10,100,10,100,100,100,100,100]
#Width=[4,4,4,4,10,10,10,10,20,20,30,30,4,4,10,10,20,10,30,20,4,4,30,10]
#Length=[4,4,30,30,10,10,30,30,20,20,30,30,4,30,10,30,20,30,30,20,4,30,30,10]

Mult=[16,100,16,100,16,100,16,100,16,100,16,100]
Width=[4,4,4,4,10,10,10,10,20,20,30,30]
Length=[4,4,30,30,10,10,30,30,20,20,30,30]


print(len(Mult))
print(len(Width))
print(len(Length))

VCR2=[]
VCR1=[]
V_coeff=[]
model_eqns=[]

for iter in range(0,len(Mult)):
    print(iter)
    print(Mult[iter])
    M=Mult[iter]
    W=Width[iter]
    L=Length[iter]






#    print(df)
#    M=100
#    W=10
#    L=10



    df_VCR1 = df[(df['M'] == M) & (df['W'] == W) & (df['L'] == L) & (df['SN'] == iter+1) ]



    print(df_VCR1)

    print(df_VCR1[(df_VCR1['V'] == 0)])
    df_vcr1_only=df_VCR1[(df_VCR1['V'] == 0)]

    cap_at_zero=df_vcr1_only['C'].iloc[0]
    print(df_vcr1_only['C'].iloc[0])

    #print(ff['ID'].iloc[11])


    #df_VCR1

    Cap_values =df_VCR1['C']
    Voltage=df_VCR1['V']




    mp.scatter(Voltage,Cap_values )
    mp.show()

    model = np.poly1d(np.polyfit(Voltage,Cap_values, 2))

    print(model)


    model2=model/df_vcr1_only['C'].iloc[0]

    print(model2)


    print(model2.c)
    model_eqns.append(model2)

    VCR2.append(model2.c[0])
    VCR1.append(model2.c[1])
    V_coeff.append(model2.c[2])



print(VCR2)
print(VCR1)
print(V_coeff)
print(model_eqns)

VCR2_avg = statistics.median(VCR2)
VCR1_avg = statistics.median(VCR1)
V_coeff_avg = statistics.median(V_coeff)


print(VCR2_avg)
print(VCR1_avg)
print(V_coeff_avg)

