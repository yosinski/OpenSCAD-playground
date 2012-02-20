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

from pyopenscad import *
from sp_utils import *
from util import *



def heart_segment(base, rr, frac):
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




def heart_edge(rr, deg):
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
            rotate([0, 0, deg*ii/NN])(heart_segment(base, rr, float(ii)/NN)),
            rotate([0, 0, deg*(ii+1)/NN])(heart_segment(base, rr, float(ii+1)/NN)),
            #rotate([0, 0, rot])(heart_segment(base, rr, float(ii)/NN)),
            #rotate([0, 0, rot+rotd])(heart_segment(base, rr, float(ii+1)/NN)),
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



def heartInside():
    # create flat half
    rr = 10.
    thick = 1.
    top = translate([rr, thick/2, (1+sqrt(2))*rr])(rotate([90, 0, 0])(cylinder(r = rr, h = thick)))
    junk, box = split(translate([0, -thick/2, 0])(rotate([0, -45, 0])(cube([(1+sqrt(2))*rr, thick, (1+sqrt(2)/2)*rr]))),
                      [1, 0, 0], [0, 0, 0])
    half = union()(top, box)

    # subtract areas
    hole = cylinder(r = 3, h = thick*2)
    hole.add_param('$fn', 24)
    half = difference()(half,
                        translate([0, thick, 19])(rotate([90, 0, 0])(hole)))

    # wind
    rw = 4
    wid1 = .7
    wid2 = 1 - (1-wid1)/2
    outer = cylinder(r = rw, h = thick*2)
    outer.add_param('$fn', 24)
    inner = cylinder(r = rw * wid1, h = thick*3)
    inner.add_param('$fn', 24)
    ring = difference()(outer, translate([0, 0, -thick/2])(inner))

    temp, windTop = split(ring, [0, 1, 0], [0, 0, 0])
    windTop2, junk = split(temp, [1, -1, 0], [0, 0, 0])
    junk, windMid = split(temp, [sqrt(3), 1, 0], [0, 0, 0])
    windBot = translate([rw*wid2, -sqrt(3)*rw*wid2, 0])(rotate([0, 0, 180])(windMid))
    wind = union()(windTop, windTop2, windMid, windBot)
    wind = translate([10, thick, 19])(rotate([90, 90, 0])(wind))
    
    half = difference()(half, wind)

    layers = [half]
    NLayers = 13
    for ii in range(NLayers-1):
        splitLoc = (ii+1)*rr*3.5/NLayers
        if ii == 7: splitLoc = (ii+1.1)*rr*3.5/NLayers
        one, two = split(layers[ii], [0, 0, 1], [0, 0, splitLoc])
        layers[ii] = one
        layers.append(two)

    # Special layer joins/splits to ensure it doesn't fall apart
    #layers[6] = union()(layers[6], cylinder(r = 5, h = 20))
    
    six, five = split(layers[6], [-1, 0, -1], [15, 0, 10])
    layers[5] = union()(layers[5], five)
    layers[6] = six

    seven, six = split(layers[6], [1, 0, -1], [0, 0, 5])
    layers[7] = union()(layers[7], seven)
    layers[6] = six

    seven, six = split(layers[7], [1, 0, 0], [12.8, 0, 0])
    layers[7] = seven
    layers[6] = union()(layers[6], six)

    seven, six = split(layers[8], [1, 0, 0], [10, 0, 0])
    layers[8] = []
    layers[7] = union()(layers[7], seven)
    layers[6] = union()(layers[6], six)

    rots = [0.0 for ii in range(NLayers)]
    for ii in range(NLayers):
        if ii == 0:
            rots[ii] = ru(0, 180)
        else:
            rots[ii] = rots[ii-1] + ru(30, 140)
        layers[ii] = rotate([0, 0, rots[ii]])(layers[ii])
        #layers[ii] = translate([0, 0, ii*2])(layers[ii])

    # Rotations tweaks for seed 8
    layers[7] = rotate([0, 0, -30])(layers[7])
    layers[9] = rotate([0, 0, -30])(layers[9])
    
    for ii in range(NLayers):
        layers.append(rotate([0, 0, 180])(layers[ii]))

    #layers = [layers[ii] for ii in [1, 5, 6, 7, NLayers+1, int(NLayers+6), int(NLayers+7)]]
    #layers = [layers[ii] for ii in [5, 6, 7, 8, 9]]

    ret = union()(layers)
    return ret



def pendant():
    rr = 10.
    NN = 7
    shell = []
    # different slopes
    #shell.extend([rotate([0, 0, ii*360./NN])(heart_edge(rr, -180+360.*ii/NN)) for ii in range(NN)])
    # constant slope
    shell.extend([rotate([0, 0, ii*360./NN])(heart_edge(rr, 200)) for ii in range(NN)])
    shell.extend([rotate([0, 0, ii*360./NN])(heart_edge(rr, -100)) for ii in range(NN)])

    inside = heartInside()

    h1 = cylinder(r = 2, h = 40).add_param('$fn', 48)
    h2 = translate([0, 5, 38])(rotate([90, 0, 0])(cylinder(r = 1, h = 10))).add_param('$fn', 24)
    handle = translate([0, 0, 28.5])(h1 - h2)

    support = (cylinder(r = 1, h = 16).add_param('$fn', 48) +
               translate([0, 0, 22])(cylinder(r = 1, h = 4).add_param('$fn', 48)))

    tip = translate([0, 0, -1.4])(cylinder(r1=0, r2=1, h=1).add_param('$fn', 24))
    
    return union()(
        handle,
        shell,
        inside,
        support,
        tip,
        #translate([30, 0, 0])(cylinder(r = 5, h = 10)),
        )



def main():
    seed = ri(0, 1000)
    seed = 8
    print 'seed is', seed
    random.seed(seed)

    aa = pendant()
    
    file_out = os.path.join(os.getenv('HOME'), 'Desktop', 'out.scad')
    scad_render_to_file(aa, file_out)



if __name__ == '__main__':
    main()
