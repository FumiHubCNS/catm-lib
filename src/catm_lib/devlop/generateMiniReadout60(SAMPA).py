import math

def process_number_odd(num):
    if (num - 1) % 4 == 0:  # 1, 5, 9, 13...
        return +1
    elif (num - 3) % 4 == 0:  # 3, 7, 11, 15...
        return -1
    else:
        return 0
    

def process_number_even(num):
    if num % 4 == 0:  # 4, 8, 12, 16...
        return +1
    elif (num - 2) % 4 == 0:  # 2, 6, 10, 14...
        return -1
    else:
        return 0


def write_linier_patt(myFile, w=0, x1=0, y1=0, x2=0, y2=0, label='GND'):
    myFile.write(f"WIRE '{label}' {w:5.3f}  ({x1:5.3f}  {y1:5.3f}) ({x2:5.3f}  {y2:5.3f})\n")

def write_gnd_patt(myFile, x0=0, y0=0, mirrorFlag=False):
    x, y = 5, 150
    xstep, ystep = 25, 7
    # ボード上にパッドを作成
    npad1, npad2 = 33, 34
    npad = npad1 + npad2
    pitch, pitchy = 0.6, 0.8  # ビアのピッチと分離
    pdx1, pdy1, pdy2 = 0.3, 0.5, 0.67  # SMDパッドの幅と高さ
    x1, y1 = -19.2 / 2, 1.55  # 最初の行のパッドの中心点
    x2, y2 = -19.8 / 2, -2.4 + pdy2 / 2  # 2列目のパッドの中心点
    sepa2, dia, wwidth = 1.5, 0.6, 0.13  # ビアのy方向分離、直径、幅

    # ボトムレイヤーへの変更
    myFile.write("\n\n################################################\n\n")
    myFile.write("# Change the layer to bottom (16)\n")
    myFile.write("LAYER 16;\n\n")
    myFile.write("# Create wires of connectors No. 1 to 4 on bottom layer\n")

    # SMDパッドをトップレイヤーでグランドに接続
    myFile.write("################################################\n\n")
    grndy = 0.8

    if mirrorFlag == True:
        y1 *= -1
        grndy *= -1

    myFile.write("# Change the layer to bottom (16)\n")
    myFile.write("LAYER 16;\n\n")

    myFile.write("\n\n# Connect pads of connector No.1 to 4 to ground on bottom layer\n")
    y = y0 + y1

    for j in range(1, 2):
        x = x0 + x1 + xstep * (j - 1)
        for i in range(2, npad + 1, 2):
            pn = i + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                  myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y + grndy:5.3f})\n")
            x += pitch

    myFile.write("\n\n# Connect pads of connector No.5 to 8 to ground on bottom layer\n")

    myFile.write("\n\n")
    myFile.write("# Connect pads no.1 and no.67 to ground on bottom layer\n")
    y = y0 + y2
    
    signal_smd_posx = []

    for j in range(1, 2):
        
        x = x0 + x2 + pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2

        for i in range(4, npad, 4):

            if (x > x0 - 5) & (x < x0 + 5):
                  signal_smd_posx.append(x)

            x += 2 * pitch
            
        x = x0 + x2 + 2 * pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2 - pitchy

        for i in range(3, npad, 4):

            if (x > x0 - 5) & (x < x0 + 5):
                  signal_smd_posx.append(x)
            
            x += 2 * pitch


    sorted_signal_smd_posx = sorted(signal_smd_posx)

    return sorted_signal_smd_posx, y0 + grndy * y2

def calculate_conner_points(x,y,d,condition="12"):

    points = []
    
    x1 = x + d 
    x2 = x
    x3 = x - d
    x4 = x

    y1 = y 
    y2 = y - d
    y3 = y
    y4 = y + d

    if condition[0] == "1":
        points.append(x1)
        points.append(y1)
    elif condition[0] == "2":
        points.append(x2)
        points.append(y2)
    elif condition[0] == "3":
        points.append(x3)
        points.append(y3)
    elif condition[0] == "4":
        points.append(x4)
        points.append(y4)
    else:
        print("invalid condition")

    if condition[1] == "1":
        points.append(x1)
        points.append(y1)
    elif condition[1] == "2":
        points.append(x2)
        points.append(y2)
    elif condition[1] == "3":
        points.append(x3)
        points.append(y3)
    elif condition[1] == "4":
        points.append(x4)
        points.append(y4)
    else:
        print("invalid condition")

    if len(points) != 4:
        print("invalid condition")

    return points

if __name__ == "__main__":
    ########################### open script file ####################################

    myfile = open('scr_file/generateMiniReadout60(SAMPA).scr','w')
    # myfile = open('scr_file/generateMiniReadout60(SAMPA)-実装図.scr','w')
    myfile.write('#This is a script for ReadoutPad of MiniTPC, Signal lines should be manually connected \n\n')
    myfile.write('# Only redout part\n\n')
    myfile.write('################################################\n\n')
    myfile.write('#Use the connector library writen by Kojima\n')
    myfile.write('#USE FH39A-67S.lbr;\n\n')
    myfile.write('#USE ReadoutPad3mm.lbr;\n\n')
    #myfile.write('#USE ReadoutPad.lbr;\n\n')
    ################# edit schech ##################################################
    myfile.write('# Edit the schematic window\n')
    myfile.write('edit .sch;\n')
    myfile.write('# Set the grid \n')
    myfile.write('Grid mm 0.01 100 on;\n\n')
    myfile.write('# Put the connectors on screen \n')

    nconnect=4       # number of connector
    x=5.0              # temp position
    y=150.0            # temp position
    i=1

    while i <= nconnect:
        myfile.write("ADD 5025983393@5025983393.lbr 'Cd%d' SMR0 (%5.2f %5.2f)\n" %(i,x,y) ) 
        y=y-150
        i+=1
    j=1
    npad=60
    x=100
    y=186-4
    while j<= npad:
        myfile.write("ADD PAD3MM@ReadoutPad3mmEndo.lbr 'RPad%d' SMR0 (%5.2f %5.2f)\n"%(j,x,y) )
        y=y-6
        j+=1
        
    #############################  edit board  #####################################
    myfile.write('################################################\n\n')
    myfile.write('# Edit the Borad window\n')
    myfile.write('edit .brd;\n')
    myfile.write('# Set the grid \n')
    myfile.write('Grid mm 0.005 200 on;\n')
    myfile.write('Change SIZE 2.0;\n')
    myfile.write('Change ratio 16;\n')
    myfile.write('Change text 2.0;\n')
    #myfile.write('CHANGE THERMALS ON\n')
    myfile.write('# Set Pad names off \n')
    myfile.write('SET PAD_NAMES OFF \n')

    ###################### Create a board ####################
    
    bdx=94       # Board Size along beam axis
    bdy= 70      # Board Size  
    xc=bdx/2     # Center of Board
    yc=bdy/2     # Center of Board
    bw=0.2       # line width
    dia=3.2      # hole diameter near the center connected to M2.6
    hx1=9.0      # hole x position
    hx2=bdx-hx1  # hole x position
    hy1=13.5     # hole y position
    hy2=yc       # hole y position
    hy3=bdy-hy1  # hole y position

    delta=5.0       
    ########################################################################################

    myfile.write('\n\n');
    myfile.write('################################################\n\n')
    myfile.write('# Create board on dimension layer (20) \n')
    myfile.write('Change width %4.2f;\n' %(bw))
    myfile.write('LAYER 20;\n')
    myfile.write("WIRE \'B1'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(bw,   0,   0, bdx,   0 ))
    myfile.write("WIRE \'B2'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(bw, bdx,   0, bdx, bdy ))
    myfile.write("WIRE \'B3'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(bw, bdx, bdy,   0, bdy ))
    myfile.write("WIRE \'B4'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(bw,   0, bdy,   0,   0 ))


    myfile.write('\n\n');
    myfile.write('################################################\n\n')
    myfile.write('# Create holes on dimension layer (20) \n')
    myfile.write('Change Diameter %3.2f ;\n' %(dia))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx1,hy1))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx1,hy2))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx1,hy3))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx2,hy1))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx2,hy2))
    myfile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(dia,  hx2,hy3))


    ########################################### Create Vias on Pad center  ########################
    myfile.write('\n\n')
    myfile.write('#################################')
    myfile.write('# Change Layer to top \n')
    myfile.write('LAYER 1; \n\n')
    myfile.write('################################################\n\n')
    myfile.write('# Change the drill size to 0.3mm \n')
    myfile.write('CHANGE DRILL 0.3mm; \n')
    myfile.write('# Create vias of connector \n')

    padlw=0.2
    a=3          # size or readout pad
    nRpad=22/2 # number of read out pad in one raw
    pitchrp=a/2
    vdia=0.6             # diameter of via
    rpx0=pitchrp*(nRpad-1)/2
    k=1
    vdia = 0.6

    padinfo = []

    myfile.write('Change width %4.2f;\n' %(padlw))
    myfile.write('SET WIRE_BEND 2;\n')
    myfile.write('CHANGE Isolate 0.1mm ;\n\n');

    offset_x = - 4.75 * a + a / 4
    offset_y = - a * math.sqrt(3)/2
    for i in range(20):
        j = i+1

        if i%2 == 0:
            myfile.write("ROTATE R180  \'RPAD%d\';\n" %(j))
            dy =   a * math.sqrt(3)/12
        else:
            dy = - a * math.sqrt(3)/12

        myfile.write("MOVE  \'RPAD%d\' (%5.3f  %5.3f);\n" %(j, xc+a/2*i+offset_x, yc+dy+offset_y))
        myfile.write("VIA   \'VIA%d\' %3.2f R  (%5.3f  %5.3f) \n" %(j,vdia, xc+a/2*i+offset_x, yc+dy+offset_y))
        padinfo.append( [ j, xc+a/2*i+offset_x, yc+dy+offset_y ] )

    offset_x = - 4.75 * a 
    offset_y = 0
    for i in range(20):
        j = i+21

        if i%2 == 0:
            myfile.write("ROTATE R180  \'RPAD%d\';\n" %(j))
            dy =   a * math.sqrt(3)/12
        else:
            dy = - a * math.sqrt(3)/12

        myfile.write("MOVE  \'RPAD%d\' (%5.3f  %5.3f);\n" %(j, xc+a/2*i+offset_x, yc+dy+offset_y))
        myfile.write("VIA   \'VIA%d\' %3.2f R  (%5.3f  %5.3f) \n" %(j,vdia, xc+a/2*i+offset_x, yc+dy+offset_y))
        padinfo.append( [ j, xc+a/2*i+offset_x, yc+dy+offset_y ] )

    offset_x = - 4.75 * a - a / 4
    offset_y = + a * math.sqrt(3)/2
    for i in range(20):
        j = i+41

        if i%2 == 0:
            myfile.write("ROTATE R180  \'RPAD%d\';\n" %(j))
            dy =   a * math.sqrt(3)/12
        else:
            dy = - a * math.sqrt(3)/12

        myfile.write("MOVE  \'RPAD%d\' (%5.3f  %5.3f);\n" %(j, xc+a/2*i+offset_x, yc+dy+offset_y))
        myfile.write("VIA   \'VIA%d\' %3.2f R  (%5.3f  %5.3f) \n" %(j, vdia, xc+a/2*i+offset_x, yc+dy+offset_y))
        padinfo.append( [ j, xc+a/2*i+offset_x, yc+dy+offset_y ] )

    ########## Create ground pads on top layer ##########
    myfile.write('################################################\n\n')
    #myfile.write('# Change Gounrd Pads on Top Layer \n')
    #myfile.write('CHANGE THERMALS ON\n')
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia,     25,    15))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia, bdx-25,    15))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia, bdx-25,bdy-15))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia,     25,bdy-15))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia,     25,   yc))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia, bdx-25,   yc))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia,     xc,   yc+20))
    myfile.write("VIA \'GND\' %3.2f R  (%5.3f  %5.3f) \n" %(vdia,     xc,   yc-20))

    ########## Create cupper area on  top layer ##########
    lw=0.2
    copperx1=14
    copperx2=copperx1+66
    coppery1=0.5
    coppery2=coppery1+69

    myfile.write('\n\n')
    myfile.write('################################################\n\n')
    myfile.write('# Create copper area on Top layer \n')
    myfile.write('Change width %4.2f;\n' %(lw))
    myfile.write('Change Isolate 0.15;\n')
    myfile.write("POLYGON \'GND\' (%5.3f  %5.3f)  (%5.3f  %5.3f)  (%5.3f  %5.3f)  (%5.3f  %5.3f) (%5.3f  %5.3f)\n" \
                %(copperx1+lw/2,coppery1+lw/2,copperx2-lw/2,coppery1+lw/2,copperx2-lw/2,coppery2-lw/2,copperx1+lw/2,coppery2-lw/2,copperx1+lw/2,coppery1+lw/2))


    # ########################################### put the connectors on bottom layer ########################

    myfile.write('#################################')
    myfile.write('# Put the connectors on bottom layer \n')
    myfile.write('LAYER 16; \n\n')
    myfile.write('Change width %4.2f;\n' %(lw))
    
    cony = 0
    conx = xc
    mirrorFlag=False

    smds_posx=[]
    smds_posy=[]

    for  i in range(4):

        myfile.write('MIRROR Cd%d ;\n'%(i+1))

        if i < 2:
            cony = 21 
            mirrorFlag=True
        else:
            cony = 49
            myfile.write('ROTATE Cd%d ;\n'%(i+1))
            myfile.write('ROTATE Cd%d ;\n'%(i+1))
            mirrorFlag=False
        
        if i % 2 == 0:
            conx = xc - 10  
        else:
            conx = xc + 10

        

        myfile.write('MOVE Cd%d (%5.2f %5.2f);\n' %(i+1,conx,cony))
        xs,y = write_gnd_patt(myfile,conx,cony,mirrorFlag)

        smds_posx.append(xs)
        smds_posy.append(y)

    ########################################### signal line drawing part ###########################################

    padsx = []
    padsy = []

    for i in range(len(padinfo)):
     padsx.append(padinfo[i][1])
     padsy.append(padinfo[i][2])
     
    center_pads_x = sum(padsx) / len(padsx)
    center_pads_y = sum(padsy) / len(padsy)

    padinfo1 = [row for row in padinfo if row[2] < yc]
    padinfo2 = [row for row in padinfo if row[2] > yc]

    sorted_padinfo1 = sorted(padinfo1, key=lambda row: row[1])
    sorted_padinfo2 = sorted(padinfo2, key=lambda row: row[1])

    for i in range(60):

        ################ connector 1 2 ################
        if i < 30:
            j = i//16
            k = i%16
        
            x_con = smds_posx[j][k]
            y_con = smds_posy[j]
            x_pad = sorted_padinfo1[i][1]
            y_pad = sorted_padinfo1[i][2]

            # print("%d %d %d (%5.3f %5.3f) (%5.3f %5.3f)" %(i,j,k, x_con,y_con,x_pad,y_pad))

            ################ connector 1 ################
            if i < 16:

                base_midy = center_pads_y - 1.5 * 3. * math.sqrt(3.) / 2. 

                cpoints1 = calculate_conner_points(x_con, base_midy-0.5*i, 0.5, "21")
                cpoints2 = calculate_conner_points(x_pad, base_midy-0.5*i, 0.5, "34")

                if abs(cpoints2[0] - cpoints1[2]) <= bw / 2. :
                    myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2], cpoints1[1] + cpoints2[2]-cpoints1[0], x_pad, y_pad))

                elif cpoints2[0] - cpoints1[2] > bw / 2. :
                    myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, *cpoints1, *cpoints2, x_pad, y_pad))

            ################ connector 2 ################
            else:

                if i < 24:

                    base_midy = y_con + 1.5 * 3. * math.sqrt(3.) / 2. 

                    cpoints1 = calculate_conner_points(x_con, base_midy+0.5*(i-16), 0.5, "23")
                    cpoints2 = calculate_conner_points(x_pad, base_midy+0.5*(i-16), 0.5, "14")
                    
                    if i > 20:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2],cpoints1[1] + cpoints1[0] - cpoints2[2], x_pad, y_pad))

                    else:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, *cpoints1, *cpoints2, x_pad, y_pad))
                
                else:

                    base_midy = center_pads_y - 1.5 * 3. * math.sqrt(3.) / 2. 

                    cpoints1 = calculate_conner_points(x_con, base_midy-0.5*(i-22), 0.5, "21")
                    cpoints2 = calculate_conner_points(x_pad, base_midy-0.5*(i-22), 0.5, "34")

                    if i < 27:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2], cpoints1[1] + cpoints2[2]-cpoints1[0], x_pad, y_pad))

                    else:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, *cpoints1, *cpoints2, x_pad, y_pad))

        ################ connector 3 4 ################
        else:
            j = (i-30)//16 + 2 
            k = (i-30)%16

            x_con = smds_posx[j][k]
            y_con = smds_posy[j]
            x_pad = sorted_padinfo2[i-30][1]
            y_pad = sorted_padinfo2[i-30][2]

            # print("%d %d %d (%5.3f %5.3f) (%5.3f %5.3f)" %(i,j,k, x_con,y_con,x_pad,y_pad))

            ################ connector 3 ################
            if (i-30) < 16:
            
                base_midy = center_pads_y + 1.5 * 3. * math.sqrt(3.) / 2. 

                cpoints1 = calculate_conner_points(x_con, base_midy+0.5*(i-30), 0.5, "43")
                cpoints2 = calculate_conner_points(x_pad, base_midy+0.5*(i-30), 0.5, "12")

                if i-30 == 0 :
                    myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1]+ 0.8, cpoints2[2], cpoints1[1] + cpoints2[2]-cpoints1[0] + 0.8, x_pad, y_pad))
                elif i-30 < 3 :
                    myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2], cpoints1[1] + cpoints2[2]-cpoints1[0], x_pad, y_pad))

                else:

                    base_midy = center_pads_y + 1.5 * 3. * math.sqrt(3.) / 2. 

                    cpoints1 = calculate_conner_points(x_con, base_midy+0.5*(i-30), 0.5, "41")
                    cpoints2 = calculate_conner_points(x_pad, base_midy+0.5*(i-30), 0.5, "32")

                    if i-30 < 6 :
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2], cpoints1[1]-(cpoints2[2]-cpoints1[0]), x_pad, y_pad))

                    else:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, *cpoints1, *cpoints2, x_pad, y_pad))

            ################ connector 4 ################
            else:
                if (i-30) < 28:

                    base_midy = y_con - 1 

                    cpoints1 = calculate_conner_points(x_con, base_midy-0.5*(i-30-16), 0.5, "43")
                    cpoints2 = calculate_conner_points(x_pad, base_midy-0.5*(i-30-16), 0.5, "12")

                    print(i-30, y_con, cpoints1, cpoints2)
                    
                    if (i-30) > 24:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2],cpoints1[1]-(cpoints1[0] - cpoints2[2]), x_pad, y_pad))

                    else:
                        myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, *cpoints1, *cpoints2, x_pad, y_pad))
                
                else:

                    
                    base_midy = center_pads_y + 1.5 * 3. * math.sqrt(3.) / 2. 

                    cpoints1 = calculate_conner_points(x_con, base_midy+0.5*(i-30-22), 0.5, "41")
                    cpoints2 = calculate_conner_points(x_pad, base_midy+0.5*(i-30-22), 0.5, "32")

                    myfile.write("WIRE 'WIREp%d' 0.13  (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) (%5.3f %5.3f) \n" %(i, x_con, y_con, cpoints1[0], cpoints1[1], cpoints2[2], cpoints1[1]-(cpoints2[2]-cpoints1[0]), x_pad, y_pad))


    write_linier_patt(myfile, 0.13, smds_posx[1][14],smds_posy[1], smds_posx[1][14], smds_posy[1]+0.8, 'GND')
    write_linier_patt(myfile, 0.13, smds_posx[1][15],smds_posy[1], smds_posx[1][15], smds_posy[1]+0.8, 'GND')
    write_linier_patt(myfile, 0.13, smds_posx[3][14],smds_posy[3], smds_posx[3][14], smds_posy[3]-0.8, 'GND')
    write_linier_patt(myfile, 0.13, smds_posx[3][15],smds_posy[3], smds_posx[3][15], smds_posy[3]-0.8, 'GND')


    ################## Create cupper area on bottom layer
    myfile.write('#################################')
    myfile.write('Change width %4.2f;\n' %(lw))
    myfile.write("POLYGON \'GND\' (%5.3f  %5.3f)  (%5.3f  %5.3f)  (%5.3f  %5.3f)  (%5.3f  %5.3f) (%5.3f  %5.3f)\n" \
                %(copperx1+lw/2,coppery1+lw/2,copperx2-lw/2,coppery1+lw/2,copperx2-lw/2,coppery2-lw/2,copperx1+lw/2,coppery2-lw/2,copperx1+lw/2,coppery1+lw/2))

    ######################### Parameter of HIROSE Connectors ######


    myfile.write('LAYER 29; \n\n')
    myfile.write('RECT (%5.3f  %5.3f)  (%5.3f  %5.3f);\n' \
                %(copperx1, coppery1+25, copperx2, coppery2-25))

    #myfile.write("RATSNEST \'GND\' ;\n\n")
    myfile.write('CHANGE THERMALS OFF\n')
    myfile.write('SET WIRE_BEND 2;\n')

    myfile.close()