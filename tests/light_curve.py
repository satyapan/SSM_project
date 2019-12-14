from numpy import *
from pylab import *

file_maxi = input("Enter MAXI lightcurve file name: ")
file_ssm = input("Enter SSM lightcurve filename: ")

maxi_data = loadtxt(file_maxi, float)
ssm_data = loadtxt(file_ssm, float)

maxi_jd = maxi_data[:,0]
maxi_total = maxi_data[:,1]
maxi_total_err = maxi_data[:,2]

ssm_jd = ssm_data[:,0]
ssm_total = ssm_data[:,3]
ssm_total_err = ssm_data[:,4]

errorbar(maxi_jd, maxi_total, yerr=maxi_total_err, linestyle="none", marker=".", capsize=2, label="MAXI")
errorbar(ssm_jd, ssm_total, yerr=ssm_total_err, linestyle="none", marker=".",capsize=2, label="SSM")
xlabel("MJD")
ylabel("Flux (Photons/s/cm^2)")
legend()
show()
