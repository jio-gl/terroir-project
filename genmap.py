'''
Created on Dec 7, 2017

@author: jose.orlicki
'''

from logging import info
import logging,csv
logging.basicConfig(level=logging.INFO)

class TerrunioMapGenerator(object):
    
    MARKER = '%%%DATAPOINTS%%%'
    MARKER2 = '%%%DATAPOINTS2%%%'
    
    def __init__(self):
        self.template = open('web/template.html').read()
        self.template2 = open('web/template2.html').read()
        

    def generateExampleMap(self, outfname='web/terrunioMap-0.html'):
        info('generating example map %s ..' % outfname)
        data = open('data/example.dat').read()
        of = open(outfname,'w').write( self.template.replace(self.MARKER,data) )

    def generateTrainingMap(self, outfname='web/terrunioMap-1.html'):
        info('generating Training Wineries Map %s ..' % outfname)
        data = ''
        itemTemplate = '{location: new google.maps.LatLng(%s, %s), weight: %s},'
        with open('data/wineries-factors-latlng.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print row
                item = itemTemplate % (row[13],row[14],row[5])
                print item
                data += item +'\n'
        of = open(outfname,'w').write( self.template.replace(self.MARKER,data) )

    def generatePredictMap(self, outfname='web/terrunioMap-2.html'):
        info('generating Training Wineries Map %s ..' % outfname)
        itemTemplate = '{location: new google.maps.LatLng(%s, %s), weight: %s},'
        of = open(outfname,'w')

        data = ''
        with open('data/wineries-factors-latlng.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print row
                item = itemTemplate % (row[13],row[14],row[5])
                print item
                data += item +'\n'
        self.template2 = self.template2.replace(self.MARKER,data) 

        data = ''
        with open('data/localidades-normal-codes-factors-latlng.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print row
                #if float(row[5]) < 92.01:
                #    continue
                item = itemTemplate % (row[13],row[14],row[5])
                print item
                data += item +'\n'
        of.write( self.template2.replace(self.MARKER2,data) )


if __name__ == '__main__':
    
    generator = TerrunioMapGenerator()
    
    generator.generateExampleMap()
    generator.generateTrainingMap()
    generator.generatePredictMap()
    
    # regions
    # https://support.google.com/fusiontables/answer/1032332
    # https://developers.google.com/maps/documentation/javascript/examples/layer-fusiontables-heatmap
    
    # https://es.wikipedia.org/wiki/Categor%C3%ADa:Localidades_de_Argentina_por_provincia