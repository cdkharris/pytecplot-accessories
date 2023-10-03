"""
This is a script to interpolate Tecplot-formatted data on a spherical grid onto a uniform rectangular grid with ~15 km resolution and save the data as HDF5.

Call it like:
$ python tp_interpolate.py filename.plt

1. load data
2. if 2d, interp onto a 10x5 rectangle
3. if 3d, interp onto a 10x5x10 prism
4. write the new data as hdf5

Camilla D. K. Harris
Jan 2023
"""

import swmfpy.tecplottools as tpt
import tecplot as tp

import sys
import os

filename = sys.argv[1]
basename = os.path.basename(filename)

# parameters for interpolation
imax = 300
jmax = 150
kmax = 300
x1 = -5
y1 = -2.5
z1 = -5
x2 = 5
y2 = 2.5
z2 = 5

# load data
print('loading data')
data = tp.data.load_tecplot(filename)
aux_dict = data.zone(0).aux_data.as_dict()

# interpolate onto a regular rectangular prism
if basename[0] == '3':
    print('interpolating 3d file')
    rect_zone = tpt.interpolate_zone_to_geometry(
        data,
        data.zone(0),
        geometry='rectprism',
        center=[0, 0, 0],
        halfwidths=[x2, y2, z2],
        npoints=[imax, jmax, kmax]
    )
else:
    print('interpolating 2d file')
    tp.macro.execute_command(f'''$!CreateRectangularZone 
    IMax = {imax}
    JMax = {jmax}
    KMax = 1
    X1 = {x1}
    Y1 = {y1}
    Z1 = 0
    X2 = {x2}
    Y2 = {y2}
    Z2 = 0
    XVar = 1
    YVar = 2''')
    tp.data.operate.interpolate_linear(source_zones=[0],
                                       destination_zone=1)
    rect_zone = data.zone(1)

# save as hdf5
print('saving '+filename[:-4]+'_rectprism.h5')
tpt.write_zone(
    tecplot_dataset=data,
    tecplot_zone=rect_zone,
    write_as='hdf5',
    filename=filename[:-4]+'_rectprism.h5'
)
