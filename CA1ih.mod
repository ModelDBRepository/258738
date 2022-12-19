: $Id: CA1ih.mod,v 1.6 2013/01/02 14:28:37 samn Exp $ 
TITLE Ih CA3

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}
 
NEURON {
  SUFFIX hcurrent
  NONSPECIFIC_CURRENT ih
  RANGE gbar, g, e, v50, htau, hinf
  RANGE gfactor, htaufactor
}
 
PARAMETER {
  celsius	(degC)
  gbar= 0.0001	(mho/cm2)
  e= -30	(mV)
  v50=-82	(mV)
  gfactor = 1
  htaufactor = 1
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
  : ih=g*h*(v-e)*gfactor
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
  : HCN1
  :hinf = 1/(1+exp(0.151*(v-v50)))
  :htau = exp((0.033*(v+75)))/(0.011*(1+exp(0.083*(v+75))))

  : HCN2
  hinf = 1/(1+exp((v-v50)/10.5))
  htau = htaufactor/(exp(-14.59-0.086*v)+exp(-1.87+0.0701*v))
  UNITSON
}

