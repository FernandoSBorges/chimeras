from neuron import h # NEURON simulator

def loadCell():
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    soma = h.Section(name='soma')
    soma.nseg = 1 #
    soma.diam = 96 #
    soma.L = 96 #			// so that area is about 29000 um2
    soma.cm = 1 #
    soma.Ra = 100 #		// geometry 
    soma.insert('pas');
    soma.insert('hh2'); #		// Hodgin-Huxley INa and IK 
    soma.insert('im'); #		// M current 
    soma.insert('cad');  #		// calcium decay
    soma.insert('ical'); #// IL current (Reuveni et al. model, Nernst)
    soma.insert('it'); #// IT current 
    print ('Creating a generic HH cell from Pospischil2008 template')
    return soma

def loadCellCfg(template):
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    #h.load_file(f'cells/{template}_template')
    #h.xopen(f'cells/{template}_template')
    h.xopen(f'cells/{template}_template')
    add_synapses=False
    print ("Loading cell",template)
    cell = getattr(h, template)(1 if add_synapses else 0)    
    print (f'Creating a generic {template} cell from Pospischil2008 template')
    return cell

def loadDemoCell(template):
    h.load_file('cells/mosinit.hoc')
    h.load_file(f'../cells/{template}.hoc')
    add_synapses=False
    print ("Loading cell",template)
    cell = getattr(h, template)(1 if add_synapses else 0)    
    print (f'Creating a generic {template} cell from Pospischil2008 template')
    return cell

def loadCellNotebook(template):
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")
    h.xopen(f'../cells/{template}_template')
    add_synapses=False
    print ("Loading cell", template)
    cell = getattr(h, template)(1 if add_synapses else 0)    
    print (f'Creating a generic {template} cell from Pospischil2008 template')
    return cell
