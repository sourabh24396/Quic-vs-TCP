# -*- coding: utf-8 -*-
"""
This script averages diferent instances of the same test. By default, each test is run five times.
Run this script after preprocess.py
"""

import os
import collections


means = ['10', '50']
losses = ['0.0', '5.0']
bandwidths = ['100', '40', '5']
methods = ['quic', 'tcp']
spikes = ['0', '1']
testnumber = ['1', '2', '3', '4', '5']


pathfile = os.path.normpath('./processed/')

#main method which opens the file and calculates the values
for method in methods:
	for bandwidth in bandwidths:
		for loss in losses:
			for mean in means:
				for spike in spikes:
                    avg_overhead, avg_delay, avg_bandwidth = 0, 0, 0
                    dic = collections.OrderedDict()
                    err = False
                    for number in testnumber:
                        file_path = os.path.normpath(pathfile+'/DATA'+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+variance+'_'+spike+'_'+ number+'.txt')

                        try:
                            with open(file_path, 'r') as f:
                                line = f.readline()
                                parts = line.split()
                                avg_overhead += float(parts[0])
                                avg_delay += (float(parts[2]) - float(parts[1]))
                                avg_bandwidth += float(parts[3])

                        except:
                            err = True
                            print 'File '+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+variance+'_'+spike+'_'+number+'.txt not found'
                        file_path = os.path.normpath(pathfile+'/SUM'+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+spike+'_'+number+'.txt')
                        try:
                            with open(file_path, 'r') as f:
                                for line in f:
                                    parts = line.split()
                                    if parts[0] in dic:
                                        dic[float(parts[0])] += int(parts[1])
                                    else:
                                        dic[float(parts[0])] = int(parts[1])
                        except:
                            err = True
                            print 'File '+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+spike+'_'+number+'.txt not found'
                    #here we will calculate the average values based on the number of tests conducted
                    if not err:
                        avg_overhead /= len(testnumber)
                        avg_delay /= len(testnumber)
                        avg_bandwidth /= len(testnumber)
                        avg_bandwidth /= 1000000
                        file_path = os.path.normpath(pathfile+'/AVGDATA'+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+spike+'.txt')
                        f = open(file_path, 'w')
                        f.write(str(avg_overhead)+' '+str(avg_delay)+' '+str(avg_bandwidth)+'\n')
                        f.close()

                        file_path = os.path.normpath(pathfile+'/AVGSUM'+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+spike+'.txt')
                        f = open(file_path, 'w')
                        for key in sorted(dic.keys()):
                            f.write(str(key)+' '+str(float(float(dic[key])/len(testnumber)))+'\n')

                        f.close()
                        print 'SUCCESS '+method+'_'+bandwidth+'_'+loss+'_'+mean+'_'+spike+'.txt'
