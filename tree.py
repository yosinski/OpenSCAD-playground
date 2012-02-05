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
        branchPos = [ru(.4, 1) for ii in range(NN)]
        maxBP = max(branchPos)
        #print 'maxBP is', maxBP
        branchPos = [branchPos[ii] / maxBP for ii in range(NN)]
        for ii in range(NN):
            rx = rn(35, 55)
            nodes.append(
                translate([0, 0, branchPos[ii] * stemh * .9])(scale(sc)(rotate(a = [rx, 0, ii * (360./NN)])(branch(nn - 1, sc, rx)))),
                )
        return union()(nodes)



def treeWithBase():
    base = cylinder(r = 6, h = .75)
    base.add_param('$fn', 40)
    trunk1 = cylinder(r1 = 3.5, r2 = 0, h = 2)
    trunk1.add_param('$fn', 5)
    trunk2 = cylinder(r1 = 2, r2 = 0, h = 4)
    trunk2.add_param('$fn', 5)
    return union()(
        base,
        trunk1,
        trunk2,
        branch(5),                  # tree
        )



def main():
    if len(sys.argv) > 1:
        # Hint: try 918 for a nice round tree
        seed = int(sys.argv[1])
    else:
        seed = ri(0, 1000)
    print 'tree seed is', seed
    random.seed(seed)

    tree = treeWithBase()
    
    scad_render_to_file(tree, 'tree.scad')



if __name__ == '__main__':
    main()
