'''
Author: satyapan
Purpose: This code generates a single binned lightcurve from the pv extensions of all SSM event files placed in the same folder.
Inputs: inttime: binning time in seconds
Outputs: .txt file containing binned lightcurve, .txt file containing number of binned data points for each event file.
'''


from numpy import *
from pylab import *
from astropy.io import fits
from glob import glob
import os

filenames = sorted(glob("*.fits"))

inttime = int(input("Enter binning time: "))

outfile = open("lcurve_binned_" + str(inttime) + "s.txt", "w")

output_MJD = []
output_events = []
sizes = open("sizes_"+str(inttime)+"s.txt", "w")

for filename in filenames:
	hdulist = fits.open(filename)
	outfile = open("hdulist.txt", 'w')
	hdulist.info(output=outfile)
	with open("hdulist.txt") as infile:
		lines = infile.read().splitlines()
	
	selectlist = []
	for i in lines:
		if i[11:13] == "pv":
			selectlist.append(int(i[1:3]))

	JD = []
	for hduno in selectlist:
		temp = array(hdulist[hduno].data.field("SSM_PL_EVTTIME_MJD"))
		for m in temp:
			JD.append(m)

	JD = sort(JD)
	events = ones((len(JD)))
	JD_temp = (JD - JD[0])*86400
	length = int(JD_temp[len(JD_temp)-1])
	JD_binned = linspace(0,length,(length+1)//inttime)
	JD_bin = []
	events_bin = []
	for i in range(len(JD_binned)-1):
		temp = 0
		tempx = 0
		for j in range(len(JD_temp)):
			if JD_binned[i] <= JD_temp[j] <= JD_binned[i+1]:
				temp = JD_binned[i]
				tempx += events[j]
			else:
				pass
		if temp == 0:
			JD_bin.append(JD_binned[i])
			events_bin.append(0)
		else:
			JD_bin.append(temp)
			events_bin.append(tempx)
		prog = (float(i)/float(len(JD_binned)-1))*100
		sys.stdout.write("\r" + "#"*int(prog/2) + repr(prog)[0:4] + "%")
		sys.stdout.flush()
	sys.stdout.write("\n")
	MJD = (array(JD_bin)/86400)+JD[0]
	sizes.write(str(len(MJD))+"\n")
	with open("lcurve_binned_" + str(inttime) + "s.txt", 'a') as f:
    		for k in range(len(MJD)):
        		print >> f, str(MJD[k])+" "+str(events_bin[k])



