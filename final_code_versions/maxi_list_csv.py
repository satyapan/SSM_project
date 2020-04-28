'''
Author: satyapan
Purpose: Detect MAXI outbursts from MAXI lightcurves in same folder.
Inputs: Threshold flux value for detection
Outputs: Plots of each lightcurve, Logfile containing detections.
'''

from numpy import *
from pylab import *
from glob import glob
import csv

flux_limit = float(input("Enter limit of flux (in photons/s/cm^2) above which we call it a detection: "))

files = sorted(glob("*.dat"))
logfile = open("logfile.csv", "w+")
logfile.close()
for filename in files:
	data = loadtxt(filename, float)
	jd_0 = data[:,0]
	flux_0 = data[:,3]+data[:,5]
	start = 0
	for k in range(len(jd_0)):
		if jd_0[k]>57296:
			start = k
			break
	jd = jd_0[k:]
	flux = flux_0[k:]
	outburst_0 = []
	for i in range(len(flux)):
		if flux[i] > flux_limit:
			outburst_0.append(int(1))
		else:
			outburst_0.append(int(0))
	outburst_0 = array(outburst_0)
	outburst_1 = []
	for j in range(len(outburst_0)-1):
		if outburst_0[j+1] > outburst_0[j]:
			outburst_1.append(jd[j+1])
		elif outburst_0[j+1] < outburst_0[j]:
			outburst_1.append(jd[j])
	outburst = []
	if outburst_0[0] == 0:
		for j in range(0,len(outburst_1)-1,2):
			outburst.append((outburst_1[j],outburst_1[j+1]))
	if outburst_0[0] == 1:
		for j in range(1,len(outburst_1)-1,2):
			outburst.append((outburst_1[j],outburst_1[j+1]))
	full = []
	for i in outburst_0:
		if i == 1:
			full.append(i)
	if len(full) == len(outburst_0):
		outburst.append((jd[0],jd[len(jd)-1]))
	if len(outburst) != 0:
		output_line = [str(i) for i in outburst]
	else:
		output_line = ['None']
	output_line.insert(0,filename[0:9])
	with open("logfile.csv", "a+") as f:
		source_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		source_writer.writerow(output_line)
	print(outburst)
	plot(jd, flux, label="MAXI lightcurve")
	xlabel("MJD")
	ylabel("Flux (Photons/s/cm^2)")
	legend()
	show()

