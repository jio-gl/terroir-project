'''
Created on Dec 17, 2017

@author: joign
'''

import urllib2

class WundergroundScraper(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.baseUrl = 'https://www.wunderground.com/weather/'
    
    def latlongWheater(self, lat, long):
        # -33.5824226%2C-69.0620787
        url = self.baseUrl + '%f%%2C%f' % (lat,long)
        print 'Scraping %s ..' % url
        cont = urllib2.urlopen(url).read()
        print cont
        
        
if __name__ == '__main__':
    
    scraper = WundergroundScraper()
    scraper.latlongWheater(-33.5824226, -69.0620787)