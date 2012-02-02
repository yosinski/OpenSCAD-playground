#! /usr/bin/python

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
        for ii in range(NN):
            rx = rn(35, 55)
            nodes.append(
                translate([0, 0, stemh * ru(.4, 1)])(scale(sc)(rotate(a = [rx, 0, ii * (360./NN)])(branch(nn - 1, sc, rx)))),
                )
        return union()(nodes)



def treeWithBase():
    return union()(
        cylinder(r = 6, h = .5),    # base
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
