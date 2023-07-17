import sys 
import os

v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

os.system(f'python3 plotRaster.py {v} {batch} {subbatch}')
os.system(f'python3 plotPhase.py {v} {batch} {subbatch}')
os.system(f'python3 plotHistBoxPlot.py {v} {batch} {subbatch}')
os.system(f'python3 plotGOP.py {v} {batch} {subbatch}')
os.system(f'python3 plotLOP.py {v} {batch} {subbatch}')
os.system(f'python3 plotMeanLOPWindow.py {v} {batch} {subbatch}')