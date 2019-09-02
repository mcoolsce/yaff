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
'''lammpsio

    Reading/writing of LAMMPS output/input files
'''

import numpy as np
import os
from scipy.special import erf

from yaff.external.lammps_generator import apply_lammps_generators
from yaff.log import log
from yaff.pes import PairPotEI, ForcePartPair, Parameters, ForceField
from yaff.sampling.utils import cell_lower

from molmod.units import angstrom, amu, femtosecond, kcalmol, atm, pascal, \
    rad, deg

__all__ = ['write_lammps_system_data','write_lammps_table','get_lammps_ffatypes',
           'read_lammps_table', 'ff2lammps']


# LAMMPS can work with different unit styles, see
# https://lammps.sandia.gov/doc/units.html
lammps_units = {
    'real': {'mass':amu, 'distance':angstrom, 'time':femtosecond,
             'energy':kcalmol, 'velocity':angstrom/femtosecond,
             'pressure':atm},
    'electron': {'mass':amu, 'distance':1.0, 'time':femtosecond,
                 'energy':1.0, 'velocity':1.03275, 'pressure':pascal},
}


def write_lammps_system_data(system, ff=None, fn='lammps.data', triclinic=True):
    '''
        Write information about a Yaff system to a LAMMPS data file
        Following information is written: cell vectors, atom type ids
        and topology (as defined by the bonds)

        **Arguments**
            system
                Yaff system

            fn
                Filename to write the LAMMPS data to

            triclinic
                Boolean, specify whether a triclinic cell will be used during
                the simulation. If the cell is orthogonal, set it to False
                as LAMMPS should run slightly faster.
                Default: True
    '''
    if system.cell.nvec != 3:
        raise ValueError('The system must be 3D periodic for Lammps calculations.')
    if system.ffatypes is None:
        raise ValueError('Atom types need to be defined.')
    if system.bonds is None:
        raise ValueError('Bonds need to be defined')
    if system.charges is None:
        if log.do_warning:
            log.warn("System has no charges, writing zero charges to LAMMPS file")
        charges = np.zeros((system.natom,))
    else:
        charges = system.charges
    if ff is None:
        ffatypes, ffatype_ids = system.ffatypes, system.ffatype_ids
    else:
        ffatypes, ffatype_ids = get_lammps_ffatypes(ff)
    fdat = open(fn,'w')
    fdat.write("Generated by Yaff\n\n%20d atoms\n%20d bonds\n%20d angles \n%20d dihedrals\n%20d impropers\n\n" % (system.natom, system.nbond, 0, 0, 0))
    fdat.write("%20d atom types\n%20d bond types\n%20d angle types\n%20d dihedral types\n%20d improper types\n\n" % (np.amax(ffatype_ids) + 1, 1,0,0,0) )
    rvecs, R = cell_lower(system.cell.rvecs)
    pos = np.einsum('ij,kj', system.pos, R)
    fdat.write("%30.24f %30.24f xlo xhi\n%30.24f %30.24f ylo yhi\n%30.24f %30.24f zlo zhi\n" % (0.0,rvecs[0,0],0.0,rvecs[1,1],0.0,rvecs[2,2]) )
    if triclinic:
        fdat.write("%30.24f %30.24f %30.24f xy xz yz\n" % (rvecs[1,0],rvecs[2,0],rvecs[2,1]) )
    fdat.write("Atoms\n\n")
    for i in range(system.natom):
        fdat.write("%5d %3d %3d %30.24f %30.24f %30.24f %30.24f\n" % (i+1,1,ffatype_ids[i]+1, charges[i], pos[i,0], pos[i,1], pos[i,2]) )
    fdat.write("\nBonds\n\n")
    for i in range(system.nbond):
        fdat.write("%5d %3d %5d %5d\n" % (i+1,1,system.bonds[i,0]+1, system.bonds[i,1]+1))
    fdat.close()

def write_lammps_table(ff, fn='lammps.table', rmin=0.50*angstrom,
    nrows=2500, unit_style='electron'):
    '''
       Write tables containing noncovalent interactions for LAMMPS.
       For every pair of ffatypes, a separate table is generated.
       Because electrostatic interactions require a specific treatment, point-
       charge electrostatics are NOT included in the tables.

       When distributed charge distributions (e.g. Gaussian) are used, this
       complicates matters. LAMMPS will still only treat point-charge
       electrostatics using a dedicated method (e.g. Ewald or PPPM), so the
       table has to contain the difference between the distributed charges and
       the point charge electrostatic interactions. This also means that every
       ffatype need a unique charge distribution, i.e. all atoms of the same
       atom type need to have the same charge and Gaussian radius.

       All pair potentials contributing to the table need to have the same
       scalings for near-neighbor interactions; this is however independent
       of the generation of the table and is dealt with elsewhere

       **Arguments:**

       ff
            Yaff ForceField instance

       **Optional arguments:**

       fn
            Filename where tables will be stored

    '''
    # Find out if we are dealing with electrostatics from distributed charges
    corrections = []
    for part in ff.parts:
        if part.name=='pair_ei':
            if np.any(part.pair_pot.radii!=0.0):
                # Create a ForcePart with electrostatics from distributed
                # charges, completely in real space.
                pair_pot_dist = PairPotEI(part.pair_pot.charges, 0.0,
                     part.pair_pot.rcut, tr=part.pair_pot.get_truncation(),
                     dielectric=part.pair_pot.dielectric, radii=part.pair_pot.radii)
                fp_dist = ForcePartPair(ff.system,ff.nlist,part.scalings,pair_pot_dist)
                corrections.append( (fp_dist,1.0) )
                # Create a ForcePart with electrostatics from point
                # charges, completely in real space.
                pair_pot_point = PairPotEI(part.pair_pot.charges, 0.0,
                     part.pair_pot.rcut, tr=part.pair_pot.get_truncation(),
                     dielectric=part.pair_pot.dielectric)
                fp_point = ForcePartPair(ff.system,ff.nlist,part.scalings,pair_pot_point)
                corrections.append( (fp_point,-1.0) )
    # Find the largest cut-off
    rmax = 0.0
    for part in ff.parts:
        if part.name.startswith('pair_'):
            if part.name=='pair_ei' and len(corrections)==0: continue
            rmax = np.amax([rmax,part.pair_pot.rcut])
    # Get LAMMPS ffatypes
    ffatypes, ffatype_ids = get_lammps_ffatypes(ff)
    # Select atom pairs for each pair of atom types
    ffa_pairs = []
    for i in range(len(ffatypes)):
        index0 = np.where(ffatype_ids==i)[0][0]
        for j in range(i,len(ffatypes)):
            index1 = -1
            candidates = np.where(ffatype_ids==j)[0]
            for cand in candidates:
                if cand==index0 or cand in ff.system.neighs1[index0] or\
                    cand in ff.system.neighs2[index0] or cand in ff.system.neighs3[index0] or\
                    cand in ff.system.neighs4[index0]: continue
                else:
                    index1 = cand
                    break
            if index1==-1:
                log("ERROR constructing LAMMPS tables: there is no pair of atom types %s-%s which are not near neighbors"%(ffatypes[i],ffatypes[j]))
                log("Consider using a supercell to fix this problem")
                raise ValueError
            ffa_pairs.append([index0,index1])
    if log.do_medium:
        with log.section('LAMMPS'):
            log("Generating LAMMPS table with covalent interactions")
            log.hline()
            log("rmin = %s | rmax = %s" % (log.length(rmin),log.length(rmax)))
    # We only consider one neighbor interaction
    ff.compute()
    ff.nlist.nneigh = 1
    # Construct array of evenly spaced values
    distances = np.linspace(rmin, rmax, nrows)
    ftab = open(fn,'w')
    ftab.write("# LAMMPS tabulated potential generated by Yaff\n")
    ftab.write("# All quantities in atomic units\n")
    ftab.write("# The names of the tables refer to the ffatype_ids that have to be used in the Yaff system\n")
    ftab.write("#%4s %13s %21s %21s\n" % ("i","d","V","F"))
    # Loop over all atom pairs
    for index0, index1 in ffa_pairs:
        energies = []
        for d in distances:
            gposnn = np.zeros(ff.system.pos.shape, float)
            ff.nlist.neighs[0] = (index0, index1, d, 0.0, 0.0, d, 0, 0, 0)
            energy = 0.0
            for part in ff.parts:
                if not part.name.startswith('pair'): continue
                if part.name=='pair_ei': continue
                energy += part.compute(gpos=gposnn)
            for part, sign in corrections:
                gposcorr = np.zeros(ff.system.pos.shape, float)
                energy += sign*part.compute(gpos=gposcorr)
                gposnn[:] += sign*gposcorr
            row = [d, energy, gposnn[index0,2]]
            energies.append( row )
        energies = np.asarray(energies)
        ffai = ffatypes[ffatype_ids[index0]]
        ffaj = ffatypes[ffatype_ids[index1]]
        if np.all(energies[:,1]==0.0):
            log.warn("Noncovalent energies between atoms %d (%s) and %d (%s) are zero"\
                    % (index0,ffai,index1,ffaj))
        if np.all(energies[:,2]==0.0):
            log.warn("Noncovalent forces between atoms %d (%s) and %d (%s) are zero"\
                    % (index0,ffai,index1,ffaj))
        if ffai>ffaj:
            name = '%s---%s' % (str(ffai),str(ffaj))
        else:
            name = '%s---%s' % (str(ffaj),str(ffai))
        ftab.write("%s\nN %d R %13.8f %13.8f\n\n" % (name, nrows,
            rmin/lammps_units[unit_style]['distance'],
            rmax/lammps_units[unit_style]['distance']))
        for irow, row in enumerate(energies):
            ftab.write("%05d %+13.8f %+21.12f %+21.12f\n" % (irow+1,
                row[0]/lammps_units[unit_style]['distance'],
                row[1]/lammps_units[unit_style]['energy'],
                row[2]/lammps_units[unit_style]['energy']*lammps_units[unit_style]['distance']))
        if log.do_medium:
            log("%s done"%name)
#        if make_plots:
#            if not os.path.isdir(os.path.join(workdir,'lammps_table_plots')): os.mkdir(os.path.join(workdir,'lammps_table_plots'))
#            pt.clf()
#            #pt.subplot(2,1,1)
#            pt.plot(energies[:,0]/angstrom,energies[:,1]/kjmol)
#            pt.yscale('symlog',linthreshy=1.0)
#            #pt.gca().set_xticks(np.arange(1.5,9.0,1.5))
#            #pt.gca().set_yticks(np.arange(-50,75,12.5))
#            #pt.xlim([1.5,7.5])
#            #pt.ylim([-50.0,50.0])
#            pt.xlabel('d [$\AA$]')
#            pt.ylabel('E [kJ/mol]')
#            #pt.subplot(2,1,2)
#            #pt.plot(energies[:,0]/angstrom,energies[:,2])
#            pt.savefig(os.path.join(workdir,'lammps_table_plots','%s.png'%name))


def get_lammps_ffatypes(ff):
    '''
    Fine grain the atomtypes, so that each atomtype has a unique charge and
    Gaussian radius. This is only necessary when electrostatics from charge
    distributions are used, so otherwise the original atomtypes are returned.
    '''
    newffas = None
    for part in ff.parts:
        if part.name=='pair_ei':
            if np.any(part.pair_pot.radii!=0.0):
                newffas = [ff.system.get_ffatype(iatom) for iatom in range(ff.system.natom)]
                # Loop over all atomtypes
                for iffa, ffa in enumerate(ff.system.ffatypes):
                    # Find all different charge distributions, ie unique
                    # combinations of charge and Gaussian radius
                    ei_combs = []
                    for iatom in np.where(ff.system.ffatype_ids==iffa)[0]:
                        # Round of to 8 decimals, to avoid false detection of
                        # unique combinations due to numerical noise
                        comb = (np.around(part.pair_pot.charges[iatom],8),
                                np.around(part.pair_pot.radii[iatom],8))
                        if not comb in ei_combs: ei_combs.append(comb)
                        newffas[iatom] = "%s_%05d"%(newffas[iatom],ei_combs.index(comb))
                ffatypes = sorted(list(set(newffas)))
                ffatype_ids = np.zeros(ff.system.natom, int)
                for iatom in range(ff.system.natom):
                    ffatype_ids[iatom] = ffatypes.index(newffas[iatom])
                return ffatypes, ffatype_ids
    return ff.system.ffatypes, ff.system.ffatype_ids


def read_lammps_table(fn):
    tables = []
    with open(fn,'r') as f:
        while True:
            line = f.readline()
            if not line: break
            if line.startswith('#'): continue
            ffas = line[:-1]
            w = f.readline().split()
            N, rmin, rmax = int(w[1]), float(w[3]), float(w[4])
            data = np.zeros((N,3))
            f.readline()
            for i in range(N):
                data[i] = [float(w) for w in f.readline().split()[1:]]
            tables.append((ffas,[N,rmin,rmax],data))
    return tables


def ff2lammps(system, parameter_fns, dn, triclinic=True,
              rcut=12.0*angstrom, switch=4.0*angstrom, smooth_ei=False,
              tailcorrections=True, mode='md', unit_style='electron',
              tabulated=False):
    '''
    Convert a Yaff ForceField parameter file and accompanying System instance
    to LAMMPS input files. Not all potentials available in Yaff are
    transferable to LAMMPS.

    **Arguments:**
        system
            Yaff system instance

        parameter_fns
            A single filename or a list of filenames

        dn
            Directory where files will be saved. Existing files will be
            overwritten without warning.

    **Optional arguments:**

        triclinic
            Boolean, specify whether a triclinic cell will be used during
            the simulation. If the cell is orthogonal, set it to False
            as LAMMPS should run slightly faster.
            Default: True

        rcut
            The real space cutoff used by all pair potentials.

        switch
            The width of the Switch3 truncation. Set to 0 to turn off truncation.

        smooth_ei
            Flag for smooth truncations for the electrostatic interactions.
            Currently not available in LAMMPS, so has to be False

        tailcorrections
            Boolean: if true, apply a correction for the truncation of the
            pair potentials assuming the system is homogeneous in the
            region where the truncation modifies the pair potential

        mode
            One of ``md``, ``library``, or ``test``, indicating the input
            directives for LAMMPS
            ``md``: generic input file for MD simulations
            ``library``: generic input file for using LAMMPS as a library
            ``test``: provide excessive output in order to debug things

        unit_style
            One of ``real`` or ``electron``, see
            https://lammps.sandia.gov/doc/units.html for details

        tabulated
            Boolean; if True, the van der Waals interactions will be read from
            a lammps.table file, which can be generated with the
            ``write_lammps_table`` function.
    '''
    # Check some properties of the supplied system
    if system.cell.nvec != 3:
        raise ValueError('The system must be 3d periodic for Lammps calculations.')
    if system.ffatypes is None:
        raise ValueError('Atom types need to be defined.')
    if system.bonds is None:
        raise ValueError('Bonds need to be defined')
    if system.masses is None:
        if log.do_high:
            log("Setting standard masses")
        system.set_standard_masses()
    if not unit_style in lammps_units.keys():
        raise ValueError('Invalid unit style selected')
    if smooth_ei:
        raise ValueError('smooth_ei should be set to False. '
            'Note that using smooth_ei=True in YAFF introduces an artificial '
            'effect, that however should be very small when using proper settings.')
    # Select the LAMMPS units
    units = lammps_units[unit_style]
    # Apply the parameters of the force field to the system
    parameters = apply_lammps_generators(system, Parameters.from_file(parameter_fns))
    if system.charges is None: charges = np.zeros((system.natom,))
    else: charges = system.charges
    if system.radii is None: radii = np.zeros((system.natom,))
    else: radii = system.radii
    # Use atom types compatible with tables
    if tabulated:
        ff = ForceField.generate(system, parameter_fns)
        ffatypes, ffatype_ids = get_lammps_ffatypes(ff)
    else:
        ffatypes, ffatype_ids = system.ffatypes, system.ffatype_ids
    # The following dictionary maps prefixes appearing in the Yaff ForceField
    # file to corresponding LAMMPS potentials, including the type of potential
    # and the dimensions of the paramters.
    all_prefixes = {
        'MM3QUART': ('Bond','mm3',
            [units['energy']/units['distance']**2/0.5, units['distance']]),
        'BONDTABLE': ('Bond','table',[]),
        'BONDHARM': ('Bond','harmonic',
            [units['energy']/units['distance']**2/0.5, units['distance']]),
        'BONDMORSE': ('Bond','morse',
            [units['energy'], 1.0/units['distance'], units['distance']]),
        'MM3BENDA': ('Angle','mm3',
            [units['energy']/rad**2/0.5, deg]),
        'BENDAHARM': ('Angle','harmonic',
            [units['energy']/rad**2/0.5, deg]),
        'BENDCOS': ('Angle','cosine/periodic',
            [1,units['energy']*4.0,deg]),
        'BENDCHARM': ('Angle','cosine/squared',
            [units['energy']/0.5, deg]),
        'CROSS': ('Angle','cross',
            [units['energy']/units['distance']**2, units['energy']/units['distance']/rad,
             units['energy']/units['distance']/rad, units['distance'], units['distance'], deg]),
        'TORSION': ('Dihedral','fourier',
            [1,units['energy'],deg]),
        'OOPDIST': ('Improper','distharm',
            [units['energy']/units['distance']**2/0.5,units['distance']]),
        'SQOOPDIST': ('Improper','sqdistharm',
            [units['energy']/units['distance']**4/0.5,units['distance']**2]),
        'MM3': ('Pair','mm3'),
        'LJ': ('Pair','lj'),
        'FIXQ': ('Charge','coul')
    }
    # Find out which prefixes need to be treated and how
    present_prefixes = {'Bond':[],'Angle':[],'Dihedral':[],'Improper':[],'Pair':[],'Charge':[]}
    for prefix in parameters.keys():
        present_prefixes[all_prefixes[prefix][0]].append(prefix)
    assert len(present_prefixes['Pair']) <= 1, "There should be at most one van der Waals contribution!"
    assert len(present_prefixes['Charge']) == 1, "There should be one electrostatic contribution!"
    # Count how many different coefficients and terms are present for each
    # type of internal coordinate
    counters = {}
    for term in ['Bond','Angle','Dihedral','Improper']:
        ncoeffs, nterms = 0,0
        for prefix in present_prefixes[term]:
            ncoeffs += len(parameters[prefix][1])
            nterms += len(parameters[prefix][0])
        counters[term] = (ncoeffs,nterms)
    if tabulated and not np.all(system.radii==0.0):
        # Potential messy situation: if a table is used to specify vdW
        # interactions and Gaussian electrostatics is used, the correction
        # due to Gaussian electrostatics is included in the vdW table. This
        # poses a problem when different scaling rules for vdW and EI are used.
        # If this is the case, we correct for this by including the scaled
        # electrostatics as bonded terms. Note that this possibly messes up the
        # topology LAMMPS uses, as for instance 1-3 neighbors will become
        # pseudo-bonded.
        scales_lj = parameters[present_prefixes['Pair'][0]][1]
        scales_ei = parameters[present_prefixes['Charge'][0]][1]
        # Get unique combinations of charges and radii
        ei_terms, ei_data = [], []
        parameters['BONDTABLE'] = [[],[]]
        dists = []
        npoints_table, rmin, rmax = 1000,0.5*angstrom,5.5*angstrom
        # Add 1-2 electrostatics to the bond terms
        if scales_ei[1]!=scales_lj[1]:
            rescale = scales_ei[1] - scales_lj[1]
            for i,j in system.bonds:
                gamma = np.sqrt(system.radii[i]**2+system.radii[j]**2)
                comb = (rescale*system.charges[i]*system.charges[j],gamma)
                if not comb in ei_data:
                    parameters['BONDTABLE'][1].append( ("btab%03d"%len(ei_data)) )
                    ei_data.append(comb)
                ei_terms.append( [i,j, ei_data.index(comb)] )
                parameters['BONDTABLE'][0].append( (ei_data.index(comb), [i,j] ) )
                delta = system.pos[i]-system.pos[j]
                system.cell.mic(delta)
                dists.append(np.linalg.norm(delta))
        # Add 1-3 electrostatic interactions as bond terms
        if scales_ei[2]!=scales_lj[2]:
            rescale = scales_ei[2] - scales_lj[2]
            realangles = []
            for i,_,k in system.iter_angles():
                if [i,k] in realangles: continue
                realangles.append([i,k])
            for i,k in realangles:
                gamma = np.sqrt(system.radii[i]**2+system.radii[k]**2)
                comb = (rescale*system.charges[i]*system.charges[k],gamma)
                if not comb in ei_data:
                    parameters['BONDTABLE'][1].append( ("btab%03d"%len(ei_data)) )
                    ei_data.append(comb)
                ei_terms.append( [i,k, ei_data.index(comb)] )
                parameters['BONDTABLE'][0].append( (ei_data.index(comb), [i,k] ) )
                delta = system.pos[i]-system.pos[k]
                system.cell.mic(delta)
                dists.append(np.linalg.norm(delta))
            dists = np.asarray(dists)
        if np.amin(dists)<rmin: raise ValueError
        if np.amax(dists)>rmax: raise ValueError
        # Update general bond information
        ncoeffs,nterms = counters["Bond"]
        ncoeffs += len(ei_data)
        nterms += len(ei_terms)
        counters["Bond"] = (ncoeffs,nterms)
        present_prefixes['Bond'].append('BONDTABLE')
        # Write the tables
        fn_table = os.path.join(dn,'eibonded.table')
        with open(fn_table,'w') as f:
            f.write("#Table containing 1-3 electrostatic interactions\n")
            rval = np.linspace(rmin,rmax,npoints_table)
            for icomb, pars in enumerate(ei_data):
                qprod, gamma = pars
                f.write("btab%03d\nN %d\n\n"%(icomb,npoints_table))
                for ir, r in enumerate(rval):
                    y = r/gamma
                    e = qprod*erf(y)/r
                    g = -qprod*(2.0/np.sqrt(np.pi)*np.exp(-y**2)/r/gamma-erf(y)/r**2)
                    f.write("%5d %12.4f %20.12f %20.12f\n" % (ir+1,
                        r/lammps_units[unit_style]['distance'],
                        e/lammps_units[unit_style]['energy'],
                        g/lammps_units[unit_style]['energy']*lammps_units[unit_style]['distance']))
    # Check that there is a bond term for every bond
    if not counters['Bond'][1] >= system.nbond:
        raise ValueError("Please ensure that there is a bond term "
        "(possibly with force constant 0) for each bond in the system")
    # Write the headers to file
    with open(os.path.join(dn,'lammps.data'),'w') as fdat:
        fdat.write("Generated by Yaff\n\n%20d atoms\n%20d bonds\n%20d "
            "angles \n%20d dihedrals\n%20d impropers\n\n" %
            (system.natom, counters['Bond'][1], counters['Angle'][1],
             counters['Dihedral'][1], counters['Improper'][1]))
        fdat.write("%20d atom types\n%20d bond types\n%20d angle types\n "
            "%20d dihedral types\n%20d improper types\n\n" %
            (np.amax(ffatype_ids) + 1, counters['Bond'][0],
             counters['Angle'][0], counters['Dihedral'][0],
             counters['Improper'][0]) )
        # Write cell vectors (in LAMMPS format) to file
        rvecs, _ = cell_lower(system.cell.rvecs)
        fdat.write("%40.34f %40.34f xlo xhi\n%40.34f %40.34f ylo yhi\n"
            "%40.34f %40.34f zlo zhi\n" %
            (0.0,rvecs[0,0]/units['distance'],0.0,rvecs[1,1]/units['distance'],
             0.0,rvecs[2,2]/units['distance']) )
        if triclinic:
            fdat.write("%40.34f %40.34f %40.34f xy xz yz\n" %
            (rvecs[1,0]/units['distance'],
             rvecs[2,0]/units['distance'],
             rvecs[2,1]/units['distance']) )
        else:
            # Make sure that cell is not triclinic
            if not np.all( np.abs(rvecs.ravel()[[3,6,7]])<1e-10*units['distance'] ):
                raise ValueError("Cell is triclinic, but triclinic was set to False!")
        # Write atomic masses, add the atom type as comment (not read by LAMMPS)
        fdat.write("\nMasses\n\n")
        for iffa, ffa in enumerate(ffatypes):
            mask = ffatype_ids == iffa
            mass = system.masses[mask][0]
            assert np.all(mass==system.masses[mask])
            fdat.write("%5d %15.8f # %15s\n" % (iffa+1, mass/units['mass'], ffa))
        # Write coefficients of the covalent terms
        for term in ['Bond','Angle','Dihedral','Improper']:
            counter = 1
            if len(present_prefixes[term])==0: continue
            fdat.write("\n%s Coeffs\n\n" % term)
            for prefix in present_prefixes[term]:
                par_units = all_prefixes[prefix][2]
                for pars in parameters[prefix][1]:
                    fdat.write("%8d"%counter)
                    if len(present_prefixes[term])>1:
                        fdat.write("%20s" % (all_prefixes[prefix][1]))
                    if prefix == 'TORSION':
                        fdat.write("%5d %15.8f %5d %15.8f" %
                        (1,0.5*pars[1]/par_units[1],pars[0],
                        (pars[0]*pars[2]-np.pi)/par_units[2]))
                    elif prefix == 'BENDCHARM':
                        fdat.write("%15.8f %15.8f" %
                        (pars[0]/par_units[0],np.arccos(pars[1])/deg))
                    elif prefix == 'BENDCOS':
                        if pars[2]==0.0:
                            fdat.write("%15.8f %5d %5d" %
                            (pars[1]/par_units[1]*pars[0]**2,(-1.0)**(pars[0]),pars[0]))
                        elif pars[2]==np.pi:
                            fdat.write("%15.8f %5d %5d" %
                            (pars[1]/par_units[1]*pars[0]**2,(-1.0)**(pars[0]+1),pars[0]))
                        else: raise NotImplementedError
                    elif prefix == 'BONDTABLE':
                        fdat.write("%20s %15s" % ("eibonded.table",pars))
                    else:
                        for ipar, par in enumerate(pars):
                            fdat.write(" %15.8f" % (par/par_units[ipar]))
                    counter += 1
                    fdat.write("\n")
        # Write coefficients of the non-covalent terms
        if len(present_prefixes['Pair'])>0 and (not tabulated):
            paircoeff_prefix = present_prefixes['Pair'][0]
            mapping = parameters[paircoeff_prefix][0][0]
            fdat.write("\nPair Coeffs\n\n")
            for iffa, ffa in enumerate(ffatypes):
                mask = ffatype_ids == iffa
                radius = radii[mask][0]
                if not np.all(radius==system.radii[mask]):
                    raise ValueError("All atoms with the same ffatype should "
                                     "have the same radius")
                index = mapping[(ffa,)][0]
                tpars = parameters[paircoeff_prefix][0][1][index]
                # Check that onlypauli is turned off, not yet present in LAMMPS
                if paircoeff_prefix=='MM3': assert tpars[2]==0
                fdat.write("%5d %20.12f %20.12f %20.12f # %15s\n" %
                    (iffa+1,tpars[1]/units['energy'],
                    tpars[0]/units['distance'],
                    radius/units['distance'],ffa))
        else:
            if not tabulated:
                if not np.all(radii==0.0):
                    raise ValueError("When no vdW contribution is provided, "
                   " Gaussian charge distributions are not supported")
        # Write atom types, atomic charges and positions
        fdat.write("\nAtoms\n\n")
        for i in range(system.natom):
            # Coordinates need to be rotated, because LAMMPS uses a different cell
            pos = np.dot(rvecs.T, np.dot(system.cell.gvecs, system.pos[i]))
            fdat.write("%5d %3d %3d %40.34f %40.34f %40.34f %40.34f\n" %
            ( i+1,1,ffatype_ids[i]+1, charges[i],
              pos[0]/units['distance'],
              pos[1]/units['distance'],
              pos[2]/units['distance'])
            )
        # Write covalent terms
        for term in ['Bond','Angle','Dihedral','Improper']:
            counter = 1
            type_counter = 1
            if len(present_prefixes[term])==0: continue
            fdat.write("\n%ss\n\n" % term)
            for prefix in present_prefixes[term]:
                for coeff_type, indexes in parameters[prefix][0]:
                    fdat.write("%5d %5d" % (counter,coeff_type+type_counter))
                    for index in indexes: fdat.write(" %5d" % (index+1))
                    counter += 1
                    fdat.write("\n")
                type_counter += len(parameters[prefix][1])
    # Write a partial LAMMPS input file
    with open(os.path.join(dn,'lammps.in'),'w') as fin:
        fin.write("#"*30)
        fin.write("General settings")
        fin.write("#"*30+"\n")
        fin.write("units           %s\n"%(unit_style))
        fin.write("atom_style      full\n")
        fin.write("boundary        p p p\n")
        fin.write("dielectric      1\n\n")
        if len(present_prefixes['Pair'])>0:
            lj = present_prefixes['Pair'][0]
            scales_lj = parameters[lj][1]
            if tabulated:
                scales_lj[1] = scales_lj[2]
                scales_lj[2] = 1.0
        else: scales_lj = {1:0,2:0,3:0}
        ei = present_prefixes['Charge'][0]
        scales_ei = parameters[ei][1]
        if tabulated: scales_ei[1] = 0.0
        if 4 in scales_lj.keys(): assert scales_lj[4]==1.0
        if 4 in scales_ei.keys(): assert scales_ei[4]==1.0
        fin.write("#"*30)
        fin.write("Force field and system specification")
        fin.write("#"*30+"\n")
        fin.write("special_bonds   lj %f %f %f coul %f %f %f\n" % \
            (scales_lj[1],scales_lj[2],scales_lj[3],scales_ei[1],scales_ei[2],scales_ei[3]) )
        fin.write("#Note that when a table is used, it is possible that the\n"
                  "#topology might have been adapted to correctly include\n"
                  "#Gaussian electrostatics in LAMMPS. The scaling rules might\n"
                  "#need to be different from what is specified in the Yaff parameter file\n")
        if tabulated:
            fin.write("pair_style hybrid/overlay coul/long %13.8f table spline 5000\n"%(rcut/units['distance']))
            pass
        else:
            if len(present_prefixes['Pair'])>0:
                fin.write("%-15s %s/%s/%s/%s %13.8f"% ("pair_style",all_prefixes[lj][1],
                        "switch3","coulgauss",
                        "long", rcut/units['distance']))
                fin.write("%8.4f" % (switch/units['distance']))
                fin.write("\n")
            else:
                fin.write("pair_style      coul/long %13.8f\n" % (rcut/units['distance']) )
            fin.write("pair_modify     table 16 # Accuracy of the table used for real space electrostatics\n")
            fin.write("pair_modify     mix arithmetic\n")
            fin.write("pair_modify     tail %s\n" % ("yes" if tailcorrections else "no"))
        for term in ['Bond','Angle','Dihedral','Improper']:
            if len(present_prefixes[term])==0: continue
            fin.write("%-15s" % ("%s_style"%(term.lower())))
            if len(present_prefixes[term])>1: fin.write(" hybrid")
            for prefix in present_prefixes[term]:
                fin.write(" %s" % (all_prefixes[prefix][1]))
                if all_prefixes[prefix][1]=='table': fin.write(" spline %d"%npoints_table)
            fin.write("\n")
        fin.write("box tilt large\n")
        fin.write("\n%-15s %s       # Data file location\n" % ("read_data","lammps.data"))
        if len(present_prefixes['Pair'])==0:
            fin.write("pair_coeff * *\n")
        if tabulated:
            fin.write("pair_coeff * * coul/long\n")
            for iffa, ffai in enumerate(ffatypes):
                for jffa, ffaj in enumerate(ffatypes):
                    if jffa < iffa: continue
                    if ffai>ffaj:
                        name = '%s---%s' % (str(ffai),str(ffaj))
                    else:
                        name = '%s---%s' % (str(ffaj),str(ffai))
                    fin.write("pair_coeff %d %d table %s %s\n" % (iffa+1,jffa+1,'lammps.table',name))
        if mode=='library':
            fin.write("kspace_style    pppm 0.000001      # Ewald accuracy\n")
            fin.write('\nthermo_style  custom pe ebond eangle edihed eimp evdwl ecoul elong etail pxx pyy pzz pxy pxz pyz\n')
            fin.write('neigh_modify delay 0 every 1 check no\n')
            fin.write('variable eng equal pe\n')
            fin.write('compute virial all pressure NULL virial\n')
            fin.write('fix 1 all nve\n')
            fin.write('run 0\n')
        elif mode=='test':
            fin.write("kspace_style    pppm 0.000000001      # Ewald accuracy\n")
            fin.write('\ncompute Pmol all pressure NULL bond angle dihedral improper\n')
            fin.write('compute Ppair all pressure NULL pair kspace\n')
            fin.write('thermo_style  custom step emol evdwl ecoul elong etail c_Pmol[1] c_Pmol[2] c_Pmol[3] c_Pmol[4] c_Pmol[5] c_Pmol[6] c_Ppair[1] c_Ppair[2] c_Ppair[3] c_Ppair[4] c_Ppair[5] c_Ppair[6]\n')
            fin.write('neigh_modify delay 0 every 1 check no\n')
            fin.write('variable eng equal pe\n')
            fin.write('compute virial all pressure NULL virial\n')
            fin.write('fix 1 all nve\n')
            fin.write('run 0\n')
        elif mode=='md':
            fin.write("kspace_style    pppm 0.000001      # Ewald accuracy\n")
            fin.write("neighbor        2.0 multi\n")
            fin.write("neigh_modify    every 2 delay 4 check yes\n\n")
            fin.write("#"*30)
            fin.write("Output settings")
            fin.write("#"*30+"\n")
            fin.write("thermo 10       # Provide output every n steps\n")
            fin.write("thermo_style     custom step time etotal ke temp pe emol evdwl ecoul elong etail pxx pyy pzz pxy pxz pyz vol press\n")
            fin.write("#dump 1 all custom 10 positions.dat id type x y z\n")
            fin.write("#dump 2 all custom 10 velocities.dat id type vx vy vz\n\n")
            fin.write("#"*30)
            fin.write("Sampling options")
            fin.write("#"*30+"\n")
            fin.write("timestep 0.5 # in time units\n")
            fin.write("velocity all create 0.0 5 # initial temperature in Kelvin and random seed\n")
            fin.write("#fix 1 all npt temp 300.0 300.0 100.0 tri 1.0 1.0 1000.0 tchain 3 mtk yes nreset 1000 volconstraint no\n")
            fin.write("#fix_modify 1 energy yes # Add thermo/barostat contributions to energy\n")
            fin.write("run 0\n")
        else: raise NotImplementedError
