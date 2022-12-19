'''this file contains conig parameters for the model'''
import configparser
import io
import numpy as np

# default config as string
def_config = """
[seed]
#iseed = [1234, 6912, 9876, 6789,3219]
#wseed = [4321, 5012, 9281, 8130,6143]
iseed = 1234
wseed = 4321
pseed = 4321
signal_rseed = 7483
[chan]
# ampatau1 =
# amptau2 =
# nmdatau1 =
# nmdatau2 =
[run]
# tstop = 20000
tstop = 3000
dt = 0.1
saveout = 0
simstr = 134mar10_mpi_rxd_test_
statestr = 14mar8_600s_700s_700s_continue_700s_A
dorun = 0
verbose = 0
saveSomaVolt = 0
getOnlyInterneuronsSomaVolt = 0
strCellsRecordVoltage = 0 800 1000
cvodeactive=0
recdt = 10 
recvdt = 1
binsz = 5
savestate = 0
restorestate = 0
loadtstop = 0
saveconn = 0
recordNetStimInputs = 0
saveNetStimInputs = 0
recPyrInputSpikes = 0
savePyrInputSpikes = 0
recSignalSpikes = 0
saveSignalSpikes = 0
[rxd]
useRXD = 0
caDiffCoeff = 0
PV_frate = 5.0
PV_init = 0.2
useIP3 = 1
gip3 = 120400.0
gserca = 4.0
gleak = 3.0
cacytinit = 100e-6
caerinit = 100e-6
[net]
connections = 1
scale=0
includeCCKcs = 0
hCurrent_g_pv_scaling = 1.0
hCurrent_g_olm_scaling = 1.0
hCurrent_g_pyr_scaling = 1.0
hCurrent_g_cck_scaling = 1.0
CB1R_cck_somaPyr_weight = 1.0
CB1R_cck_Adend2Pyr_weight = 1.0
CB1R_pyr_recurrent_weight = 1.0
CB1R_pyr_pv_weight = 1.0
CB1R_MS_weight = 1.0
CB1R_cck_Adend3_weight = 1.0
CB1R_pyr_olm_weight = 1.0
olm_NMDARw_scaling = 1.0
pv_NMDARw_scaling = 1.0
pyr_NMDARw_scaling = 1.0
cck_Soma_NMDARw_scaling = 1.0
cck_Adend2_NMDARw_scaling = 1.0
cck_Adend3_NMDARw_scaling = 1.0
olm_AMPARw_scaling = 1.0
# wirety = swire
# wirety = convwire
pyrPop_cNum = 800
basPop_cNum = 200
olmPop_cNum = 200
cck_somaPyrPop_cNum = 100
cck_Adend2PyrPop_cNum = 100
cck_Adend3Pop_cNum = 0
pyr_pyr_location = mid-apical
olm_pyr_location = distal-apical
pyr_bas_conv = 100
pyr_olm_conv = 10
pyr_cck_somaPyr_conv = 100
pyr_cck_Adend2Pyr_conv = 20
pyr_pyr_conv = 25
bas_bas_conv = 60
bas_pyr_conv = 50
cck_somaPyr_pyr_conv = 50
cck_Adend2Pyr_pyr_conv = 50
cck_somaPyr_bas_conv = 40
bas_cck_somaPyr_conv = 20 
cck_somaPyr_cck_somaPyr_conv = 30
bas_olm_conv = 1
olm_pyr_conv = 20
pyr_cck_Adend3_conv = 10
cck_Adend3_pyr_conv = 20
nmfracca = 0
extrinsic_pyr_AMPAfR_weight_scale = 1
intrinsic_pyr_AMPAfR_weight_scale = 1
extrinsic_pyr_GABAfR_weight_scale = 1
intrinsic_pyr_GABAfR_weight_scale = 1
extrinsic_pv_AMPAfR_weight_scale = 1
intrinsic_pv_AMPAfR_weight_scale = 1
extrinsic_pv_GABAfR_weight_scale = 1
intrinsic_pv_GABAfR_weight_scale = 1
extrinsic_olm_AMPAfR_weight_scale = 1
intrinsic_olm_AMPAfR_weight_scale = 1
extrinsic_olm_GABAfR_weight_scale = 1
intrinsic_olm_GABAfR_weight_scale = 1
extrinsic_cck_AMPAfR_weight_scale = 1
intrinsic_cck_AMPAfR_weight_scale = 1
extrinsic_cck_GABAfR_weight_scale = 1
intrinsic_cck_GABAfR_weight_scale = 1
tau2_bas_pyr_GA_scale = 1
[stim]
noise = 1
DoMakeNoise = 1
UseNetStim = 1
useGfluct = 0
DoMakeSignal = 0
PyrGABAw = 0
PyrGABAISI = 1
PyrAMPAw = 0.05e-3
PyrAMPAISI = 4
PyrNMDAw = 6.5e-3
PyrNMDAISI = 100
BasAMPAw = 0
BasAMPAISI = 1
BasGABAw = 0
BasGABAISI = 1
#sgrhzEE = 1000
sgrhzEE = 1000
#sgrhzEI = 500
sgrhzEI = 0
#sgrhzIE = 1000
#sgrhzIE = 500
sgrhzIE = 250
#sgrhzII = 500
sgrhzII = 0
#sgrhzENM = 10
sgrhzENM = 0
#sgrhzINM = 10
sgrhzINM = 0
#sgrhzINM = 30
#E4RexGain = 2.0
#E4RexGain = 1.0
E4RexGain = 0.5
#sgrhzLTSSlowSlowGaba = 20
sgrhzLTSSlowSlowGaba = 0
EXGain = 10.0
#EXGain = 5.0
MedialSeptum_gain_olm = 1.0
MedialSeptum_gain_pv = 1.0
MedialSeptum_gain_cck = 1.0
signal_isi = 200
[iclamp]
pyr = 0.0
bas = 0.0
olm = 0.0
cck = 0.0
[netsyn]
STDP = 0
GABAontoCCK_scale = 3
"""

def writeconf (fn,sec,opt,val):
  '''write config file starting with defaults andnew entries
  specified in section (sec) , option (opt), and value (val) 
  saves to output filepath fn'''

  conf = configparser.ConfigParser()
  # conf.readfp(io.BytesIO(def_config)) # start with defaults - ERROR FROM THIS LINE in python3 - FIXED
  conf.read_string(def_config)
  # then change entries by user-specs
  for i in range(len(sec)):
      # conf.set(sec[i],opt[i],val[i]) # error here related to val having to be a string
      conf[sec[i]][opt[i]] = str(val[i])
  # write config file
  with open(fn, 'w') as cfile: conf.write(cfile) # not writing as binary

# read config file
def readconf (fn="netcfg.cfg"):

  config = configparser.ConfigParser()
  config.read(fn)

  def conffloat (base,var,defa): # defa is default value
    val = defa
    try: val=config.getfloat(base,var)
    except: pass
    return val

  def confint (base,var,defa):
    val = defa
    try: val=config.getint(base,var)
    except: pass
    return val

  def confstr (base,var,defa):
    val = defa
    try: val = config.get(base,var)
    except: pass
    return val

  def confarr(base,var,defa):
    val = defa
    try: val = config.get(base,var)
    except: pass
    val = val.strip('[]')
    val = np.fromstring(val, dtype = int, sep = ' ')
    return val

  d = {}
  d['iseed'] = confint('seed','iseed',1234)
  d['wseed'] = confint('seed','wseed',4321)
  d['pseed'] = confint('seed','pseed',4321)
  d['signal_rseed'] = confint('seed','signal_rseed',7483)
  d['tstop'] = conffloat("run","tstop", 3000)
  d['dt'] = conffloat("run","dt",0.1)
  d['saveout'] = conffloat("run","saveout",1)
  d['simstr'] = confstr("run","simstr","2021feb17_test_")
  d['statestr'] = confstr("run","statestr","14mar6_reload_700s_continue_600s_A")
  d['dorun'] = confint("run","dorun",1)
  d['verbose'] = confint("run","verbose",0)
  d['saveSomaVolt'] = confint("run","saveSomaVolt",0)
  d['getOnlyInterneuronsSomaVolt'] = confint("run","getOnlyInterneuronsSomaVolt",0)
  d['strCellsRecordVoltage'] = confarr("run","strCellsRecordVoltage", '0 800 1000')
  d['cvodeactive'] = confint("run","cvodeactive",0)
  d['recdt'] = conffloat("run","recdt",10.0)
  d['recvdt'] = conffloat("run","recvdt",1.0)
  d['binsz'] = conffloat("run","binsz",5)
  d['savestate'] = confint("run","savestate",0)
  d['restorestate'] = confint("run","restorestate",0)
  d['loadtstop'] = conffloat("run","loadtstop",0)
  d['saveconn'] = confint('run','saveconn',0)
  d['recordNetStimInputs'] = confint('run','recordNetStimInputs',0)
  d['saveNetStimInputs'] = confint('run','saveNetStimInputs',0)
  d['recPyrInputSpikes'] = confint('run','recPyrInputSpikes',0)
  d['savePyrInputSpikes'] = confint('run','savePyrInputSpikes',0)
  d['recSignalSpikes'] = confint('run','recSignalSpikes',0)
  d['saveSignalSpikes'] = confint('run','saveSignalSpikes',0)
  d['useRXD'] = confint("rxd","useRXD",1)
  d['caDiffCoeff'] = conffloat('rxd','caDiffCoeff',0)
  d['PV_frate'] = conffloat("rxd","PV_frate", 5.0)
  d['PV_init'] = conffloat("rxd","PV_init", 0.2)
  d['useIP3'] = confint("rxd","useIP3",1)
  d['gip3'] = conffloat("rxd","gip3",120400.0)
  d['gserca'] = conffloat("rxd","gserca",4.0)
  d['gleak'] = conffloat("rxd","gleak",3.0)
  d['cacytinit'] = conffloat("rxd","cacytinit",100e-6)
  d['caerinit'] = conffloat("rxd","caerinit",100e-6)
  d['connections'] = confint('net','connections',1)
  d['scale'] = conffloat("net","scale",1.0)
  d['includeCCKcs'] = confint('net','includeCCKcs',0)
  d['hCurrent_g_pv_scaling'] = conffloat('net','hCurrent_g_pv_scaling',1.0)
  d['hCurrent_g_olm_scaling'] = conffloat('net','hCurrent_g_olm_scaling',1.0)
  d['hCurrent_g_pyr_scaling'] = conffloat('net','hCurrent_g_pyr_scaling',1.0)
  d['hCurrent_g_cck_scaling'] = conffloat('net','hCurrent_g_cck_scaling',1.0)
  d['CB1R_cck_weight'] = conffloat('net','CB1R_cck_weight',0.5)
  d['CB1R_cck_somaPyr_weight'] = conffloat('net','CB1R_cck_somaPyr_weight', 1.0)
  d['CB1R_cck_Adend2Pyr_weight'] = conffloat('net','CB1R_cck_Adend2Pyr_weight',1.0)
  d['CB1R_pyr_recurrent_weight'] = conffloat('net','CB1R_pyr_recurrent_weight',0.5)
  d['CB1R_pyr_pv_weight'] = conffloat('net','CB1R_pyr_pv_weight',1.0)
  d['CB1R_cck_Adend3_weight'] = conffloat('net','CB1R_cck_Adend3_weight',1.0)
  d['CB1R_pyr_olm_weight'] = conffloat('net','CB1R_pyr_olm_weight',1.0)
  d['CB1R_MS_weight'] = conffloat('net','CB1R_MS_weight',1.0)
  d['olm_NMDARw_scaling'] = conffloat('net','olm_NMDARw_scaling',1.0)
  d['pv_NMDARw_scaling'] = conffloat('net','pv_NMDARw_scaling',1.0)
  d['pyr_NMDARw_scaling'] = conffloat('net','pyr_NMDARw_scaling',1.0)
  d['cck_Soma_NMDARw_scaling'] = conffloat('net','cck_Soma_NMDARw_scaling',1.0)
  d['cck_Adend2_NMDARw_scaling'] = conffloat('net','cck_Adend2_NMDARw_scaling',1.0)
  d['cck_Adend3_NMDARw_scaling'] = conffloat('net','cck_Adend3_NMDARw_scaling',1.0)
  d['olm_AMPARw_scaling'] = conffloat('net','olm_AMPARw_scaling', 1.0)
  d['pyrPop_cNum'] = confint('net','pyrPop_cNum',800)
  d['basPop_cNum'] = confint('net','basPop_cNum',100)
  d['olmPop_cNum'] = confint('net','olmPop_cNum',200)
  d['cck_somaPyrPop_cNum'] = confint('net','cck_somaPyrPop_cNum',100)
  d['cck_Adend2PyrPop_cNum'] = confint('net','cck_Adend2PyrPop_cNum',100)
  d['cck_Adend3Pop_cNum'] = confint('net','cck_Adend3Pop_cNum',100)
  d['pyr_pyr_location'] = confstr('net','pyr_pyr_location','mid-apical')
  d['olm_pyr_location'] = confstr('net','olm_pyr_location','distal-apical')
  d['pyr_bas_conv'] = confint('net','pyr_bas_conv',50)
  d['pyr_cck_somaPyr_conv'] = confint('net','pyr_cck_somaPyr_conv',50)
  d['pyr_cck_Adend2Pyr_conv'] = confint('net','pyr_cck_Adend2Pyr_conv',10)
  d['pyr_cck_conv'] = confint('net','pyr_cck_conv',50)
  d['pyr_olm_conv'] = confint('net','pyr_olm_conv',10)
  d['pyr_pyr_conv'] = confint('net','pyr_pyr_conv',25)
  d['bas_bas_conv'] = confint('net','bas_bas_conv',15)
  d['bas_pyr_conv'] = confint('net','bas_pyr_conv',25)
  d['cck_somaPyr_pyr_conv'] = confint('net','cck_somaPyr_pyr_conv',25)
  d['cck_Adend2Pyr_pyr_conv'] = confint('net','cck_Adend2Pyr_pyr_conv',10)
  d['cck_somaPyr_bas_conv'] = confint('net','cck_somaPyr_bas_conv',20)
  d['bas_cck_somaPyr_conv'] = confint('net','bas_cck_somaPyr_conv',10)
  d['cck_somaPyr_cck_somaPyr_conv'] = confint('net','cck_somaPyr_cck_somaPyr_conv',2)
  d['bas_olm_conv'] = confint('net','bas_olm_conv',1)
  d['olm_pyr_conv'] = confint('net','olm_pyr_conv',20)
  d['pyr_cck_Adend3_conv'] = confint('net','pyr_cck_Adend3_conv',10)
  d['cck_Adend3_pyr_conv'] = confint('net','cck_Adend3_pyr_conv',10)
  d['nmfracca'] = conffloat('net','nmfracca',0)
  d['extrinsic_pyr_AMPAfR_weight_scale'] = conffloat('net','extrinsic_pyr_AMPAfR_weight_scale',1)
  d['intrinsic_pyr_AMPAfR_weight_scale'] = conffloat('net','intrinsic_pyr_AMPAfR_weight_scale',1)
  d['extrinsic_pyr_GABAfR_weight_scale'] = conffloat('net','extrinsic_pyr_GABAfR_weight_scale',1)
  d['intrinsic_pyr_GABAfR_weight_scale']= conffloat('net','intrinsic_pyr_GABAfR_weight_scale',1)
  d['extrinsic_pv_AMPAfR_weight_scale']= conffloat('net','extrinsic_pv_AMPAfR_weight_scale',1)
  d['intrinsic_pv_AMPAfR_weight_scale']= conffloat('net','intrinsic_pv_AMPAfR_weight_scale',1)
  d['extrinsic_pv_GABAfR_weight_scale'] = conffloat('net','extrinsic_pv_GABAfR_weight_scale',1)
  d['intrinsic_pv_GABAfR_weight_scale']= conffloat('net','intrinsic_pv_GABAfR_weight_scale',1)
  d['extrinsic_olm_AMPAfR_weight_scale']= conffloat('net','extrinsic_olm_AMPAfR_weight_scale',1)
  d['intrinsic_olm_AMPAfR_weight_scale']= conffloat('net','intrinsic_olm_AMPAfR_weight_scale',1)
  d['extrinsic_olm_GABAfR_weight_scale'] = conffloat('net','extrinsic_olm_GABAfR_weight_scale',1)
  d['intrinsic_olm_GABAfR_weight_scale']= conffloat('net','intrinsic_olm_GABAfR_weight_scale',1)
  d['extrinsic_cck_AMPAfR_weight_scale'] = conffloat('net','extrinsic_cck_AMPAfR_weight_scale',1)
  d['intrinsic_cck_AMPAfR_weight_scale'] = conffloat('net','intrinsic_cck_AMPAfR_weight_scale',1)
  d['extrinsic_cck_GABAfR_weight_scale'] = conffloat('net','extrinsic_cck_GABAfR_weight_scale',1)
  d['intrinsic_cck_GABAfR_weight_scale'] = conffloat('net','intrinsic_cck_GABAfR_weight_scale',1)
  d['tau2_bas_pyr_GA_scale'] = conffloat('net','tau2_bas_pyr_GA_scale',1)
  d['noise'] = conffloat("stim","noise",1.0)
  d['DoMakeNoise'] = confint('stim','DoMakeNoise',1)
  d['UseNetStim'] = confint('stim','UseNetStim',1)
  d['useGfluct'] = confint('stim','useGfluct',0)
  d['DoMakeSignal'] = confint('stim','DoMakeSignal',0)
  d['PyrGABAw'] = confint('stim','PyrGABAw',0)
  d['PyrGABAISI'] = confint('stim','PyrGABAISI',1)
  d['PyrAMPAw'] = confint('stim','PyrAMPAw',0.05e-3)
  d['PyrAMPAISI'] = confint('stim','PyrAMPAISI',4)
  d['PyrNMDAw'] = confint('stim','PyrNMDAw',6.5e-3)
  d['PyrNMDAISI'] = confint('stim','PyrNMDAISI',100)
  d['BasAMPAw'] = confint('stim','BasAMPAw',0)
  d['BasAMPAISI'] = confint('stim','BasAMPAISI',1)
  d['BasGABAw'] = confint('stim','BasGABAw',0)
  d['BasGABAISI'] = confint('stim','BasGABAISI',1)
  d['MedialSeptum_gain_olm'] = conffloat('stim','MedialSeptum_gain_olm',1)
  d['MedialSeptum_gain_pv'] = conffloat('stim','MedialSeptum_gain_pv',1)
  d['MedialSeptum_gain_cck'] = conffloat('stim','MedialSeptum_gain_cck',1)
  d['signal_isi'] = conffloat('stim','signal_isi',200)
  d['pyr'] = conffloat('iclamp','pyr',0.0)
  d['bas'] = conffloat('iclamp','bas',0.0)
  d['olm'] = conffloat('iclamp','olm',0.0)
  d['cck'] = conffloat('iclamp','cck',0.0)
  d['STDP'] = confint('netsyn','STDP',0)
  d['GABAontoCCK_scale'] = conffloat('netsyn','GABAontoCCK_scale',3)
  if config.has_option("net","wnq"): d['wnq'] = config.get("net","wnq")

  return d

def compareConfigParsers(parser1, parser2):
    '''will compare the parser1 and parser2 and return a dictionary of the differences if there are any. If the parsers do not contain the same sections or the same options, no dictionary is returned'''
    resultsDic = {'same':[], 'different':{}}
    if parser1.sections() == parser2.sections():
        print ('\nParsers have same sections, proceeding to examine options')
        for mysection in parser1.sections():
            if parser1.options(mysection) == parser2.options(mysection):
                for myoption in parser1.options(mysection):
                    myval1 = parser1.get(mysection, myoption)
                    myval2 = parser2.get(mysection, myoption)
                    if myval1 == myval2:
                        resultsDic['same'].append(myoption)
                    else:
                        resultsDic['different'][myoption] = {'first':myval1, 'second':myval2}
            else:
                print ('Sections of parsers do not have the same options. Will not run further analysis')
                return
    else:
        print ('Parsers do not have the same sections. Will not run further analysis')
        return
    if len(resultsDic['different']) == 0:
        print ("Parsers are the same")
    else:
        print ('There are differences between the parsers. Please check the returned dictionary')
    return resultsDic

