'''
Author: satyapan
Purpose: This code fits a fred signature to the combined binned lightcurve, once for each interval specified in the sizes file.
Inputs: .txt file containing binned lightcurve, .txt file containing number of binned points to be used for each fit. (Both are outputs of generate_lcurve_multi.py)
Outputs: Plots of data and fit for each fit, .txt file containing confidence values for each fit.
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import sys

def residual(variables, t, data, eps_data):
    tau1 = variables[0]
    tau2 = variables[1]
    model = maxvalue*(np.exp(2*np.sqrt(tau1/tau2)))*np.exp((-tau1/t)-(t/tau2))
    return (data-model) / eps_data

def func(t,tau1,tau2):
	return maxvalue*(np.exp(2*np.sqrt(tau1/tau2)))*np.exp((-tau1/t)-(t/tau2))


filename = input("Enter path to binned lightcurve file: ")
sizesname = input("Enter path to file containing fit sizes: ")

fp = open(filename, "r")
lines = fp.readlines()
fs = open(sizesname, "r")
sizes = fs.readlines()
detections = []
confidence = []

count = 0
step = 0
interval_end = int(sizes[len(sizes)-1].split()[0])

while step < len(lines)-interval_end:
	xdata = []
	ydata = []
	interval = 60
	for k in range(step,step+interval):
		p = lines[k].split()
		xdata.append(float(p[0]))
		ydata.append(float(p[1]))
	starttime = xdata[0]
	xdata = np.array(xdata)-starttime
	ydata = np.array(ydata)
	meanvalue = np.mean(ydata)
	maxvalue = max(ydata)
	variables = [0.01, 0.001]
	out = leastsq(residual, variables, args=(xdata, ydata, 100))
	yfit = func(xdata,out[0][0],out[0][1])
	y1 = (ydata+0.0001)/sum(ydata)
	y2 = (yfit+0.0001)/sum(yfit)
	chisq = sum([(y1[i]-y2[i])**2/(y2[i]) for i in range(len(xdata))])
	redchisq = chisq/(len(xdata)-2)
	plt.plot(xdata+starttime,yfit,label="Best Fit Model Redchisq="+str(redchisq))
	plt.plot(xdata+starttime,ydata,".",label="Data")
	plt.title("File "+str(count+1))
	plt.legend()
	plt.savefig("Fred_Fit_"+str(count+1)+".png")
	plt.close()
	detections.append((xdata[0]+starttime,xdata[interval-1]+starttime))
	confidence.append(redchisq)
	step = step + interval
	count += 1
	prog = (float(count)/float(len(lines)//interval))*100
	sys.stdout.write("\r" + "#"*int(prog/2) + repr(prog)[0:4] + "%")
	sys.stdout.flush()
sys.stdout.write("\n")

np.savetxt("confidence_"+sizesname[-7:], confidence)


