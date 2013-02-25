# -*- coding: utf-8 -*-
# YAFF is yet another force-field code
# Copyright (C) 2011 - 2012 Toon Verstraelen <Toon.Verstraelen@UGent.be>,
# Louis Vanduyfhuys <Louis.Vanduyfhuys@UGent.be>, Center for Molecular Modeling
# (CMM), Ghent University, Ghent, Belgium; all rights reserved unless otherwise
# stated.
#
# This file is part of YAFF.
#
# YAFF is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# YAFF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


from molmod import angstrom, amu, picosecond
from molmod.io import DLPolyHistoryReader
from yaff.conversion.common import get_trajectory_group, \
    get_trajectory_datasets, append_to_dataset, check_trajectory_rows
from yaff.log import log


__all__ = ['dlpoly_history_to_hdf5']


def dlpoly_history_to_hdf5(f, fn_history, sub=slice(None), pos_unit=angstrom,
    vel_unit=angstrom/picosecond, frc_unit=amu*angstrom/picosecond**2,
    time_unit=picosecond, mass_unit=amu):
    """Convert XYZ trajectory file to Yaff HDF5 format.

       **Arguments:**

       f
            An open and writable HDF5 file.

       fn_hisotyr
            The filename of the DLPOLY history file.

       **Optional arguments:**

       sub
            The sub argument for the DLPolyHistoryReader. This must be a slice
            object that defines the subsampling of the samples from the history
            file. By default all frames are read.

       pos_unit, vel_unit, frc_unit, time_unit and mass_unit
            The units used in the dlpoly history file. The default values
            correspond to the defaults used in DLPOLY.

       This routine will also test the consistency of the row attribute of the
       trajectory group. If some trajectory data is already present, it will be
       replaced by the new data. It is highly recommended to first initialize
       the HDF5 file with the ``to_hdf5`` method of the System class.
    """
    with log.section('DPH5'):
        if log.do_medium:
            log('Loading DLPOLY history file \'%s\' into \'trajectory\' of HDF5 file \'%s\'' % (
                fn_history, f.filename
            ))

        # Take care of the data group
        tgrp, existing_row = get_trajectory_group(f)

        # Open the history file for reading
        hist_reader = DLPolyHistoryReader(fn_history, sub, pos_unit, vel_unit,
                                          frc_unit, time_unit, mass_unit)

        # Take care of the datasets that should always be present
        natom = hist_reader.num_atoms
        ds_step, ds_time, ds_cell, ds_pos = get_trajectory_datasets(
            tgrp,
            ('step', (1,)),
            ('time', (1,)),
            ('cell', (3,3)),
            ('pos', (natom, 3)),
        )

        # Take care of optional data sets
        if hist_reader.keytrj > 0:
            ds_vel = get_trajectory_datasets(tgrp, ('vel', (natom, 3)))[0]
        if hist_reader.keytrj > 1:
            ds_frc = get_trajectory_datasets(tgrp, ('frc', (natom, 3)))[0]

        # Load data
        row = 0
        for frame in hist_reader:
            append_to_dataset(ds_step, frame["step"], row)
            append_to_dataset(ds_time, frame["time"], row)
            append_to_dataset(ds_cell, frame["cell"].T, row)
            append_to_dataset(ds_pos, frame["pos"], row)
            if hist_reader.keytrj > 0:
                append_to_dataset(ds_vel, frame["vel"], row)
            if hist_reader.keytrj > 1:
                append_to_dataset(ds_frc, frame["frc"], row)
            row += 1

        # Check number of rows
        check_trajectory_rows(tgrp, existing_row, row)