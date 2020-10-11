import juliet
import numpy as np
import glob

folders = glob.glob('sim_*')
for folder in folders:
    files = glob.glob(folder+'/noisy_model*')
    for lcfile in files:
        print(lcfile)
        f = lcfile.split('/')[-1].split('.dat')[0]
        dataset = juliet.load(priors='priors_no_transit.dat', lcfilename=lcfile, out_folder = folder+'/'+f+'_results-no-transit', verbose = True)
        results = dataset.fit(use_dynesty=True, dynamic = True, dynesty_nthreads = 6, n_live_points = 1000)
