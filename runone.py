# $Id: runone.py,v 1.2 2012/09/14 20:12:02 samn Exp $ 
#
# loads a single sim, h.run() to run it
#
if __name__ == "__main__":

    import sys
    import os
    import string

    from neuron import h, gui # *
    h("strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment")
    h.simname=simname = "mtlhpc"
    h.allfiles=allfiles = "geom.hoc pyinit.py geom.py network.py params.py run.py"
    h.simfiles=simfiles = "pyinit.py geom.py network.py params.py run.py"
    h("runnum=1")
    runnum = 1.0
    h.datestr=datestr = "2021feb17"
    h.output_file=output_file = "data/10dec13.14"
    h.uname=uname = "x86_64"
    h.osname=osname="linux"
    h("templates_loaded=0")
    templates_loaded=0
    h("xwindows=1.0")
    xwindows = 1.0

    h.xopen("nrnoc.hoc")
    h.xopen("init.hoc")

    from pyinit import *

    exec(open("./geom.py").read()) # execfile("geom.py")
    exec(open("./network.py").read()) # execfile("network.py")
    exec(open("./params.py").read()) # execfile("params.py") # from params import *
    exec(open("./run.py").read()) # execfile("run.py") # from run import *

    if dconf['recordNetStimInputs']:
        net.record_all_netStim_times()


    if dconf['dorun']:
        if dconf['restorestate']:
            runFromSavedState(dconf['statestr'], h.tstop, statedir = './data/stateFiles/')
        else: myrun()

    if dconf['savestate']: savestate(dconf['statestr'], statedir = './data/stateFiles/')

    if dconf['saveout']:
        print ('calculating...')
        net.setsnq()
        net.calc_lfp()
        net.getnqvolt(onlyInterneurons = dconf['getOnlyInterneuronsSomaVolt'])
        if dconf['recPyrInputSpikes']: # make sure spike timings of pyr drive has been recorded
            net.setnqin()
            savePyrDrivingSpikes = dconf['savePyrInputSpikes']
        else: savePyrDrivingSpikes = False
        if dconf['DoMakeSignal']:
            saveSignalSpikes = dconf['saveSignalSpikes']
        else: saveSignalSpikes = False
        print ('saving...')
        saveSimH5py(dconf['simstr'], datadir='./data/batch/', savevoltnq = dconf['saveSomaVolt'], savePyrDrivingSpikes = savePyrDrivingSpikes, saveSignalSpikes = saveSignalSpikes)

    # to obtain and save connectivity matrix
    if dconf['saveconn']:
        print ('getting connectivity NQS and saving it as H5Py group...')
        f = h5py.File('./data/batch/'+dconf['simstr']+'_connMatrix.h5py', 'a')
        saveNQS_h5pyGroup(f, net.nqcon, 'connMatrix')
        f.close()

    # to save spike timings of netStims
    if dconf['saveout'] and len(net.linputVec) >0 and dconf['saveNetStimInputs']: # if net.record_all_netStims_times() is called
        print ('saving netstim spike timings as numpy array...')
        linputVecArr = np.array([np.array(myvec) for myvec in net.linputVec])
        np.save('./data/batch/'+dconf['simstr']+'_netstimSpikeTimings.npy', linputVecArr)
