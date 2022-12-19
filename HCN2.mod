: $Id: HCN2.mod,v 1.4 2013/01/02 15:02:32 samn Exp $ 

TITLE HCN2

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}
 
NEURON {
  SUFFIX HCN2
  NONSPECIFIC_CURRENT ih
  RANGE gbar, g, e, v50, htau, hinf
  RANGE gfactor, htaufactor
}
 
PARAMETER {
  celsius	(degC)
  gbar= 0.0001	(mho/cm2)
  e= -30	(mV)
  v50=-92	(mV)
  gfactor = 1
  htaufactor = 1.9
}
 
STATE {
  h
}
 
ASSIGNED {
  ih	  (mA/cm2) 
  hinf
  htau    (ms)
  v	  (mV)
  g       (mho/cm2)
}

PROCEDURE giassign () {
  :ih=g*h*(v-e)*gfactor 
  g = gbar*h*gfactor
  ih = g*(v-e)
}
 
BREAKPOINT {
  SOLVE states METHOD cnexp
  giassign()
}
 
DERIVATIVE states { 
  rates(v)
  h'= (hinf- h)/ htau
}

INITIAL { 
  rates(v)
  h = hinf
  giassign()
}

PROCEDURE rates(v (mV)) {
  UNITSOFF
  : HCN2
  hinf = 1/(1+exp((v-v50)/10.5))
  htau = htaufactor/(exp(-14.59-0.086*v)+exp(-1.87+0.0701*v))
  UNITSON
}

