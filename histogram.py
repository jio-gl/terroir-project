'''
Created on Nov 21, 2017

@author: joign
'''

class Histogram(object):
    '''
    classdocs
    '''


    def __init__(self, data, maxLen=None):
        '''
        Constructor
        '''
        self.originalData = data
        self.data = data
        if not maxLen:
            self.maxLen = len(data)
        self.data.sort()
        self.median = self.data[len(self.data)/2]


    def addItem(self, item):
        removeItem = self.originalData[0]
        self.originalData.append(item)
        self.originalData = self.originalData[1:]
        self.data.remove(removeItem)
        self.data.append(item)
        self.data.sort()
        

    def greaterOrEqualToMedian(self, item):
        return item >= self.median
        
    def lowerThanMedian(self, item):
        return item < self.median
        
    def percentil(self, item):
        i = 0
        j = len(self.data)
        m = (i + j) / 2
        found = False
        d = self.data
        m0,m1 = None,None
        while not found:
            if j == i+1:
                found = True
            if d[m] > item:
                j = m 
                m = (i + j) / 2
            elif d[m] < item:
                i = m
                m = (i + j) / 2
            elif d[m] == item:
                m0,m1 = m,m
                while m0 >= 0 and d[m0] == item:
                    m0 -= 1 
                while m1 < len(self.data) and d[m1] == item:
                    m1 += 1 
                found = True
        if m0 == None:
            ret = float(i+1) / len(d)
        else:
            m0 += 1
            m1 -= 1
            ret = float((m0+m1)/2)/len(d) 
        return ret
def test(self):
    #h = Histogram([0.3,0.6,0.9,1.4,1.8])
    h = Histogram( map( lambda x : float(x)/100, range(100)) )
    print h.median
    print h.greaterOrEqualToMedian(1.0)
    print h.lowerThanMedian(10.0)
    print h.percentil(0.89) == 0.89
    print h.percentil(0.01) == 0.01

    
if __name__ == '__main__':
    pass