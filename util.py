from numpy import random

'''
A few shorter definitions for convenience
'''

def rn(aa, bb):
    '''A Normal random variable generator that takes a range, like
    random.uniform, instead of mean and standard deviation.'''
    
    return random.normal((bb+aa)/2., (bb-aa)/4.)

ru = random.uniform

ri = random.randint
