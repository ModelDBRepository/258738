# $Id: params.py,v 1.21 2012/11/09 21:00:39 samn Exp $ 

from pyinit import *
from geom import *
# from network import *

# run params
# h.tstop = float(config.get('run', 'tstop')) #900e3 # 8e3 # 31e3 
# h.dt = float(config.get('run', 'dt')) #0.1
h.tstop = dconf['tstop']
h.dt = dconf['dt']
h.steps_per_ms = 1/h.dt
#h.cvode_local(1)
h.v_init = -65

# # network NMDA params
# olmSomaNMDA=1
# bassomaNMDA=1
# pyrBdendNMDA=1
# pyrAdend3NMDA=1

# def gSetNMDA(net):
#     net.olm.set_r("somaNMDA",olmSomaNMDA)
#     net.bas.set_r("somaNMDA",bassomaNMDA)
#     net.pyr.set_r("BdendNMDA",pyrBdendNMDA)
#     net.pyr.set_r("Adend3NMDA",pyrAdend3NMDA)

# gSetNMDA(net)
 
