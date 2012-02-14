from numpy import array, random, cross
from numpy.linalg import norm

from pyopenscad import *

'''
A few shorter definitions for convenience
'''

def rn(aa, bb):
    '''A Normal random variable generator that takes a range, like
    random.uniform, instead of mean and standard deviation.'''
    
    return random.normal((bb+aa)/2., (bb-aa)/4.)

ru = random.uniform

ri = random.randint



def split(shape, normal, offset):
    #one = shape
    #two = intersection()(shape, cube(50))

    sep = translate([0, -25, -25])(cube(50))
    normal = array(normal, dtype=float)
    normal /= norm(normal)
    vecA = cross(normal, [1.23, 2.34, 2.54])
    vecA /= norm(vecA)
    vecB = cross(normal, vecA)
    vecB /= norm(vecB)
    mm = [[normal[0], vecA[0], vecB[0], offset[0]],
          [normal[1], vecA[1], vecB[1], offset[1]],
          [normal[2], vecA[2], vecB[2], offset[2]],
          [0, 0, 0, 1]]
    sep = multmatrix(m = mm)(sep)
    return difference()(shape, sep), intersection()(shape, sep)
