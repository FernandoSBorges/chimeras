import neuron as nrn # NEURON simulator

class HHCellMinimalClass(Cell):
    """
    Célula do modelo minimal HH
    """
    def createSections(self):
        """Create the sections of the cell."""
        self.soma = nrn.h.Section(name='soma', cell=self)
        self.dend = nrn.h.Section(name='dend', cell=self)
    
    
    def defineGeometry(self):
        """Set the 3D geometry of the cell."""
        self.soma.L = 18.8 # Length of a section in microns.
        self.soma.diam = 18.8 # Diameter range variable of a section in microns.
        self.soma.Ra = 123.0 # Axial resistivity in ohm-cm.

        self.dend.L = 200.0
        self.dend.diam = 1.0
        self.dend.Ra = 100.0
        
    def defineBiophysics(self):
        """Assign the membrane properties across the cell."""
        
        # specified in "2.2.1 Sodium and potassium currents to generate action potentials"
        ## https://doi.org/10.1007/s00422-008-0263-8
        self.soma.insert('hh2'); # Hodgin-Huxley INa and IK self.soma.insert('hh'); 
        self.soma.ek = -100 # potassium reversal potential 
        self.soma.ena = 50 # sodium reversal potential 
        self.soma.vtraub_hh2 = -55 # Resting Vm, BJ was -55
        self.soma.gnabar_hh2 = 0.05 # McCormick=15 muS, thal was 0.09
        self.soma.gkbar_hh2 = 0.005 # spike duration of pyr cells
        
        # I_m
        # specified in "2.2.2 Slow potassium current for spike-frequency adaptation" of 
        ## https://doi.org/10.1007/s00422-008-0263-8
        self.soma.insert('im'); # M current Yamada et al. (1989)
        self.taumax_im = 1000
        self.soma.gkbar_im = 3e-5 # specific to LTS pyr cell
        
        # I_L calcium decay
        # specified in "2.2.3 Calcium currents to generate bursting" of 
        ## https://doi.org/10.1007/s00422-008-0263-8
        self.soma.insert('cad') # calcium decay (Destexhe et al. 1996a, b; see Huguenard and McCormick 1992)
        self.soma.depth_cad = 1 # McCormick= 0.1 um
        self.soma.taur_cad = 5 # McCormick=1 ms !!!
        self.soma.cainf_cad = 2.4e-4 # McCormick=0
        self.soma.kt_cad = 0 # no pump
        
        # I_L the low-threshold Ca^(2+)
        # specified in "2.2.3 Calcium currents to generate bursting" of 
        ## https://doi.org/10.1007/s00422-008-0263-8
        self.soma.insert('ical'); # IL current (Reuveni et al. model, Nernst)  
        self.soma.cai = 2.4e-4 
        self.soma.cao = 2 
        self.soma.eca = 120 
        self.soma.gcabar_ical = 2.2e-4
        
        # I_T
        # specified in "2.2.3 Calcium currents to generate bursting" of 
        ## https://doi.org/10.1007/s00422-008-0263-8
        self.soma.insert('it'); #// IT current (Destexhe et al. 1998;)
        self.soma.cai = 2.4e-4 
        self.soma.cao = 2 
        self.eca = 120 
        self.soma.gcabar_it = 0.0004 #// specific to LTS pyr cell
    
