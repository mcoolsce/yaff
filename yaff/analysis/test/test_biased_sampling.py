# -*- coding: utf-8 -*-
# YAFF is yet another force-field code.
# Copyright (C) 2011 Toon Verstraelen <Toon.Verstraelen@UGent.be>,
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
# --


from __future__ import division

import shutil, os
import pkg_resources
import h5py
import numpy as np

from yaff import *
from molmod.units import kjmol


def test_sum_hills_alanin():
    npoints = 10
    # Construct a regular 2D grid, spanning from -pi to +pi in both dimensions
    grid0 = np.linspace(-3.0,2.0,3)
    grid1 = np.linspace(2.0,3.0,3)
    grid = np.zeros((grid0.shape[0]*grid1.shape[0],2))
    grid[:,0] = np.repeat(grid0, grid1.shape[0])
    grid[:,1] = np.tile(grid1, grid0.shape[0])
    mtd = SumHills(grid)
    fn = pkg_resources.resource_filename(__name__, '../../data/test/mtd_alanine.h5')
    with h5py.File(fn,'r') as fh5:
        q0s = fh5['hills/q0'][:]
        Ks = fh5['hills/K'][:]
        sigmas = fh5['hills/sigma'][:]
    mtd.load_hdf5(fn)
    fes = mtd.compute_fes()
    for igrid in range(grid.shape[0]):
        f = 0.0
        for ihill in range(q0s.shape[0]):
            deltas = grid[igrid]-q0s[ihill]
            f -= Ks[ihill]*np.exp(-np.sum(deltas**2/2.0/sigmas**2))
        assert np.abs(f-fes[igrid])<1e-10*kjmol
#        print("%5d %12.6e"%(igrid,f/kjmol))
