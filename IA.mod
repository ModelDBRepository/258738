COMMENT
IA channel

Reference:

1.	Zhang, L. and McBain, J. Voltage-gated potassium currents in
	stratum oriens-alveus inhibitory neurons of the rat CA1
	hippocampus, J. Physiol. 488.3:647-660, 1995.

		Activation V1/2 = -14 mV
		slope = 16.6
		activation t = 5 ms
		Inactivation V1/2 = -71 mV
		slope = 7.3
		inactivation t = 15 ms
		recovery from inactivation = 142 ms

2.	Martina, M. et al. Functional and Molecular Differences between
	Voltage-gated K+ channels of fast-spiking interneurons and pyramidal
	neurons of rat hippocampus, J. Neurosci. 18(20):8111-8125, 1998.	
	(only the gkAbar is from this paper)

		gkabar = 0.0175 mho/cm2
		Activation V1/2 = -6.2 +/- 3.3 mV
		slope = 23.0 +/- 0.7 mV
		Inactivation V1/2 = -75.5 +/- 2.5 mV
		slope = 8.5 +/- 0.8 mV
		recovery from inactivation t = 165 +/- 49 ms  

3.	Warman, E.N. et al.  Reconstruction of Hippocampal CA1 pyramidal
	cell electrophysiology by computer simulation, J. Neurophysiol.
	71(6):2033-2045, 1994.

		gkabar = 0.01 mho/cm2
		(number taken from the work by Numann et al. in guinea pig
		CA1 neurons)

File was downloaded from modeldb accession number: 123815
File was modified so that rates() gets called everytime breakpoint is called - table is not used
File was modified to allow for simulations to run at different temperatures other than those used to obtain data (Q10 and qTEMP were implemented to tau_a and tau_b) by Mohamed Sherif, MD, March 16, 2015
Q10 = 3
Q10TEMP = 24 (degC)

ENDCOMMENT

UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
}
 
NEURON {
        SUFFIX IA
        USEION k READ ek WRITE ik
        RANGE gkAbar,ik, tau_a, tau_b, tau_b_tempInsensitive
        RANGE ainf, binf, aexp, bexp
        GLOBAL qt
}
 
PARAMETER {
        v (mV)
        dt (ms)
        gkAbar = 0.0165 (mho/cm2)	:from Martina et al.
        ek = -90 (mV)
	tau_a_tempInsensitive = 5 (ms)
        Q10 = 3
        Q10TEMP = 24 (degC)
}
 
STATE {
        a b
}
 
ASSIGNED {
        ik (mA/cm2)
	ainf binf aexp bexp
	tau_b tau_a
        tau_b_tempInsensitive
        celsius (degC)
        qt (1)
}
 
BREAKPOINT {
        SOLVE deriv METHOD cnexp
        ik = gkAbar*a*b*(v - ek)
}
 
INITIAL {
        qt = Q10 ^ ((celsius - Q10TEMP) / 10)
        rates(v)
	a = ainf
	b = binf
}

DERIVATIVE deriv {  :Computes state variables m, h, and n rates(v)      
		: at the current v and dt.
        rates(v)
        a' = (ainf - a)/(tau_a)
        b' = (binf - b)/(tau_b)
}
 
PROCEDURE rates(v) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.
        LOCAL alpha_b, beta_b
	alpha_b = 0.000009/exp((v-26)/18.5)
	beta_b = 0.014/(exp((v +70)/(-11))+0.2)
        ainf = 1/(1 + exp(-(v + 14)/16.6))
        tau_a = tau_a_tempInsensitive / qt
        aexp = 1 - exp(-dt/(tau_a))
        tau_b_tempInsensitive = 1/(alpha_b + beta_b)
	tau_b = tau_b_tempInsensitive / qt
        binf = 1/(1 + exp((v + 71)/7.3))
        bexp = 1 - exp(-dt/(tau_b))
}
 
UNITSON
