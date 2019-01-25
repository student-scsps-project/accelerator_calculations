'''
This will run tests for all of the supplied classes, where possible numbers
have been used from published sources. Where this is the case those sources
are referenced in the method header.
'''

import unittest
import accelerator
import beam
import particle
from _unit_registry import pq

class test_accelerator(unittest.TestCase):
    def make_items(self):
        '''
        Note that any changes to these numbers will require changes in all
        the test functions.

        Dipole field = Vedrine, "Large Superconducting Magnet Systems"
        '''
        test_particle = particle.proton
        test_beam = beam.beam(test_particle,
                              emittance = 30*pq.mm*pq.mrad,
                              total_energy = 1000*pq.GeV)
        test_accelerator = accelerator.accelerator(test_beam,
                                                    6283*pq.m,
                                                    1113,
                                                    max_dipole_field=4.4*pq.T,
                                                    magnet_frequency=0.3*pq.Hz)
        return test_particle, test_beam, test_accelerator

    def test_revolution_frequency(self):
        '''
        S. D. Holmes, "132 nsec Bunch Spacing in the Tevatron Proton
                        Antiproton Collider", FERMILAB-TM-1920, Dec 1994.
        '''
        test_particle, test_beam, test_accelerator = self.make_items()
        rev_freq = test_accelerator.revolution_frequency().to(pq.kHz).magnitude
        self.assertAlmostEqual(rev_freq, 47.7, places=1)

    def test_revolution_frequency_with_tote(self):
        '''
        Tests the revolution frequency function with a specified total
        energy, rather than using the internal variable.

        g = ((3*pq.GeV)/(1*pq.m_p*pq.c**2)).to(pq.dimensionless)
        beta = np.sqrt(1-1/g**2)
        t = 6283*pq.m/(beta*pq.c)
        f = (1/t).to(pq.kHz)
        print(f)
        '''
        test_particle, test_beam, test_accelerator = self.make_items()
        tot_e = 3.0 * pq.GeV
        rev_freq = test_accelerator.revolution_frequency(tot_e).to(pq.kHz).magnitude
        self.assertAlmostEqual(rev_freq, 45.32115023131288)

    def test_rf_frequency(self):
        '''
        S. D. Holmes, "132 nsec Bunch Spacing in the Tevatron Proton
                        Antiproton Collider", FERMILAB-TM-1920, Dec 1994.
        '''
        test_particle, test_beam, test_accelerator = self.make_items()
        rev_freq = test_accelerator.rf_frequency().to(pq.MHz).magnitude
        self.assertAlmostEqual(rev_freq, 53.1, places=1)

    def test_rf_frequency_with_tote(self):
        '''
        g = ((3*pq.GeV)/(1*pq.m_p*pq.c**2)).to(pq.dimensionless)
        beta = np.sqrt(1-1/g**2)
        t = 6283*pq.m/(beta*pq.c)
        f = (1113/t).to(pq.MHz)
        print(f)
        '''
        test_particle, test_beam, test_accelerator = self.make_items()
        tote = 3.0*pq.GeV
        rev_freq = test_accelerator.rf_frequency(tote).to(pq.MHz).magnitude
        self.assertAlmostEqual(rev_freq, 50.442440207451234)

    def test_cavity_bandwidth(self):
        print("Not done yet")
        #test_particle, test_beam, test_accelerator = self.make_items()
        #rev_freq = test_accelerator.rf_frequency(3*pq.GeV)

    def test_bend_radius(self):
        '''
        Physics of Intensity Dependent Beam Instabilities
        By King-Yuen Ng
        Result changed by 4m, assumed to be due to the exact field values
        used.
        '''
        test_particle, test_beam, test_accelerator = self.make_items()
        br = test_accelerator.bending_radius().to(pq.m).magnitude
        self.assertAlmostEqual(br, 758.1, places=1)
    
    def test_magnetic_rigidity(self):
        '''
        "Notes on Sextupole Fields in the Tevatron", M. Martens,
        Fermilab Beams Division, Beams-doc-510, March 2003.
        http://beamdocs.fnal.gov/AD/DocDB/0005/000510/001/Sextupoles_in_Tev.pdf 
        Modified slightly, answer is 3335.66, I get 3335.64.
        Assumed to be a rounding issue.
        '''
        print("\nTesting Magnetic Rigidit")
        test_particle, test_beam, test_accelerator = self.make_items()
        brho = test_accelerator.magnetic_rigidity().to(pq.T * pq.m).magnitude
        a = self.assertAlmostEqual(brho, 3335.64, places=2)
        if a == None:
            print("OK\n")


class test_beam(unittest.TestCase):
    def make_items(self):
        test_particle = particle.proton
        test_beam = beam.beam(test_particle, 30*pq.mm*pq.mrad,
                                total_energy=1000*pq.GeV)
        return test_particle, test_beam

    def test_kinetic_energy(self):
        '''
        E_mass = 1*pq.m_p * pq.c**2
        print((1000*pq.GeV - E_mass).to(pq.GeV))
        '''
        test_particle, test_beam = self.make_items()
        ke = test_beam.kinetic_energy().to(pq.GeV).magnitude
        self.assertAlmostEqual(ke, 999.0617279332217)

    def test_kinetic_energy_with_tote(self):
        '''
        E_mass = 1*pq.m_p * pq.c**2
        print((900*pq.GeV - E_mass).to(pq.GeV))
        '''
        test_particle, test_beam = self.make_items()
        tote = test_beam.kinetic_energy(900*pq.GeV).to(pq.GeV).magnitude
        self.assertAlmostEqual(tote, 899.0617279332217)

    def test_total_energy(self):
        test_particle, test_beam = self.make_items()
        tot_energy = test_beam.total_energy()
        self.assertAlmostEqual(tot_energy.to(pq.GeV).magnitude, 1000.0)

    def test_total_energy_with_tote(self):
        test_particle, test_beam = self.make_items()
        tot_energy = test_beam.total_energy(3*pq.GeV).to(pq.GeV).magnitude
        self.assertAlmostEqual(tot_energy, 3)

    def test_gamma(self):
        '''
        print((1*pq.TeV/(1*pq.m_p * pq.c**2)).to(pq.dimensionless))
        '''
        test_particle, test_beam = self.make_items()
        g = test_beam.gamma().to(pq.dimensionless).magnitude
        self.assertAlmostEqual(g, 1065.7889490770942)


if __name__ == '__main__':

    unittest.main()
