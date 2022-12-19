# $Id: batch.py,v 1.63 2013/02/15 19:15:41 samn Exp $ 

# execfile("runone.py") # loads sim

import sys
import os
import numpy
# from modindex import *
import multiprocessing
# from Queue import Queue
from conf import writeconf

# from IPython.core.debugger import Tracer
# debug_here = Tracer()


# if __name__ != "__main__":
#   from neuron import h
#   from network import net
#   execfile("run.py")
#   #from run import loadminrundat

liseed = [1234] # ,6912,9876,6789,3219,5936]
lwseed = [4321] # ,5012,9281,8130,6143,7131]

def appline (s,fn):
  fp = open(fn,"a")
  fp.write(s)
  fp.write("\n")
  fp.close()

batchf = "mybatch.sh"
def mycomm (s, fn=batchf):
  appline(s,fn)

def mylog(s,fn="OLMbatchLong_13aug5B.log"):
  appline(s,fn)

# runs batch modulating strength of NMDA synapses at OLM cells
# loops & calls ntebatchrun.py to run the sim/save data
def ntebatch(nlevels,startnum=0):
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                #net.olm.set_r("somaNMDA",r1)
                if y < startnum:
                    print ("skipping sim num ", y)
                    y += 1
                    continue
                s = "./mod/x86_64/special -python ntebatchrun.py"
                s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)
                print ("sim num = ", y, ", command = ", s)
                y += 1
                mylog(s)
                os.system(s)

# load info about batch run into an NQS. returns the NQS
def ntebatchnq(nlevels=5):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","OLMr")
    nq.strdec("simstr")
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                simstr = "11may20.05_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                simstr += "_OLMr_"+str(r1)
                nq.append(y,simstr,iseed,wseed,r1)
                y += 1
    return nq


# runs batch modulating strength of NMDA synapses at different cell types/locations
# loops & calls nmbatchrun.py to run the sim/save data
def nmbatch(nlevels,startnum=0):
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                #net.olm.set_r("somaNMDA",r1)
                for i2, r2 in enumerate(x):
                    #net.bas.set_r("somaNMDA",r2)
                    for i3, r3 in enumerate(x):
                        #net.pyr.set_r("BdendNMDA",r3)
                        for i4, r4 in enumerate(x):
                            if y < startnum:
                                print ("skipping sim num ", y)
                                y += 1
                                continue
                            s = "./mod/x86_64/special -python nmbatchrun.py"
                            s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)+" "+str(r2)+" "+str(r3)+" "+str(r4)
                            print ("sim num = ", y, ", command = ", s)
                            y += 1
                            mylog(s)
                            os.system(s)
                            #net.pyr.set_r("Adend3NMDA",r4)

# runs batch modulating level of Ih conductance at PYR,BAS cells together - maintaining OLM Ih conductance
# loops & calls ihbatchrun.py to run the sim/save data
def longihbatchPYRBAS (nlevels,startnum=0,qsz=25):
    procs = []
    q = Queue(qsz)
    x,y = numpy.linspace(0,2,nlevels), 0
    iseed, wseed = liseed[0], lwseed[0]

    def myworker (scomm,num):        
        os.system(scomm) #worker function, invoked in a process.

    for ih1 in x:
        for ih2 in x:
            if y < startnum:
                print ("skipping sim num ", y)
                y += 1
                continue
            s = "./mod/x86_64/special -python ihbatchrun.py"
            s += " "+str(iseed)+" "+str(wseed)+" "+str(ih1)+" "+str(ih2)+" "+str(1.0)+" 1.0"
            p = multiprocessing.Process(target=myworker,args=(s,2))
            procs.append(p)
            q.put(p,True) # put proc on q and wait for free slot
            print ("sim num = ", y, ", command = ", s)
            mylog(s)
            p.start() # maybe have to put this before placing on q
            y += 1

    for p in procs: p.join() # Wait for all worker processes to finish

# runs batch modulating level of Ih conductance at OLM cells - maintaining PYR,BAS Ih conductance
# loops & calls ihbatchrun.py to run the sim/save data
def longihbatchOLM (nlevels,startnum=0,qsz=11):
  procs = []
  q = Queue(qsz)
  x,y = numpy.linspace(0,2,nlevels), 0
  iseed, wseed = liseed[0], lwseed[0]

  def myworker (scomm,num):        
    os.system(scomm) #worker function, invoked in a process.

  for ih1 in x:
    if y < startnum:
      print ("skipping sim num ", y)
      y += 1
      continue
    s = "./mod/x86_64/special -python ihbatchrun.py"
    s += " "+str(iseed)+" "+str(wseed)+" "+str(1.0)+" "+str(1.0)+" "+str(ih1)+" 1.0"
    p = multiprocessing.Process(target=myworker,args=(s,2))
    procs.append(p)
    q.put(p,True) # put proc on q and wait for free slot
    print ("sim num = ", y, ", command = ", s)
    mylog(s)
    p.start() # maybe have to put this before placing on q
    y += 1

  for p in procs: p.join() # Wait for all worker processes to finish


#
def getihsimstr (iseed,wseed,ihpyr,ihbas,iholm):
  simstr = "12nov09.09_iseed_"+str(iseed)+"_wseed_"+str(wseed)
  simstr += "_ihpyr_"+str(ihpyr)+"_ihbas_"+str(ihbas)+"_iholm_"+str(iholm)
  return simstr

# return an NQS with concatenated vectors from longihbatcPYRBAS run
# only loads data <= savenums
def longihbatchPYRBASNQ (nlevels,savenums):
    x,y = numpy.linspace(0,2,nlevels), 0
    iseed, wseed = liseed[0], lwseed[0]
    nq = h.NQS("id","simstr","iseed","wseed","ihpyr","ihbas","iholm","vlfp")
    nq.strdec("simstr")
    nq.odec("lfp")
    for ih1 in x:
        for ih2 in x:
            simstr = getihsimstr(iseed,wseed,ih1,ih2,1.0)
            fbase = "./data/lfp/" + simstr + "_"
            vlfp = catlfp(fbase,savenums)
            nq.append(y,simstr,iseed,wseed,ih1,ih2,1.0,vlfp)
            y += 1
    return nq

# runs batch modulating level of Ih conductance at PYR,BAS cells together - maintaining OLM Ih conductance
# loops & calls ihbatchrun.py to run the sim/save data
def ihbatchPYRBAS (nlevels,startnum=0):
    x = numpy.linspace(0,2,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for r1 in x:
                for r2 in x:
                    if r1 == 1.0 and r2 == 1.0:
                        continue # already ran all at baseline
                    elif r1 != r2:
                        continue # only running where they're equal
                    else:
                        xl = [[r1, r2, 1.0]]
                    #elif r1 == r2:
                    #    continue # already ran same values of r1,r2
                    for xll in xl:
                        if y < startnum:
                            print ("skipping sim num ", y)
                            y += 1
                            continue
                        s = "./mod/x86_64/special -python ihbatchrun.py"
                        s += " "+str(iseed)+" "+str(wseed)+" "+str(xll[0])+" "+str(xll[1])+" "+str(xll[2])
                        print ("sim num = ", y, ", command = ", s)
                        y += 1
                        mylog(s)
                        os.system(s)
                        # mycomm(s)

# load info about batch run into an NQS. returns the NQS
def ihbatchPYRBASnq (nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","ihpyr","ihbas","iholm")
    nq.strdec("simstr")
    x = numpy.linspace(0,2,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for r1 in x:
                for r2 in x:
                    if r1 == 1.0 and r2 == 1.0:
                        continue # already ran all at baseline
                    else:
                        xl = [[r1, r2, 1.0]]
                    for xll in xl:
                        simstr = "12nov09.09_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                        simstr += "_ihpyr_"+str(xll[0])+"_ihbas_"+str(xll[1])+"_iholm_"+str(xll[2])
                        nq.append(y,simstr,iseed,wseed,xll[0],xll[1],xll[2])
                        y += 1
    return nq

# runs batch modulating level of ih conductance 
# loops & calls ihbatchrun.py to run the sim/save data
def ihbatch (nlevels,startnum=0):
  x = numpy.linspace(0,2,nlevels)
  y = 0
  for iseed in liseed:
    for wseed in lwseed:
      for r1 in x:
        if r1 == 1.0:
          xl = [[1.0, 1.0, 1.0]] # skip dups
        else:
          xl = [[r1, r1, r1], [r1, 1.0, 1.0], [1.0, r1, 1.0], [1.0, 1.0, r1] ]
        for xll in xl:
          if y < startnum:
            print ("skipping sim num ", y)
            y += 1
            continue
          s = "./mod/x86_64/special -python ihbatchrun.py"
          s += " "+str(iseed)+" "+str(wseed)+" "+str(xll[0])+" "+str(xll[1])+" "+str(xll[2])
          print ("sim num = ", y, ", command = ", s)
          y += 1
          mylog(s)
          os.system(s)

# load info about batch run into an NQS. returns the NQS
def ihbatchnq(nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","ihpyr","ihbas","iholm")
    nq.strdec("simstr")
    x = numpy.linspace(0,2,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for r1 in x:
                if r1 == 1.0:
                    xl = [[1.0, 1.0, 1.0]] # skip dups
                else:
                    xl = [[r1, r1, r1], [r1, 1.0, 1.0], [1.0, r1, 1.0], [1.0, 1.0, r1] ]
                for xll in xl:
                    simstr = "12nov09.09_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                    simstr += "_ihpyr_"+str(xll[0])+"_ihbas_"+str(xll[1])+"_iholm_"+str(xll[2])
                    nq.append(y,simstr,iseed,wseed,xll[0],xll[1],xll[2])
                    y += 1
    return nq

# load info about batch run into an NQS. returns the NQS (batch from 13aug1)
def newihbatchnq (nlevels):
  nq = h.NQS("id","simstr","iseed","wseed","ihpyr","ihbas","iholm")
  nq.strdec("simstr")
  x = numpy.linspace(0,2,nlevels)
  y = 0
  liseed = [1234]; lwseed = [4321];
  for iseed in liseed:
    for wseed in lwseed:
      for r1 in x:
        if r1 == 1.0:
          xl = [[1.0, 1.0, 1.0]] # skip dups
        else:
          xl = [[r1, r1, r1], [r1, 1.0, 1.0], [1.0, r1, 1.0], [1.0, 1.0, r1] ]
        for xll in xl:
          simstr = "13aug1_iseed_"+str(iseed)+"_wseed_"+str(wseed)
          simstr += "_ihpyr_"+str(xll[0])+"_ihbas_"+str(xll[1])+"_iholm_"+str(xll[2])
          nq.append(y,simstr,iseed,wseed,xll[0],xll[1],xll[2])
          y += 1
      for r1 in x:
        for r2 in x:
          if r1 == 1.0 and r2 == 1.0:
            continue # already ran all at baseline
          elif r1 != r2:
            continue
          else:
            xl = [[r1, r2, 1.0]]
            for xll in xl:
              simstr = "13aug1_iseed_"+str(iseed)+"_wseed_"+str(wseed)
              simstr += "_ihpyr_"+str(xll[0])+"_ihbas_"+str(xll[1])+"_iholm_"+str(xll[2])
              nq.append(y,simstr,iseed,wseed,xll[0],xll[1],xll[2])
              y += 1
  return nq



# load info about batch run into an NQS. returns the NQS
def nmbatchnq(nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","OLMr","BASr","PYRBr","PYRAr")
    nq.strdec("simstr")
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                for i2, r2 in enumerate(x):
                    for i3, r3 in enumerate(x):
                        for i4, r4 in enumerate(x):
                            simstr = "11jun22.02_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                            simstr += "_OLMr_"+str(r1)+"_BASr_"+str(r2)+"_PYRBr_"+str(r3)+"_PYRAr_"+str(r4)
                            nq.append(y,simstr,iseed,wseed,r1,r2,r3,r4)
                            y += 1
    return nq

def testit ():
#    global h,net,loadminrundat
#    from neuron import h
#    from network import net
#    from run import loadminrundat
    print (h,net,loadminrundat)

# get cross-frequency coupling arrays  - vlfp is a vector
def getcfc (vlfp):
  v1 = h.Vector()
  v1.copy(vlfp) # (vlfp,nsamp,vlfp.size()-1-nsamp)
  v1.sub(v1.mean())
  sampr = 1e3 / h.dt
  from_t = 1
  to_t = int( vlfp.size() / sampr - 1 )
  phaseFreq,ampFreq,modArr = varModIndArr(v1, sampr, from_t, to_t, 4, 12, 25, 55, 1 , 1, 1)
  return phaseFreq, ampFreq, modArr

# run CFC analysis on LFPs in nqb - save output to text files
def addCFCcol (nqb,datadir="./data/"):
    global h
    nqb.tog("DB")
    if nqb.fi("fcfc") == -1:
        nqb.resize("fcfc")
        nqb.strdec("fcfc")
        nqb.pad()
    for i in range(int(nqb.v[0].size())):
        print ("up to " + str(i) + " out of " + str(nqb.v[0].size()))
        simstr = nqb.get("simstr",i).s
        fcfc = "./data/cfc/" + simstr + "_cfc.txt"
        if os.path.exists(fcfc):
            print ("skipping ", fcfc, " already done.")
            nqb.set("fcfc",i,fcfc)
            continue
        loadminrundat(simstr,datadir)
        phaseFreq, ampFreq, modArr = getcfc(net.vlfp)
        if i == 0:
            numpy.savetxt("./data/cfc/phaseFreq.txt",phaseFreq)
            numpy.savetxt("./data/cfc/ampFreq.txt",ampFreq)
        numpy.savetxt(fcfc,modArr)
        nqb.set("fcfc",i,fcfc)

# add a column to nqb with power spectra from h.matpmtm.
# skipms is milliseconds of signal to skip from beginning and end of LFP
# ty determines method to use for calculating power spectrum
def addnqpcol(nqb,skipms=200,ty=0,datadir="./data/"):
    global h
    nqb.tog("DB")
    if nqb.fi("nqp") == -1:
        nqb.resize("nqp")
        nqb.odec("nqp")
        nqb.pad()
    hasvlfp = False
    if nqb.fi("vlfp") != -1: hasvlfp = True
    v1=h.Vector()
    nsamp = skipms / h.dt # number of samples to skip from start,end
    for i in range(int(nqb.v[0].size())):
        print ("up to " + str(i) + " out of " + str(nqb.v[0].size()))
        if hasvlfp:
            v1.copy(nqb.get("vlfp",i).o[0])
        else:
            loadminrundat(nqb.get("simstr",i).s,datadir)
            v1.copy(net.vlfp,nsamp,net.vlfp.size()-1-nsamp)
        v1.sub(v1.mean())
        if ty==0:
            nqp=h.matpmtm(v1,1e3/h.dt)
        elif ty==1:
            nqp=h.pypmtm(v1,1e3/h.dt)
        elif ty==2:
            nqp=h.pypsd(v1,1e3/h.dt)
        else:
            nqp=h.nrnpsd(v1,1e3/h.dt)
        nqb.set("nqp",i,nqp)
        h.nqsdel(nqp)

# add columns to nqb with synchrony of each population (uses cvpsync in stats.hoc)
# skipms is milliseconds of signal to skip from beginning and end of sim
def addCVpcol (nqb,skipms=200,simdur=8e3,datadir="./data/"):
    nqb.tog("DB")
    if nqb.fi("pyrCVp") == -1:
        for s in ["pyrCVp","basCVp","olmCVp","pyrbasCVp","pyrolmCVp","basolmCVp","allCVp"]: nqb.resize(s)
        nqb.pad()
    cdx = int(nqb.fi("pyrCVp")) # column index
    for i in range(int(nqb.v[0].size())):
        print ("up to " + str(i) + " out of " + str(nqb.v[0].size()))
        loadminrundat(nqb.get("simstr",i).s,datadir)
        net.snq.verbose=0
        idx = cdx
        for ty in range(7):
            cvp = 0
            if ty <= 2: # PYR then BAS then OLM
                if net.snq.select("ty",ty,"t","[]",skipms,simdur-skipms) > 0:
                    cvp = h.cvpsync(net.snq.getcol("t"),net.cells[ty].n)
            elif ty == 3: # PYR + BAS
                if net.snq.select("ty","!=",2,"t","[]",skipms,simdur-skipms) > 0:
                    cvp = h.cvpsync(net.snq.getcol("t"),net.cells[0].n+net.cells[1].n)
            elif ty == 4: # PYR + OLM
                if net.snq.select("ty","!=",1,"t","[]",skipms,simdur-skipms) > 0:
                    cvp = h.cvpsync(net.snq.getcol("t"),net.cells[0].n+net.cells[2].n)
            elif ty == 5: # BAS + OLM
                if net.snq.select("ty","!=",0,"t","[]",skipms,simdur-skipms) > 0:
                    cvp = h.cvpsync(net.snq.getcol("t"),net.cells[1].n+net.cells[2].n)
            elif ty == 6: # ALL
                if net.snq.select("t","[]",skipms,simdur-skipms) > 0:
                    cvp = h.cvpsync(net.snq.getcol("t"),net.cells[0].n+net.cells[1].n+net.cells[2].n)
            nqb.v[idx].x[i] = cvp
            idx += 1        
        net.snq.verbose=1

# add columns to nqb with frequency of each population
# skipms is milliseconds of signal to skip from beginning and end of sim
def addHzcol (nqb,skipms=200,simdur=8e3,datadir="./data/"):
    nqb.tog("DB")
    if nqb.fi("pyrHz") == -1:
        for s in ["pyrHz", "basHz", "olmHz"]: nqb.resize(s)
        nqb.pad()
    cdx = int(nqb.fi("pyrHz")) # column index
    for i in range(int(nqb.v[0].size())):
        print ("up to " + str(i) + " out of " + str(nqb.v[0].size()))
        loadminrundat(nqb.get("simstr",i).s,datadir)
        net.snq.verbose=0
        idx = cdx
        for ty in range(3):
            nspks = net.snq.select("ty",ty,"t","[]",skipms,simdur-skipms)
            hz = 1e3 * nspks / ( (simdur-2*skipms) * net.cells[ty].n ) # to hz
            nqb.v[idx].x[i] = hz
            idx += 1        
        net.snq.verbose=1

# runs a batch of sims of form baseline/washin/washout . during washin, OLM NMDA is turned off.
# at washout, it's turned back on.
def washbatch(nlevels,startnum=0):
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for r1 in x:
                if y < startnum:
                    print ("skipping sim num ", y)
                    y += 1
                    continue
                s = "./mod/x86_64/special -python washbatchrun.py"
                s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)
                print ("sim num = ", y, ", command = ", s)
                y += 1
                mylog(s,"washbatch_10dec13.14.log")
                os.system(s)

# load info about washbatch run into an NQS. returns the NQS
def washbatchnq(nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","OLMr")
    nq.strdec("simstr")
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for r1 in x:
                simstr = "10dec14.10dec13.14_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                simstr += "_washOLMr_"+str(r1)
                nq.append(y,simstr,iseed,wseed,r1)
                y += 1
    return nq

# addwashnqpcol -- add a column to nqb from washbatchnq with power spectra from h.matpmtm.
def addwashnqpcol(nqb):
    from neuron import h
#    from network import net
#    from run import loadminrundat
    nqb.tog("DB")
    if nqb.fi("nqpbase") == -1:
        nqb.resize("nqpbase") # baseline power spectra
        nqb.odec("nqpbase")
        nqb.resize("nqpwin")  # washin power spectra
        nqb.odec("nqpwin")
        nqb.resize("nqpwout") # washout power spectra
        nqb.odec("nqpwout")
        nqb.pad()
    cdx = int(nqb.fi("nqpbase")) # column id
    vec=h.Vector()
    dt = h.dt # time interval
    sampr = 1e3/dt # sampling rate
    vsidx = [2e3/dt,4e3/dt,6e3/dt] # start times for different periods
    veidx = [4e3/dt,6e3/dt,8e3/dt] # end times for different periods
    for i in range(int(nqb.v[0].size())):
        simstr = nqb.get("simstr",i).s
        print ("up to " + str(i) + " out of " + str(nqb.v[0].size()))
        print ("\tsim = " , simstr)
        loadminrundat(simstr) # load the sim data
        j = cdx # j has column index into nqb
        for k in range(len(vsidx)):
            print ("interval=",k,vsidx[k],veidx[k])
            vec.resize(0)
            vec.copy(net.vlfp,vsidx[k],veidx[k]) # copy relevant portion of LFP
            vec.sub(vec.mean())       # remove mean
            nqp=h.matpmtm(vec,sampr)  # get the power spectra
            nqb.set(nqb.s[j].s,i,nqp) # save nqp in correct row,column of nqb
            h.nqsdel(nqp) # free memory
            j += 1 # increment column index

# runs a batch of sims where BAS cells are turned off
def basbatch(startnum=0):
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            if y < startnum:
                print ("skipping sim num ", y)
                y += 1
                continue
            s = "./mod/x86_64/special -python basbatchrun.py"
            s += " "+str(iseed)+" "+str(wseed)
            print ("sim num = ", y, ", command = ", s)
            y += 1
            mylog(s,"basbatch_10dec13.14.log")
            os.system(s)

# load info about basbatch run into an NQS. returns the NQS
def basbatchnq():
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed")
    nq.strdec("simstr")
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            simstr = "10dec15.10dec13.14_iseed_"+str(iseed)+"_wseed_"+str(wseed)
            simstr += "_BASoff_"
            nq.append(y,simstr,iseed,wseed)
            y += 1
    return nq


# runs a batch of sims where OLM NMDA is off and different levels of current injection
# into the OLM cells is applied. calls currinjbatchrun.py to run sim & save data.
def currinjbatch(nlevels,startnum=0):
    x = numpy.linspace(10,50,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                if y < startnum:
                    print ("skipping sim num ", y)
                    y += 1
                    continue
                s = "./mod/x86_64/special -python currinjbatchrun.py"
                s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)
                print ("sim num = ", y, ", command = ", s)
                y += 1
                mylog(s,"currinjbatch_10dec13.14.log")
                os.system(s)

# load info about currinjbatch run into an NQS. returns the NQS
def currinjbatchnq(nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","incOLMInj")
    nq.strdec("simstr")
    x = numpy.linspace(10,50,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for ic in x:
                simstr = "10dec14.10dec13.14_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                simstr += "_incOLMInj_"+str(ic)
                nq.append(y,simstr,iseed,wseed,ic)
                y += 1
    return nq


# runs a batch of sims with 3 periods: baseline, washin, current injection (to replace washout)
# during washin, ALL OLM NMDA is off. during current injection different levels of current injection
# are sent into the OLM cells instead of washout. calls washinjbatchrun.py to run sim & save data.
def washinjbatch(nlevels,startnum=0):
    x = numpy.linspace(0,50,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                if y < startnum:
                    print ("skipping sim num ", y)
                    y += 1
                    continue
                s = "./mod/x86_64/special -python washinjbatchrun.py"
                s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)
                print ("sim num = ", y, ", command = ", s)
                y += 1
                mylog(s,"washinjbatch_10dec15.06.log")
                os.system(s)

# load info about washinjbatch run into an NQS. returns the NQS
def washinjbatchnq(nlevels):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","incOLMInj")
    nq.strdec("simstr")
    x = numpy.linspace(0,50,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for ic in x:
                simstr = "10dec16.10dec15.06_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                simstr += "_washincOLMInj_"+str(ic*1e-3)
                nq.append(y,simstr,iseed,wseed,ic)
                y += 1
    return nq

# runs a batch of sims varying the MSGain (medial septal weight gain)
# msbatchrun.py to run sim & save data.
def msbatch(nlevels,startnum=0):
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for i1,r1 in enumerate(x):
                if y < startnum:
                    print ("skipping sim num ", y)
                    y += 1
                    continue
                s = "./mod/x86_64/special -python msbatchrun.py"
                s += " "+str(iseed)+" "+str(wseed)+" "+str(r1)
                print ("sim num = ", y, ", command = ", s)
                y += 1
                mylog(s,"msbatch_11mar28.12.log")
                os.system(s)

# load info about msbatch run into an NQS. returns the NQS
def msbatchnq(nlevels=5):
    from neuron import h
    nq = h.NQS("id","simstr","iseed","wseed","msgain")
    nq.strdec("simstr")
    x = numpy.linspace(0,1,nlevels)
    y = 0
    for iseed in liseed:
        for wseed in lwseed:
            for msgain in x:
                simstr = "11mar28.12_iseed_"+str(iseed)+"_wseed_"+str(wseed)
                simstr += "_msgain_"+str(msgain)
                nq.append(y,simstr,iseed,wseed,msgain)
                y += 1
    return nq

# # append line s to filepath fn
# def appline (s,fn):
#   '''append line s to filepath fn'''
#   fp = open(fn,"a"); fp.write(s + "\n"); fp.close()

# append to the lists
def NewParam (lsec,lopt,lval,sec,opt,val):
  '''append to the lists of params'''
  lsec.append(sec); lopt.append(opt); lval.append(val)


# check that the batch dir exists
def checkdir (d):
  '''check that the batch dir exists'''
  try:
    if not os.path.exists(d): os.mkdir(d)
    return True
  except:
    print ("could not create directory :" + d)
    return False



# run a batch using multiprocessing 
#  based on http://www.bryceboe.com/2011/01/28/the-python-multiprocessing-queue-and-large-objects/
# obtained from /u/samn/ca1d/batch.py
def batchRun (whichParams,blog,skip=[],qsz=10,bdir="./batchconfigFiles"):
  '''run a batch using multiprocessing'''
  if not checkdir(bdir): return False
  jobs = multiprocessing.Queue()
  lsec,lopt,lval,lconfigfilestr = whichParams()

  def myworker (jobs):
    while True:
      scomm = jobs.get()
      if scomm == None: break
      print ("worker starting : " , scomm)
      os.system(scomm) #worker function, invoked in a process.

  for i in range(len(lsec)):
    if i in skip: continue
    cfgname = os.path.join(bdir, lconfigfilestr[i] + ".cfg")
    writeconf(cfgname,sec=lsec[i],opt=lopt[i],val=lval[i])
    cmd = "python runone.py " + cfgname
    print (cmd, type(cmd))
    appline(cmd,blog)
    jobs.put(cmd)
  workers = []
  for i in range(qsz):
    jobs.put(None)
    tmp = multiprocessing.Process(target=myworker, args=(jobs,))
    tmp.start()
    workers.append(tmp)
  for worker in workers: worker.join()
  return jobs.empty()




# main...
if __name__ == "__main__":
    na = len(sys.argv) # number of args
    print (sys.argv)
    if na < 2:
        print ("Usage: python batch.py type[0=nmbatch,1=washbatch,2=currinjbatch,3=basbatch,4=washinj,5=msbatch,6=ntebatch,7=ihbatch],[nlevels,startnum]")
        sys.exit(1)

    ty = int(sys.argv[1])

    print ("hello!!! ty is : " + str(ty))

    if ty == 0:
        print ("nmbatch")
        bru = nmbatch
    elif ty == 1:
        print ("washbatch")
        bru = washbatch
    elif ty == 2:
        print ("currinjbatch")
        bru = currinjbatch
    elif ty == 3:
        print ("basbatch")
        if na > 2:
            startnum = int(sys.argv[2])
            basbatch(startnum)
        else:
            basbatch()
        sys.exit(0)
    elif ty == 4:
        print ("washinj")
        bru = washinjbatch
    elif ty == 5:
        print ("msbatch")
        bru = msbatch
    elif ty == 6:
        print ("ntebatch")
        bru = ntebatch
    elif ty == 7:
        print ("ihbatch")
        bru = ihbatch
    elif ty == 8:
        print ("ihbatchPYRBAS")
        bru = ihbatchPYRBAS
    elif ty == 9:
        print ("longihbatchPYRBAS")
        bru = longihbatchPYRBAS
    elif ty == 10:
        print ("longihbatchOLM")
        bru = longihbatchOLM
    else:
        print (str(ty) + "is an unknown batch type!")
        sys.exit(1)
        
    nlevels = int(sys.argv[2])
    if na > 3:
        startnum = int(sys.argv[3])
        bru(nlevels,startnum)
    else:
        bru(nlevels)

    sys.exit(0)

