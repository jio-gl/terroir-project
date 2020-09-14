#!/usr/bin/python
# -*- coding: latin-1 -*-
'''
Created on Nov 28, 2017

@author: joign
'''

import csv,time,urllib2,urllib
import math,re,json
from bs4 import BeautifulSoup

from score import PercentilTerroirScoring


def extractFloat(pre,post,cont,regex):
    fs = re.findall(pre+regex+post,cont)
    return float(fs[0][len(pre):-len(post)])


def geocode(textAddress):
    data = {'key':'AIzaSyA6CrCY91kEjb7wD2zc2ibJM9nfq5GyJfU',
            'address':textAddress }
    
    good = False
    while not good:
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(data)
            cont = urllib2.urlopen(url).read()
            print '='*80
            #print cont
            obj = json.loads(cont)
            geometry = obj['results'][0]['geometry']
            good = True
        except:
            print 'Error: sleeping 10 seconds... ', textAddress
            time.sleep(10.0)
    return {'lat':geometry['location']['lat'],'lng':geometry['location']['lng']}


class TerrunioScraper(object):
    '''
    classdocs
    '''


    def __init__(self, fname):
        '''
        Constructor
        '''
        self.fname = fname
        self.rows = []
        with open(fname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print ', '.join(row)
                self.rows.append( row )
        print 'END of Data Input.'        
        
    
    def scrapingTerroir(self, countyIndex=5,provinceIndex=3,wineriesIndex=None):
        
        ofname = self.fname.replace('.','-codes.')
        codes = open(ofname,'w')
        
        baseUrl = 'https://www.timeanddate.com/scripts/completion.php?'
        for r in self.rows[1:]:
            
            # https://www.timeanddate.com/scripts/completion.php?query=chicoana
            
            county = r[countyIndex]
            province = r[provinceIndex]
            print county,',',province
            
            locationEnc = urllib.urlencode({'query':county})
            url = baseUrl + locationEnc
            print url,' ..'
            cont = urllib2.urlopen(url).read()
            #print cont
            cont = cont.split('\n')
            #print cont
            ret = None
            for l in cont:
                if l.startswith('Creating URL for') or l.strip()=='':
                    continue
                
                if not 'Argentina' in l:
                    continue
                
                if province.title() in l:
                    ret = l
                    break
                            
            if ret == None:
                #raise Exception('Country=%s, from Province=%s not found in Server!' % (county,province))
                continue
                
            print ret
            wineries = len(r)>=8 and r[8] or None
            codes.write('%s,%s,Argentina,%s,%s\n' % (county,province,wineries,ret.split('\t')[0]))
            codes.flush()
                
            time.sleep(0.5)
            
            
    def scrapingWeather(self,farmsIndex=3):
        count = 0
        rows = []
        ifname = self.fname.replace('.','-codes.')
        
        #if farmsIndex == None:
        scoring = PercentilTerroirScoring()

        with open(ifname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                
                score = None
                row.append(score)
                rows.append(row)

                
        print count
        
        # Scraping Weather...
        ofname = ifname.replace('.', '-factors.')
        csvfile = open(ofname, 'wb')
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row3 = []
        for r in rows: #l[:3]:
            url = 'https://www.timeanddate.com%s/climate' % r[4].replace('worldclock','weather')
            print url
            cont = urllib2.urlopen(url).read()
            import re

#             pre = 'Annual Rainfall</th><td>'
#             post = '"'
#             regex = '[1-9\.]+'
#             rainFall = extractFloat(pre, post, cont, regex)
#             #print rainFall
        
            soup = BeautifulSoup(cont, 'html.parser')
            hottestTemp = float(str(soup.find(id="stat-hot").parent).replace(' °F avg)</td>','').split('(')[1])
            
            soup = BeautifulSoup(cont, 'html.parser')
            coldestTemp = float(str(soup.find(id="stat-cold").parent).replace(' °F avg)</td>','').split('(')[1])

            soup = BeautifulSoup(cont, 'html.parser')
            rainFall = float( str(soup.find(id="stat-totalrain").parent).replace('<td>','').split('"')[0])
        
            aveTemp = (hottestTemp+coldestTemp) / 2.0
            rangeTemp = hottestTemp  - coldestTemp
            
            # Humidity
            #climate-month climate-month--allyear
            soup = BeautifulSoup(cont, 'html.parser')
            find = soup.findAll("div", { "class" : "climate-month climate-month--allyear" })[0]
            finds = find.text.replace('&nbsp','')
            import re
            
            humidity = str(re.findall('[0-9]+%',finds)[0])
            humidity = int(humidity[:-1])

            wind = str(re.findall('[0-9]+ mph',finds)[0])
            wind = int(wind[:-4])

            pressure = str(re.findall('[0-9\.]+ "Hg',finds)[0])
            pressure = float(pressure[:-4])
            
            #visibility = str(re.findall('[0-9]+.+mi',finds)[0])
            print finds.split('Visibility')[-1][2:-3]
            visibility = int(finds.split('Visibility')[-1][2:-3])
            
            print '='*80
            print r
            print r[3]
            print 'AveTemperatureF = ',aveTemp
            print 'TemperatureRangeF = ',rangeTemp
            print 'RainFallPerYear (inches) = ',rainFall 
            print 'Humidity %% = ',humidity
            print 'Wind (mph) = ',wind
            print 'Pressure ("Hg) = ',pressure
            print 'Visibility (miles) = ',visibility
            #if farmsIndex == None:
            r.append(aveTemp)
            r.append(rangeTemp)
            r.append(rainFall)    
            r.append(humidity)
            r.append(wind)
            r.append(pressure)
            r.append(visibility)

            params = r[6:10] # 13]
            estScore = scoring.scoring(params)
            print 'Estimated Vineyard Scoring (0-100) = ',estScore
            r[5] = estScore #'%.0f' % estScore
            
            row3.append(r)        
            spamwriter.writerow(r)
            csvfile.flush()
            
            
            print len(row3),' / ',len(rows)
            time.sleep(0.5)
        
            
    def geocoding(self):
        # AIzaSyA6CrCY91kEjb7wD2zc2ibJM9nfq5GyJfU
        # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyA6CrCY91kEjb7wD2zc2ibJM9nfq5GyJfU
        count = 0
        rows = []
        ifname = self.fname.replace('.','-codes-factors.')
        ofname = self.fname.replace('.','-codes-factors-latlng.')
        ofile = open(ofname, 'wb')
        spamwriter = csv.writer(ofile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open(ifname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in list(spamreader):#[370:]:
                if row[3]!='None' and int(row[3]) == 0:
                    continue
                print ', '.join(row)
                count += 1

                print row
                
                text = ','.join(row[:3])
                # f1 
                text = text.replace('\xf1','n').replace('\xe1','a').replace('\xe9','e').replace('\xed','i').replace('\xf3','o').replace('\xfa','u')
                latlong = geocode( text )
               
                row.append(latlong['lat'])
                row.append(latlong['lng'])

                
                rows.append(row)
                spamwriter.writerow(row)
                ofile.flush()
                time.sleep(2.0)
                
        print count
        
        
        
if __name__ == '__main__':

    #fname = 'data/wineries.csv'
    fname = 'data/localidades-normal.csv'
    scraper = TerrunioScraper(fname)
    #scraper.scrapingTerroir(countyIndex=0,provinceIndex=1)
    #scraper.scrapingWeather() # none for localidades.csv
    scraper.geocoding()
    
    # Data del Gobierno Argentino
    # https://qcvarnish.smn.gob.ar/graficos_smn.php?app=variables_extremas&omm_id=87257&grupo_variables=temperaturas
    # https://www2.smn.gob.ar/caracterizaci%C3%B3n-estad%C3%ADsticas-de-largo-plazo
    
    # Wunderground
    # https://www.wunderground.com/weather/ar/calingasta/-31.331%2C-69.408
    # probar por Lat Long para ser mas preciso, hay mas estaciones en Wunderground!
    # Aca esta todo!! Max, Min, Precipitation
    # https://www.wunderground.com/history/airport/SAAR/2017/12/2/DailyHistory.html?req_city=Saladillo&req_statename=Argentina
    # https://www.wunderground.com/history/airport/SAAR/2017/1/1/CustomHistory.html?dayend=2&monthend=12&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=