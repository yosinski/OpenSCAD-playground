#! /usr/bin/python

# Copyright 2012 by Jason Yosinski
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
from numpy import random

from pyopenscad import *
from sp_utils import *

from util import *



def cyl():
    ret = cylinder(10, 20)
    ret.add_param('$fn', 24)
    return ret



def box():
    return cube(10)



def thing():
    return minkowski()(
        box(),
        cyl(),
        )



def randboxes():
    nodes = []
    for ii in range(10):
        nodes.append(translate([random.uniform(-100, 100), random.uniform(-100, 100), 0])(box()))
    ret = union()(nodes)
    return ret



def branch(nn = 3, sc = .7, rx = 15):
    if nn <= 0:
        stemr = rn(.9, 1.1)
        stemh = rn(8, 12)
        leafr = rn(4, 6)
        leafh = rn(.8, 1.2)
        cylStem = cylinder(r = stemr, h = stemh)
        cylStem.add_param('$fn', ri(4, 8))
        cylLeaf = cylinder(r = leafr, h = leafh)
        cylLeaf.add_param('$fn', ri(4, 8))
        
        return union()(
            cylStem,
            translate([0, 0, stemh - leafh/2.])(cylLeaf),
            )
    else:
        NN = ri(3, 5)
        stemr = rn(.9, 1.1)
        stemh = rn(8, 12)
        sc = rn(.6, .8)
        nodes = []
        nodes.append(cylinder(r = stemr, h = stemh))
        for ii in range(NN):
            rx = rn(35, 55)
            nodes.append(
                translate([0, 0, stemh * ru(.4, 1)])(scale(sc)(rotate(a = [rx, 0, ii * (360./NN)])(branch(nn - 1, sc, rx)))),
                )
        return union()(nodes)



def assemble():
    return union()(
        #thing(),
        #randboxes(),
        cylinder(r = 6, h = .5),
        branch(5),
        )



def ht1():
    nodes = []
    NN = 24
    rr = 10
    for ii in [3, 9, 15, 21]:
        jj = ii - .5
        nodes.append(
            hull()(
            rotate(a = [jj * (360./NN), 0, 0])(translate([0, rr, 0])(cylinder(r = rr, h = .1))),
            rotate(a = [(jj+1) * (360./NN), 0, 0])(translate([0, rr, 0])(cylinder(r = rr, h = .1)))
            )
            )
    donut = rotate(a = [0, 90, 0])(union()(nodes))
    heart = union()(
        donut,
        translate([0, 0, -20-rr/sqrt(2)])(cylinder(r1 = 0, r2 = rr*(2+sqrt(2))/2, h = 20)),
        
        translate([30, 0, 0])(cylinder(r = 5, h = 10)),
        )
    return difference()(
        heart,
        translate([0, 25, -8])(rotate([90, 0, 0])(cylinder(r = 8, h = 50))),
        )



def ht2_segment(base, rr, frac):
    '''frac is between 0 and 1'''
    straightCir = 1 + sqrt(2)
    circleCir = 5*pi/4
    straightRatio = straightCir / (straightCir + circleCir)

    if frac < straightRatio:
        localFrac = frac / straightRatio
        #rotate([0, 0, ii*deg/NN])    (translate([sqrt(2)* ii   *rr/NN, 0, sqrt(2)* ii   *rr/NN])(base)),
        ret = base
        ret = rotate([0, 45, 0])(ret)
        ret = translate([rr*(1+sqrt(2)/2)*localFrac, 0, rr*(1+sqrt(2)/2)*localFrac])(ret)
    else:
        localFrac = (frac - straightRatio) / (1 - straightRatio)
        ret = base
        ret = translate([rr, 0, 0])(ret)
        ret = rotate([0, -localFrac*215+45, 0])(ret)
        ret = translate([rr, 0, (1+sqrt(2))*rr])(ret)
    
    return ret




def ht2_edge(rr, deg):
    deg = float(deg)
    nodes = []
    base = cylinder(r = 1, h = .01)
    NN = 24*2
    rot0 = 0
    rotd = 5
    rot = 0
    for ii in range(NN):
        rot1 = rot0 + random.uniform(-5, 10)
        nodes.append(
            hull()(
            #rotate([0, 0, 180*ii/NN])(ht2_segment(base, rr, float(ii)/NN)),
            #rotate([0, 0, 180*(ii+1)/NN])(ht2_segment(base, rr, float(ii+1)/NN)),
            rotate([0, 0, rot])(ht2_segment(base, rr, float(ii)/NN)),
            rotate([0, 0, rot+rotd])(ht2_segment(base, rr, float(ii+1)/NN)),
            )
            )
        rot += rotd
        rotd += random.uniform(-5, 5)
        rot0 = rot1
    return union()(nodes)
    return minkowski()(
        sphere(r=.5),
        union()(nodes),
        )



def ht2():
    rr = 10.
    NN = 10
    nodes = [rotate([0, 0, ii*360./NN])(ht2_edge(rr, -180+360.*ii/NN)) for ii in range(NN)]
    return union()(nodes, translate([30, 0, 0])(cylinder(r = 5, h = 10)))



def main():
    seed = ri(0, 1000)
    #seed = 918   # nice round
    #print 'seed is', seed
    random.seed(seed)
    aa = ht2()
    
    file_out = os.path.join(os.getenv('HOME'), 'Desktop', 'jason.scad')
    scad_render_to_file(aa, file_out)



if __name__ == '__main__':
    main()
