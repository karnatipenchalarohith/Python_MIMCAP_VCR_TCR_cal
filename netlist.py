# create Netlist

def createnetlist(wt, lt, mt, Voltage_start, Voltage_stop, Voltage_step, hertz, Temp, lib_path, corner, modelname,terminals):
    filename = "netlist.sp"


    vss = 0


    with open(filename, 'w') as f:
        f.write("* Creating MIMCAP Netlist\n")
        f.write('.option brief \n')
        f.write('.option ingold=2\n')
        f.write('.option gmindc=1e-15\n')
        f.write('.param vg=1 \n')
        f.write('.param ac_v=0.1 \n')




        f.write('.param wt1=' + str(wt) + '\n')
        f.write('.param lt1=' + str(lt) + '\n')
        f.write('.param mt1=' + str(mt) + '\n\n')

        if terminals == 3:
            f.write('xc1  2 3 0 ' + modelname + ' w=wt1 l=lt1 m=mt1   \n\n')
        else:
            f.write('xc1  2 3 ' + modelname + '  w=wt1 l=lt1 m=mt1 \n\n')

        f.write('rg1 1 2 1e-2 \n')
        f.write('v1 1 0 vg ac ac_v \n')
        f.write('v3 3 0 0 \n')


        f.write('.ac lin 1 ' + str(hertz) + ' 10k sweep vg ' + str(Voltage_start) +
                ' ' + str(Voltage_stop) + ' ' + str(Voltage_step) +'\n')

        f.write('.temp ' + str(Temp) + '\n')



        f.write('.meas dc cap1 find par(\'i(rg1)/(2*3.14159*hertz*ac_v)\') when par(\'hertz\') = 100k\' \n\n')


        f.write('.lib ' + '\'' + lib_path + '\'  ' + corner + ' \n\n')
        f.write('.end')

