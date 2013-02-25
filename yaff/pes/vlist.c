// YAFF is yet another force-field code
// Copyright (C) 2011 - 2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>,
// Louis Vanduyfhuys <Louis.Vanduyfhuys@UGent.be>, Center for Molecular Modeling
// (CMM), Ghent University, Ghent, Belgium; all rights reserved unless otherwise
// stated.
//
// This file is part of YAFF.
//
// YAFF is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// YAFF is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>
//
//--


#include <math.h>
#include "vlist.h"

typedef double (*v_forward_type)(vlist_row_type*, iclist_row_type*);

double forward_harmonic(vlist_row_type* term, iclist_row_type* ictab) {
  double x;
  x = ictab[(*term).ic0].value - (*term).par1;
  return 0.5*((*term).par0)*x*x;
}

double forward_polyfour(vlist_row_type* term, iclist_row_type* ictab) {
  double q = ictab[(*term).ic0].value;
  return (*term).par0*q + (*term).par1*q*q + (*term).par2*q*q*q + (*term).par3*q*q*q*q;
}

double forward_fues(vlist_row_type* term, iclist_row_type* ictab) {
  double x;
  x = (*term).par1/ictab[(*term).ic0].value;
  return 0.5*(*term).par0*(*term).par1*(*term).par1*(1.0+x*(x-2.0));
}

double forward_cross(vlist_row_type* term, iclist_row_type* ictab) {
  return (*term).par0*( ictab[(*term).ic0].value - (*term).par1 )*( ictab[(*term).ic1].value - (*term).par2 );
}

double forward_cosine(vlist_row_type* term, iclist_row_type* ictab) {
  return 0.5*(*term).par1*(1-cos(
    (*term).par0*(ictab[(*term).ic0].value - (*term).par2)
  ));
}

double forward_chebychev1(vlist_row_type* term, iclist_row_type* ictab) {
  return 0.5*(*term).par0*(1-ictab[(*term).ic0].value);
}

double forward_chebychev2(vlist_row_type* term, iclist_row_type* ictab) {
  double c;
  c = ictab[(*term).ic0].value;
  return (*term).par0*(1-c*c);
}

v_forward_type v_forward_fns[7] = {
  forward_harmonic, forward_polyfour, forward_fues, forward_cross,
  forward_cosine, forward_chebychev1, forward_chebychev2
};

double vlist_forward(iclist_row_type* ictab, vlist_row_type* vtab, long nv) {
  long i;
  double energy;
  energy = 0.0;
  for (i=0; i<nv; i++) {
    vtab[i].energy = v_forward_fns[vtab[i].kind](vtab + i, ictab);
    energy += vtab[i].energy;
  }
  return energy;
}


typedef void (*v_back_type)(vlist_row_type*, iclist_row_type*);

void back_harmonic(vlist_row_type* term, iclist_row_type* ictab) {
  ictab[(*term).ic0].grad += ((*term).par0)*(ictab[(*term).ic0].value - (*term).par1);
}

void back_polyfour(vlist_row_type* term, iclist_row_type* ictab) {
  double q = ictab[(*term).ic0].value;
  ictab[(*term).ic0].grad += (*term).par0 + 2.0*(*term).par1*q + 3.0*(*term).par2*q*q + 4.0*(*term).par3*q*q*q;
}

void back_fues(vlist_row_type* term, iclist_row_type* ictab) {
  double x = (*term).par1/ictab[(*term).ic0].value;
  ictab[(*term).ic0].grad += (*term).par0*(*term).par1*(x*x-x*x*x);
}

void back_cross(vlist_row_type* term, iclist_row_type* ictab) {
  ictab[(*term).ic0].grad += (*term).par0*( ictab[(*term).ic1].value - (*term).par2 );
  ictab[(*term).ic1].grad += (*term).par0*( ictab[(*term).ic0].value - (*term).par1 );
}

void back_cosine(vlist_row_type* term, iclist_row_type* ictab) {
  ictab[(*term).ic0].grad += 0.5*(*term).par1*(*term).par0*sin(
    (*term).par0*(ictab[(*term).ic0].value - (*term).par2)
  );
}

void back_chebychev1(vlist_row_type* term, iclist_row_type* ictab) {
  ictab[(*term).ic0].grad += -0.5*(*term).par0;
}

void back_chebychev2(vlist_row_type* term, iclist_row_type* ictab) {
  ictab[(*term).ic0].grad += -2.0*(*term).par0*ictab[(*term).ic0].value;
}

v_back_type v_back_fns[7] = {
  back_harmonic, back_polyfour, back_fues, back_cross, back_cosine,
  back_chebychev1, back_chebychev2
};

void vlist_back(iclist_row_type* ictab, vlist_row_type* vtab, long nv) {
  long i;
  for (i=0; i<nv; i++) {
    v_back_fns[vtab[i].kind](vtab + i, ictab);
  }
}
