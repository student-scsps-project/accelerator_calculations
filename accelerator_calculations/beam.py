import numpy as np
from ._unit_registry import pq
from .particle import particle

class beam(particle):
    def __init__(self, particle:particle, total_energy):
        '''
        Constructor if a particle is specified.
        '''
        super().__init__(particle.mass(),
                         particle.charge(),
                         particle.c())

        self.__total_energy = total_energy

    def kinetic_energy(self, total_energy=None):
        tot_e = self.total_energy(total_energy)
        ke = tot_e - self.rest_mass_energy()
        return ke

    def total_energy(self, total_energy=None):
        if total_energy is None:
            return self.__total_energy
        else:
            return total_energy

    def gamma(self, total_energy=None):
        '''
        Returns relativistic gamma factor based on the value of the
        specified total energy and the beam particle. If the total
        energy is not specified then the beams own total energy is used.
        '''
        total_energy = self.total_energy(total_energy)
        return total_energy / self.rest_mass_energy()

    def beta(self, total_energy=None):
        '''
        Returns the relativistic velocity vactor beta = velocity / c. If the
        total energy is specifed this will be used, otherwise the beams
        total energy variable will be used.
        '''
        gamma = self.gamma(total_energy)
        beta = np.sqrt(1-1/gamma**2)
        return beta

    def momentum(self, total_energy=None):
        gamma = self.gamma(total_energy)
        beta = self.beta(total_energy)
        momentum = gamma * self.mass() * (beta*self.c())
        return momentum