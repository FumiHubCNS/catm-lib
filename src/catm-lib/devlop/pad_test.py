"""!
@file padinfo.py
@version 1
@author Fumitaka ENDO
@date 2025-07-25T20:10:19+09:00
@brief get pad configuration 
"""
import argparse
import pathlib
import catmlib as cat
import numpy as np
import copy

this_file_path = pathlib.Path(__file__).parent

def get_tpc_info(zoffset=0):  

  base_padinfo = cat.readoutpad.basepad.generate_regular_n_polygon(3, 2.75, 90,False)

  pad = cat.readoutpad.basepad.TReadoutPadArray()
  pad.add_basepad(base_padinfo)
  pad_distance = 3
  gid = 0
  nmax=21
  offset = 15.75

  for i in range(nmax+1):
    if i >1:
      pad.add_pads([(i-0.5)*pad_distance/2-offset, 0, pad_distance/np.sqrt(3)/2*((i-1)%2)+zoffset], 0, 0, 180*((i-1)%2), 0, gid)
      pad.id = gid
      gid += 1
  for i in range(nmax):
    if i >0:
      pad.add_pads([((i+0))*pad_distance/2-offset, 0, pad_distance/np.sqrt(3)/2*((i)%2) + np.sqrt(3)*pad_distance/2+zoffset], 0, 0, 180*((i)%2), 0, gid)
      pad.id = gid
      gid += 1
  for i in range(nmax):
    if i < nmax-1:
      pad.add_pads([(i+0.5)*pad_distance/2-offset, 0, pad_distance/np.sqrt(3)/2*((i-1)%2) + 2*np.sqrt(3)*pad_distance/2+zoffset] , 0, 0, 180*((i-1)%2), 0, gid)
      pad.id = gid
      gid += 1

  return pad


def marge_padinfos(pad1:cat.readoutpad.basepad.TReadoutPadArray, pad2: cat.readoutpad.basepad.TReadoutPadArray):

  obj = copy.deepcopy(pad1)
  gid = max(pad1.ids)

  offset = gid + 1 
  for i in range(len(pad2.ids)):
    polygon_new = pad2.pads[i]
    id = offset + pad2.ids[i]

    obj.pads.append(polygon_new)
    obj.ids.append(id)
    obj.centers.append(np.mean(polygon_new, axis=0))
    obj.charges.append(0)

  return obj

def main():
    offset = -3.031088913245535
    pad1 = get_tpc_info(offset+45)
    pad2 = get_tpc_info(offset+136.5)
    tpcs = marge_padinfos(pad1,pad2)

    # tpcs.show_pads(check_id=True)

    bins, colors = cat.util.catmviewer.get_color_list(tpcs.ids)
    color_array = cat.util.catmviewer.get_color_array(tpcs.ids,bins,colors)

    # for i in range(len(colors)):
    #   print(colors[i])

    tpcs.show_pads(plot_type='map',color_map=color_array,check_id=True)

if __name__ == "__main__":
    main()
