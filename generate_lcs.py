import os
import numpy as np
import batman

P, a, inc, ecc, omega = 34.75, 16.49, 88.39, 0., 90.
times = np.linspace(0.,27,19440)
def transit_model(times, rp):
    params = batman.TransitParams()
    params.t0 = 13.5 # time of inferior conjunction
    params.per = P # orbital period (days)
    params.a = a # semi-major axis (in units of stellar radii)
    params.rp = rp # planet/star radius ratio
    params.inc = inc # orbital inclination (in degrees)
    params.ecc = ecc # eccentricity
    params.w = omega # longitude of periastron (in degrees) p
    params.limb_dark = 'quadratic' # limb darkening profile to use
    coeff1,coeff2 = 0.42767669222857835, 0.32963466956391446
    params.u = [coeff1, coeff2] # limb darkening coefficients

    tmodel = batman.TransitModel(params, times.astype('float64'))
    return tmodel.light_curve(params)

def save_data(folder,fname,index,t,f,precision):
    fout = open(folder+'/'+fname+'_'+str(index)+'.dat','w')
    for i in range(len(t)):
        fout.write('{0:.10f} {1:.10f} {2:.10f} TESS\n'.format(t[i],f[i],precision*1e-6))

# Number of simulations per bin:
nsim = 5
# Precisions:
sigmas = np.logspace(np.log10(300),np.log10(1000),5)
# Depths:
depths = np.logspace(np.log10(100),np.log10(1000),5)
# Cuts
ndata_cuts = np.linspace(1,10,5).astype('int')

# Generate datasets:
for sigma in sigmas:
    for depth in depths:
        for ndata_cut in ndata_cuts:
            folder_name = 'sim_'+str(ndata_cut)+'_'+str(int(sigma))+'_'+str(int(depth))
            os.mkdir(folder_name)
            for i in range(nsim):
                new_times = np.copy(times)
                if ndata_cut == 1:
                    model = transit_model(times,np.sqrt(depth*1e-6))
                else:
                    ndata = len(times)/np.double(ndata_cut)
                    left_ndata = int(19440./2.) - int(ndata/2.)
                    right_ndata = int(19440./2.) + int(ndata/2.)
                    new_times = np.copy(times[left_ndata:right_ndata])
                    model = transit_model(new_times,np.sqrt(depth*1e-6))
                noise = np.random.normal(0.,sigma*1e-6,len(new_times))
                data = model + noise
                save_data(folder_name,'real_model',i,new_times,model,sigma)
                save_data(folder_name,'noisy_model',i,new_times,data,sigma)
