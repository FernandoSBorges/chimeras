import os
from neuron import h # NEURON simulator

def loadCell():
    os.chdir("cells/PospischilEtAl2008/")
    os.system("nrnivmodl")
    os.chdir("x86_64")
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    soma = h.Section(name='soma')
    soma.nseg = 1 #
    soma.diam = 96 #
    soma.L = 96 #			// so that area is about 29000 um2
    soma.cm = 1 #
    soma.Ra = 100 #		// geometry 
    
    soma.insert('pas')
    soma.e_pas = -85
    soma.g_pas = 1e-5 #		// idem TC cell
    
    soma.insert('hh2') #		// Hodgin-Huxley INa and IK
    soma.ek = -100 #		// potassium reversal potential 
    soma.ena = 50 #			// sodium reversal potential 
    soma.vtraub_hh2 = -55 #	// Resting Vm, BJ was -55
    soma.gnabar_hh2 = 0.05 #	// McCormick=15 muS, thal was 0.09
    soma.gkbar_hh2 = 0.005 #	// spike duration of pyr cells

    soma.insert('im') #		// M current
    taumax_im = 1000
    soma.gkbar_im = 3e-5 #		// specific to LTS pyr cell


    soma.insert('cad')  #		// calcium decay
    soma.depth_cad = 1 #		// McCormick= 0.1 um
    soma.taur_cad = 5 #		// McCormick=1 ms !!!
    soma.cainf_cad = 2.4e-4 #	// McCormick=0
    soma.kt_cad = 0 #		// no pump

    soma.insert('ical') #// IL current (Reuveni et al. model, Nernst)
    soma.cai = 2.4e-4 
    soma.cao = 2 
    soma.gcabar_ical = 2.2e-4


    soma.insert('it') #// IT current 
    soma.cai = 2.4e-4 
    soma.cao = 2 
    #eca = 120 
    soma.gcabar_it = 0.0004 #// specific to LTS pyr cell
    print('Creating a generic HH cell from Pospischil2008 template')
    print(soma)
    return soma

def loadCellTemplate(template):
    # -- before to xopen template cell is necessary to compile the mod files
    # usage nrnivmodl
    os.chdir("cells/PospischilEtAl2008/")
    try:
        os.system("nrnivmodl")
    except:
        raise Exception("Erro ao compilar...")

    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    h.xopen(f'{template}_template')
    add_synapses=False
    print ("Loading cell", template)
    cell = getattr(h, template)(1 if add_synapses else 0)    
    print (f'Creating a generic {template} cell from Pospischil2008 template')
    os.chdir(".. ")
    os.chdir(".. ")
    return cell
