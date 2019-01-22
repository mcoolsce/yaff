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

import numpy as np

from molmod import angstrom

from yaff import *


__all__ = [
    'get_system_water32', 'get_system_water', 'get_system_graphene8',
    'get_system_polyethylene4', 'get_system_quartz', 'get_system_glycine',
    'get_system_cyclopropene', 'get_system_caffeine', 'get_system_butanol',
    'get_system_2T', 'get_system_peroxide', 'get_system_mil53',
    'get_system_2atoms', 'get_2systems_2oxygens', 'get_system_formaldehyde',
    'get_system_amoniak', 'get_system_4113_01WaterWater', 'get_nacl_cubic',
    'get_system_fluidum_grid',
]


def get_system_water32():
    return System(
        numbers=np.array([8, 1, 1]*32),
        pos=np.array([ # Coordinates ripped from the CP2K test suite.
            [-4.583, 5.333, 1.560], [-3.777, 5.331, 0.943], [-5.081, 4.589,
            1.176], [-0.083, 4.218, 0.070], [-0.431, 3.397, 0.609], [0.377,
            3.756, -0.688], [-1.488, 2.692, 4.125], [-2.465, 2.433, 3.916],
            [-1.268, 2.145, 4.952], [-2.461, -2.548, -6.136], [-1.892, -2.241,
            -6.921], [-1.970, -3.321, -5.773], [4.032, 0.161, 2.183], [4.272,
            -0.052, 1.232], [4.044, -0.760, 2.641], [2.950, -3.497, -1.006],
            [2.599, -3.901, -0.129], [3.193, -4.283, -1.533], [-2.890, -4.797,
            -2.735], [-2.810, -5.706, -2.297], [-2.437, -4.128, -2.039],
            [-0.553, 0.922, -3.731], [-0.163, 1.552, -3.085], [-1.376, 0.544,
            -3.469], [4.179, 4.017, 4.278], [3.275, 3.832, 3.876], [4.658,
            4.492, 3.572], [5.739, 1.425, 3.944], [5.125, 2.066, 4.346], [5.173,
            1.181, 3.097], [0.988, -0.760, -5.445], [1.640, -1.372, -4.989],
            [0.546, -0.220, -4.762], [-0.748, 1.985, 1.249], [-0.001, 1.490,
            1.540], [-1.160, 2.255, 2.109], [4.127, -0.234, -3.149], [5.022,
            -0.436, -3.428], [3.540, -0.918, -3.601], [-2.473, 2.768, -1.395],
            [-1.533, 2.719, -1.214], [-2.702, 1.808, -1.479], [-0.124, -2.116,
            2.404], [0.612, -2.593, 2.010], [0.265, -1.498, 3.089], [0.728,
            2.823, -2.190], [0.646, 3.694, -2.685], [1.688, 2.705, -1.947],
            [4.256, -5.427, -2.644], [5.222, -5.046, -2.479], [4.174, -5.628,
            -3.593], [-3.178, -0.508, -4.227], [-2.762, -1.221, -4.818],
            [-3.603, 0.073, -4.956], [-1.449, 5.300, -4.805], [-1.397, 4.470,
            -5.317], [-2.102, 5.091, -4.067], [3.354, 2.192, -1.755], [3.407,
            1.433, -2.405], [3.971, 2.958, -2.196], [1.773, -4.018, 1.769],
            [1.121, -4.532, 1.201], [1.975, -4.529, 2.618], [1.526, 1.384,
            2.712], [2.317, 1.070, 2.251], [1.353, 0.657, 3.364], [2.711,
            -2.398, -4.253], [2.202, -3.257, -4.120], [3.305, -2.610, -5.099],
            [6.933, 0.093, -1.393], [6.160, -0.137, -0.795], [6.748, -0.394,
            -2.229], [-5.605, -2.549, 3.151], [-4.756, -2.503, 3.616], [-5.473,
            -3.187, 2.378], [0.821, -4.406, 6.516], [0.847, -3.675, 7.225],
            [-0.014, -4.240, 5.988], [1.577, 3.933, 3.762], [1.221, 2.975,
            3.640], [1.367, 4.126, 4.659], [-2.111, -3.741, -0.219], [-1.378,
            -4.425, -0.036], [-1.825, -2.775, 0.003], [0.926, -1.961, -2.063],
            [0.149, -1.821, -1.402], [1.725, -2.303, -1.536], [4.531, -1.030,
            -0.547], [4.290, -1.980, -0.581], [4.292, -0.597, -1.390], [-0.740,
            -1.262, -0.029], [-1.272, -0.422, -0.099], [-0.403, -1.349, 0.873],
            [3.655, 3.021, 0.988], [2.706, 3.053, 1.282], [3.542, 2.615, 0.020]
        ])*angstrom,
        ffatypes=['O', 'H', 'H']*32,
        bonds=np.array([[(i//3)*3,i] for i in range(96) if i%3!=0]),
        rvecs=np.array([[9.865, 0.0, 0.0], [0.0, 9.865, 0.0], [0.0, 0.0, 9.865]])*angstrom,
        charges=np.array([-0.834, 0.417, 0.417]*32)
    )


def get_system_water():
    return System(
        numbers=np.array([8, 1, 1]),
        pos=np.array([
            [-4.583, 5.333, 1.560],
            [-3.777, 5.331, 0.943],
            [-5.081, 4.589, 1.176],
        ])*angstrom,
        ffatypes=['O', 'H', 'H'],
        bonds=np.array([[0,1], [0, 2]]),
        rvecs=None,
        charges=np.array([-0.834, 0.417, 0.417])
    )


def get_system_graphene8():
   return System(
        numbers=np.array([6]*8),
        pos=np.array([
            [2.465, 0.001, 0.000], [4.923, 1.423, 0.000], [3.697, 2.134, 0.000],
            [6.152, 3.557, 0.000], [1.237, 2.135, 0.000], [3.693, 3.556, 0.000],
            [0.003, 0.002, 0.000], [2.464, 1.426, 0.000]
        ])*angstrom,
        ffatypes=['C']*8,
        bonds=np.array([
            [0, 1], [1, 2], [1, 3], [3, 6], [4, 0], [2, 6], [2, 4], [7, 0], [7,
            3], [5, 6], [5, 4], [5, 7]
        ]),
        rvecs=np.array([[4.922, 0.0, 0.0], [2.462, 4.262, 0.0]])*angstrom,
    )


def get_system_polyethylene4():
    return System(
        numbers=np.array([6]*4 + [1]*8),
        pos=np.array([
            [4.4665, -0.2419, 0.0939], [3.1498, 0.5401, 0.0859], [1.9114,
            -0.3549, 0.0216], [0.6320, 0.4677, 0.0288], [4.4927, -0.8901,
            0.9785], [4.4935, -0.9016, -0.7825], [3.1442, 1.2221, -0.7735],
            [3.1012, 1.1657, 0.9858], [1.9051, -1.0408, 0.8766], [1.9429,
            -0.9675, -0.8867], [0.5566, 1.0682, 0.9410], [0.5949, 1.1431,
            -0.8319],
        ])*angstrom,
        ffatypes=['C']*4 + ['H']*8,
        bonds=np.array([
            [3, 2], [10, 3], [11, 3], [1, 0], [2, 1], [4, 0], [5, 0], [6, 1],
            [7, 1], [8, 2], [9, 2], [3, 0],
        ]),
        rvecs=np.array([[5.075, 0.187, 0.055]])*angstrom,
    )


def get_system_quartz():
    return System(
        numbers=np.array([14]*3 + [8]*6),
        pos=np.array([
            [ 1.999357437, -1.154329699, -1.801733563],
            [ 0.000000000,  2.308659399,  1.801733563],
            [-1.999357437, -1.154329699,  0.000000000],
            [ 1.762048976,  0.299963042, -1.159593954],
            [-1.140800226,  1.375997798,  2.443872642],
            [-0.621248751, -1.675960841,  0.642139609],
            [ 0.621248751, -1.675960841, -2.443872642],
            [-1.762048976,  0.299963042, -0.642139609],
            [ 1.140800226,  1.375997798,  1.159593954],
        ])*angstrom,
        ffatypes=['Si']*3 + ['O']*6,
        bonds=np.array([
            [2, 8], [1, 8], [2, 7], [0, 7], [1, 6], [0, 6], [2, 5], [1, 5],
            [1, 4], [0, 4], [2, 3], [0, 3],
        ]),
        rvecs=np.array([[0.0, 0.0, 5.405222], [0.0, 4.913416, 0.0], [-4.255154, 2.456708, 0.0]])*angstrom,
        charges=np.array([1.8]*3 + [-0.9]*6),
    )


def get_system_glycine():
    return System(
        numbers=np.array([7, 6, 6, 8, 8, 1, 1, 1, 1, 1]),
        pos=np.array([
            [ 1.421031,  0.728490,  0.340852],
            [ 0.372356,  0.085434, -0.431299],
            [-0.863219, -0.325923,  0.373824],
            [-1.853953, -0.929623, -0.341462],
            [-0.982444, -0.142046,  1.563332],
            [ 0.995984,  1.527545,  0.820162],
            [ 1.657981,  0.097447,  1.111926],
            [ 0.044404,  0.759440, -1.244685],
            [ 0.776702, -0.817449, -0.926065],
            [-1.568843, -0.983316, -1.266586],
        ])*angstrom,
        ffatypes=['N', 'C', 'C', 'O', 'O', 'H', 'H', 'H', 'H', 'H'],
        bonds=np.array([[3, 9], [1, 8], [1, 7], [0, 6], [0, 5], [2, 4], [2, 3], [1, 2], [0, 1]]),
    )


def get_system_cyclopropene():
    # structure taken from pubchem
    return System(
        numbers=np.array([6, 6, 6, 1, 1, 1, 1]),
        pos=np.array([
           [-0.8487, -0.0002,  0.0000],
           [ 0.4242,  0.6507,  0.0000],
           [ 0.4245, -0.6505,  0.0000],
           [-1.4015, -0.0004,  0.9258],
           [-1.4015, -0.0004, -0.9258],
           [ 0.9653,  1.5624,  0.0000],
           [ 0.9661, -1.5620,  0.0000],
        ])*angstrom,
        ffatypes=['C', 'C', 'C', 'H', 'H', 'H', 'H'],
        bonds=[[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 5], [2, 6]],
    )


def get_system_caffeine():
    # structure taken from pubchem
    return System(
        numbers=np.array([8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1,
                          1, 1, 1, 1, 1, 1]),
        pos=np.array([
           [ 0.4700,  2.5688,  0.0006],
           [-3.1271, -0.4436, -0.0003],
           [-0.9686, -1.3125,  0.0000],
           [ 2.2182,  0.1412, -0.0003],
           [-1.3477,  1.0797, -0.0001],
           [ 1.4119, -1.9372,  0.0002],
           [ 0.8579,  0.2592, -0.0008],
           [ 0.3897, -1.0264, -0.0004],
           [ 0.0307,  1.4220, -0.0006],
           [-1.9061, -0.2495, -0.0004],
           [ 2.5032, -1.1998,  0.0003],
           [-1.4276, -2.6960,  0.0008],
           [ 3.1926,  1.2061,  0.0003],
           [-2.2969,  2.1881,  0.0007],
           [ 3.5163, -1.5787,  0.0008],
           [-1.0451, -3.1973, -0.8937],
           [-2.5186, -2.7596,  0.0011],
           [-1.0447, -3.1963,  0.8957],
           [ 4.1992,  0.7801,  0.0002],
           [ 3.0468,  1.8092, -0.8992],
           [ 3.0466,  1.8083,  0.9004],
           [-1.8087,  3.1651, -0.0003],
           [-2.9322,  2.1027,  0.8881],
           [-2.9346,  2.1021, -0.8849],
        ])*angstrom,
        ffatypes=['O', 'O', 'N', 'N', 'N', 'N', 'C', 'C', 'C', 'C', 'C', 'C',
                  'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        bonds=[[0, 8], [1, 9], [2, 7], [9, 2], [2, 11], [3, 6], [10, 3],
               [3, 12], [8, 4], [9, 4], [4, 13], [5, 7], [10, 5], [6, 7],
               [8, 6], [10, 14], [11, 15], [16, 11], [17, 11], [18, 12],
               [19, 12], [20, 12], [13, 21], [13, 22], [13, 23]],
    )


def get_system_butanol():
    # structure taken from pubchem
    return System(
        numbers=np.array([8, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1]),
        pos=np.array([
           [-1.8622,  0.0000, -0.1725],
           [-0.5458,  0.0001,  0.4145],
           [ 0.4329,  1.0636, -0.1254],
           [ 0.4327, -1.0637, -0.1253],
           [ 1.5424,  0.0000,  0.0087],
           [-0.6136,  0.0033,  1.5101],
           [ 0.5601,  1.9522,  0.4983],
           [ 0.2340,  1.3756, -1.1571],
           [ 0.2337, -1.3760, -1.1569],
           [ 0.5595, -1.9521,  0.4986],
           [ 2.2999, -0.0001, -0.7787],
           [ 2.0392, -0.0001,  0.9857],
           [-2.2842, -0.8098,  0.1615],
        ])*angstrom,
        ffatypes=['O', 'C', 'C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        bonds=[[0, 1], [0, 12], [1, 2], [1, 3], [1, 5], [2, 4], [2, 6], [2, 7],
               [3, 4], [8, 3], [9, 3], [10, 4], [11, 4]],
    )


def get_system_2T():
    return System(
        numbers=np.array([14, 14, 8, 1, 1, 1, 1, 1, 1]),
        pos=np.array([
            [-2.9835,  0.1405,  0.000],
            [ 2.9833,  0.1398,  0.000],
            [ 0.0000, -0.7979,  0.000],
            [-3.1350,  2.9359, -0.240],
            [-4.3117, -1.0502, -2.160],
            [-4.2010, -0.6480,  2.398],
            [ 3.5767,  1.5031, -2.380],
            [ 4.6018, -2.1344,  0.211],
            [ 3.4720,  1.8512,  2.171]
        ]),
        ffatypes=['Si', 'Si', 'O', 'H', 'H', 'H', 'H', 'H', 'H'],
        bonds=np.array([[1, 7], [0, 4], [0, 5], [0, 2], [1, 2], [0, 3], [1, 6], [8, 1]]),
    )


def get_system_peroxide():
    return System(
        numbers=np.array([8,8,1,1]),
        pos=np.array([
            [ 0.7247,  0.0000,  0.0000],
            [-0.7247,  0.0000,  0.0000],
            [ 0.8233, -0.7000, -0.6676],
            [-0.8233, -0.6175,  0.7446],
        ]),
        ffatypes=['O','O','H','H'],
        bonds=np.array([[0,1],[0,2],[1,3]]),
    )


def get_system_mil53():
    numbers =np. array([
        13, 13, 13, 13,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,
        8,  8,  8,  8,  8,  8,  8,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
        6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
        6,  6,  6,  6,  6,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
        1,  1,  1,  1,  1,  1,  1,  1
    ])
    pos = np.array([
        [  1.53474108e+01,   0.00000000e+00,   1.27502657e+01],
        [  1.53474108e+01,   6.26935542e+00,   1.27502657e+01],
        [  0.00000000e+00,   6.26934975e+00,   0.00000000e+00],
        [  0.00000000e+00,  -5.66917840e-06,   0.00000000e+00],
        [  1.75758552e+01,   1.00723537e+00,   1.55272730e+01],
        [  1.52642269e+01,   3.13467771e+00,   1.12299224e+01],
        [  1.54305947e+01,   9.40403313e+00,   1.42706052e+01],
        [  2.84633083e+01,   1.00723537e+00,   2.31723321e+01],
        [  1.31158975e+01,   1.00723537e+00,   1.50784650e+01],
        [  2.22844443e+00,   1.00723915e+00,   2.27235240e+01],
        [  1.31158975e+01,   5.26212005e+00,   1.50784650e+01],
        [  1.31189664e+01,   7.27658890e+00,   9.97325833e+00],
        [  2.23151334e+00,   7.27658512e+00,   2.32819929e+00],
        [  1.75758552e+01,   5.26212005e+00,   1.55272730e+01],
        [  1.75789260e+01,   7.27659079e+00,   1.04220664e+01],
        [  2.84663772e+01,   7.27658701e+00,   2.77700547e+00],
        [  2.22844632e+00,   5.26212383e+00,   2.27235221e+01],
        [  1.31189645e+01,   1.15314736e+01,   9.97325644e+00],
        [  2.23151334e+00,   1.15314698e+01,   2.32819740e+00],
        [  2.84663753e+01,   1.15314717e+01,   2.77700358e+00],
        [  1.75789260e+01,   1.15314755e+01,   1.04220645e+01],
        [  2.84633083e+01,   5.26212005e+00,   2.31723321e+01],
        [  8.31876341e-02,   9.40403880e+00,   2.39801881e+01],
        [  3.06116377e+01,   3.13467393e+00,   1.52034326e+00],
        [  2.40807008e+01,   5.37672439e+00,   2.00944180e+01],
        [  2.51390589e+01,   3.13467771e+00,   2.08364832e+01],
        [  2.40807008e+01,   8.92631037e-01,   2.00944180e+01],
        [  2.19615316e+01,   8.92631037e-01,   1.86051872e+01],
        [  2.09001046e+01,   3.13467771e+00,   1.78605727e+01],
        [  2.19615316e+01,   5.37672439e+00,   1.86051872e+01],
        [  1.85795757e+01,   3.13467771e+00,   1.62336394e+01],
        [  2.74595878e+01,   3.13467771e+00,   2.24659676e+01],
        [  1.21121770e+01,   3.13467771e+00,   1.57848295e+01],
        [  9.79164809e+00,   3.13467960e+00,   1.74143139e+01],
        [  8.73329185e+00,   5.37672628e+00,   1.81563791e+01],
        [  6.61412273e+00,   5.37672628e+00,   1.96456080e+01],
        [  5.55269379e+00,   3.13467960e+00,   2.03902244e+01],
        [  6.61412084e+00,   8.92632926e-01,   1.96456099e+01],
        [  8.73328996e+00,   8.92632926e-01,   1.81563810e+01],
        [  3.23216490e+00,   3.13468149e+00,   2.20171595e+01],
        [  1.21152459e+01,   9.40403124e+00,   9.26689004e+00],
        [  9.79471700e+00,   9.40403124e+00,   7.63995678e+00],
        [  8.73328807e+00,   1.16460779e+01,   6.89534232e+00],
        [  6.61411895e+00,   1.16460760e+01,   5.40611152e+00],
        [  5.55576271e+00,   9.40402935e+00,   4.66404630e+00],
        [  6.61412084e+00,   7.16198268e+00,   5.40611341e+00],
        [  8.73328996e+00,   7.16198457e+00,   6.89534421e+00],
        [  3.23523382e+00,   9.40402746e+00,   3.03456191e+00],
        [  1.85826446e+01,   9.40403124e+00,   9.71569999e+00],
        [  2.09031735e+01,   9.40403124e+00,   8.08621561e+00],
        [  2.19615316e+01,   7.16198457e+00,   7.34415039e+00],
        [  2.40806989e+01,   7.16198457e+00,   5.85491958e+00],
        [  2.51421259e+01,   9.40403124e+00,   5.11030513e+00],
        [  2.40806989e+01,   1.16460779e+01,   5.85491769e+00],
        [  2.19615297e+01,   1.16460779e+01,   7.34414850e+00],
        [  2.74626548e+01,   9.40402935e+00,   3.48337187e+00],
        [  2.48137898e+01,   5.60662658e+00,   5.33885238e+00],
        [  2.12276697e+01,   5.60726152e+00,   7.86103773e+00],
        [  2.48153545e+01,   6.93088807e+00,   2.06118590e+01],
        [  2.12284426e+01,   6.93208238e+00,   1.80891181e+01],
        [  1.56998447e+01,   3.62071527e+00,   9.60358821e+00],
        [  1.50705659e+01,   9.05934709e+00,   1.60588908e+01],
        [  1.14328620e+00,   9.18407279e+00,   2.22156204e+01],
        [  2.95704345e+01,   3.15017158e+00,   3.41095756e+00],
        [  9.46637898e+00,   5.60662658e+00,   7.41141330e+00],
        [  5.87946713e+00,   5.60781899e+00,   4.88867238e+00],
        [  5.88103371e+00,   6.93208427e+00,   2.01616790e+01],
        [  9.46715377e+00,   6.93144932e+00,   1.76394936e+01],
        [  5.77288279e+00,   1.34282786e+01,   4.81359545e+00],
        [  9.57467162e+00,   1.34282805e+01,   7.48764674e+00],
        [  9.82767383e+00,  -6.70711048e-01,   1.73861343e+01],
        [  5.77273539e+00,  -8.89569680e-01,   2.02379124e+01],
        [  2.11211818e+01,  -8.90301004e-01,   1.80136065e+01],
        [  2.49219369e+01,  -8.89571570e-01,   2.06869321e+01],
        [  2.08671478e+01,   1.32094219e+01,   8.11439520e+00],
        [  2.49210487e+01,   1.34290100e+01,   5.26333704e+00]
    ])
    ffatypes = [
        'AL',   'AL',   'AL',   'AL',   'O_CA', 'O_HY', 'O_HY', 'O_CA', 'O_CA', 'O_CA',
        'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA', 'O_CA',
        'O_CA', 'O_CA', 'O_HY', 'O_HY', 'C_PH', 'C_PC', 'C_PH', 'C_PH', 'C_PC', 'C_PH',
        'C_CA', 'C_CA', 'C_CA', 'C_PC', 'C_PH', 'C_PH', 'C_PC', 'C_PH', 'C_PH', 'C_CA',
        'C_CA', 'C_PC', 'C_PH', 'C_PH', 'C_PC', 'C_PH', 'C_PH', 'C_CA', 'C_CA', 'C_PC',
        'C_PH', 'C_PH', 'C_PC', 'C_PH', 'C_PH', 'C_CA', 'H_PH', 'H_PH', 'H_PH', 'H_PH',
        'H_HY', 'H_HY', 'H_HY', 'H_HY', 'H_PH', 'H_PH', 'H_PH', 'H_PH', 'H_PH', 'H_PH',
        'H_PH', 'H_PH', 'H_PH', 'H_PH', 'H_PH', 'H_PH'
    ]
    bonds = np.array([
        [ 0,  4], [ 0,  5], [ 0,  6], [ 0,  8], [ 0, 17], [ 0, 20], [ 1,  5], [ 1,  6],
        [ 1, 10], [ 1, 11], [ 1, 13], [ 1, 14], [ 2, 12], [ 2, 15], [ 2, 16], [ 2, 21],
        [ 2, 22], [ 2, 23], [ 3,  7], [ 3,  9], [ 3, 18], [ 3, 19], [ 3, 22], [ 3, 23],
        [ 4, 30], [ 5, 60], [ 6, 61], [ 7, 31], [ 8, 32], [ 9, 39], [10, 32], [11, 40],
        [12, 47], [13, 30], [14, 48], [15, 55], [16, 39], [17, 40], [18, 47], [19, 55],
        [20, 48], [21, 31], [22, 62], [23, 63], [24, 25], [24, 29], [24, 58], [25, 26],
        [25, 31], [26, 27], [26, 73], [27, 28], [27, 72], [28, 29], [28, 30], [29, 59],
        [32, 33], [33, 34], [33, 38], [34, 35], [34, 67], [35, 36], [35, 66], [36, 37],
        [36, 39], [37, 38], [37, 71], [38, 70], [40, 41], [41, 42], [41, 46], [42, 43],
        [42, 69], [43, 44], [43, 68], [44, 45], [44, 47], [45, 46], [45, 65], [46, 64],
        [48, 49], [49, 50], [49, 54], [50, 51], [50, 57], [51, 52], [51, 56], [52, 53],
        [52, 55], [53, 54], [53, 75], [54, 74]
    ])
    rvecs = np.array([
        [ 30.69482159,   0.        ,   0.        ],
        [  0.        ,  12.5383329 ,   0.        ],
        [  0.        ,   0.        ,  25.49996445]
    ])
    return System(numbers=numbers, pos=pos, ffatypes=ffatypes, bonds=bonds, rvecs=rvecs)


def get_system_2atoms():
    return System(
        numbers=np.array([6, 6]),
        pos=np.array([[0.000, 0.000, 0.000], [2.500, 0.000, 0.000]])*angstrom,
        ffatypes=['C','C'],
        bonds=np.array([[0, 1]]),
        rvecs=np.diag([200.0, 200.0, 200.0])*angstrom,
    )


def get_2systems_2oxygens():
    sys1= System(
        numbers=np.array([8, 8]),
        pos=np.array([
            [-0.01759211, 9.45053452, 25.07298388],
            [30.37068628, 3.14903370,  1.67501988]
        ]),
        ffatypes=['O', 'O'],
        rvecs=np.array([
            [30.371, -0.001, -0.016],
            [ 0.000, 12.601,  0.000],
            [-0.021,  0.000, 26.730],
        ]),
    )
    sys2= System(
        numbers=np.array([8, 8]),
        pos=np.array([
            [-0.01759242, 9.45053331, 25.07298331],
            [30.37068699, 3.14903366,  1.67501905]
        ]),
        ffatypes=['O', 'O'],
        rvecs=np.array([
            [30.371, -0.001, -0.016],
            [ 0.000, 12.601,  0.000],
            [-0.021,  0.000, 26.730],
        ]),
    )
    return sys1, sys2


def get_system_formaldehyde():
    return System(
        numbers=np.array([6,8,1,1]),
        pos=np.array([
            [0.0000000000,  0.0000000000,  -0.5265526741],
            [0.0000000000,  0.0000000000,   0.6555124750],
            [0.0000000000, -0.9325664988,  -1.1133424527],
            [0.0000000000,  0.9325664988,  -1.1133424527],
        ])*angstrom,
        ffatypes=['C','O','H','H'],
        bonds=np.array([[0,1],[0,2],[0,3]]),
    )


def get_system_amoniak():
    return System(
        numbers=np.array([7, 1, 1, 1]),
        pos=np.array([
            [ 6.14905839e-08, -3.78376023e-05, -2.05755522e-01],
            [-2.23993227e-05,  1.79042587e+00,  4.80028576e-01],
            [ 1.55059860e+00, -8.95061229e-01,  4.80130135e-01],
            [-1.55057663e+00, -8.95099775e-01,  4.80129946E-01],
        ]),
        ffatypes=['N', 'H', 'H', 'H'],
        bonds=np.array([[0,1], [0, 2], [0, 3]]),
        rvecs=None,
        charges=np.array([-0.819, 0.273, 0.273, 0.273])
    )


def get_system_4113_01WaterWater():
    numbers = np.array([8,1,1,8,1,1])
    pos = np.array([
       [-0.702196054, -0.056060256,  0.009942262],
       [-1.022193224,  0.846775782, -0.011488714],
       [ 0.257521062,  0.042121496,  0.005218999],
       [ 2.220871067,  0.026716792,  0.000620476],
       [ 2.597492682, -0.411663274,  0.766744858],
       [ 2.593135384, -0.449496183, -0.744782026],
    ])*angstrom
    bonds = np.array([[0,1],[0,2],[3,4],[3,5]])
    slater_widths = np.array([0.41319930026598994, 0.3627838006301428,
                              0.36506437561248933, 0.41325284559113074,
                              0.3630690392361035, 0.3630602780887136])
    slater_charges = np.array([-7.1864406538427446, -0.5757853693582672,
                               -0.5779228946118505, -7.189537747105163,
                               -0.575295591836335, -0.5752744321374641])
    slater_Z = np.array([6.340131543436602,1.0,1.0,6.34008454441325,1.0,1.0])
    charges = slater_Z + slater_charges
    ffatypes = ['at%03d'%i for i in range(len(numbers))]
    system = System(numbers, pos, bonds=bonds, ffatypes=ffatypes,
                    charges=charges, radii=slater_widths,
                    valence_charges=slater_charges)
    return system


def get_system_nacl_cubic():
    r0 = 2.82*angstrom
    return System(
        numbers=np.array([11, 11, 11, 11, 17, 17, 17, 17]),
        ffatypes=['Na', 'Na', 'Na', 'Na', 'Cl', 'Cl', 'Cl', 'Cl'],
        charges=np.array([1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0]),
        pos = np.array([
            [0, 0, 0], [1, 1, 0], [1, 0, 1.1], [0, 1, 1],
            [1.01, 0, 0], [0, 0.9, 0], [0, 0, 1], [1, 1, 1]
        ])*r0,
        rvecs=np.identity(3)*(2*r0),
        bonds=[],
    )


def get_system_fluidum_grid(natom, l0=3.0*angstrom, ffatypes=['X']):
    '''
    Return a system with natom particles placed on a cubic grid with spacing
    l0. Only natom sites are occupied and the atoms are randomly displaced
    '''
    numbers = np.array([1]*natom, dtype=int)
    ffatypes = ffatypes*natom
    N = int(np.ceil(np.power(natom,1.0/3.0)))
    rvecs = np.eye(3)*l0*N
    pos = np.zeros((N**3,3))
    pos[:,0] = np.repeat(np.repeat(np.arange(N),N),N)*l0
    pos[:,1] = np.repeat(np.tile(np.arange(N),N),N)*l0
    pos[:,2] = np.tile(np.tile(np.arange(N),N),N)*l0
    pos = pos[:natom]
    system = System(numbers, pos, rvecs=rvecs, bonds=[], ffatypes=ffatypes[:natom])
    system.pos += np.random.normal(0.0,0.01*l0,system.natom*3).reshape((-1,3))
    return system
