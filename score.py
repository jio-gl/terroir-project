'''
Created on Dec 7, 2017

@author: jose.orlicki
'''

import csv

from histogram import Histogram

import random

class PercentilTerroirScoring(object):
    
    def __init__(self):
        history = [[]]*4
        ifname = 'data/wineries-codes-factors.csv'
        with open(ifname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                for _ in range(int(row[3])):
                    rnd = (random.random()-1.0) / 1000.0 
                    history[0].append( float(row[6]) )#+ rnd )
                    history[1].append( float(row[7]) )#+ rnd )
                    history[2].append( float(row[8]) )#+ rnd )
                    history[3].append( float(row[9]) )#+ rnd )
                    #history[4].append( float(row[10]) )#+ rnd )
                    #history[5].append( float(row[11]) )#+ rnd )
                    #history[6].append( float(row[12]) )#+ rnd )
                    print float(row[9])
 
        self.histograms = map(Histogram,history)


    def scoring(self, paramList): #meanTemp, tempRange, rainFall):
        percs = [histogram.percentil(param) for histogram,param in zip(self.histograms,paramList)]
        percs = [ (perc>0.5 and 2.0*(1.0-perc) or 2.0*perc) for perc in percs ]
        print percs
        ret = 100*sum([ perc/len(percs) for perc in percs])
        ret = min(ret,100.0)
        if ret < 1.0:
            ret = 0.0
        #ret = (ret-50.0)*2.0
        ret = max(ret,0.0)
        return ret


def terroirScoring(meanTemp, tempRange, rainFall):
    ret = meanTemp * 1.58899622 + tempRange * 2.56699454 + rainFall * -0.67520085
    print 'terroirScoring Debug = ',ret
    if ret < 1.0:
        ret = 0.0
    elif ret > 110.0:
        ret = 0.0
    elif ret > 100.0 and ret <=110:
        ret = 100.0
    return ret
    #('Coefficients: \n', array([[ 1.58899622,  2.56699454, -0.67520085]]))

# TODO Mapa con Weighted Data Points
# https://developers.google.com/maps/documentation/javascript/heatmaplayer#add_weighted_data_points
# https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap

if __name__ == '__main__':
    
    scoring = PercentilTerroirScoring()
    print scoring.scoring([62.5,19.0,14.11,71,5,29.96,8])
    print scoring.scoring([63.5,31.0,1.88,53,5,29.9,8])
    print scoring.scoring([63.5,31,1.88,53,5,29.9,8])
    print scoring.scoring([48.5,23,7.7,59,12,29.9,18])
