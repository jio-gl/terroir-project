'''
Created on Dec 17, 2017

@author: joign
'''

from score import PercentilTerroirScoring

import csv

if __name__ == '__main__':
    scoring = PercentilTerroirScoring()

    ifname = 'data/wineries-factors-latlng.csv'
    #ifname = 'data/localidades-normal-codes-factors-latlng.csv'
    
    minVal = min(26.94742762,24.87119948)-1
    maxVal = max(58.93984471,60.71130542)+1
    
    #if farmsIndex == None:
    scoring = PercentilTerroirScoring()

    rows = []
    with open(ifname, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            rows.append(row)

    ofname = ifname
    csvfile = open(ofname, 'wb')
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        sco = scoring.scoring( map(float,r[6:10]) ) #13]) )
        sco = 100*(sco-minVal) / (maxVal-minVal)
        r[5] = sco
        spamwriter.writerow( r )