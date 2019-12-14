from numpy import *
from pylab import *
from astropy.io import fits

filename = input("Enter name of SSM event file: ")
inttime = input("Enter binning time: ")

#filename = "/home/satyapan/SSM_project/lightcurve/AS1G06_164T01_9000000844_06383ssm_level2_clean_ssm3.fits"
#inttime = 1

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


plot(MJD,events_bin,"+")
show()




