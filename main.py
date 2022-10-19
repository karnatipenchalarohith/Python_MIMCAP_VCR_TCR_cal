# This is a sample Python script.



import pandas as pd
import matplotlib.pyplot as mp

from scipy.stats import linregress
from sklearn import linear_model



path_point_meas= r"C:\All_projects\tC18d_CMIM_update\W6C442.W14_cmim2_clr\clr\\"

Device_name="cmim2"

filename= Device_name + '_p025.txt'

with open(path_point_meas + filename) as f:
    df = pd.read_csv(f, sep="\t", header=None)

df.columns = ["SN", "M", "W", "L", "TEMP", "V", "C"]

temperature=25


print(df)

#df_id_vg_0 = df[(df['TEMP'] == temperature) & (df['V'] == 0) & (df['SN'] >0)]

df_id_vg_0 = df[(df['TEMP'] == temperature) & (df['V'] == 0) & (df['SN'] >0)]
# df_id_vg_2 = df[(df['W'] == W) & (df['L'] == L) & (df['SETUP'] == SETUP_linear_2) & (df['VB'] == VB_Bias)]

df_id_vg_0['Area'] = df_id_vg_0['M'] * df_id_vg_0['W'] * df_id_vg_0['L']
df_id_vg_0['Perimeter'] = 2*df_id_vg_0['M'] * (df_id_vg_0['W'] + df_id_vg_0['L'])
df_id_vg_0['ratio_peri_area'] = df_id_vg_0['Perimeter'] / df_id_vg_0['Area']
print(df_id_vg_0)

print(df_id_vg_0.info())

df_id_vg_0_peri=df_id_vg_0[(df_id_vg_0['ratio_peri_area'] > 0.5) & (df_id_vg_0['ratio_peri_area'] <0.9)]


CArea_values =df_id_vg_0['Area']
Cap_values=df_id_vg_0['C']

mp.scatter(CArea_values,Cap_values )
mp.show()



slope_area, intercept, r_value, p_value, std_err = linregress(CArea_values,Cap_values )

print(slope_area)


print(CArea_values)
print(Cap_values)

#print([df_id_vg_0['m'] df_id_vg_0['W'] df_id_vg_0['L'] df_id_vg_0['Area'] df_id_vg_0['Perimeter'] df_id_vg_0['ratio_peri_area'] )

print(df_id_vg_0[['M', 'W', 'L', 'Area', 'Perimeter', 'ratio_peri_area']])

print(df_id_vg_0_peri)


CPeri_values =df_id_vg_0_peri['Perimeter']
Cap_values_peri=df_id_vg_0_peri['C']

mp.scatter(CPeri_values,Cap_values_peri )
mp.show()


slope_peri, intercept, r_value, p_value, std_err = linregress(CPeri_values,Cap_values_peri )

print(slope_peri)
print(slope_area)

print(df_id_vg_0)

X = df_id_vg_0[['Area', 'Perimeter']]
y = df_id_vg_0['C']

regr = linear_model.LinearRegression()
regr.fit(X, y)

# coefficients of Area and Perimeter components
print(regr.coef_)

