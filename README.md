# Hippocampal CA3 model (Sherif et al, 2020)

This is the code for the CA3 hippocampal model in the paper by [Sherif et al](https://www.nature.com/articles/s41537-020-00109-0), 2020, in npj Schizophrenia.

The code has been updated to use Python3. In addition to [NEURON](https://neuron.yale.edu/neuron/), the following python packages are needed:
    
    hyp5
    configparser

(You can use conda or pip to install them).

After you install the required packages, compile the mod files:

    nrnivmodl

To plot a figure similar to figure 1 in the paper with the control conditions, you will need first to run a control simulation. The configuraiton file with the parameters for the model are in fig1simulationConfig.cfg file.
The following code will run a simulation that is 3 seconds long (it takes around one minute to run on my machine with 8 cores), and save the resulting output file in directory ./data/batch.

After the file has been generated (or if you want to plot the provided output sample file), you can run the following code:

    python -i analysisPlottingCode.py
    
Then inside python:

    simstr = 'controlSimulation' # name of simulation that just ran - set in the configuration file.

    loadedSim = loadSimH5py(simstr, datadir = './data/batch/')
    myfig, rastsp, lfpsp, psdsp = plotloadedsimProfiling(loadedSim, 0)
    rastsp.set_xlim(2000, 3000) # plot the last 1000 ms (1 second).

    # annotate y-axis of raster for the different neuronal populations
    rastsp.set_ylabel('')
    rastsp.set_yticklabels('')
    rastsp.annotate('PYR', xy=(-0.1, 0.33), xycoords='axes fraction', color = 'red', fontsize = 12, fontweight='bold')
    rastsp.annotate('PV', xy=(-0.1, 0.73), xycoords='axes fraction', color = 'green', fontsize = 12, fontweight='bold')
    rastsp.annotate('OLM', xy=(-0.1, 0.88), xycoords='axes fraction', color = 'blue', fontsize = 12, fontweight='bold')

    # change color of LFP voltage plot to black
    lfpline = lfpsp.get_lines()[0]
    lfpline.set_color('k')

    # change color of PSD plot to black
    psdline = psdsp.get_lines()[0]
    psdline.set_color('k')

You should get a figure similar to the one below:
![Alt text](fig1sample.png?raw=true "Optional Title")
