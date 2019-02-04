import numpy as np
from ._unit_registry import pq
from scipy.special import jn_zeros

class cavity():
    '''
    Contains methods for calculating various cavity properties
    given a set of properties.
    '''

    def __init__(self, cavity_frequency):
        self.__frequency = cavity_frequency

    def frequency(self):
        return self.__frequency

    def radius_for_tm101(self):
        '''
        Computes the required radius of a cylindrical cavity to resonate with
        a TM010 mode, given a frequency.
        '''
        a_nml = (1*pq.c/(2*np.pi) * jn_zeros(0, 1)[-1] / self.frequency()).to(pq.m)
        return a_nml

    def bandwidth(self, Quality_factor):
        bw = self.frequency() / Quality_factor
        return bw


def resonant_frequency(a, d, n, m, l):
    '''
    Returns the resonant frequency
    Assumes that the waveguide is filled with vacuum.
    a = radius
    d = length
    n = bessel function of order n
    m = mth zero of nth order bessel function
    l = longitudinal integer number
    '''
    coef = 1*pq.c / (2*np.pi)
    p_nm = jn_zeros(n, m)[-1]
    f_nml = coef * np.sqrt( (p_nm/a)**2 + (l*np.pi/d)**2)
    return f_nml




if __name__ == '__main__':

    cavity_frequency = 10 * pq.MHz
    a_nml = (1*pq.c/(2*np.pi) * jn_zeros(0, 1)[-1] / cavity_frequency).to(pq.m)
    print("a_nml = {:.2f}".format(a_nml))

    print("TM011 mode has frequency {:.2f}".format(f_nml(a_nml, 50*pq.cm, 0, 1, 1).to(pq.MHz)))
