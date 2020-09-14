'''
Created on Dec 8, 2017

@author: jose.orlicki
'''

localidades = open('localidades-normal.csv','w')

prov = None
for l in open('localidades.csv'):
    
    l = l.strip()
    if len(l) <= 1 or l.startswith('Anexo'):
        continue
    
    if l.startswith('PROV'):
        prov = l.split('(')[1][:-1]
        continue
        
    if prov == 'San Juan':
        if not l.startswith('9 de Julio'):
            l = l.replace('25 de Mayo','').replace('Ruta 40','').replace('9 de Julio','')
        for d in range(1,10):
            if str(d) in l:
                l = l.split(str(d))[0]
                break
        while l[-1] in ['1','2','3','4','5','6','7','8','9','0','.']:
            l = l[:-1].strip()
    elif prov == 'Santa Cruz':
        l = l.split('Localidad')[0].strip()
    elif '(' in l:
        l = l.split('(')[0].strip()
    
    print '%s,%s,%s' % (l.strip(),prov,'Argentina')
    localidades.write( '%s,%s,%s\n' % (l.strip(),prov,'Argentina') )
