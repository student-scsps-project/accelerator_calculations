import numpy as np
from ._unit_registry import pq

class particle():
    def __init__(self, mass, charge, c):
        '''
        mass         = particle rest mass
        charge       = particle charge
        c            = speed of light constant to use
        '''
        self.__c = c
        self.__mass = mass
        self.__charge = charge

    def rest_mass_energy(self):
        return (self.__mass * self.__c**2)

    def c(self):
        return self.__c

    def mass(self):
        return self.__mass

    def charge(self):
        return self.__charge

proton = particle(1*pq.m_p, 1*pq.e, pq.c)
electron = particle(1*pq.m_e, -1*pq.e, pq.c)
