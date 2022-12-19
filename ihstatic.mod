: $Id: ihstatic.mod,v 1.1 2012/12/28 17:44:27 samn Exp $ 
TITLE passive membrane channel - calling ihstatic

UNITS {
  (mV) = (millivolt)
  (mA) = (milliamp)
  (S) = (siemens)
}

NEURON {
  SUFFIX ihstatic
  NONSPECIFIC_CURRENT i
  RANGE g, e, nv, gfactor
}

PARAMETER {
  g = .001	(S/cm2)	<0,1e9>
  e = -30	(mV)
  gfactor = 1
}

ASSIGNED {
  v  (mV)  
  nv (mV)  
  i (mA/cm2)
}

BREAKPOINT {
  i = gfactor * g * (v - e)
  nv=-v
}
