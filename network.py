# $Id: network.py,v 1.128 2012/11/09 19:40:34 samn Exp $ 

# from pyinit import *
# from geom import *
import random
import math


########### parameters read from config file ###########
# endocannabinoid system
includeCCKcs = dconf['includeCCKcs']
CB1R_cck_somaPyr_weight = dconf['CB1R_cck_somaPyr_weight']
CB1R_cck_Adend2Pyr_weight = dconf['CB1R_cck_Adend2Pyr_weight']
CB1R_pyr_recurrent_weight = dconf['CB1R_pyr_recurrent_weight']
CB1R_pyr_pv_weight = dconf['CB1R_pyr_pv_weight']
CB1R_MS_weight = dconf['CB1R_MS_weight']
CB1R_cck_Adend3_weight = dconf['CB1R_cck_Adend3_weight']
CB1R_pyr_olm_weight = dconf['CB1R_pyr_olm_weight']
# CB1R_pyr_randomInput_weight = dconf['CB1R_pyr_randomInput_weight'] # which ones should go here? apical or soma??? mostly apical 


# number of cells and convergence
scale = dconf['scale'] # when scale==1, there are 800 pyr cs, 200 bas cs, and 200 olm cs

if scale==0:
    pyrPop_cNum = dconf['pyrPop_cNum'] 
    basPop_cNum = dconf['basPop_cNum']
    olmPop_cNum = dconf['olmPop_cNum']
    cck_somaPyrPop_cNum = dconf['cck_somaPyrPop_cNum']
    cck_Adend2PyrPop_cNum = dconf['cck_Adend2PyrPop_cNum']
    cck_Adend3Pop_cNum = dconf['cck_Adend3Pop_cNum']
    pyr_pyr_location = dconf['pyr_pyr_location']
    olm_pyr_location = dconf['olm_pyr_location']
    # cell convergence ratios
    pyr_bas_conv = dconf['pyr_bas_conv'] 
    pyr_olm_conv = dconf['pyr_olm_conv']
    # pyr_cck_conv = dconf['pyr_cck_conv'] # will remove this
    pyr_cck_somaPyr_conv = dconf['pyr_cck_somaPyr_conv']
    pyr_cck_Adend2Pyr_conv = dconf['pyr_cck_Adend2Pyr_conv']
    pyr_pyr_conv = dconf['pyr_pyr_conv']
    bas_bas_conv = dconf['bas_bas_conv']
    bas_pyr_conv = dconf['bas_pyr_conv']
    cck_somaPyr_pyr_conv = dconf['cck_somaPyr_pyr_conv']
    cck_Adend2Pyr_pyr_conv = dconf['cck_Adend2Pyr_pyr_conv']
    cck_somaPyr_bas_conv = dconf['cck_somaPyr_bas_conv'] # for later
    bas_cck_somaPyr_conv = dconf['bas_cck_somaPyr_conv'] # for later
    cck_somaPyr_cck_somaPyr_conv = dconf['cck_somaPyr_cck_somaPyr_conv'] # for later
    bas_olm_conv = dconf['bas_olm_conv']
    olm_pyr_conv = dconf['olm_pyr_conv']
    pyr_cck_Adend3_conv = dconf['pyr_cck_Adend3_conv']
    cck_Adend3_pyr_conv = dconf['cck_Adend3_pyr_conv']


    
else:
    pyrPop_cNum = int(math.ceil(800*scale))
    basPop_cNum = int(math.ceil(200*scale))
    olmPop_cNum = int(math.ceil(200*scale))
    pyr_pyr_location = 'basal'
    olm_pyr_location = 'mid-apical'
    pyr_bas_conv = 100
    pyr_olm_conv = 10
    pyr_pyr_conv = 25
    bas_bas_conv = 60
    bas_pyr_conv = 50
    olm_pyr_conv = 20
    bas_olm_conv = 1


# noise
noise = dconf['noise']
DoMakeNoise = dconf['DoMakeNoise']
UseNetStim = dconf['UseNetStim']
useGfluct = dconf['useGfluct']

# signal
DoMakeSignal = dconf['DoMakeSignal']
SIGNAL_RSEED = dconf['signal_rseed']
signal_isi = dconf['signal_isi']

# recording/saving spikes
recPyrInputSpikes = dconf['recPyrInputSpikes']
savePyrInputSpikes = dconf['savePyrInputSpikes']
recSignalSpikes = dconf['recSignalSpikes']
saveSignalSpikes = dconf['saveSignalSpikes']



# make connections
connections = dconf['connections']

# NMDAR on the different cells
olm_NMDARw_scaling = dconf['olm_NMDARw_scaling']
pv_NMDARw_scaling = dconf['pv_NMDARw_scaling']
pyr_NMDARw_scaling = dconf['pyr_NMDARw_scaling']
cck_Soma_NMDARw_scaling = dconf['cck_Soma_NMDARw_scaling']
cck_Adend2_NMDARw_scaling = dconf['cck_Adend2_NMDARw_scaling']
cck_Adend3_NMDARw_scaling = dconf['cck_Adend3_NMDARw_scaling']

# AMPAR on OLM cells
olm_AMPARw_scaling = dconf['olm_AMPARw_scaling']


# Medial Septum input onto differnet subpopulations
MedialSeptum_gain_olm = dconf['MedialSeptum_gain_olm']
MedialSeptum_gain_pv = dconf['MedialSeptum_gain_pv']
MedialSeptum_gain_cck = dconf['MedialSeptum_gain_cck']

# scaling of the weights of intrinsic and extrinsic AMPAfR and GABAfR
extrinsic_pyr_AMPAfR_weight_scale = dconf['extrinsic_pyr_AMPAfR_weight_scale']
intrinsic_pyr_AMPAfR_weight_scale = dconf['intrinsic_pyr_AMPAfR_weight_scale']
extrinsic_pyr_GABAfR_weight_scale = dconf['extrinsic_pyr_GABAfR_weight_scale']
intrinsic_pyr_GABAfR_weight_scale = dconf['intrinsic_pyr_GABAfR_weight_scale']

extrinsic_pv_AMPAfR_weight_scale = dconf['extrinsic_pv_AMPAfR_weight_scale']
intrinsic_pv_AMPAfR_weight_scale = dconf['intrinsic_pv_AMPAfR_weight_scale']
extrinsic_pv_GABAfR_weight_scale = dconf['extrinsic_pv_GABAfR_weight_scale']
intrinsic_pv_GABAfR_weight_scale = dconf['intrinsic_pv_GABAfR_weight_scale']

extrinsic_olm_AMPAfR_weight_scale = dconf['extrinsic_olm_AMPAfR_weight_scale']
intrinsic_olm_AMPAfR_weight_scale = dconf['intrinsic_olm_AMPAfR_weight_scale']
extrinsic_olm_GABAfR_weight_scale = dconf['extrinsic_olm_GABAfR_weight_scale']
intrinsic_olm_GABAfR_weight_scale = dconf['intrinsic_olm_GABAfR_weight_scale']

extrinsic_cck_AMPAfR_weight_scale = dconf['extrinsic_cck_AMPAfR_weight_scale']
intrinsic_cck_AMPAfR_weight_scale = dconf['intrinsic_cck_AMPAfR_weight_scale']
extrinsic_cck_GABAfR_weight_scale = dconf['extrinsic_cck_GABAfR_weight_scale']
intrinsic_cck_GABAfR_weight_scale = dconf['intrinsic_cck_GABAfR_weight_scale']


# scaling of inactivation time constant of GABAf bas -> pyr
tau2_bas_pyr_GA_scale = dconf['tau2_bas_pyr_GA_scale']

ISEED = dconf['iseed']
WSEED = dconf['wseed']
STDP = dconf['STDP']
SaveConn = dconf['saveconn']
# saveNetStimInputs = dconf['saveNetStimInputs']
GABAontoCCK_scale = dconf['GABAontoCCK_scale']
# h.fracca_MyExp2SynNMDABB = dconf['nmfracca'] # fraction of NMDA current that is from calcium - set to 0 if calcium dynamics are not involved # commented that out since we are using the older version of MyExp2SynNMDABB


########### code for setting population and cells 
gGID = 0 # global ID for cells

class Population:
    "Population of cells"
    # cell_type -- pyr, bas, olm, [cck_somaPyr, cck_Adend2Pyr] (if includeCCKcs)
    # n -- number of cells in the population
    # x, y, z -- initial position for the first Cell
    # dx -- an increment of the x-position for the cell location
    # amp, dur, delay -- parameters for the IClamp in the soma
    # Spikes are stored in ltimevec (times) and lidvec (cell # within the population)
    def __init__(self, cell_type, n, x, y, z, dx, amp, dur, delay):
        global gGID
        self.cell = [] # List of cells in the population
        self.nc   = [] # NetCon list for recording spikes
        self.n    = n  # number of cells
        self.x    = x
        self.y    = y
        self.z    = z
        self.ltimevec = h.List() # list of Vectors for recording spikes, one per cell
        self.lidvec = h.List()
        self.nssidx = {}
        self.nseidx = {}
        self.ncsidx = {}
        self.nceidx = {}
        for i in range(n):
            self.cell.append(cell_type(x+i*dx,y,z,gGID))
            self.cell[-1].somaInj.amp   = amp
            self.cell[-1].somaInj.dur   = dur
            self.cell[-1].somaInj.delay = delay
            self.nc.append(h.NetCon(self.cell[-1].soma(0.5)._ref_v, None, sec=self.cell[-1].soma))
            self.ltimevec.append(h.Vector()) #NB: each NetCon gets own Vectors for recording. needed to avoid multithreading crash
            self.lidvec.append(h.Vector())
            self.nc[-1].record(self.ltimevec[-1],self.lidvec[-1],gGID) # record cell spikes with gGID
            gGID = gGID + 1 # inc global cell ID
            
    def set_r(self, syn, r):
        for c in self.cell:
            c.__dict__[syn].syn.r = r

    def clear_volt(self):
        for cell in self.cell: cell.clear_volt()

    def clear_spikes(self):
        for L in [self.ltimevec, self.lidvec]:
            for vec in L: vec.resize(0)

class MSpec: # this class uses matlab to make a spectrogram

    def __init__(self,vlfp,maxfreq,nsamp,dodraw): #make a spectrogram using matlab
        h("jjj=name_declared(\"nqspec\")")
        h("if(jjj){nqsdel(nqspec) print \"deleted nqspec\"}")
        h("objref nqspec")
        vslfp = h.Vector()
        vslfp.copy(vlfp)
        vslfp.sub(vlfp.mean())
        h.nqspec = h.matspecgram(vslfp,1e3/h.dt,maxfreq,nsamp,dodraw)
        self.nqspec = h.nqspec

    def powinrange(self,minf,maxf): # get scalar power in range of frequencies
        nn = self.nqspec.select(-1,"f","[]",minf,maxf)
        if nn == 0:
            return 0
        h("jnk = 0")
        h("vec.resize(0)")
        for i in self.nqspec.ind:
            mystr = "vec.copy(nqspec.get(\"pow\","
            mystr += str(int(i))
            mystr += ").o)"
            h(mystr)
            h("jnk += vec.sum()")
        jnk = h.jnk
        return jnk / nn

    def vecinrange(self,minf,maxf): # get vector of power in range of frequencies vs time
        nn = self.nqspec.select(-1,"f","[]",minf,maxf)
        if nn == 0:
            return None
        h("objref vjnk")
        h("vjnk=new Vector()")
        h.vec.resize(0)
        for i in self.nqspec.ind:
            mystr = "vec.copy(nqspec.get(\"pow\","
            mystr += str(int(i))
            mystr += ").o)"
            h(mystr)
            if h.vjnk.size()==0:
                h.vjnk.copy(h.vec)
            else:
                h.vjnk.add(h.vec)
        h.vjnk.div(self.nqspec.ind.size())
        return h.vjnk

class Network(object):

    def __init__(self,noise=True,connections=True,DoMakeNoise=True,iseed=1234,UseNetStim=True,DoMakeSignal=False,signal_rseed=7483,signal_isi=200,wseed=4321,scale=1.0,MSGain_olm=0.0,MSGain_pv=0.0,MSGain_cck=0.0,SaveConn=False,UseSTDP=False):
        #import math
        print ("Setting Cells")
        self.pyr = Population(cell_type=PyrAdr,n=pyrPop_cNum, x= 0, y=0, z=0, dx=50, amp= 50e-3, dur=1e9, delay=2*h.dt)
        self.bas = Population(cell_type=PVC,   n=basPop_cNum, x=10, y=0, z=0, dx=50, amp=     0, dur=  0, delay=2*h.dt)
        self.olm = Population(cell_type=Ow,   n=olmPop_cNum, x=20, y=0, z=0, dx=50, amp=-25e-3, dur=1e9, delay=2*h.dt)
        if includeCCKcs:
            self.cck_somaPyr = Population(cell_type=CCKC, n = cck_somaPyrPop_cNum, x=30, y=0, z=0, dx=50, amp =0, dur = 0, delay = 2*h.dt)
            self.cck_Adend2Pyr = Population(cell_type=CCKC, n = cck_Adend2PyrPop_cNum, x=40, y=0, z=0, dx=50, amp =0, dur = 0, delay = 2*h.dt)
            if cck_Adend3Pop_cNum != 0:
                self.cck_Adend3 = Population(cell_type=CCKC, n = cck_Adend3Pop_cNum, x=50, y=0, z=0, dx=50, amp = 0, dur = 0, delay = 2*h.dt)

        # psr = sensor cell to estimate the E->E connections
        self.psr = Population(cell_type=PyrAdr,n=1,   x= 0, y=0, z=0, dx=50, amp= 50e-3, dur=1e9, delay=2*h.dt) 
        if includeCCKcs:
            if cck_Adend3Pop_cNum == 0: # no cck_Adend3 cells
                self.cells = [self.pyr, self.bas, self.olm, self.cck_somaPyr, self.cck_Adend2Pyr, self.psr]
            else:
                self.cells = [self.pyr, self.bas, self.olm, self.cck_somaPyr, self.cck_Adend2Pyr, self.cck_Adend3, self.psr]                
        else: self.cells = [self.pyr, self.bas, self.olm, self.psr]
        self.iseed = iseed # seed for noise inputs
        self.noise = noise
        self.DoMakeNoise = DoMakeNoise
        self.UseNetStim = UseNetStim
        self.useGfluct = useGfluct
        self.signal_rseed = signal_rseed
        self.signal_isi = signal_isi
        self.DoMakeSignal = DoMakeSignal
        self.wseed = wseed # seed for 'wiring'
        self.MSGain_olm = MSGain_olm # gain for MS weights onto olm cells
        self.MSGain_pv = MSGain_pv # gain for MS weights onto pv cells
        self.MSGain_cck = MSGain_cck # gain for MS weights onto cck cells
        self.RecPyr = False
        self.SaveConn = SaveConn
        self.UseSTDP = UseSTDP
        self.linputVec = [] # list of vectors recording from netstims
        
        if connections:
            print ("Setting Connections")
            self.set_all_conns()

    def set_noise_inputs(self,simdur): #simdur only used for make_all_noise
        if self.UseNetStim:
            self.make_all_NetStims(simdur,self.iseed)
        if self.useGfluct and not self.DoMakeNoise:
            self.set_gfluct_noise()
            print('will use Gfluct for synaptic noise')
            pass
        print ("Done!")


    def set_signal_input(self, simdur):
        print ('Will make signal netstim')
        self.make_signal(simdur, self.signal_isi)


    #this should be called @ beginning of each sim - done in an FInitializeHandler in run.py
    def init_NetStims(self):
        # h.mcell_ran4_init(self.iseed)
        for i in range(len(self.nrl)):
            rds = self.nrl[i]
            sead = self.nrlsead[i]
            rds.MCellRan4(sead,sead)
            rds.negexp(1)           
            # print i,rds,sead

    #creates NetStims (and associated NetCon,Random) - provide 'noise' inputs
    #returns next useable value of sead
    def make_NetStims(self,po,syn,w,ISI,time_limit,sead):
        po.nssidx[syn] = len(self.nsl) #index into net.nsl
        po.ncsidx[syn] = len(self.ncl) #index into net.ncl
        # implement uniform random number distribution to chose the starting point from
        rd2 = h.Random()
        rd2.ACG(sead)
        # rd2.uniform(0,1e3)
        rd2.uniform(0,250)
        for i in range(po.n):
            cel = po.cell[i]

            ns = h.NetStim()
            ns.interval = ISI
            ns.noise = 1            
            ns.number = (1e3 / ISI) * time_limit
            ns.start = 0

            nc = h.NetCon(ns,cel.__dict__[syn].syn)
            nc.delay = h.dt * 2 # 0
            nc.weight[0] = w

            rds = h.Random()
            rds.negexp(1)            # set random # generator using negexp(1) - avg interval in NetStim
            rds.MCellRan4(sead,sead) # seeds are in order, shouldn't matter         
            ns.noiseFromRandom(rds)  # use random # generator for this NetStim
            
            ns.start = rd2.repick() # start inputs random time btwn 0-1e3 ms to avoid artificial sync

#rds.MCellRan4(sead,sead) # reinit rand # generator

            self.nsl.append(ns)
            self.ncl.append(nc)
            self.nrl.append(rds)
            self.nrlsead.append(sead)
            sead = sead + 1

        po.nseidx[syn] = len(self.nsl)-1
        po.nceidx[syn] = len(self.ncl)-1
        
        return sead

    def set_gfluct_noise(self):
        '''will insert gfluct into soma of cells in population po, and set its parameters'''
        self.grseedl = [] # list of seeds for Gfluctp
        grseed = self.iseed
        for po in [self.pyr, self.bas, self.olm]:
            for i in range(po.n):
                cel = po.cell[i]
                cel.insert_gfluct_noise()
                cel.Gfluctp.seed1 = grseed # we will need to change this so that not every cell wwould have the same exact random numbers
                cel.Gfluctp.noiseFromRandom123()
                self.grseedl.append(grseed)
                grseed += 1

    # setup recording of pyramidal cell driving inputs, assumes using NetCon,NetStims
    def RecPYRInputs(self):
        self.RecPyr = True
        self.NCV = {}
        self.sys = ['somaAMPAf', 'Adend3AMPAf', 'somaGABAf', 'Adend3GABAf']
        sys=self.sys
        for s in sys:
            self.NCV[s] = []
            sidx = self.pyr.ncsidx[s]
            eidx = self.pyr.nceidx[s]
            for i in range(sidx,eidx+1):
                self.NCV[s].append(h.Vector())
                self.ncl[i].record(self.NCV[s][-1])

    # make an NQS with pyramidal cell drive input times
    def setnqin(self):
        try:
            h.nqsdel(self.nqin)
        except:
            pass
        self.nqin = h.NQS("id","sy","vt")
        nqin=self.nqin
        nqin.odec("vt")
        jdx = 0
        for s in self.sys:
            sidx = self.pyr.ncsidx[s]
            eidx = self.pyr.nceidx[s]
            idx = 0
            for i in range(0,len(self.NCV[s])):
                nqin.append(idx,jdx,self.NCV[s][i])
                idx = idx + 1
            jdx = jdx + 1

    def RecPyrIntrinsicInputs(self):# NOT FINISHED YET
        '''set up recording of pyramidal cells intrinsic connectvitny with other cells within the model        - NOT FINISHED YET'''
        self.RecIntrinsicPyr = True
        self.dintrinsicPyrRecVecs = {}
        self.intrinsicPyrSyns = ['bas_pyr_GA', 'cck_somaPyr_pyr_GA', 'pyr_pyr_NM', 'pyr_pyr_AM', 'cck_Adend2Pyr_pyr_GA', 'olm_pyr_GA']
        for mysyn in self.intrinsicPyrSyns:
            self.dintrinsicPyrRecVecs[mysyn] = []
            for mynetcon in self.__getattribute__(mysyn):
                self.dintrinsicPyrRecVecs[mysyn].append(h.Vector())
                mynetcon.record(self.dintrinsicPyrRecVecs[mysyn][-1])
                                                     

    # make a histogram of pyramidal cell spike outputs
    def mkspkh(self,binsz):
        snq=self.snq
        snq.verbose = 0
        self.spkh = h.List()
        for i in range(0,800):
            if snq.select("id",i) > 0:
                vt = snq.getcol("t")
                self.spkh.append(vt.histogram(0,h.tstop,binsz))
            else:
                self.spkh.append(h.Vector())
        snq.verbose=1

    def make_all_NetStims(self,simdur,rdmseed):
        '''Making NetStims for Generating Random Input (Noise), including input from Medial Septum'''
        # h.mcell_ran4_init(self.iseed)
        self.nsl = [] #NetStim List
        self.ncl = [] #NetCon List
        self.nrl = [] #Random List for NetStims
        self.nrlsead = [] #List of seeds for NetStim randoms
        # numpy.random.seed(rdmseed) # initialize random # generator
        rdtmp = rdmseed # starting sead value - incremented in make_NetStims
        if self.DoMakeNoise:
            print ("Making NetStims for Generating Random Input (Noise)")
            print ("Making Noise")
            print ("to PYR")
            rdtmp=self.make_NetStims(po=self.pyr, syn="somaAMPAf",   w=0.05e-3 * extrinsic_pyr_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp) 
            rdtmp=self.make_NetStims(po=self.pyr, syn="Adend3AMPAf", w=0.05e-3 * extrinsic_pyr_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.pyr, syn="somaGABAf",   w=0.012e-3 * extrinsic_pyr_GABAfR_weight_scale, ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.pyr, syn="Adend3GABAf", w=0.012e-3 * extrinsic_pyr_GABAfR_weight_scale, ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.pyr, syn="Adend3NMDA",  w=6.5e-3,   ISI=100,time_limit=simdur, sead=rdtmp)
            print ("to BAS")          
            rdtmp=self.make_NetStims(po=self.bas, syn="somaAMPAf",   w=0.02e-3 * extrinsic_pv_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.bas, syn="somaGABAf",   w=0.2e-3 * extrinsic_pv_GABAfR_weight_scale,   ISI=1,  time_limit=simdur, sead=rdtmp)
            print ("to OLM")
            #rdtmp=self.make_NetStims(po=self.olm, syn="somaAMPAf",   w=0.02e-3,  ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.olm, syn="somaAMPAf",   w=0.0625e-3 * olm_AMPARw_scaling * extrinsic_olm_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
            rdtmp=self.make_NetStims(po=self.olm, syn="somaGABAf",   w=0.2e-3 * extrinsic_olm_GABAfR_weight_scale,   ISI=1,  time_limit=simdur, sead=rdtmp)
            if includeCCKcs:
                print ("to CCK")          
                # soma targeting cck cells
                rdtmp=self.make_NetStims(po=self.cck_somaPyr, syn="somaAMPAf",   w=0.02e-3 * extrinsic_cck_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
                rdtmp=self.make_NetStims(po=self.cck_somaPyr, syn="somaGABAf",   w=0.2e-3 * GABAontoCCK_scale * extrinsic_cck_GABAfR_weight_scale,   ISI=1,  time_limit=simdur, sead=rdtmp)
                # mid-apical dendrite targeting cck cells
                rdtmp=self.make_NetStims(po=self.cck_Adend2Pyr, syn="somaAMPAf",   w=0.02e-3 * extrinsic_cck_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
                rdtmp=self.make_NetStims(po=self.cck_Adend2Pyr, syn="somaGABAf",   w=0.2e-3 * GABAontoCCK_scale * extrinsic_cck_GABAfR_weight_scale,   ISI=1,  time_limit=simdur, sead=rdtmp)
                if cck_Adend3Pop_cNum != 0:
                    # distal dendrite targeting cck cells
                    rdtmp=self.make_NetStims(po=self.cck_Adend3, syn="somaAMPAf",   w=0.02e-3 * extrinsic_cck_AMPAfR_weight_scale,  ISI=1,  time_limit=simdur, sead=rdtmp)
                    rdtmp=self.make_NetStims(po=self.cck_Adend3, syn="somaGABAf",   w=0.2e-3 * GABAontoCCK_scale * extrinsic_cck_GABAfR_weight_scale,   ISI=1,  time_limit=simdur, sead=rdtmp)

        #setup medial septal inputs to OLM and BASKET cells, note that MSGain can be 0 == no effect
        print("Making NetStims for MS input")
        ns = h.NetStim()
        ns.interval = 150
        ns.noise = 0 # NO randomness for the MS inputs
        ns.number = (1e3 / 150.0) * simdur
        self.nsl.append(ns)
        for i in range(self.bas.n): # MS inputs to BASKET cells
            nc = h.NetCon(ns,self.bas.cell[i].__dict__["somaGABAss"].syn)
            nc.delay = 2*h.dt
            nc.weight[0] = 1.6e-3 * self.MSGain_pv / CB1R_MS_weight
            self.ncl.append(nc)
        for i in range(self.olm.n): # MS inputs to OLM cells
            nc = h.NetCon(ns,self.olm.cell[i].__dict__["somaGABAss"].syn)
            nc.delay = 2*h.dt
            nc.weight[0] = 1.6e-3 * self.MSGain_olm / CB1R_MS_weight
            self.ncl.append(nc)
        if includeCCKcs:
            # cck cells targeting pyr soma
            for i in range(self.cck_somaPyr.n): # MS inputs to CCK cells
                nc = h.NetCon(ns,self.cck_somaPyr.cell[i].__dict__["somaGABAss"].syn)
                nc.delay = 2*h.dt
                nc.weight[0] = 1.6e-3 * self.MSGain_cck * GABAontoCCK_scale / CB1R_MS_weight
                self.ncl.append(nc)
            # cck cells targeting pyr mid-apical dendrites
            for i in range(self.cck_Adend2Pyr.n): # MS inputs to CCK cells
                nc = h.NetCon(ns,self.cck_Adend2Pyr.cell[i].__dict__["somaGABAss"].syn)
                nc.delay = 2*h.dt
                nc.weight[0] = 1.6e-3 * self.MSGain_cck * GABAontoCCK_scale / CB1R_MS_weight
                self.ncl.append(nc)
            if cck_Adend3Pop_cNum != 0:
                # cck cells targeting pyr distal dendrites
                for i in range(self.cck_Adend3.n): # MS inputs to CCK cells
                    nc = h.NetCon(ns,self.cck_Adend3.cell[i].__dict__["somaGABAss"].syn)
                    nc.delay = 2*h.dt
                    nc.weight[0] = 1.6e-3 * self.MSGain_cck * GABAontoCCK_scale / CB1R_MS_weight
                    self.ncl.append(nc)
            
    def record_all_netStim_times(self):
        '''It will record the spike timings from netcons (receiving stimulation from netstims) to a list of vectors. Will be called only if recordNetStimInputs is True.'''
        self.linputVec = [h.Vector() for i in range(len(self.ncl))]
        for vec, nc in zip(self.linputVec, self.ncl):
            nc.record(vec)

    
    def make_conn(self, preN, postN, conv):
        conn = numpy.zeros((postN,conv),dtype=numpy.int16)
        for i in range(postN):
            conn[i,:]=random.sample(range(preN),conv)
        return conn

    def set_all_conns(self):
        random.seed(self.wseed) # initialize random # generator for wiring
        print ("PYR -> X , NMDA")   # src, trg, syn, delay, weight, conv
        self.pyr_bas_NM=self.set_connections(self.pyr,self.bas, "somaNMDA", 2, 1.15*1.2e-3 * (1 / CB1R_pyr_pv_weight), pyr_bas_conv)
        self.pyr_olm_NM=self.set_connections(self.pyr,self.olm, "somaNMDA", 2, 1.0*0.7e-3 * (1 / CB1R_pyr_olm_weight), pyr_olm_conv)
	# location of targeting of pyr to pyr connections
        if pyr_pyr_location == 'basal':
            self.pyr_pyr_NM=self.set_connections(self.pyr,self.pyr, "BdendNMDA",2, 1*0.004e-3 * (1 / CB1R_pyr_recurrent_weight),  pyr_pyr_conv)
        elif pyr_pyr_location == 'mid-apical':
            self.pyr_pyr_NM=self.set_connections(self.pyr,self.pyr, "Adend2NMDA",2, 1*0.004e-3 * (1 / CB1R_pyr_recurrent_weight),  pyr_pyr_conv)
        if includeCCKcs:
            self.pyr_cck_somaPyr_NM=self.set_connections(self.pyr,self.cck_somaPyr, "somaNMDA", 2, 1.15*1.2e-3, pyr_cck_somaPyr_conv)
            self.pyr_cck_Adend2Pyr_NM = self.set_connections(self.pyr,self.cck_Adend2Pyr, "somaNMDA", 2, 1.15*1.2e-3, pyr_cck_Adend2Pyr_conv)
            if cck_Adend3Pop_cNum != 0:
                self.pyr_cck_Adend3_NM = self.set_connections(self.pyr,self.cck_Adend3, "somaNMDA", 2, 1.15*1.2e-3, pyr_cck_Adend3_conv)
        
        if self.UseSTDP: # did NOT implement CB1R agonism, or AMPAR agonism with STDP
            print ("PYR -> X , AMPA with STDP")
            self.pyr_bas_AM=self.set_connections(self.pyr,self.bas, "somaAMPASTDP",2, 0.3 * 1.2e-3 * (1 / CB1R_pyr_pv_weight),  pyr_bas_conv)
            self.pyr_olm_AM=self.set_connections(self.pyr,self.olm, "somaAMPASTDP",2, 0.3 * 1.2e-3 * (1 / CB1R_pyr_olm_weight),  pyr_olm_conv)
            self.pyr_pyr_AM=self.set_connections(self.pyr,self.pyr, "Adend3AMPASTDP",2, 0.5 * 0.04e-3, pyr_pyr_conv)
            if includeCCKcs:
                self.pyr_cck_somaPyr_AM=self.set_connections(self.pyr,self.cck_somaPyr, "somaAMPASTDP",2,0.3 * 1.2e-3, pyr_cck_somaPyr_conv)
                self.pyr_cck_Adend2Pyr_AM=self.set_connections(self.pyr,self.cck_Adend2Pyr, "somaAMPASTDP",2,0.3 * 1.2e-3, pyr_cck_Adend2Pyr_conv)
                if cck_Adend3Pop_cNum != 0:
                    self.pyr_cck_Adend3_AM=self.set_connections(self.pyr,self.cck_Adend3, "somaAMPASTDP",2,0.3 * 1.2e-3, pyr_cck_Adend3_conv)                
                
        else:
            print ("PYR -> X , AMPA")
            self.pyr_bas_AM=self.set_connections(self.pyr,self.bas, "somaAMPAf",2, 0.3 * 1.2e-3 * (1 / CB1R_pyr_pv_weight) * intrinsic_pv_AMPAfR_weight_scale,  pyr_bas_conv)
            self.pyr_olm_AM=self.set_connections(self.pyr,self.olm, "somaAMPAf",2, 0.3 * 1.2e-3 * (1 / CB1R_pyr_olm_weight) * olm_AMPARw_scaling * intrinsic_olm_AMPAfR_weight_scale,  pyr_olm_conv)
	    # location of targeting of pyr to pyr connections
            if pyr_pyr_location == 'basal':
            	self.pyr_pyr_AM=self.set_connections(self.pyr,self.pyr, "BdendAMPA",2, 0.5 * 0.04e-3 * (1 / CB1R_pyr_recurrent_weight) * intrinsic_pyr_AMPAfR_weight_scale, pyr_pyr_conv)
            elif pyr_pyr_location == 'mid-apical':
            	self.pyr_pyr_AM=self.set_connections(self.pyr,self.pyr, "Adend2AMPA",2, 0.5 * 0.04e-3 * (1  / CB1R_pyr_recurrent_weight) * intrinsic_pyr_AMPAfR_weight_scale, pyr_pyr_conv)
            if includeCCKcs:
                self.pyr_cck_somaPyr_AM=self.set_connections(self.pyr,self.cck_somaPyr, "somaAMPAf",2, 0.3 * 1.2e-3 * intrinsic_cck_AMPAfR_weight_scale,  pyr_cck_somaPyr_conv)
                self.pyr_cck_Adend2Pyr_AM=self.set_connections(self.pyr,self.cck_Adend2Pyr, "somaAMPAf",2, 0.3 * 1.2e-3 * intrinsic_cck_AMPAfR_weight_scale,  pyr_cck_Adend2Pyr_conv)
                if cck_Adend3Pop_cNum != 0:
                    self.pyr_cck_Adend3_AM=self.set_connections(self.pyr,self.cck_Adend3, "somaAMPAf",2, 0.3 * 1.2e-3 * intrinsic_cck_AMPAfR_weight_scale,  pyr_cck_Adend3_conv)
            
        print ("BAS -> X , GABA")
        #self.bas_bas_GA=self.set_connections(self.bas,self.bas, "somaGABAf",2, 1.0e-3, 60)#orig 1
        #self.bas_bas_GA=self.set_connections(self.bas,self.bas, "somaGABAf",2, 2  *  1.5*1.0e-3, 60)#new 1
        self.bas_bas_GA=self.set_connections(self.bas,self.bas, "somaGABAf",2, 3 * 1.5 * 1.0e-3 * intrinsic_pv_GABAfR_weight_scale, bas_bas_conv)#new 2
        self.bas_pyr_GA=self.set_connections(self.bas,self.pyr, "somaGABAf",2, 2 * 2 * 0.18e-3 * intrinsic_pyr_GABAfR_weight_scale, bas_pyr_conv)#new 1
        if tau2_bas_pyr_GA_scale != 1: # to run batches varying inactivatin time constant of GABAf bas -> pyr
            for i in range(basPop_cNum):
                self.bas.cell[i].somaGABAf.syn.tau2 *= tau2_bas_pyr_GA_scale
        self.bas_olm_GA=self.set_connections(self.bas,self.olm, "somaGABAf",2, 0.8 * 0.04 * 2 * 2 * 0.18e-3 * intrinsic_olm_GABAfR_weight_scale, bas_olm_conv)# addn MSJ 0.0288 e-3
        if includeCCKcs: # will not use for now
            self.bas_cck_somaPyr_GA=self.set_connections(self.bas,self.cck_somaPyr, "somaGABAf",2, 3 * 1.5 * 1.0e-3 * intrinsic_cck_GABAfR_weight_scale, bas_cck_somaPyr_conv)


        print ("OLM -> PYR , GABA")
        #self.olm_pyr_GA=self.set_connections(self.olm,self.pyr, "Adend2GABAs",2, 3*6.0e-3, 20)#original weight value
        if olm_pyr_location == 'mid-apical':
            self.olm_pyr_GA=self.set_connections(self.olm,self.pyr, "Adend2GABAs",2, 4.0 * 3 * 6.0e-3 * intrinsic_pyr_GABAfR_weight_scale, olm_pyr_conv)#new weight value
        elif olm_pyr_location == 'distal-apical':
            self.olm_pyr_GA=self.set_connections(self.olm,self.pyr, "Adend3GABAs",2, 4.0 * 3 * 6.0e-3 * intrinsic_pyr_GABAfR_weight_scale, olm_pyr_conv)#new weight value - olm targeting distal dendrites
       

        if includeCCKcs:
            print ("CCK -> X , GABA") # src, trg, syn, delay, weight, conv
            # CCK_somaPyr to themselves and to bas
            self.cck_somaPyr_bas_GA=self.set_connections(self.cck_somaPyr,self.bas, "somaGABAf",2, 3 * 1.5 * 1.0e-3 * intrinsic_pv_GABAfR_weight_scale, cck_somaPyr_bas_conv)
            self.cck_somaPyr_cck_somaPyr_GA=self.set_connections(self.cck_somaPyr,self.cck_somaPyr, "somaGABAf",2, 3 * 1.5 * 1.0e-3 * intrinsic_cck_GABAfR_weight_scale, cck_somaPyr_cck_somaPyr_conv)
            self.cck_somaPyr_pyr_GA=self.set_connections(self.cck_somaPyr,self.pyr, "somaGABAf",4, (1 /  CB1R_cck_somaPyr_weight) * 2  *  2*0.18e-3 * intrinsic_pyr_GABAfR_weight_scale, cck_somaPyr_pyr_conv)# delay of cck -> pyr is double that of pv -> pyr Glickfeld2006Distinct
            self.cck_Adend2Pyr_pyr_GA=self.set_connections(self.cck_Adend2Pyr,self.pyr, "Adend2GABAf",4, (1 / CB1R_cck_Adend2Pyr_weight) * 2  *  2*0.18e-3 * intrinsic_pyr_GABAfR_weight_scale, cck_Adend2Pyr_pyr_conv)# delay of cck -> pyr is double that of pv -> pyr Glickfeld2006Distinct
            if cck_Adend3Pop_cNum != 0:
                self.cck_Adend3_pyr_GA=self.set_connections(self.cck_Adend3,self.pyr, "Adend3GABAf",4, (1 / CB1R_cck_Adend3_weight) * 2  *  2*0.18e-3 * intrinsic_pyr_GABAfR_weight_scale, cck_Adend3_pyr_conv)# delay of cck -> pyr is double that of pv -> pyr Glickfeld2006Distinct

            #pyramidal to PSR cell -- for testing only
        # print "PYR -> PSR, AMPA/NMDA"
        # self.pyr_psr_NM=self.set_connections(self.pyr,self.psr, "BdendNMDA",2, 1*0.004e-3,  25)
        # self.pyr_psr_AM=self.set_connections(self.pyr,self.psr, "BdendAMPA",2, 0.5*0.04e-3, 25)


    def set_conn_weight(self, conn, weight):
        for nc in conn:
            nc.weight[0] = weight
            
    def set_connections(self,src,trg,syn,delay,w,conv):
        conn = self.make_conn(src.n,trg.n,conv)
        nc = []
        for post_id, all_pre in enumerate(conn):
            for j, pre_id in enumerate(all_pre):
                nc.append(h.NetCon(src.cell[pre_id].soma(0.5)._ref_v, trg.cell[post_id].__dict__[syn].syn, 0, delay, w, sec=src.cell[pre_id].soma)) 
        if self.SaveConn:
            try:
                print (self.nqcon.size())
            except:
                self.nqcon = h.NQS("id1","id2","w","syn")
                self.nqcon.strdec("syn")
            for post_id, all_pre in enumerate(conn):
                for j, pre_id in enumerate(all_pre):
                    self.nqcon.append(src.cell[pre_id].id,trg.cell[post_id].id,w,syn)   
        return nc

    def load_spikes(self,fn,po,syn,w,time_limit=10000):
        fn = os.path.join("data",fn)
        events = numpy.load(fn)
        print ("Begin setting events...", po)
        print (events.shape)
        for i,ii in enumerate(events):
            ii=ii[ii<=time_limit]
            po.cell[i].__dict__[syn].append(ii)
            po.cell[i].__dict__[syn].syn.Vwt = w
        print ("End setting events")
        return events

    def rasterplot(self,sz=2):
        pon  = 0        
        if h.g[0] == None:
            h.gg()
        col = [2, 4, 3, 1]
        for po in self.cells:
            id = h.Vector()
            tv = h.Vector()
            for i in range(po.n):
                id.append(po.lidvec[i])
                tv.append(po.ltimevec[i])
            id.mark(h.g[0],tv,"O",sz,col[pon],1)
            pon += 1
        h.g[0].exec_menu("View = plot")

    def setrastervecs(self):
        self.myidvec = h.Vector() #IDs and firing times for ALL cells
        self.mytimevec = h.Vector()
        for po in self.cells:
            for i in range(po.n):
                self.myidvec.append(po.lidvec[i])
                self.mytimevec.append(po.ltimevec[i])

    # setsnq - make an NQS with ids, spike times, types
    def setsnq(self):
          """setsnq - make an NQS with ids, spike times, types. ty 0 are pyramidal cells, type 1 are basket cells, type 2 are OLM cells, type 3 are cck cells targeting pyr soma, type 4 are cck cells targeting pyr distal dendrites"""
          try:
              h.nqsdel(self.snq)
          except:
              pass
          self.snq = h.NQS("id","t","ty")
          ty = 0
          vec = h.Vector()
          for po in self.cells:
              for i in range(po.n):
                  self.snq.v[0].append(po.lidvec[i])
                  self.snq.v[1].append(po.ltimevec[i])
                  vec.resize(po.lidvec[i].size())
                  vec.fill(ty)
                  self.snq.v[2].append(vec)
              ty += 1

    def clear_volt (self):
          for pop in self.cells: pop.clear_volt()

    def clear_spikes (self):
          for pop in self.cells: pop.clear_spikes()

    def clear_mem (self):
          self.clear_volt()
          self.clear_spikes()

        # get an nqs with somatic voltage from each cell - only valid after a run
    def getnqvolt (self, onlyInterneurons=True):
        '''get an nqs with somatic voltage from each cell - only valid after a run. If onlyInterneurons, the nqs contains voltages only from interneuorns'''
        try:
            h.nqsdel(self.nqv)
        except:
            pass
        if includeCCKcs:
            if cck_Adend3Pop_cNum == 0: # no cck_Adend3 cells
                if onlyInterneurons: whichCells = range(1,5) # exclude pyramidal cells
                else: whichCells = range(5)
            else: # there are cck_Adend3 cells
                if onlyInterneurons: whichCells = range(1,6)
                else: whichCells = range(6)
        else: 
            if onlyInterneurons: whichCells = range(1, 3)
            else: whichCells= range(3)
        allcells=0
        for i in whichCells: allcells += len(self.cells[i].cell)
        self.nqv=h.NQS(allcells); cdx=0; pops=['pyr', 'bas', 'olm', 'cck_somaPyr', 'cck_Adend2Pyr', 'cck_Adend3Pyr']
        for i in whichCells:
            for c in self.cells[i].cell:
                self.nqv.v[cdx].copy(c.soma_volt)
                self.nqv.s[cdx].s = pops[i] + '_' + str(cdx)
                cdx += 1
        self.nqv.resize('t'); self.nqv.v[int(self.nqv.m[0])-1].indgen(0,h.t,h.dt)


    # setfnq - make an NQS with ids, firing rates, types
    def setfnq (self,skipms=200):
        try: 
            self.snq.tog("DB")
        except:
            self.setsnq()
        try:
            h.nqsdel(self.fnq)
        except:
            pass
        self.fnq = h.NQS("id","freq","ty")
        tf = h.tstop - skipms
        ty = 0
        for po in self.cells:
            for i in range(po.n):
                id = po.cell[i].id
                n = float( self.snq.select("t",">",skipms,"id",id) )
                self.fnq.append(id, n*1e3/tf, ty)
            ty += 1

    # pravgrates - print average firing rates using self.fnq
    def pravgrates(self,skipms=200):
        try:
            self.fnq.tog("DB")
        except:
            self.setfnq(skipms)
        ty = 0
        tf = float( h.tstop - skipms )
        for po in self.cells:
            self.fnq.select("ty",ty)
            vf = self.fnq.getcol("freq")
            if vf.size() > 1:
                print ("ty: ", ty, " avg rate = ", vf.mean(), "+/-", vf.stderr(), " Hz")
            else:
                print ("ty: ", ty, " avg rate = ", vf.mean(), "+/-", 0.0 , " Hz")
            ty += 1

    # lfp is modeled as a difference between voltages in distal apical and basal compartemnts
    def calc_lfp (self):
          """lfp is modeled as a difference between voltages in distal apical and basal compartemnts"""
          self.vlfp = h.Vector(self.pyr.cell[0].Adend3_volt.size()) #lfp in neuron Vector
          for cell in self.pyr.cell: 
              self.vlfp.add(cell.Adend3_volt)
              self.vlfp.sub(cell.Bdend_volt)
          self.vlfp.div(len(self.pyr.cell)) # normalize lfp by amount of pyr cells
          self.lfp=numpy.array(self.vlfp.to_python()) # convert to python array (so can do PSD)

    def getlfp (self,skipms=200,subm=True):
        v1=h.Vector()
        nsamp = skipms / h.dt # number of samples to skip from start,end
        self.calc_lfp()
        v1.copy(self.vlfp,nsamp,self.vlfp.size()-1-nsamp)
        if subm: v1.sub(v1.mean())  
        return v1

    def calc_specgram(self,maxfreq,nsamp,dodraw,skipms=0):
        """calculate spectrogram"""
        self.calc_lfp()
        if skipms > 0:
            vtmp = h.Vector()
            vtmp.copy(self.vlfp,skipms/h.dt,self.vlfp.size()-1)
            self.MSpec = MSpec(vtmp,maxfreq,nsamp,dodraw)
        else:
            self.MSpec = MSpec(self.vlfp,maxfreq,nsamp,dodraw)
        
    def calc_psd(self,fig=3):
        self.calc_lfp()
        t0   = 200 # reject first ms of the signal
        fmax = 200 # upper limit for a periodogram frequency
        div  = int(1000/h.dt/(2*fmax)) # downsample the signal
        tr = [3,  12] # Theta frequency range
        gr = [30, 80] # Gamma frequency range
        t0i = int(t0/h.dt)
        if t0i > len(self.lfp):
            print ("LFP is too short! (<200 ms)")
            return 0,0,0,0,0,0
        
        pylab.figure(fig)
        pylab.clf()
        
        pylab.subplot(2,1,1) # plot LFP
        pylab.plot(numpy.array(range(len(self.lfp)))*h.dt, self.lfp)
        
        pylab.subplot(2,1,2) # plot periodogram
        data = self.lfp[t0i::div] # downsample data
        Pxx, freqs = pylab.psd(data-data.mean(), Fs=1000/h.dt/div) # calculate FFT
        tind = numpy.where((freqs>=tr[0]) & (freqs<=tr[1]))[0] # index where for theta frequences  
        gind = numpy.where((freqs>=gr[0]) & (freqs<=gr[1]))[0] # index where for gamma frequences
        self.tp = Pxx[tind].mean() * numpy.diff(tr) # integral over theta power
        self.gp = Pxx[gind].mean() * numpy.diff(gr) # integral over gamma power
        self.ti = self.get_lim_max(Pxx, tind) # index of the frequency with a maximal power in theta range  
        self.gi = self.get_lim_max(Pxx, gind) # index of the frequency with a maximal power in gamma range
        self.tf = freqs[self.ti]
        self.gf = freqs[self.gi]
        pylab.scatter(self.tf, 10*numpy.log10(Pxx[self.ti]), 100, 'b','o')
        pylab.scatter(self.gf, 10*numpy.log10(Pxx[self.gi]), 100, 'r','o')
        pylab.xlim(0,fmax)


    def make_signal(self, simdur, signal_isi):
        '''will set signal that is being delievered to the Adend2AMPAf dendrites. The function is
        called from run.py after the call for the netstims and netcons generating driving input is
        called. This way the netstim (ns) and netcons (nc) are added to the end of nsl and ncl.
        Implementation is similar to implementing drives. All pyramidal cells will recieve the same
        signal input.'''
        print ('Making signal NetStim and NetCons')
        ns = h.NetStim()
        ns.interval = signal_isi
        ns.noise = 0.5
        ns.number = (1e3 / ns.interval) * simdur
        ns.start = 0
        rd_signal = h.Random()
        sead = self.nrlsead[-1] + 1
        rd_signal.MCellRan4(sead,sead) # we are using sead as seed - we are NOT using signal_rseed
        ns.noiseFromRandom(rd_signal)
        self.nsl.append(ns) # this is the last one appended so to access this one, we can use nsl[-1]
        self.nrl.append(rd_signal)
        self.nrlsead.append(sead)
        for cel in self.pyr.cell: # signal to all pyramidal cells
            nc = h.NetCon(ns, cel.__dict__['Adend2AMPA'].syn)
            nc.delay = h.dt * 2
            nc.weight[0] = 100 * 0.05e-3 # 0.05e-3 # same as the ones from self.make_NetStims for Adend3AMPAf
            self.ncl.append(nc) # these are the last ones appened, so to access them, they will be the last 800 NetCons
        print ('Done!')
                
    def recordSignal_spikes(self):
        '''will record the spike train coming from the signal netstim. Keep in mind that the delay imposed by the signal NetCon is not taken into account.'''
        self.signalVec = h.Vector()
# since all netcons will receive the same input, will record from the last one in self.ncl
        self.ncl[-1].record(self.signalVec)

    def get_lim_max(self, data, ind):   # return the position of the maximal element in data located in the postion indexed by ind
        return  ind[data[ind].argmax()]



#          make the Network - uses params in netcfg.cfg if the file exists -- makes it easier to run a batch
net = Network(noise=noise,connections=connections,DoMakeNoise=DoMakeNoise,iseed=ISEED,UseNetStim=UseNetStim,signal_rseed = SIGNAL_RSEED, signal_isi = signal_isi, DoMakeSignal=DoMakeSignal,wseed=WSEED, scale=scale, MSGain_olm=MedialSeptum_gain_olm, MSGain_pv=MedialSeptum_gain_pv, MSGain_cck=MedialSeptum_gain_cck, SaveConn = SaveConn, UseSTDP=STDP) 

# scaling of NMDAR current
net.olm.set_r("somaNMDA", olm_NMDARw_scaling)
net.bas.set_r("somaNMDA", pv_NMDARw_scaling)
net.pyr.set_r("BdendNMDA", pyr_NMDARw_scaling)
net.pyr.set_r("Adend2NMDA", pyr_NMDARw_scaling)
net.pyr.set_r("Adend3NMDA", pyr_NMDARw_scaling)
if includeCCKcs:
    net.cck_somaPyr.set_r("somaNMDA", cck_Soma_NMDARw_scaling)
    net.cck_Adend2Pyr.set_r("somaNMDA", cck_Adend2_NMDARw_scaling)
    if cck_Adend3Pop_cNum > 0:
        net.cck_Adend3.set_r("somaNMDA", cck_Adend3_NMDARw_scaling)



#setup some variables in hoc
def sethocix():
    h("PYRt=0")
    h("BASKETt=1")
    h("OLMt=2")
    h("PSRt=3")
    h("CTYP.o(PYRt).s=\"PYRt\"")
    h("CTYP.o(BASKETt).s=\"BASKETt\"")
    h("CTYP.o(OLMt).s=\"OLMt\"")
    h("CTYP.o(PSRt).s=\"PSRt\"")
    h("ix[PYRt]=0")
    h("ixe[PYRt]=799")
    h("ix[BASKETt]=800")
    h("ixe[BASKETt]=999")
    h("ix[OLMt]=1000")
    h("ixe[OLMt]=1199")
    h("ix[PSRt]=1200")
    h("ixe[PSRt]=1200")
    h("numc[PYRt]=800")
    h("numc[BASKETt]=200")
    h("numc[OLMt]=200")
    h("numc[PSRt]=1")

sethocix()
