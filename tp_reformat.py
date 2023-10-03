"""
This is a script to reformat data from a Tecplot plt file to hdf5 at full resolution, preserving auxiliary data and the nodemap for the original simulation grid.

Call it like:
$ python tp_interpolate.py filename.plt

1. load the data
2. restrict the data to R < 10
3. copy the primary zone to a restricted zone
4. write the copied zone to hdf5
5. add the nodemap

Camilla D. K. Harris
Jan 2023
"""

import h5py
import numpy as np
import swmfpy.tecplottools as tpt
import tecplot as tp

import sys

filename = sys.argv[1]

# load data
print('loading data')
data = tp.data.load_tecplot(filename)
aux_dict = data.zone(0).aux_data.as_dict()
tp.data.operate.execute_equation('{R [R]} = SQRT(V1**2 + V2**2 + V3**2)')
frame = tp.active_frame()
plot = frame.plot()

# blank out extra cells
print('apply blanking')
plot.value_blanking.active = True
plot.value_blanking.cell_mode = tp.constant.ValueBlankCellMode.AnyCorner
constraint = plot.value_blanking.constraint(0)
constraint.active = True
constraint.compare_by = tp.constant.ConstraintOp2Mode.UseConstant
constraint.comparison_operator = tp.constant.RelOp.GreaterThan
constraint.comparison_value = 10
constraint.variable = frame.dataset.variable('R [[]R[]]')

# extract the blanked zone
print('extract blanked zone')
extracted_zone = tp.data.extract.extract_blanked_zones(data.zone(0))

print('write the zone to file')
out_filename = filename[:-4]+'_reformat_nodemap.h5'
print('saving '+out_filename)
tpt.write_zone(
    tecplot_dataset=data,
    tecplot_zone=extracted_zone[0],
    write_as='hdf5',
    filename=out_filename,
    verbose=True
)

print('save nodemap and aux data')
nmap = np.array(data.zone(0).nodemap[:])
with h5py.File(out_filename, 'r+') as f:
    dset = f.create_dataset('nodemap', data=nmap)
    for key in aux_dict:
        f['data'].attrs.create(name=key, data=aux_dict[key])
