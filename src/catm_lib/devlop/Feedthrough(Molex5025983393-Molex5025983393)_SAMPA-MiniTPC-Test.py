def add_deviceList(lbrName, deviceLabel, devicePosition,deviceList=[]):
      deviceList.append([lbrName,deviceLabel,devicePosition])
      return deviceList

def add_devices(myFile, devicesInfo):

      for i in range(len(devicesInfo)):
            myFile.write("ADD "+devicesInfo[i][0]+" "+devicesInfo[i][1]+" (%5.2f %5.2f)\n" %(devicesInfo[i][2][0],devicesInfo[i][2][1]))

def SetVias2(myFile, fX=0, fY=0,dL=0.6,dY=0.4,j=1):
      myFile.write('CHANGE DRILL 0.35; \n')
      for i in range(34):
            xv1=fX+dL*i
            yv1=fY+dY*(-1)**(i%2)
            myFile.write('LAYER 18; \n\n')
            if (j!=35)&(j!=34):
                  myFile.write("VIA  \'%d\' %3.2f R (%5.3f %5.3f) \n" %(j, 0.6, xv1, yv1))
            if j!=35:
                  myFile.write('LAYER 1; \n\n')
                  myFile.write("WIRE \'%d'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(j, 0.127, xv1, yv1,  xv1, yv1-dY*(-1)**(i%2) ) )
            if j!=34:
                  myFile.write('LAYER 16; \n\n')
                  myFile.write("WIRE \'%d'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(j, 0.127, xv1, yv1,  xv1, yv1-dY*(-1)**(i%2) ) )
            j+=1
            
      return j

def write_patt(myFile, x0=0, y0=0):
    x, y = 5, 150
    xstep, ystep = 25, 7
    # ボード上にパッドを作成
    npad1, npad2 = 33, 34
    npad = npad1 + npad2
    pitch, pitchy = 0.6, 0.8  # ビアのピッチと分離
    pdx1, pdy1, pdy2 = 0.3, 0.5, 0.67  # SMDパッドの幅と高さ
    x1, y1 = -19.2 / 2, 1.55  # 最初の行のパッドの中心点
    x2, y2 = -19.8 / 2, -1.85 + pdy2 / 2  # 2列目のパッドの中心点
    sepa2, dia, wwidth = 1.5, 0.6, 0.13  # ビアのy方向分離、直径、幅

    # ドリルサイズの変更とビアおよびワイヤの配置
    myFile.write("\n\n################################################\n\n")
    myFile.write("# Change the layer to top (1)\n")
    myFile.write("LAYER 1;\n\n")

    myFile.write("################################################\n\n")
    myFile.write("# Change the drill size to 0.3mm\n")
    myFile.write("CHANGE DRILL 0.3mm;\n")

    myFile.write("################################################\n\n")
    myFile.write("# Create via and wires of connectors No. 1 to 4 on top layer\n")

    for j in range(1, 2):
        
        x = x0 + x2 + pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2

        for i in range(4, npad, 4):
            pn = i - 1 + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                  myFile.write(f"VIA  'Vt{pn}' {dia:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
                  myFile.write(f"WIRE 'Wt{pn}' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y0 + y2:5.3f})\n")
            x += 2 * pitch
            

        x = x0 + x2 + 2 * pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2 - pitchy

        for i in range(3, npad, 4):
            pn = i + 2 + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                  myFile.write(f"VIA 'Vt{pn}' {dia:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
                  myFile.write(f"WIRE 'Wt{pn}' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y0 + y2:5.3f})\n")
            
            x += 2 * pitch
            

    myFile.write("\n\n")
    myFile.write("# Create via and wires of connectors No. 5 to 8 on top layer\n")

    # ボトムレイヤーへの変更
    myFile.write("\n\n################################################\n\n")
    myFile.write("# Change the layer to bottom (16)\n")
    myFile.write("LAYER 16;\n\n")
    myFile.write("# Create wires of connectors No. 1 to 4 on bottom layer\n")

    for j in range(1, 2):
        x = x0 + x2 + pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2

        for i in range(4, npad, 4):
            pn = npad - i + 2 + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                myFile.write(f"WIRE 'Wb{pn}' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y0 + y2:5.3f})\n")
            x += 2 * pitch

        x = x0 + x2 + 2 * pitch + xstep * (j - 1)
        y = y0 + y2 - sepa2 - pitchy
        for i in range(3, npad, 4):
            pn = npad - i - 1 + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                  myFile.write(f"WIRE 'Wb{pn}' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y0 + y2:5.3f})\n")
            x += 2 * pitch

    myFile.write("\n\n")
    myFile.write("# Create wires of connectors No. 5 to 8 on bottom layer\n")

    # SMDパッドをトップレイヤーでグランドに接続
    myFile.write("################################################\n\n")
    grndy = 0.8

    myFile.write("# Change the layer to top (1)\n")
    myFile.write("LAYER 1;\n\n")

    myFile.write("\n\n# Connect pads of connector No.1 to 4 to ground on top layer\n")
    y = y0 + y1

    for j in range(1, 2):
        x = x0 + x1 + xstep * (j - 1)
        for i in range(2, npad + 1, 2):
            pn = i + 100 * j
            if (x > x0 - 5) & (x < x0 + 5):
                  myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y + grndy:5.3f})\n")
            x += pitch

    myFile.write("\n\n# Connect pads of connector No.5 to 8 to ground on top layer\n")

    myFile.write("\n\n")
    myFile.write("# Connect pads no.1 and no.67 to ground on top layer\n")
    y = y0 + y2

    for j in range(1, 2):
        x = x0 + x2 + xstep * (j - 1)
        pn1 = 100 * j + 1
        pn67 = 100 * j + 67
        if (x > x0 - 5) & (x < x0 + 5):
            myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y - grndy:5.3f})\n")
            myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x + (npad2 - 1) * pitch:5.3f}  {y:5.3f}) ({x + (npad2 - 1) * pitch:5.3f}  {y - grndy:5.3f})\n")

    # SMDパッドをトップレイヤーでグランドに接続
    myFile.write("################################################\n\n")
    grndy = 0.8

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

    for j in range(1, 2):
        x = x0 + x2 + xstep * (j - 1)
        pn1 = 100 * j + 1
        pn67 = 100 * j + 67
        if (x > x0 - 5) & (x < x0 + 5):
            myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x:5.3f}  {y:5.3f}) ({x:5.3f}  {y - grndy:5.3f})\n")
            myFile.write(f"WIRE 'GND' {wwidth:5.3f}  ({x + (npad2 - 1) * pitch:5.3f}  {y:5.3f}) ({x + (npad2 - 1) * pitch:5.3f}  {y - grndy:5.3f})\n")



def write_scr_file(fileName='tmpl', devicesInfo=[], basicInfo=[]):

      filePath = './' + fileName + '.scr'

      myFile = open(filePath,'w')
      myFile.write('edit .sch;\n')
      myFile.write('Grid mm 0.01 100 on;\n\n')
      myFile.write('SET PAD_NAMES ON\n')

      if len(devicesInfo)>0:
            add_devices(myFile, devicesInfo)

      myFile.write('edit .brd;\n')
      myFile.write('Grid mm 0.005 200 on;\n')
      myFile.write('Change SIZE 2.0;\n')
      myFile.write('Change ratio 16;\n')
      myFile.write('Change text 0.40;\n')
      myFile.write('SET WIRE_BEND 2;\n')


      myFile.write('\n\n')
      myFile.write('################################################\n\n')
      myFile.write('# Create board on dimension layer (20) \n')
      myFile.write('Change width %4.2f;\n' %(basicInfo[2]))
      myFile.write('LAYER 20;\n')
      myFile.write("WIRE \'B1'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(basicInfo[2], -basicInfo[0],   basicInfo[1],   basicInfo[0],  basicInfo[1] ))
      myFile.write("WIRE \'B2'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(basicInfo[2],  basicInfo[0],   basicInfo[1],   basicInfo[0], -basicInfo[1] ))
      myFile.write("WIRE \'B3'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(basicInfo[2],  basicInfo[0],  -basicInfo[1],  -basicInfo[0], -basicInfo[1] ))
      myFile.write("WIRE \'B4'  %5.3f  (%5.3f  %5.3f)  (%5.3f  %5.3f) \n"  %(basicInfo[2], -basicInfo[0],  -basicInfo[1],  -basicInfo[0],  basicInfo[1] ))
      myFile.write('\n\n')

      myFile.write('################################################\n\n')
      myFile.write('# Create holes on dimension layer (20) \n')
      myFile.write('Change Diameter %3.2f ;\n' %(basicInfo[3]))
      myFile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(basicInfo[3],  basicInfo[4], basicInfo[5]))
      myFile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(basicInfo[3], -basicInfo[4], basicInfo[5]))
      myFile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(basicInfo[3],  basicInfo[4],-basicInfo[5]))
      myFile.write('HOLE %3.2f (%5.3f  %5.3f) \n'%(basicInfo[3], -basicInfo[4],-basicInfo[5]))

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to top stop(29) \n')
      myFile.write('LAYER 29; \n\n')
      myFile.write('# Create tstop layer \n')
      myFile.write('CHANGE WIDTH %5.3fmm;\n'%( basicInfo[7]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%( basicInfo[4],  basicInfo[5],  basicInfo[4],   basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%(-basicInfo[4],  basicInfo[5], -basicInfo[4],   basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%( basicInfo[4], -basicInfo[5],  basicInfo[4],  -basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%(-basicInfo[4], -basicInfo[5], -basicInfo[4],  -basicInfo[5] +basicInfo[6]))
      myFile.write('CHANGE WIDTH %5.3f;\n\n' %(0.13))

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to bottom stop(30) \n')
      myFile.write('LAYER 30; \n\n')
      myFile.write('# Create tstop layer \n')
      myFile.write('CHANGE WIDTH %5.3fmm;\n'%( basicInfo[7]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%( basicInfo[4],  basicInfo[5],  basicInfo[4],   basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%(-basicInfo[4],  basicInfo[5], -basicInfo[4],   basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%( basicInfo[4], -basicInfo[5],  basicInfo[4],  -basicInfo[5] +basicInfo[6]))
      myFile.write('CIRCLE (%5.3f  %5.3f) (%5.3f  %5.3f) \n'%(-basicInfo[4], -basicInfo[5], -basicInfo[4],  -basicInfo[5] +basicInfo[6]))
      myFile.write('CHANGE WIDTH %5.3f;\n\n' %(0.13))


      return myFile

if __name__ == "__main__":
      
      base_dir = 'scr_file'
      
      output_file_name = 'Feedthrough(Molex5025983393-Molex5025983393)_SAMPA-MiniTPC-Test'
      # output_file_name = 'Feedthrough(Molex5025983393-Molex5025983393)_SAMPA-MiniTPC-Test-実装図'

      # devicesInfo=[]
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Ct1',[120,0])
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Ct2',[120,0], devicesInfo)
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Ct3',[120,0], devicesInfo)
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Ct4',[120,0], devicesInfo)

      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Cb1',[130,0], devicesInfo)
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Cb2',[130,0], devicesInfo)
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Cb3',[130,0], devicesInfo)
      devicesInfo = add_deviceList('5025983393@5025983393.lbr','Cb4',[130,0], devicesInfo)

      basicInfo = [100./2, 30./2, 0.2, 6., 90./2., 20./2, 6./2, 1.65] 
      # board x, board y, line width, diameter, hole x, hole y, hole stop radius, hole stop width
      
      myFile = write_scr_file(base_dir+'/'+output_file_name, devicesInfo, basicInfo)

      ################################################################################################
      ## コネクター
      ################################################################################################
      shiftx1 = 24.0
      shiftx2 =  8.0

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to top (1)  \n')
      myFile.write('LAYER 1; \n\n')
      
      myFile.write('MOVE   Ct1 (%5.2f %5.2f);\n' %( 0. - shiftx1 , 0.))
      myFile.write('MOVE   Ct2 (%5.2f %5.2f);\n' %( 0. - shiftx2 , 0.))
      myFile.write('MOVE   Ct3 (%5.2f %5.2f);\n' %( 0. + shiftx2 , 0.))
      myFile.write('MOVE   Ct4 (%5.2f %5.2f);\n' %( 0. + shiftx1 , 0.))

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to bottom (16)  \n')
      myFile.write('LAYER 16; \n\n')

      myFile.write('Mirror Cb1; \n')
      myFile.write('Mirror Cb2; \n')
      myFile.write('Mirror Cb3; \n')
      myFile.write('Mirror Cb4; \n')

      myFile.write('MOVE   Cb1 (%5.2f %5.2f);\n' %( 0. - shiftx1 , 0.))
      myFile.write('MOVE   Cb2 (%5.2f %5.2f);\n' %( 0. - shiftx2 , 0.))
      myFile.write('MOVE   Cb3 (%5.2f %5.2f);\n' %( 0. + shiftx2 , 0.))
      myFile.write('MOVE   Cb4 (%5.2f %5.2f);\n' %( 0. + shiftx1 , 0.))

      myFile.write('ROTATE Ct1;\n' )
      myFile.write('ROTATE Ct1;\n' )
      myFile.write('ROTATE Ct2;\n' )
      myFile.write('ROTATE Ct2;\n' )
      myFile.write('ROTATE Ct3;\n' )
      myFile.write('ROTATE Ct3;\n' )
      myFile.write('ROTATE Ct4;\n' )
      myFile.write('ROTATE Ct4;\n' )

      myFile.write('ROTATE Cb1;\n' )
      myFile.write('ROTATE Cb1;\n' )
      myFile.write('ROTATE Cb2;\n' )
      myFile.write('ROTATE Cb2;\n' )
      myFile.write('ROTATE Cb3;\n' )
      myFile.write('ROTATE Cb3;\n' )
      myFile.write('ROTATE Cb4;\n' )
      myFile.write('ROTATE Cb4;\n' )
      ################################################################################################
      ## 回路パターン
      ################################################################################################
      
      write_patt(myFile, -shiftx1, 0)
      write_patt(myFile, -shiftx2, 0)
      write_patt(myFile, +shiftx2, 0)
      write_patt(myFile, +shiftx1, 0)

      ################################################################################################
      ## ストップパターン
      ################################################################################################
      x1 = 82.2
      x2 = 73.0
      y1 = 25.2
      y2 = 16.0
      delta1 = 0.2
      delta2 = 0.1
      r1 = 8.1
      r2 = 3.5

      stopx=((x1-delta1)+(x2+delta1))/2
      stopy=((y1-delta1)+(y2+delta1))/2
      r0=((r1-delta2)+(r2+delta2))/2
      stopwidth=((y1-delta1)-(y2+delta1))/2+delta1

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to top stop(29) \n')
      myFile.write('LAYER 29; \n\n')
      myFile.write('# Create tstop layer \n')
      myFile.write('Change width %4.2f;\n' %(basicInfo[2]))
      myFile.write('WIRE \'Wtstop\' %5.3f  (%5.3f  %5.3f) @+%5.3f (%5.3f  %5.3f)  (%5.3f  %5.3f) @+%5.3f  (%5.3f  %5.3f) (%5.3f  %5.3f) @+%5.3f (%5.3f  %5.3f) (%5.3f  %5.3f)  @+%5.3f (%5.3f  %5.3f) (%5.3f  %5.3f) \n' %(stopwidth , -stopx/2+r0, stopy/2, r0, -stopx/2, stopy/2-r0, -stopx/2,-stopy/2+r0, r0,-stopx/2+r0,-stopy/2,stopx/2-r0,-stopy/2, r0,  stopx/2,-stopy/2+r0,  stopx/2, stopy/2-r0, r0, stopx/2-r0, stopy/2, -stopx/2+r0, stopy/2))

      myFile.write('#################################\n\n')
      myFile.write('# Change the layer to bottom stop(30) \n')
      myFile.write('LAYER 30; \n\n')
      myFile.write('# Create tstop layer \n')
      myFile.write('Change width %4.2f;\n' %(basicInfo[2]))
      myFile.write('WIRE \'Wbstop\' %5.3f  (%5.3f  %5.3f) @+%5.3f (%5.3f  %5.3f)  (%5.3f  %5.3f) @+%5.3f  (%5.3f  %5.3f) (%5.3f  %5.3f) @+%5.3f (%5.3f  %5.3f) (%5.3f  %5.3f)  @+%5.3f (%5.3f  %5.3f) (%5.3f  %5.3f) \n' %(stopwidth , -stopx/2+r0, stopy/2, r0, -stopx/2, stopy/2-r0, -stopx/2,-stopy/2+r0, r0,-stopx/2+r0,-stopy/2,stopx/2-r0,-stopy/2, r0,  stopx/2,-stopy/2+r0,  stopx/2, stopy/2-r0, r0, stopx/2-r0, stopy/2, -stopx/2+r0, stopy/2))

      ################################################################################################
      ## ベタパターン
      ################################################################################################

      copperx = basicInfo[0] * 2 - 2.5 + 0.13/2
      coppery = basicInfo[1] * 2 - 2.5 + 0.13/2
      r0 = 4 - 0.4
      copperon = 1

      bigD=2.0
      smallD=0.600

      myFile.write("\n\n")
      myFile.write("################################################\n\n")
      myFile.write("# Change isolation distance between pads(wires) and ground to 0.3mm \n")
      myFile.write("CHANGE Isolate 0.3mm ;\n\n")
      myFile.write('CHANGE WIDTH 0.13mm;\n')

      myFile.write("################################################\n\n")
      myFile.write("# Change the layer to top (1) \n")
      if copperon == 1:
            myFile.write("LAYER 1 ;\n\n")

            x,y = 0,0
            myFile.write(f"VIA 'GND' {bigD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            
            x,y = 0,6
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {-y:5.3f})\n")

            x,y = 32,0
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {y:5.3f})\n")

            x,y = 32/2,0
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {y:5.3f})\n")

            x,y = 32,6
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {-y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {-y:5.3f})\n")

            x,y = 32/2,6
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({x:5.3f}  {-y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {y:5.3f})\n")
            myFile.write(f"VIA 'GND' {smallD:3.2f} R  ({-x:5.3f}  {-y:5.3f})\n")

            myFile.write("# Create copper area on top layer \n")
            myFile.write(
                  f"POLYGON 'GND' ({-copperx / 2 + r0:5.3f} {-coppery / 2:5.3f}) ({copperx / 2 - r0:5.3f} {-coppery / 2:5.3f}) "
                  f"@+{r0:4.2f} ({copperx / 2:5.3f} {-coppery / 2 + r0:5.3f}) ({copperx / 2:5.3f} {coppery / 2 - r0:5.3f}) "
                  f"@+{r0:4.2f} ({copperx / 2 - r0:5.3f} {coppery / 2:5.3f}) ({-copperx / 2 + r0:5.3f} {coppery / 2:5.3f}) "
                  f"@+{r0:4.2f} ({-copperx / 2:5.3f} {coppery / 2 - r0:5.3f}) ({-copperx / 2:5.3f} {-coppery / 2 + r0:5.3f}) "
                  f"@+{r0:4.2f} ({-copperx / 2 + r0:5.3f} {-coppery / 2:5.3f})\n"
            )
            myFile.write("# Pour copper \n")
            myFile.write("RATSNEST 'GND' ;\n\n")

            myFile.write("# Change the layer to bottom (16) \n")
            myFile.write("LAYER 16 ;\n\n")

            myFile.write("# Create copper area on bottom layer \n")
            myFile.write(
                  f"POLYGON 'GND' ({-copperx / 2 + r0:5.3f} {-coppery / 2:5.3f}) ({copperx / 2 - r0:5.3f} {-coppery / 2:5.3f}) "
                  f"@+{r0:4.2f} ({copperx / 2:5.3f} {-coppery / 2 + r0:5.3f}) ({copperx / 2:5.3f} {coppery / 2 - r0:5.3f}) "
                  f"@+{r0:4.2f} ({copperx / 2 - r0:5.3f} {coppery / 2:5.3f}) ({-copperx / 2 + r0:5.3f} {coppery / 2:5.3f}) "
                  f"@+{r0:4.2f} ({-copperx / 2:5.3f} {coppery / 2 - r0:5.3f}) ({-copperx / 2:5.3f} {-coppery / 2 + r0:5.3f}) "
                  f"@+{r0:4.2f} ({-copperx / 2 + r0:5.3f} {-coppery / 2:5.3f})\n"
            )
            myFile.write("# Pour copper \n")
            myFile.write("RATSNEST 'GND' ;\n\n")