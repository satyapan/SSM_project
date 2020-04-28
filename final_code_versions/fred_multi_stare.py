'''
Author: satyapan
Purpose: This code fits a fred signature to the combined binned lightcurve, once for each stare.
Inputs: .txt file containing binned lightcurve, .txt file containing stare intervals. (Both are outputs of generate_lcurve_multi_stare.py), limit of redchisq above which to reject fits.
Outputs: Plots of data and fit for each stare, .txt file containing confidence values for each fit.
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import sys

def sort_list(list1, list2): 
    zipped_pairs = zip(list2, list1) 
    z = [x for _, x in sorted(zipped_pairs)]       
    return z 

def residual(variables, t, data, eps_data):
    tau1 = variables[0]
    tau2 = variables[1]
    model = minvalue+(maxvalue-minvalue)*(np.exp(2*np.sqrt(tau1/tau2)))*np.exp((-tau1/t)-(t/tau2))
    return (data-model) / eps_data

def func(t,tau1,tau2):
	return minvalue + (maxvalue-minvalue)*(np.exp(2*np.sqrt(tau1/tau2)))*np.exp((-tau1/t)-(t/tau2))


filename = input("Enter path to binned lightcurve file: ")
sizesname = input("Enter path to file containing stare intervals: ")
redchilimit = float(input("Enter limit of redchisq above which to reject fits: "))

fp = open(filename, "r")
lines = fp.readlines()
fs = open(sizesname, "r")
stares = fs.readlines()
detections = []
confidence = []

count = 0

while count < len(stares):
	xdata = []
	ydata = []
	start = float(stares[count].split()[0])
	end = float(stares[count].split()[1])
	k = 1
	for k in range(len(lines)):
		p = lines[k].split()
		if start < float(p[0]) < end:
			xdata.append(float(p[0]))
			ydata.append(float(p[1]))
	if len(xdata)>0:
		ydata = sort_list(ydata,xdata)
		xdata = sorted(xdata)
		starttime = xdata[0]
		xdata = np.array(xdata)-starttime
		ydata = np.array(ydata)
		meanvalue = np.mean(ydata)
		maxvalue = max(ydata)
		minvalue = min(ydata)
		variables = [0.001, 0.0001]
		out = leastsq(residual, variables, args=(xdata, ydata, 1000))
		yfit = func(xdata,out[0][0],out[0][1])
		y1 = ydata
		y2 = yfit
		ychi = []
		for i in range(len(xdata)):
			if y1[i] != 0:
				ychi.append((y1[i]-y2[i])**2/(y1[i]))
		chisq = sum(ychi)
		redchisq = chisq/(len(xdata)-2)
		if redchisq < redchilimit:
			plt.plot(xdata+starttime,yfit,label="Best Fit Model Redchisq="+str(redchisq))
			plt.errorbar(xdata+starttime,ydata,yerr=np.sqrt(ydata),fmt=".",label="Data")
			plt.title("Stare "+str(count+1))
			plt.legend()
			plt.ylabel("Total counts (in each bin)")
			plt.savefig("Fred_Fit_"+str(count+1)+".png")
			plt.close()
			detections.append((xdata[0]+starttime,xdata[len(xdata)-1]+starttime))
			confidence.append(redchisq)
	count += 1
	prog = (float(count)/float(len(stares)))*100
	sys.stdout.write("\r" + "#"*int(prog/2) + repr(prog)[0:4] + "%")
	sys.stdout.flush()
sys.stdout.write("\n")

np.savetxt("confidence_"+sizesname[-7:], confidence)


