#! /usr/bin/python

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



def main():
    seed = ri(0, 1000)
    seed = 918   # nice round
    print 'seed is', seed
    random.seed(seed)
    aa = assemble()
    
    file_out = os.path.join(os.getenv('HOME'), 'Desktop', 'jason.scad')
    scad_render_to_file(aa, file_out)



if __name__ == '__main__':
    main()
