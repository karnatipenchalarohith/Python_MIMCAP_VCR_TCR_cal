#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:25:07 2022

@author: rkar
"""

import pandas as pd
import statistics


import os
import matplotlib.pyplot as mp

import numpy as np
from  average_list import Average as Average

from scipy.stats import linregress
from sklearn import linear_model






path_point_meas= r"C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\\"

Device_name="cmim2"

filename= Device_name + '_p025.txt'



os.remove(r"C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\cmim2_tcr.txt")

#Mult=[16,100,16,100,16,100,16,100,16,100,16,100,10,10,10,10,10,100,10,100,100,100,100,100]
#Width=[4,4,4,4,10,10,10,10,20,20,30,30,4,4,10,10,20,10,30,20,4,4,30,10]
#Length=[4,4,30,30,10,10,30,30,20,20,30,30,4,30,10,30,20,30,30,20,4,30,30,10]

Mult=[16,100,16,100,16,100,16,100,16,100,16,100]
Width=[4,4,4,4,10,10,10,10,20,20,30,30]
Length=[4,4,30,30,10,10,30,30,20,20,30,30]

#temperature = ['m040','p000','p025','p075','p125','p200']
# p160 data seems to be wrong

temperature = ['m040','p000','p025','p075','p125','p200']

for j in range(0,len(temperature)):
    filename = Device_name + '_' + temperature[j] + '.txt'
    print(filename)

    with open(path_point_meas + filename) as f:
        df = pd.read_csv(f, sep="\t", header=None)

    df.columns = ["SN", "M", "W", "L", "TEMP", "V", "C"]

    for iter in range(0, len(Mult)):
        print(iter)
        print(Mult[iter])
        M = Mult[iter]
        W = Width[iter]
        L = Length[iter]

        df_TCR1 = df[(df['M'] == M) & (df['W'] == W) & (df['L'] == L) & (df['V'] == 0) & (df['SN'] == iter + 1)]

        df_TCR1.to_csv(r'C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\cmim2_tcr.txt', header=None, index=None,
                       sep="\t", mode='a')

    # df_TCR1.savetxt(r'C:\All_projects\tC18d_CMIM_update\W6C443.W16_cmim_clr\clr\np.txt', df_TCR1.values, fmt='%d')

    print(df_TCR1)







#path_point_meas= r"C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\"



filename_tcr= Device_name + '_tcr.txt'


with open(path_point_meas + filename_tcr) as f:
    dff = pd.read_csv(f, sep="\t", header=None)

dff.columns = ["SN", "M", "W", "L", "TEMP", "V", "C"]


print(dff)
dff['TEMP_diff']=dff['TEMP'] - 25

print(dff)

TCC2=[]
TCC1=[]
tcc_coeff=[]
model_eqns=[]
cap_peri_array=[]
area_peri_array=[]

for iter in range(0,len(Mult)):
    print(iter)
    print(Mult[iter])
    M=Mult[iter]
    W=Width[iter]
    L=Length[iter]

    dff_TCR1 = dff[(dff['M'] == M) & (dff['W'] == W) & (dff['L'] == L) & (dff['SN'] == iter + 1)]

    print(dff_TCR1)
    print(dff_TCR1[(dff_TCR1['TEMP_diff'] == 0)])
    df_tcr1_only=dff_TCR1[(dff_TCR1['TEMP_diff'] == 0)]

    cap_at_temp_zero = df_tcr1_only['C'].iloc[0]

    Cap_values =dff_TCR1['C']
    T=dff_TCR1['TEMP_diff']

    mp.scatter(T,Cap_values )


    mp.xlabel('Temp (C)')
    mp.ylabel('CAP (F)')




    titlename = "W=" + str(W) + " " + "L=" + str(L) + " " + "nf=" + str(M) + "_MIMCAP vs Temp" + "Device_{:02d}_.png".format(iter)

    mp.title(titlename)
    mp.savefig(titlename + '.png')

    #mp.show()

    model = np.poly1d(np.polyfit(T,Cap_values, 2))

    print(model)

    model2 = model / df_tcr1_only['C'].iloc[0]

    #model2=model/df_vcr1_only['C'].iloc[0]

    print(model2)

    print(model2.c)
    model_eqns.append(model2)

    TCC2.append(model2.c[0])
    TCC1.append(model2.c[1])
    tcc_coeff.append(model2.c[2])

    print(TCC2)
    print(TCC1)
    print(tcc_coeff)
    print(model_eqns)
    #res = statistics.median(test_list)
    TCC2_avg = statistics.median(TCC2)
    TCC1_avg = statistics.median(TCC1)
    tcc_coeff_avg = statistics.median(tcc_coeff)

    print(TCC2_avg)
    print(TCC1_avg)
    print(tcc_coeff_avg)

    dff_TCR1['Area'] = dff_TCR1['M'] * dff_TCR1['W'] * dff_TCR1['L']
    dff_TCR1['Perimeter'] = 2 * dff_TCR1['M'] * (dff_TCR1['W'] + dff_TCR1['L'])
    dff_TCR1['Area_per_Peri'] = dff_TCR1['Area'] / dff_TCR1['Perimeter']
    dff_TCR1['Cap_per_Peri'] = dff_TCR1['C'] / dff_TCR1['Perimeter']

    print(dff_TCR1)

    df_tcr1_cal=dff_TCR1[(dff_TCR1['TEMP_diff'] == 0)]

    cap_tcr1_capacitance_peri = df_tcr1_cal['Cap_per_Peri'].iloc[0]
    cap_tcr1_area_peri = df_tcr1_cal['Area_per_Peri'].iloc[0]

    cap_peri_array.append(cap_tcr1_capacitance_peri)

    area_peri_array.append(cap_tcr1_area_peri)

    print(cap_peri_array)
    print(area_peri_array)



    #dff_TCR1['TEMP'] - 25

    #print(dff_TCR1)





