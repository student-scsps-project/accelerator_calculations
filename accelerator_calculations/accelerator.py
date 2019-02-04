import numpy as np
from ._unit_registry import pq
from .beam import *

class cell():
    def __init__(self, cell_length):
        self.__cell_length = cell_length

    def cell_length():
        return self.__cell_length

class accelerator():
    '''
    This class contains methods related to the accelerator itself, this
    will generally involve information about equipment, such as the
    RF frequency, rather than the beams which are accelerated.
    '''
    def __init__(self, beam, circumference, harmonic_number, max_dipole_field):
        '''
        beam = a beam object defined using the beam class
        circumference = average circumference of the accelerator
        harmonic number = number of buckets (filled or unfilled)
        '''
        self.__c = beam.c()
        self.__beam = beam
        self.__h = harmonic_number
        self.__circumference = circumference
        self.__max_B = max_dipole_field

    def revolution_period(self, total_energy=None):
        velocity = self.__beam.beta(total_energy) * self.__c
        time_period = self.__circumference / velocity
        return time_period

    def revolution_frequency(self, total_energy=None):
        '''
        if total_energy is specified this will be used instead of the
        total energy of the beam. This can be useful for investigating
        revolution frequencies for different energies.
        '''
        time_period = self.revolution_period(total_energy)
        return 1/time_period

    def rf_frequency(self, total_energy=None):
        revolution_frequency = self.revolution_frequency(total_energy)
        return self.__h * revolution_frequency

    def cavity_bandwidth(self, injection_energy, extraction_energy):
        injection_rev_freq = self.revolution_frequency(injection_energy)
        extraction_rev_freq = self.revolution_frequency(extraction_energy)
        return (extraction_rev_freq - injection_rev_freq) * self.__h

    def bending_radius(self, total_energy=None):
        momentum = self.__beam.momentum(total_energy)
        rho = momentum / self.__beam.charge() / self.__max_B
        return rho

    def update_harmonic_number(self, new_h):
        '''
        Function for overwriting the harmonic number of the accelerator.
        '''
        self.__h = new_h

    def magnetic_rigidity(self, total_energy=None):
        momentum = self.__beam.momentum(total_energy)
        charge = self.__beam.charge()
        return momentum / charge

    def circumference(self):
        return self.__circumference

    def accelerator_radius(self):
        return self.circumference() / (2*np.pi)

    def filling_factor(self, max_energy):
        rho = self.bending_radius(max_energy)
        R = self.accelerator_radius()
        return rho / R

    def num_dipoles_total(self, max_energy, dipole_length):
        rho = self.bending_radius(max_energy)
        bent_circumference = 2*np.pi * rho
        number_of_dipoles = bent_circumference / dipole_length
        return number_of_dipoles

    def num_dipoles_cell(self, max_energy, dipole_length, cell_length):
        number_of_dipoles = self.num_dipoles_total(max_energy, dipole_length)
        num_cells = self.circumference() / cell_length
        return number_of_dipoles / num_cells
